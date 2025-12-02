# CV.ee API Research

**Date:** December 2, 2025  
**Status:** ✅ Complete - API discovered and tested

## Summary

CV.ee is built with Next.js and exposes a JSON data API that can be accessed directly without browser automation. This makes scraping significantly easier than initially anticipated.

**Backend Search Engine:** Elasticsearch - The vacancy search service uses Elasticsearch as its backend search engine, indicated by the `"searchMode": "ELASTIC"` field in API responses. While the REST API provides a clean abstraction layer, the underlying search infrastructure is Elasticsearch-based.

## API Endpoint

```text
https://www.cv.ee/_next/data/{buildId}/en/search.json
```

### Locations Service API

```text
https://cv.ee/api/v1/locations-service/list
```

Returns complete mappings for all locations:

- **50 towns** (Estonian cities with townId)
- **15 counties** (Estonian counties with countyId)
- **196 countries** (all countries with countryId)

Response structure:

```json
{
  "towns": [
    { "id": 312, "countyId": 67, "countryId": 1, "name": "Tallinn" },
    { "id": 314, "countyId": 78, "countryId": 1, "name": "Tartu" }
  ],
  "counties": {
    "67": { "id": 67, "countryId": 1, "name": "Harjumaa" }
  },
  "countries": {
    "1": { "id": 1, "iso": "EE", "name": "Estonia" }
  }
}
```

**No authentication required** - Public API endpoint

### Dynamic Build ID

The `{buildId}` changes with each deployment. Current build ID: `e0PETwdhhXJUed_PYi4ac`

To get the current build ID:

1. Fetch the homepage: `GET https://www.cv.ee`
2. Extract from HTML: regex pattern `"buildId":"([^"]+)"`

## Query Parameters

| Parameter  | Type    | Description       | Example                |
| ---------- | ------- | ----------------- | ---------------------- |
| `keywords` | string  | Search terms      | `"system analyst"`     |
| `location` | string  | City name         | `"Tallinn"`, `"Tartu"` |
| `limit`    | integer | Results per page  | `20` (tested: 3-30)    |
| `offset`   | integer | Pagination offset | `0`, `20`, `40`        |

## Response Structure

```json
{
  "pageProps": {
    "searchResults": {
      "total": 2618,
      "vacancies": [
        {
          "id": 1472121,
          "positionTitle": "Full-stack arendaja",
          "positionContent": "",
          "employerId": 10117,
          "employerName": "Delfi Meedia AS",
          "logoId": "1d5e74a6-deb0-4ceb-937b-4d9c1f5cdc73",
          "domain": 1,
          "publishDate": "2025-12-01T11:00:40.389+00:00",
          "renewedDate": "2025-12-01T11:00:40.389+00:00",
          "expirationDate": "2025-12-07T23:59:59.999+00:00",
          "workTimes": [2],
          "languages": null,
          "categories": [10, 14],
          "keywords": ["fullstack", "PHP", "Laravel"],
          "skills": null,
          "townId": 312,
          "quickApply": false,
          "countyId": 67,
          "countryId": 1,
          "salaryFrom": null,
          "salaryTo": null,
          "hourlySalary": false,
          "suitableForRefugees": false,
          "remoteWork": false,
          "remoteWorkType": "ON_SITE"
        }
      ],
      "categories": {...},
      "languages": {...},
      "countries": {...},
      "workTimes": {...}
    }
  }
}
```

## Job Fields

### Core Fields

- `id` (integer): Unique job identifier
- `positionTitle` (string): Job title
- `positionContent` (string): Job description (empty in search results)
- `employerId` (integer): Company identifier
- `employerName` (string): Company name
- `logoId` (uuid): Company logo identifier

### Dates

- `publishDate` (ISO 8601): When job was posted
- `renewedDate` (ISO 8601): When job was last renewed
- `expirationDate` (ISO 8601): When job expires

### Location

- `townId` (integer): Town/city identifier (e.g., 312 = Tallinn)
- `countyId` (integer): County identifier
- `countryId` (integer): Country identifier (1 = Estonia)
- `domain` (integer): Website domain (1 = cv.ee)

### Job Details

- `workTimes` (array[int]): Work time types (e.g., [2] = full-time)
- `categories` (array[int]): Job category IDs
- `keywords` (array[string]): Search keywords
- `languages` (array | null): Required languages
- `skills` (array | null): Required skills

### Compensation

- `salaryFrom` (integer | null): Minimum salary in EUR
- `salaryTo` (integer | null): Maximum salary in EUR
- `hourlySalary` (boolean): Whether salary is hourly

### Flags

- `quickApply` (boolean): Quick apply available
- `suitableForRefugees` (boolean): Suitable for refugees
- `remoteWork` (boolean): Remote work available
- `remoteWorkType` (enum): "ON_SITE" | "REMOTE" | "HYBRID"

