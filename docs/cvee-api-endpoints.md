# CV.ee API Endpoints Reference

Quick reference guide for all discovered CV.ee API endpoints.

**Backend:** Elasticsearch-powered search service (confirmed via `/search/active-engine` endpoint returning "ELASTIC")

## Vacancy Search Service API ⭐ RECOMMENDED

**Endpoint:** `https://cv.ee/api/v1/vacancy-search-service/search`

**Method:** GET

**Authentication:** None required

**Parameters:**

- `keywords` (string): Search terms
- `location` (string): City name (e.g., "Tallinn", "Tartu")
- `limit` (integer): Results per page (default: 20)
- `offset` (integer): Pagination offset (default: 0)
- `categories[]` (string): Category filter (e.g., "INFORMATION_TECHNOLOGY"), can be repeated
- `salaryFrom` (integer): Minimum salary filter (e.g., 3000)
- `salaryTo` (integer): Maximum salary filter
- `sorting` (enum): "LATEST" (newest first), "OLDEST" (oldest first), "RELEVANCE" (best match)
- `showHidden` (boolean): Include hidden jobs (default: false)

**Examples:**

```bash
# Basic search with keywords and location
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=python&location=Tallinn&limit=20"

# Filter by category and salary
curl "https://cv.ee/api/v1/vacancy-search-service/search?categories[]=INFORMATION_TECHNOLOGY&salaryFrom=3000&sorting=LATEST"

# Multiple filters with relevance sorting
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=developer&categories[]=INFORMATION_TECHNOLOGY&salaryFrom=3000&sorting=RELEVANCE&showHidden=true"
```

**Response:**

```json
{
  "total": 1221,
  "vacancies": [
    {
      "id": 1476412,
      "positionTitle": "Tehnik-mehaanik",
      "employerName": "TruckMaint OÜ",
      "townId": 314,
      "salaryFrom": 2000.0,
      "salaryTo": 3200.0,
      "remoteWork": false,
      "publishDate": "2025-12-02T...",
      "categories": [10, 14],
      "keywords": ["python", "django"]
    }
  ],
  "categories": {...},
  "workTimes": {...},
  "languages": {...}
}
```

**Benefits over Next.js API:**

- ✅ Static URL (no build ID needed)
- ✅ Cleaner parameter structure
- ✅ Better filtering options
- ✅ Decimal salary values (more precise)
- ✅ Standard REST API

---

## Job Search API (Next.js - Alternative)

**Endpoint:** `https://www.cv.ee/_next/data/{buildId}/en/search.json`

**Method:** GET

**Authentication:** None required

**Parameters:**

- `keywords` (string): Search terms
- `location` (string): City name (e.g., "Tallinn", "Tartu")
- `limit` (integer): Results per page (default: 20, tested up to 30)
- `offset` (integer): Pagination offset (default: 0)

**Dynamic Build ID:**
Extract from homepage HTML using regex: `"buildId":"([^"]+)"`

**Example:**

```bash
curl "https://www.cv.ee/_next/data/e0PETwdhhXJUed_PYi4ac/en/search.json?keywords=developer&location=Tallinn&limit=20"
```

**Response:**

```json
{
  "pageProps": {
    "searchResults": {
      "total": 2619,
      "vacancies": [...],
      "categories": {...},
      "languages": {...},
      "countries": {...},
      "workTimes": {...}
    }
  }
}
```

---

## Locations Service API

**Endpoint:** `https://cv.ee/api/v1/locations-service/list`

**Method:** GET

**Authentication:** None required

**Parameters:** None

**Example:**

```bash
curl "https://cv.ee/api/v1/locations-service/list"
```

**Response:**

```json
{
  "towns": [
    {
      "id": 312,
      "countyId": 67,
      "countryId": 1,
      "name": "Tallinn"
    }
  ],
  "counties": {
    "67": {
      "id": 67,
      "countryId": 1,
      "name": "Harjumaa"
    }
  },
  "countries": {
    "1": {
      "id": 1,
      "iso": "EE",
      "name": "Estonia"
    }
  }
}
```

**Data counts:**

- 50 Estonian towns
- 15 Estonian counties
- 196 countries

---

## Key Estonian Locations

### Major Cities (townId)

- Tallinn: 312
- Tartu: 314
- Narva: 297
- Pärnu: 303
- Kohtla-Järve: 288

