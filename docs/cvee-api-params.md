# CV.ee API Parameters Reference

Quick reference for all tested and confirmed API parameters.

## Vacancy Search Service API

**Base URL:** `https://cv.ee/api/v1/vacancy-search-service/search`

### Core Parameters

| Parameter  | Type    | Required | Description                    | Example                |
| ---------- | ------- | -------- | ------------------------------ | ---------------------- |
| `keywords` | string  | No       | Search terms                   | `"python developer"`   |
| `location` | string  | No       | City name                      | `"Tallinn"`, `"Tartu"` |
| `limit`    | integer | No       | Results per page (default: 20) | `20`, `30`             |
| `offset`   | integer | No       | Pagination offset (default: 0) | `0`, `20`, `40`        |

### Filter Parameters

| Parameter      | Type    | Required | Description               | Example                    |
| -------------- | ------- | -------- | ------------------------- | -------------------------- |
| `categories[]` | string  | No       | Job category (repeatable) | `"INFORMATION_TECHNOLOGY"` |
| `salaryFrom`   | integer | No       | Minimum salary in EUR     | `3000`, `5000`             |
| `salaryTo`     | integer | No       | Maximum salary in EUR     | `8000`                     |
| `remoteWork`   | boolean | No       | Remote work filter        | `true`, `false`            |

### Sorting & Display

| Parameter    | Type    | Required | Description                  | Values                          |
| ------------ | ------- | -------- | ---------------------------- | ------------------------------- |
| `sorting`    | enum    | No       | Sort order (default: LATEST) | `LATEST`, `OLDEST`, `RELEVANCE` |
| `showHidden` | boolean | No       | Include hidden jobs          | `true`, `false`                 |

## Sorting Options Explained

### LATEST (Recommended for monitoring)

- Shows newest jobs first
- Best for daily/regular scanning
- Ensures you don't miss new postings

**Use case:** Regular job monitoring, daily scans

### OLDEST

- Shows oldest jobs first
- Less useful for monitoring
- May include expired listings

**Use case:** Historical analysis, backfilling data

### RELEVANCE (Recommended with keywords)

- Best match to search criteria
- Requires `keywords` parameter
- Algorithm-based ranking

**Use case:** Specific job searches with keywords

## Example Queries

### Basic Search

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=python&location=Tallinn&limit=20&sorting=LATEST"
```

### IT Jobs with Salary Filter

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search?categories[]=INFORMATION_TECHNOLOGY&salaryFrom=3000&sorting=LATEST&limit=30"
```

### Multiple Categories

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search?categories[]=INFORMATION_TECHNOLOGY&categories[]=TECHNICAL_ENGINEERING&salaryFrom=3000"
```

### Keyword Search with Relevance

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=python%20django&sorting=RELEVANCE&showHidden=true"
```

### Remote Work Filter

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search?remoteWork=true&categories[]=INFORMATION_TECHNOLOGY"
```

### Salary Range

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search?salaryFrom=3000&salaryTo=6000&location=Tallinn"
```

### Pagination

```bash
# First page (0-20)
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=developer&limit=20&offset=0"

# Second page (20-40)
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=developer&limit=20&offset=20"

# Third page (40-60)
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=developer&limit=20&offset=40"
```

## Categories Reference

Common category values for `categories[]` parameter:

| Category ID                | Category Name | Typical Job Count |
| -------------------------- | ------------- | ----------------- |
| `INFORMATION_TECHNOLOGY`   | IT / Software | 215-241           |
| `TECHNICAL_ENGINEERING`    | Engineering   | 113-114           |
| `ORGANISATION_MANAGEMENT`  | Management    | 110-121           |
| `EDUCATION_SCIENCE`        | Education     | 209-289           |
| `HEALTH_SOCIAL_CARE`       | Healthcare    | 105-271           |
| `SALES`                    | Sales         | 235               |
| `SERVICE_INDUSTRY`         | Services      | 238-506           |
| `LOGISTICS_TRANSPORT`      | Logistics     | 68-228            |
| `CONSTRUCTION_REAL_ESTATE` | Construction  | 83-200            |
| `FINANCE_ACCOUNTING`       | Finance       | 86-102            |
| `MARKETING_ADVERTISING`    | Marketing     | 29-75             |
| `HUMAN_RESOURCES`          | HR            | 23                |
| `STATE_PUBLIC_ADMIN`       | Public Sector | 186-196           |

Full list available at: `https://cv.ee/api/v1/vacancies-service/categories`

## Response Structure

```json
{
  "total": 1221,
  "vacancies": [
    {
      "id": 1476412,
      "positionTitle": "Python Developer",
      "employerName": "TechCorp OÜ",
      "employerId": 12345,
      "townId": 312,
      "countyId": 67,
      "countryId": 1,
      "salaryFrom": 3000.0,
      "salaryTo": 5000.0,
      "remoteWork": false,
      "remoteWorkType": "ON_SITE",
      "publishDate": "2025-12-02T10:30:00.000+00:00",
      "expirationDate": "2025-12-30T23:59:59.999+00:00",
      "categories": [10, 14],
      "keywords": ["python", "django", "postgresql"],
      "workTimes": [2]
    }
  ],
  "categories": {...},
  "workTimes": {...},
  "languages": {...},
  "countries": {...}
}
```

## Best Practices

### For Job Monitoring

```bash
# Recommended parameters for regular scanning
sorting=LATEST           # Get newest jobs first
limit=30                # Reasonable batch size
offset=0                # Start from beginning
showHidden=false        # Only active jobs
categories[]=INFORMATION_TECHNOLOGY  # Filter by category
salaryFrom=3000         # Minimum salary threshold
```

### For Job Search

```bash
# Recommended parameters for keyword searches
keywords="python django"  # Specific technologies
sorting=RELEVANCE        # Best matches first
location=Tallinn         # City filter
remoteWork=true         # Remote work option
```

### For Data Collection

```bash
# Recommended parameters for bulk collection
limit=30                # Max per request
offset=0,30,60...       # Paginate through all results
sorting=LATEST          # Consistent ordering
showHidden=true         # Complete dataset
```

## Rate Limiting

**Status:** Unknown, not documented

**Recommendations:**

- Use 1-2 second delays between requests
- Implement exponential backoff on errors
- Monitor for HTTP 429 (Too Many Requests)
- Cache results where appropriate
- Batch requests efficiently

## URL Encoding

Remember to URL encode parameters:

- Spaces → `%20` or `+`
- Special chars → percent-encoded
- Arrays → `categories[]=VALUE&categories[]=VALUE2`

**Python example:**

```python
import urllib.parse

params = {
    "keywords": "python developer",
    "location": "Tallinn",
    "categories[]": ["INFORMATION_TECHNOLOGY"],
    "salaryFrom": 3000,
    "sorting": "LATEST"
}

# requests library handles this automatically
response = requests.get(url, params=params)
```

## Related Documentation

- [API Endpoints Reference](./cvee-api-endpoints.md)
- [Full API Research](./cvee-api-research.md)
- [Test Script](../scripts/test_cvee_api.py)
- [Issue #24](https://github.com/mitselek/cv_system/issues/24)
