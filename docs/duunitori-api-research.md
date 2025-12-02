# Duunitori API Research

## Investigation Date

2025-01-03

## Summary

Duunitori uses Django REST Framework but does **not** expose a public JSON API for job search. Only auxiliary APIs are available.

## Discovered API Endpoints

### 1. Areas API (`/api/v1/areas`)

**Purpose:** Location/area data for Finland

**Format:** JSON (with `?format=json` parameter or `Accept: application/json` header)

**Example Request:**

```bash
curl "https://duunitori.fi/api/v1/areas?format=json"
```

**Response Structure:**

```json
{
  "results": [
    {
      "name": "brändö",
      "slug": "brando",
      "type": "area"
    },
    {
      "name": "eckerö",
      "slug": "eckero",
      "type": "area"
    }
  ]
}
```

**Use Case:** Could be used for location autocomplete or validation

---

### 2. Search Autocomplete API (`/api/v1/search_autocomplete`)

**Purpose:** Employer/company group suggestions

**Format:** JSON

**Example Request:**

```bash
curl "https://duunitori.fi/api/v1/search_autocomplete?q=python" -H "Accept: application/json"
```

**Response Structure:**

```json
{
  "results": [
    {
      "name": "Barona (ryhmä)",
      "type": "group"
    },
    {
      "name": "Helsingin kaupunki, kaikki toimialat (ryhmä)",
      "type": "group"
    }
  ]
}
```

**Use Case:** Employer name suggestions during search

---

## Non-Existent Endpoints

### Job Listings API

- **Tested:** `/api/v1/jobadvertisements`, `/api/v1/jobs`, `/api/v1/vacancies`
- **Result:** All return 404 errors
- **Conclusion:** No public job listings JSON API exists

### Carousel Endpoint

- **URL:** `/carousel/search?haku=python`
- **Format:** HTML fragments (not JSON)
- **Purpose:** Server-side rendering for infinite scroll

## JavaScript API References

Found in page source:

```javascript
API_AREA_URL = "/api/v1/areas";
API_SEARCH_URL = "/api/v1/search_autocomplete";
```

No job search API endpoint defined in JavaScript.

## Architecture Analysis

**Backend:** Django REST Framework (confirmed by browsable API HTML)

- DRF provides automatic API documentation
- Browsable API available at endpoint URLs (HTML format)
- JSON available via `Accept: application/json` header or `?format=json` parameter

**Job Listings Rendering:**

- Server-side HTML rendering (not SPA)
- `/tyopaikat` endpoint returns fully rendered HTML
- Job boxes use CSS class `.job-box` with data attributes
- No client-side API calls for job data visible

## Comparison to CV.ee

| Feature            | CV.ee                                            | Duunitori                 |
| ------------------ | ------------------------------------------------ | ------------------------- |
| **Job Search API** | ✅ Yes (`/api/v1/vacancy-search-service/search`) | ❌ No                     |
| **Search Backend** | Elasticsearch                                    | Unknown (likely database) |
| **Rendering**      | React SPA + API                                  | Server-side HTML          |
| **Auxiliary APIs** | Locations, Categories                            | Areas, Autocomplete       |
| **Public Access**  | Yes (no auth required)                           | Limited (no job search)   |

## Recommendations

### Option 1: Continue HTML Scraping (RECOMMENDED)

**Pros:**

- Already implemented and working
- 20 tests passing (100% coverage)
- Handles all features (full details, contact info, descriptions)
- Cookie authentication works
- Reliable and stable

**Cons:**

- More fragile (HTML changes break scraper)
- Slower than API calls
- More complex parsing logic

**Decision:** Keep current implementation since no API alternative exists.

### Option 2: Contact Duunitori

**Request:** Public API access for job listings

**Unlikely:** Estonian competitor (CV.ee) has public API, Finnish sites may not follow same model.

## Conclusion

**Duunitori does NOT have a public job search API.** The site uses server-side rendering with Django templates. While they use Django REST Framework for auxiliary features (areas, autocomplete), job listings are not exposed via API.

**Recommendation:** Close Issue #28 (Refactor Duunitori to use APIs) as **won't-do**. Current HTML scraping implementation is the only viable approach.

## Testing Commands

```bash
# Test areas API
curl "https://duunitori.fi/api/v1/areas?format=json" | jq .

# Test autocomplete API
curl "https://duunitori.fi/api/v1/search_autocomplete?q=python" -H "Accept: application/json" | jq .

# Verify job search returns HTML (not JSON)
curl "https://duunitori.fi/tyopaikat?haku=python" -H "Accept: application/json" | head -20

# Check for API endpoints in page source
curl -s "https://duunitori.fi/tyopaikat?haku=python" | grep -oE "(/api/v[0-9]+/[a-z_/-]+)" | sort -u
```

## Metadata

- **Investigation:** 2025-01-03
- **Investigator:** GitHub Copilot
- **Related Issues:** #27 (Research), #28 (Refactor - will close)
- **Related Milestone:** #2 (Scraper Architecture Refactoring)
- **Conclusion:** No API refactoring possible
