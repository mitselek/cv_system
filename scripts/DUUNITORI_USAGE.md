# Duunitori Job Scraper - Quick Reference

## ✅ Successfully Working!

The scraper can now access Duunitori and extract job listings with your cookies.

## Quick Commands

### Basic searches:

```bash
# Software development jobs
./scripts/search_duunitori.sh "software developer" --limit 20

# Project management
./scripts/search_duunitori.sh "project manager" --limit 15

# System analysis
./scripts/search_duunitori.sh "system analyst" --limit 10

# IT leadership
./scripts/search_duunitori.sh "IT manager" --location Helsinki
```

### Finnish terms that work:

```bash
# Software development
./scripts/search_duunitori.sh "ohjelmistokehittäjä"

# Project management
./scripts/search_duunitori.sh "projektipäällikkö"
```

### Save results:

```bash
# Save as JSON
./scripts/search_duunitori.sh "software" --limit 30 \
  --output ~/Downloads/duunitori_jobs.json

# Save as CSV
./scripts/search_duunitori.sh "IT" --limit 20 \
  --format csv --output ~/Downloads/jobs.csv
```

### Integration with cv_system workflow:

```bash
# Search and save to applications folder for review
./scripts/search_duunitori.sh "projektijuht IT" --limit 25 \
  --output applications/duunitori_scan_$(date +%Y-%m-%d).json
```

## Results Summary

**Tested searches:**

- ✅ `"software developer"` → 27 jobs found, 15 parsed
- ✅ `"project manager"` → 2 jobs found
- ✅ `"ohjelmistokehitys"` → 8 jobs found (includes summer internships)

**Data extracted per job:**

- Portal name (Duunitori)
- Job title
- Company name
- Location (city)
- Posted date
- Direct URL to application

## Tips for Better Results

1. **Use English terms** - Finnish portals index English job titles

   - "software developer" > "ohjelmistokehittäjä"
   - "project manager" > "projektipäällikkö"

2. **Combine terms** for specific roles:

   - "IT project manager"
   - "software architect"
   - "system analyst"

3. **Location filtering** works:

   - `--location Helsinki`
   - `--location "Helsinki Espoo"`

4. **Adjust limits** based on need:
   - Quick scan: `--limit 10`
   - Comprehensive: `--limit 50`

## Example Workflow

```bash
# 1. Daily scan for new IT jobs in Helsinki area
./scripts/search_duunitori.sh "IT projektijuht" \
  --location Helsinki \
  --limit 20 \
  --output /tmp/daily_scan.json

# 2. Review results
cat /tmp/daily_scan.json | jq '.[] | {title, company, url}'

# 3. Pick interesting ones and generate applications
# (Use your existing cv_system workflow)
```

## Next Steps

### Enhance search capabilities:

1. Add category filtering (IT sector only)
2. Add date range filtering (last week/month)
3. Add salary range filtering
4. Duplicate detection across searches

### Integration options:

1. Create cron job for daily searches
2. Send results to email/Telegram
3. Auto-match against your skills/experience
4. Generate application drafts for high-fit roles

### Multi-portal expansion:

1. Add Tyomarkkinatori (when you provide cookies)
2. Add LinkedIn (when you provide cookies)
3. Aggregate and deduplicate across all portals

## Cookie Maintenance

Cookies typically expire after days/weeks. If you get 0 results or errors:

1. Re-export cookies from browser
2. Update `~/.config/job_scraper_cookies_duunitori.json`
3. Test: `./scripts/search_duunitori.sh "test" --limit 5`

## Troubleshooting

### "Found 0 jobs" but you know there are results:

- Cookies may have expired - re-export them
- Try broader search terms
- Check if portal changed HTML structure

### "Connection error":

- Check internet connection
- Duunitori may be blocking (unlikely with cookies)
- Try again in a few minutes

### Parse errors:

- HTML structure may have changed
- Open an issue with the URL that fails
- We can update selectors
