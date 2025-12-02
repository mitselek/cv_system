#!/usr/bin/env python3
"""Re-score all jobs from 2025-12-02 with the fixed scorer."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from job_monitor.scorer import JobScorer
from job_monitor.config import load_config
from job_monitor.schemas import JobPosting
from job_monitor.digest import DigestGenerator

def rescore_jobs(date: str = "2025-12-02"):
    """Re-score all jobs for a given date."""
    # Load config
    config = load_config(Path(__file__).parent / "search_config.yaml")
    scorer = JobScorer(config.scoring)
    
    # Find all job JSON files for the date
    candidates_dir = Path(__file__).parent / "candidates" / date
    if not candidates_dir.exists():
        print(f"No candidates directory found for {date}")
        return
    
    job_files = list(candidates_dir.rglob("*.json"))
    print(f"Found {len(job_files)} job files to re-score")
    
    updated_count = 0
    for job_file in job_files:
        # Load job data
        with open(job_file, 'r') as f:
            job_data = json.load(f)
        
        # Create job object
        job = JobPosting(**job_data['job'])
        
        # Re-score
        result = scorer.score(job)
        
        # Check if score changed
        old_score = job_data['score']
        if old_score != result.score:
            print(f"\n{job.title} ({job.company})")
            print(f"  Old score: {old_score} -> New score: {result.score}")
            print(f"  Matched keywords: {result.matched_keywords}")
            
            # Update the job data
            job_data['score'] = result.score
            job_data['score_breakdown'] = result.score_breakdown
            job_data['matched_keywords'] = result.matched_keywords
            job_data['category'] = result.category
            
            # Determine new category directory
            if result.score >= 80:
                new_category = "high_priority"
            elif result.score >= 50:
                new_category = "review"
            else:
                new_category = "low_priority"
            
            # Get current category from path
            current_category = job_file.parent.name
            
            # If category changed, we need to move the file
            if current_category != new_category:
                print(f"  Moving from {current_category} to {new_category}")
                new_dir = candidates_dir / new_category
                new_dir.mkdir(exist_ok=True)
                new_job_file = new_dir / job_file.name
                new_md_file = new_dir / job_file.with_suffix('.md').name
                old_md_file = job_file.with_suffix('.md')
                
                # Write to new location
                with open(new_job_file, 'w') as f:
                    json.dump(job_data, f, indent=2, ensure_ascii=False)
                
                # Move markdown file if it exists
                if old_md_file.exists():
                    # Read, update score, write to new location
                    md_content = old_md_file.read_text()
                    # Update score line
                    md_content = md_content.replace(f"**Score:** {old_score}/100", f"**Score:** {result.score}/100")
                    new_md_file.write_text(md_content)
                    old_md_file.unlink()
                
                # Remove old JSON file
                job_file.unlink()
            else:
                # Update in place
                with open(job_file, 'w') as f:
                    json.dump(job_data, f, indent=2, ensure_ascii=False)
                
                # Update markdown file if it exists
                md_file = job_file.with_suffix('.md')
                if md_file.exists():
                    md_content = md_file.read_text()
                    md_content = md_content.replace(f"**Score:** {old_score}/100", f"**Score:** {result.score}/100")
                    md_file.write_text(md_content)
            
            updated_count += 1
    
    print(f"\n✅ Re-scored {updated_count} jobs")
    
    # Regenerate digest
    print("\n📝 Regenerating digest...")
    digest_gen = DigestGenerator(candidates_dir.parent)
    digest_content = digest_gen.generate_digest(date)
    digest_path = candidates_dir / "digest.md"
    digest_path.write_text(digest_content)
    print(f"✅ Digest updated: {digest_path}")

if __name__ == "__main__":
    rescore_jobs()
