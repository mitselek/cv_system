#!/usr/bin/env python3
"""
Job monitoring orchestrator.

Phase 2: implement scan workflow with --dry-run and --force.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import click

from job_monitor.config import ConfigManager, ConfigurationError
from job_monitor.deduplicator import Deduplicator
from job_monitor.digest import DigestGenerator
from job_monitor.markdown_exporter import MarkdownExporter
from job_monitor.schemas import JobPosting, JobStatus, ScoredJob, SystemConfig
from job_monitor.scorer import JobScorer
from job_monitor.scrapers import ScraperRegistry
from job_monitor.state import StateManager

# Shared click option decorator for config file
config_option = click.option(
    "--config",
    default="config.example.yaml",
    type=click.Path(path_type=Path),
    help="Path to configuration file",
)


def _scrape_source(
    source_name: str,
    config: dict[str, Any],
    queries: Iterable[dict[str, Any]],
    state_manager: StateManager | None = None,
) -> list[JobPosting]:
    """Scrape a source using the registry.

    Args:
        source_name: The scraper ID (e.g., 'duunitori', 'cvee')
        config: Scraper-specific configuration (cookies_file, etc.)
        queries: List of search queries
        state_manager: Optional state manager for tracking

    Returns:
        List of job postings
    """
    # Extract cookies_file from config if present
    cookies_file = config.pop('cookies_file', None)
    if cookies_file:
        cookies_file = Path(cookies_file)

    # Get scraper from registry
    scraper = ScraperRegistry.get_scraper(source_name, config=config, cookies_file=cookies_file)

    jobs: list[JobPosting] = []
    for q in queries:
        # Pass the entire query dict to the scraper
        search_results = scraper.search(q)
        jobs.extend(search_results)

    # Annotate source consistently
    for j in jobs:
        j.source = source_name

    return jobs


def _save_candidates(candidates_dir: Path, scored_jobs: list[ScoredJob]) -> dict[str, int]:
    """Save scored jobs to date-stamped candidate directories.

    Saves both JSON (for automation) and Markdown (for humans).

    Returns dict with counts per category.
    """
    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = candidates_dir / today

    # Create category subdirectories
    high_dir = day_dir / "high_priority"
    review_dir = day_dir / "review"
    low_dir = day_dir / "low_priority"

    high_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    low_dir.mkdir(parents=True, exist_ok=True)

    counts = {"high_priority": 0, "review": 0, "low_priority": 0}

    for sj in scored_jobs:
        # Determine directory by category
        if sj.category == "High Priority":
            target_dir = high_dir
            counts["high_priority"] += 1
        elif sj.category == "Review":
            target_dir = review_dir
            counts["review"] += 1
        else:  # Low Priority
            target_dir = low_dir
            counts["low_priority"] += 1

        # Save as JSON with job ID as filename
        filepath = target_dir / f"{sj.job.id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(sj.model_dump(mode="json"), f, ensure_ascii=False, indent=2)

        # Save as Markdown for human readability
        md_filepath = target_dir / f"{sj.job.id}.md"
        MarkdownExporter.export_job(sj, md_filepath)

    return counts


@click.group()
@click.version_option(version="1.0.0")
def cli() -> None:
    """Job monitoring and application management system."""
    pass


@cli.command()
@config_option
@click.option("--dry-run", is_flag=True, help="Run without saving state or candidates")
@click.option("--force", is_flag=True, help="Force rescan of all sources")
@click.option("--full-details", is_flag=True, help="Extract full job descriptions (slower, ~1.5s per job)")
def scan(config: Path, dry_run: bool, force: bool, full_details: bool) -> None:
    """Scan enabled job sources and save candidates."""
    try:
        cm = ConfigManager(config)
    except ConfigurationError as e:
        click.echo(f"Config error: {e}", err=True)
        raise SystemExit(2)

    cfg: SystemConfig = cm.config
    # Ensure directories
    cfg.candidates_dir.mkdir(parents=True, exist_ok=True)
    cfg.state_file.parent.mkdir(parents=True, exist_ok=True)

    sm = StateManager(cfg.state_file)
    scorer = JobScorer(cfg.scoring)
    dd = Deduplicator()

    enabled = cm.get_enabled_sources()
    if not enabled:
        click.echo("No enabled sources in config.")
        return

    all_jobs: list[JobPosting] = []

    for src in cfg.sources:
        if not src.enabled:
            continue

        # Check if scraper is registered
        if not ScraperRegistry.is_registered(src.name):
            click.echo(f"Skipping unsupported source: {src.name}")
            continue

        if dry_run:
            click.echo(f"Dry-run: would scrape {src.name}")
            continue

        # Build scraper config from source settings
        scraper_config = {}
        if src.cookies_file:
            scraper_config["cookies_file"] = str(src.cookies_file)

        queries = cm.get_source_queries(src.name)
        jobs = _scrape_source(src.name, scraper_config, queries, sm)
        all_jobs.extend(jobs)

        click.echo(f"✓ Scraped {len(jobs)} jobs from {src.name}")

    unique_jobs = dd.filter_unique(all_jobs)

    # Enrich with full details if requested
    if full_details and unique_jobs:
        click.echo(f"\nFetching full details for {len(unique_jobs)} jobs...")
        enriched_jobs = []

        for i, job in enumerate(unique_jobs, 1):
            # Fetch details for supported scrapers (cvee and duunitori)
            if job.source in ("cvee", "duunitori"):
                try:
                    # Get scraper instance with cookies for duunitori
                    scraper_config = {}
                    cookies_file = None
                    if job.source == "duunitori":
                        # Find duunitori config to get cookies file
                        for src in cfg.sources:
                            if src.name == "duunitori" and src.cookies_file:
                                cookies_file = src.cookies_file
                                break

                    scraper = ScraperRegistry.get_scraper(job.source, config=scraper_config, cookies_file=cookies_file)

                    # Try to fetch full details if scraper supports it
                    details = scraper.fetch_job_details(job.id if job.source == "cvee" else str(job.url))

                    if details and details.get('description'):
                        # Update job description with full content
                        job.description = details['description']

                        # Show progress every 10 jobs
                        if i % 10 == 0:
                            click.echo(f"  Fetched {i}/{len(unique_jobs)}...")
                except Exception as e:
                    click.echo(f"Failed to fetch job details for {job.id}: {e}")

            enriched_jobs.append(job)

        unique_jobs = enriched_jobs
        click.echo("✓ Fetched full details")

    scored = [scorer.score(j) for j in unique_jobs]

    # Filter out already-seen jobs before saving (fix for issue #33)
    new_candidates = [sj for sj in scored if not sm.is_seen(sj.job.id)]

    click.echo(f"Discovered {len(all_jobs)} jobs, {len(unique_jobs)} unique, {len(new_candidates)} new.")

    # Save only NEW candidates to directories
    if new_candidates and not dry_run:
        counts = _save_candidates(cfg.candidates_dir, new_candidates)
        msg = (
            f"Saved candidates: {counts['high_priority']} high, "
            f"{counts['review']} review, {counts['low_priority']} low"
        )
        click.echo(msg)

        # Generate digest
        dg = DigestGenerator(cfg.candidates_dir)
        digest_path = dg.save_digest()
        click.echo(f"Digest saved to {digest_path}")

    # Update state for ALL jobs (new and existing with potential updates)
    for sj in scored:
        if sm.is_seen(sj.job.id):
            # Update existing job (might have new description)
            sm.update_job(sj.job)
        else:
            # Add new job
            sm.add_job(sj.job)

    sm.touch_scan_time()

    if dry_run:
        click.echo("Dry-run: not saving state or candidates")
    else:
        sm.save_state()
        click.echo(f"State saved to {cfg.state_file}")


@cli.command()
@config_option
@click.option(
    "--category",
    type=click.Choice(["high", "review", "low", "all"]),
    default="all",
    help="Filter by category",
)
@click.option("--min-score", type=float, help="Minimum score threshold")
@click.option("--source", help="Filter by source")
@click.option("--date", help="Filter by date (YYYY-MM-DD)")
def review(config: Path, category: str, min_score: float | None, source: str | None, date: str | None) -> None:
    """Review candidate jobs with optional filtering."""
    try:
        cm = ConfigManager(config)
    except ConfigurationError as e:
        click.echo(f"Config error: {e}", err=True)
        raise SystemExit(2)

    cfg = cm.config

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    day_dir = cfg.candidates_dir / date

    if not day_dir.exists():
        click.echo(f"No candidates found for {date}")
        return

    # Load candidates based on category filter
    categories = []
    if category == "all":
        categories = ["high_priority", "review", "low_priority"]
    elif category == "high":
        categories = ["high_priority"]
    elif category == "review":
        categories = ["review"]
    elif category == "low":
        categories = ["low_priority"]

    all_candidates: list[ScoredJob] = []
    for cat in categories:
        cat_dir = day_dir / cat
        if cat_dir.exists():
            for json_file in cat_dir.glob("*.json"):
                try:
                    with open(json_file) as f:
                        data = json.load(f)
                        sj = ScoredJob(**data)

                        # Apply filters
                        if min_score and sj.score < min_score:
                            continue
                        if source and sj.job.source != source:
                            continue

                        all_candidates.append(sj)
                except Exception as e:
                    click.echo(f"Warning: Failed to load {json_file}: {e}", err=True)

    if not all_candidates:
        click.echo("No candidates match the filters")
        return

    # Sort by score
    all_candidates.sort(key=lambda x: x.score, reverse=True)

    click.echo(f"\n{'='*80}")
    click.echo(f"Candidates for {date} ({len(all_candidates)} total)")
    click.echo(f"{'='*80}\n")

    for i, sj in enumerate(all_candidates, 1):
        click.echo(f"{i}. {sj.job.title} @ {sj.job.company}")
        click.echo(f"   Score: {sj.score:.1f}/100 | Category: {sj.category}")
        click.echo(f"   Location: {sj.job.location or 'N/A'} | Source: {sj.job.source}")
        if sj.matched_keywords:
            click.echo(f"   Keywords: {', '.join(sj.matched_keywords)}")
        click.echo(f"   URL: {sj.job.url}")
        click.echo()


@cli.command()
@config_option
def stats(config: Path) -> None:
    """Show monitoring statistics."""
    try:
        cm = ConfigManager(config)
    except ConfigurationError as e:
        click.echo(f"Config error: {e}", err=True)
        raise SystemExit(2)

    cfg = cm.config
    sm = StateManager(cfg.state_file)

    state = sm.state

    click.echo(f"\n{'='*80}")
    click.echo("Job Monitoring Statistics")
    click.echo(f"{'='*80}\n")

    click.echo(f"Last Scan: {state.last_scan or 'Never'}")
    click.echo(f"Total Jobs Seen: {state.total_jobs_seen}")
    click.echo(f"Total Candidates: {state.total_candidates}")
    click.echo(f"Total Applications: {state.total_applications}")
    click.echo()

    click.echo("By Status:")
    click.echo(f"  New: {len(state.new_jobs)}")
    click.echo(f"  Candidates: {len(state.candidates)}")
    click.echo(f"  Applied: {len(state.applied)}")
    click.echo()

    if state.stats_by_source:
        click.echo("By Source:")
        for source, count in sorted(state.stats_by_source.items()):
            click.echo(f"  {source}: {count}")
        click.echo()


@cli.command()
@click.argument("job-id")
@click.argument("status", type=click.Choice(["candidate", "applied", "rejected"]))
@config_option
def mark(job_id: str, status: str, config: Path) -> None:
    """Mark a job with a new status."""
    try:
        cm = ConfigManager(config)
    except ConfigurationError as e:
        click.echo(f"Config error: {e}", err=True)
        raise SystemExit(2)

    cfg = cm.config
    sm = StateManager(cfg.state_file)

    job = sm.get_job(job_id)
    if not job:
        click.echo(f"Job {job_id} not found", err=True)
        raise SystemExit(1)

    # Update job status
    if status == "candidate":
        job.status = JobStatus.CANDIDATE
        if job_id not in sm.state.candidates:
            sm.state.candidates.append(job_id)
        if job_id in sm.state.new_jobs:
            sm.state.new_jobs.remove(job_id)
    elif status == "applied":
        job.status = JobStatus.APPLIED
        if job_id not in sm.state.applied:
            sm.state.applied.append(job_id)
        if job_id in sm.state.candidates:
            sm.state.candidates.remove(job_id)
        sm.state.total_applications += 1
    elif status == "rejected":
        job.status = JobStatus.REJECTED
        if job_id in sm.state.new_jobs:
            sm.state.new_jobs.remove(job_id)
        if job_id in sm.state.candidates:
            sm.state.candidates.remove(job_id)

    sm.update_job(job)
    sm.save_state()

    click.echo(f"Marked job {job_id} as {status}")


@cli.command()
@config_option
@click.option("--days", default=60, help="Archive jobs older than this many days")
@click.option("--dry-run", is_flag=True, help="Show what would be archived without doing it")
def cleanup(config: Path, days: int, dry_run: bool) -> None:
    """Archive old jobs from state."""
    try:
        cm = ConfigManager(config)
    except ConfigurationError as e:
        click.echo(f"Config error: {e}", err=True)
        raise SystemExit(2)

    cfg = cm.config
    sm = StateManager(cfg.state_file)

    if dry_run:
        click.echo(f"Would archive jobs older than {days} days")
        # Count would-be archived
        now = datetime.now(UTC)
        count = 0
        for job_id, job in sm.state.seen_jobs.items():
            try:
                age_days = (now - job.discovered_date.replace(tzinfo=UTC)).days
                if age_days > days:
                    count += 1
            except Exception:
                pass
        click.echo(f"Would archive {count} jobs")
    else:
        archived = sm.cleanup_old_jobs(days)
        sm.save_state()
        click.echo(f"Archived {archived} jobs")


@cli.command()
@click.option("--output", default="config.yaml", type=click.Path(path_type=Path), help="Output configuration file")
def init(output: Path) -> None:
    """Create a configuration file template."""
    template = """sources:
  - name: cvee
    enabled: true
    queries:
      - keywords: python developer
        location: tallinn
        limit: 20

  - name: duunitori
    enabled: false
    cookies_file: /path/to/duunitori_cookies.json
    queries:
      - keywords: python developer
        location: helsinki
        limit: 20

scoring:
  positive_keywords:
    - python
    - django
    - postgresql
  negative_keywords:
    - java
    - .net
  required_keywords: []
  preferred_companies: []
  blocked_companies: []
  preferred_locations:
    - remote
    - helsinki
    - tallinn
  remote_bonus: 15
  days_threshold_fresh: 7
  days_threshold_old: 30

state_file: job_sources/monitor_state.json
candidates_dir: job_sources/candidates
scan_interval_hours: 24
auto_archive_days: 60
"""

    if output.exists():
        if not click.confirm(f"{output} already exists. Overwrite?"):
            click.echo("Aborted")
            return

    output.write_text(template)
    click.echo(f"Created configuration template at {output}")
    click.echo("Edit the file to customize sources and scoring rules")


def main() -> None:
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