## Job Detail URL Pattern

```text
https://www.cv.ee/vacancy/{id}/{company-slug}/{position-slug}
```

Example: `https://www.cv.ee/vacancy/1472121/delfi-meedia-as/full-stack-arendaja`

## Aggregated Data

The response also includes aggregated counts for filtering:

### Categories

Mapping of category IDs to job counts (e.g., `"INFORMATION_TECHNOLOGY": 241`)

### Work Times

Mapping of work time IDs to job counts (e.g., `"FULL_TIME": 2282`)

### Languages

Mapping of language codes to job counts (e.g., `"en": 376`)

### Countries

Mapping of country IDs to job counts (e.g., `"1": 2611`)

## Implementation Notes

### Advantages

1. **No browser automation needed** - Simple HTTP requests work
2. **JSON responses** - Easy to parse, no HTML parsing required
3. **Pagination support** - Offset-based pagination works reliably
4. **No authentication required** - Public job search API
5. **Rich metadata** - Categories, keywords, salary ranges included

### Challenges

1. **Dynamic Build ID** - Must be extracted from homepage on each session
2. ~~**Location IDs** - `townId` values need to be mapped to city names~~ ✅ **SOLVED** - Use locations service API
3. ~~**Category IDs** - Need lookup table to map category integers to names~~ (Categories available in search response)
4. **Rate limiting** - Unknown limits, implement delays to be safe
5. **Job descriptions** - Not included in search results, need separate request

### Best Practices

1. Cache build ID for session duration
2. Implement exponential backoff for rate limiting
3. Use reasonable page sizes (20-30 jobs per request)
4. Add delays between requests (1-2 seconds recommended)
5. Handle build ID changes gracefully (re-extract on 404)

## Test Script

Location: `scripts/test_cvee_api.py`

The test script demonstrates:

- Fetching location mappings from locations service API
- Extracting build ID from homepage
- Searching with keywords and location
- Resolving townId to city names
- Parsing job listings from JSON
- Testing pagination with offset

Run with: `python3 scripts/test_cvee_api.py`

## Sorting Options

- **LATEST** - Newest jobs first (recommended for monitoring)
- **OLDEST** - Oldest jobs first
- **RELEVANCE** - Best match to search criteria (recommended with keywords)

## Elasticsearch Backend

The CV.ee vacancy search service is powered by Elasticsearch. This is revealed through several indicators:

### Active Engine Endpoint

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search/active-engine"
# Returns: "ELASTIC"
```

### Response Metadata

All search responses include these fields:

- `"searchMode": "ELASTIC"` - Confirms Elasticsearch is handling queries
- `"searchId": "uuid"` - Unique identifier for each search session
- Standard Elasticsearch-style aggregations (categories, workTimes, etc.)

### Query Characteristics

**What Works:**

- Standard text search across indexed fields
- `keywords` parameter searches across positionTitle, keywords array, employer name
- Pagination via `offset` and `limit`
- Multiple filter parameters combined with AND logic
- Relevance-based scoring when using `sorting=RELEVANCE`

**Elasticsearch Features NOT Exposed:**

- ❌ Raw Elasticsearch query DSL
- ❌ Direct field-specific syntax (`field:value`)
- ❌ Boolean operators in keywords (AND/OR/NOT are treated as text)
- ❌ Explain API for score debugging
- ❌ `_source` filtering
- ❌ Direct Elasticsearch endpoint access (port 9200 not public)
- ❌ Raw Elasticsearch response format (hits, \_score, etc.)

### API Abstraction Layer

CV.ee implements a REST API abstraction that:

1. Translates clean parameters → Elasticsearch queries
2. Sanitizes/validates user input
3. Controls which Elasticsearch features are exposed
4. Returns simplified, application-specific JSON (not raw ES format)

**Implication:** While we know it's Elasticsearch underneath, we're limited to the parameters and features exposed through the REST API. Direct Elasticsearch querying is not available. The API provides sufficient functionality for job searching without needing raw ES access.

## Next Steps

1. ✅ API discovery complete
2. ✅ Test script created
3. ✅ Locations service API discovered
4. ✅ Categories service API discovered
5. ✅ REST API endpoints documented
6. ✅ Sorting and filtering options tested
7. ✅ Elasticsearch backend identified
8. ⏳ Implement `search_cvee()` in `job_monitor/scraper.py`
9. ⏳ Add CV.ee source to `config.yaml`
10. ⏳ Test with real job searches

## Related Links

- [Issue #24: Add CV.ee job portal support](https://github.com/mitselek/cv_system/issues/24)
- Sister sites (likely same API): cv.lv, cvonline.lt
