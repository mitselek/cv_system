#!/usr/bin/env python3
"""
Job monitoring orchestrator.

Phase 2: implement scan workflow with --dry-run and --force.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Iterable

from config_manager import ConfigManager, ConfigurationError
from deduplicator import Deduplicator
from job_scorer import JobScorer
from schemas import JobPosting, SystemConfig
from state_manager import StateManager
from job_scraper import JobScraper


def _supported_source(name: str) -> bool:
    n = name.lower()
    return any(k in n for k in ["duunitori", "linkedin", "tyomarkkinatori"])  # Phase 2 support


def _scrape_source(scraper: JobScraper, source_name: str, queries: Iterable[dict[str, Any]]) -> list[JobPosting]:
    jobs: list[JobPosting] = []
    for q in queries:
        kw = q.get("keywords", "")
        loc = q.get("location", "")
        lim = int(q.get("limit", 20))
        if "duunitori" in source_name.lower():
            jobs.extend(scraper.search_duunitori(kw, loc, lim))
        elif "linkedin" in source_name.lower():
            jobs.extend(scraper.search_linkedin(kw, loc or "Finland"))
        elif "tyomarkkinatori" in source_name.lower():
            jobs.extend(scraper.search_tyomarkkinatori(kw))
        # else: unsupported handled by caller
    # annotate source consistently
    for j in jobs:
        j.source = source_name
    return jobs


def scan(config_path: Path, dry_run: bool, force: bool) -> int:
    try:
        cm = ConfigManager(config_path)
    except ConfigurationError as e:
        print(f"Config error: {e}")
        return 2

    cfg: SystemConfig = cm.config
    # Ensure directories
    cfg.candidates_dir.mkdir(parents=True, exist_ok=True)
    cfg.state_file.parent.mkdir(parents=True, exist_ok=True)

    sm = StateManager(cfg.state_file)
    scorer = JobScorer(cfg.scoring)
    dd = Deduplicator()

    enabled = cm.get_enabled_sources()
    if not enabled:
        print("No enabled sources in config.")
        return 0

    all_jobs: list[JobPosting] = []

    scraper: JobScraper | None = None
    if not dry_run:
        # Choose a cookies file if any source defines it; else fallback under job_sources/
        cookies_path = None
        for s in cfg.sources:
            if s.enabled and s.cookies_file:
                cookies_path = s.cookies_file
                break
        if cookies_path is None:
            cookies_path = Path("job_sources/cookies.json")
        scraper = JobScraper(cookies_file=cookies_path)

    for src in cfg.sources:
        if not src.enabled:
            continue
        if not _supported_source(src.name):
            print(f"Skipping unsupported source: {src.name}")
            continue
        if scraper is None:
            continue  # dry-run: skip network scraping
        queries = cm.get_source_queries(src.name)
        jobs = _scrape_source(scraper, src.name, queries)
        all_jobs.extend(jobs)

    unique_jobs = dd.filter_unique(all_jobs)

    scored = [scorer.score(j) for j in unique_jobs]

    print(f"Discovered {len(all_jobs)} jobs, {len(unique_jobs)} unique.")

    # Update state and optionally persist
    for sj in scored:
        sm.add_job(sj.job)

    sm.touch_scan_time()

    if dry_run:
        print("Dry-run: not saving state")
    else:
        sm.save_state()
        print(f"State saved to {cfg.state_file}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Job monitoring tool")
    sub = parser.add_subparsers(dest="cmd")

    p_scan = sub.add_parser("scan", help="Scan enabled sources")
    p_scan.add_argument("--config", default="config.example.yaml", type=Path)
    p_scan.add_argument("--dry-run", action="store_true")
    p_scan.add_argument("--force", action="store_true")

    args = parser.parse_args()

    if args.cmd == "scan":
        return scan(args.config, args.dry_run, args.force)
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
