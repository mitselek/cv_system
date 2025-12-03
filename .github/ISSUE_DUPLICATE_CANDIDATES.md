# Bug: Duplicate Job Candidates Saved Across Daily Scans

## Summary

Job monitoring system saves duplicate candidate files across multiple daily scans, even though state tracking correctly identifies jobs as already seen. All 17 high-priority jobs from 2025-12-02 were duplicated in 2025-12-03 scan.

## Expected Behavior

According to deduplication requirements:
1. In-memory deduplication during scan (via `Deduplicator.filter_unique()`)
2. State-based deduplication across scans (via `StateManager.is_seen()`)
3. **Only NEW jobs should be saved to candidates/ directories**

## Actual Behavior

- State tracking works correctly (`state.seen_jobs` contains 238 jobs)
- Jobs are correctly identified as "seen" in state
- **BUT: Candidate files are saved anyway, creating duplicates**

## Evidence

```bash
# All 17 high-priority jobs duplicated between Dec 2 and Dec 3
$ comm -12 \
  <(ls -1 candidates/2025-12-02/high_priority/*.json | xargs basename | sort) \
  <(ls -1 candidates/2025-12-03/high_priority/*.json | xargs basename | sort) \
  | wc -l
17

# State shows 238 total jobs seen
$ jq '.total_jobs_seen' state/monitor_state.json
238

# But Dec 2 had 168 candidates, Dec 3 had 235 candidates (should be ~67 new)
$ ls candidates/2025-12-02/*/*.json | wc -l
168
$ ls candidates/2025-12-03/*/*.json | wc -l
235
```

## Root Cause

In `job-monitoring/src/job_monitor/cli.py`, the `scan()` function:

1. **Saves candidates FIRST** (line ~207):
   ```python
   if scored and not dry_run:
       counts = _save_candidates(cfg.candidates_dir, scored)
   ```

2. **Checks state AFTER** (line ~215):
   ```python
   for sj in scored:
       if sm.is_seen(sj.job.id):  # Already seen - don't save again
           sm.update_job(sj.job)
       else:
           sm.add_job(sj.job)
   ```

The state check happens too late - files already written to disk.

## Proposed Fix

Filter already-seen jobs BEFORE saving candidates:

```python
# Around line 205 in cli.py - BEFORE _save_candidates()
new_candidates = [sj for sj in scored if not sm.is_seen(sj.job.id)]

# Save only new candidates
if new_candidates and not dry_run:
    counts = _save_candidates(cfg.candidates_dir, new_candidates)
    click.echo(f"Saved candidates: {counts['high_priority']} high, {counts['review']} review, {counts['low_priority']} low")
    
    # Generate digest
    dg = DigestGenerator(cfg.candidates_dir)
    digest_path = dg.save_digest()
    click.echo(f"Digest saved to {digest_path}")

# Update state for ALL jobs (new and updated)
for sj in scored:
    if sm.is_seen(sj.job.id):
        sm.update_job(sj.job)  # Refresh description if changed
    else:
        sm.add_job(sj.job)
```

## Impact

**Current:**
- Digest files contain mostly duplicates from previous days
- User wastes time reviewing already-seen jobs
- Candidate directories grow unnecessarily
- Daily scan output misleading (reports 235 candidates when only ~67 are new)

**After Fix:**
- Only truly new jobs saved to candidates/
- Digest shows only new opportunities
- Cleaner directory structure
- Accurate reporting ("Discovered 547 jobs, 235 unique, 67 NEW")

## Additional Considerations

### Option 1: Strict Deduplication (Recommended)
- Never save already-seen jobs
- Keeps candidates/ clean
- User only sees new opportunities each day

### Option 2: Update Mode
- Save to candidates/ if job description changed
- Useful if jobs get updated with more details
- Requires comparing old vs new description

### Option 3: Daily Archive
- Save all jobs daily (current behavior)
- Add `--force-save` flag for this mode
- Default to strict deduplication

## Testing

Test cases needed:
1. First scan (no state) → All jobs saved
2. Second scan (same jobs) → 0 jobs saved
3. Second scan (mix of old + new) → Only new jobs saved
4. Second scan (job with updated description) → Depends on chosen option

## Related Files

- `job-monitoring/src/job_monitor/cli.py` (line ~200-220)
- `job-monitoring/src/job_monitor/state.py` (`is_seen()`, `add_job()`, `update_job()`)
- `job-monitoring/tests/test_integration.py` (add deduplication test)

## Labels

- `bug`
- `job-monitoring`
- `deduplication`
- `priority:high`

## Discovered

2025-12-03 during digest comparison for application generation workflow