### Counties (countyId)

- Harjumaa: 67 (includes Tallinn)
- Tartumaa: 78 (includes Tartu)
- Ida-Virumaa: 69 (includes Narva)
- Pärnumaa: 75 (includes Pärnu)
- Lääne-Virumaa: 73

---

## Work Time Types

From search response aggregation:

- `FULL_TIME`: 2282 jobs
- `FULL_TIME_WITH_SHIFTS`: 546 jobs
- `PART_TIME`: 519 jobs
- `FIXED_TERM`: 28 jobs
- `WORK_AFTER_CLASSES`: 7 jobs
- `FREELANCE`: 5 jobs
- `PRACTICE`: 5 jobs

---

## Job Categories

Common categories from search response:

- `INFORMATION_TECHNOLOGY`: 241 jobs
- `SERVICE_INDUSTRY`: 506 jobs
- `PRODUCTION_MANUFACTURING`: 340 jobs
- `EDUCATION_SCIENCE`: 289 jobs
- `HEALTH_SOCIAL_CARE`: 271 jobs
- `SALES`: 235 jobs
- `LOGISTICS_TRANSPORT`: 228 jobs
- `CONSTRUCTION_REAL_ESTATE`: 200 jobs
- `STATE_PUBLIC_ADMIN`: 196 jobs
- `TRADE`: 175 jobs
- `TOURISM_HOTELS_CATERING`: 176 jobs

---

## Language Requirements

Language codes in job postings:

- `et`: Estonian (682 jobs)
- `en`: English (376 jobs)
- `ru`: Russian (110 jobs)
- `fi`: Finnish (4 jobs)
- `de`: German (1 job)

---

## Remote Work Types

- `ON_SITE`: Office-based work
- `REMOTE`: Fully remote
- `HYBRID`: Mix of office and remote

---

## Search Engine Backend

**Endpoint:** `https://cv.ee/api/v1/vacancy-search-service/search/active-engine`

**Method:** GET

**Authentication:** None required

**Response:** `"ELASTIC"`

**Purpose:** Confirms that Elasticsearch is the backend search engine powering the vacancy search service.

**Additional Indicators:**

All search responses include:

- `"searchMode": "ELASTIC"` field
- `"searchId": "uuid"` field for tracking searches
- Elasticsearch-style aggregations for faceted search

**Note:** While Elasticsearch powers the backend, the REST API provides an abstraction layer. Direct Elasticsearch query DSL, boolean operators (AND/OR/NOT), field-specific syntax, and raw ES response formats are not exposed through the API.

---

## API Comparison

| Feature         | Vacancy Search Service       | Next.js Data API    |
| --------------- | ---------------------------- | ------------------- |
| URL Stability   | ✅ Static                    | ❌ Build ID changes |
| Authentication  | ✅ None                      | ✅ None             |
| Salary Format   | ✅ Decimal (3500.0)          | ❌ Integer (3500)   |
| Filtering       | ✅ Rich (categories, salary) | ⚠️ Limited          |
| Parameters      | ✅ Clean REST style          | ⚠️ Mixed            |
| **Recommended** | **YES**                      | Use as fallback     |

---

## Implementation Notes

### Rate Limiting

- Unknown rate limits
- Recommended: 1-2 second delay between requests
- Monitor for 429 (Too Many Requests) responses

### Build ID Handling

- Changes with each CV.ee deployment
- Must be extracted from homepage on session start
- Cache for session duration
- Gracefully handle 404 (extract new build ID)

### Location Resolution

1. Fetch locations once per session: `GET /api/v1/locations-service/list`
2. Cache in memory
3. Use `townId` from job data to lookup town name
4. Use `countyId` to lookup county name

### Best Practices

1. Start with locations API call
2. Extract and cache build ID
3. Use reasonable page sizes (20-30)
4. Implement exponential backoff
5. Add delays between requests

---

## Test Script

Location: `scripts/test_cvee_api.py`

Demonstrates all API functionality:

```bash
python3 scripts/test_cvee_api.py
```

---

## Related Documentation

- [Full API Research](./cvee-api-research.md) - Detailed technical documentation
- [Issue #24](https://github.com/mitselek/cv_system/issues/24) - Implementation tracking
- Sister sites: cv.lv, cvonline.lt (likely same API structure)
