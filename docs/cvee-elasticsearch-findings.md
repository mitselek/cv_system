# CV.ee Elasticsearch Investigation

**Date:** December 2, 2025  
**Status:** Backend identified, direct access not available

## Discovery

CV.ee's vacancy search service is powered by **Elasticsearch**, confirmed through multiple indicators.

## Confirmation Endpoints

### Active Engine Check

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search/active-engine"
# Returns: "ELASTIC"
```

### Search Metadata

Every search response includes:

```json
{
  "searchMode": "ELASTIC",
  "searchId": "856385f3-5f1a-4eff-a970-dce3d6b1cd8e",
  "total": 1222,
  "vacancies": [...],
  ...
}
```

- **searchMode**: Explicitly states "ELASTIC"
- **searchId**: UUID tracking each search session
- **Aggregations**: Standard Elasticsearch aggregation structure for facets (categories, workTimes, languages, etc.)

## What We Tested

### ✅ Works Through API

1. **Text Search**: Keywords parameter searches across multiple fields
2. **Filtering**: Categories, salary ranges, location, remote work
3. **Sorting**: LATEST (chronological), RELEVANCE (scoring)
4. **Pagination**: Offset + limit parameters
5. **Aggregations**: Faceted counts returned automatically

### ❌ NOT Exposed

1. **Raw Elasticsearch Query DSL**: Cannot send JSON query objects
2. **Boolean Operators**: AND/OR/NOT treated as literal text, not operators
3. **Field-Specific Syntax**: `positionTitle:developer` doesn't work
4. **Explain API**: No score debugging endpoint
5. **\_source Filtering**: Cannot request specific fields only
6. **Direct ES Access**: Port 9200 not publicly accessible
7. **Raw Response Format**: No `hits`, `_score`, `_source` structure

### Test Results

```bash
# Boolean operators don't work as expected
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=python%20AND%20django"
# Returns: 1221 jobs (same as just "python" - treats "AND" as text)

curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=python%20OR%20java"
# Returns: 1221 jobs (OR not recognized as operator)

# Field-specific syntax not supported
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=positionTitle:developer"
# Returns: generic results, field prefix ignored

# Elasticsearch _source parameter ignored
curl "https://cv.ee/api/v1/vacancy-search-service/search?_source=id,positionTitle&limit=1"
# Returns: full vacancy objects (parameter ignored)

# Direct ES endpoint not accessible
curl "https://cv.ee:9200/_cluster/health"
# Connection timeout (port not exposed)
```

## Architecture Analysis

### API Abstraction Layer

CV.ee implements a **REST API wrapper** around Elasticsearch:

```text
User → REST API (/api/v1/vacancy-search-service/search)
         ↓
     Abstraction Layer (sanitizes, validates, translates)
         ↓
     Elasticsearch (actual search engine)
         ↓
     Abstraction Layer (formats, filters, enriches)
         ↓
User ← JSON Response (application-specific format)
```

**Benefits of Abstraction:**

- 🔒 **Security**: Prevents injection attacks, limits access to sensitive data
- ✅ **Simplicity**: Clean parameters instead of complex query DSL
- 🎯 **Control**: Exposes only intended functionality
- 📊 **Enrichment**: Adds metadata (searchId, aggregations) automatically
- 🛡️ **Validation**: Ensures queries are safe and performant

**Limitations:**

- ❌ Cannot leverage advanced ES features (fuzzy matching control, boosting, etc.)
- ❌ Cannot debug relevance scoring
- ❌ Limited query complexity

## Search Behavior

### Keywords Parameter

The `keywords` parameter appears to search across:

- `positionTitle` field
- `keywords` array field (employer-provided tags)
- `employerName` field
- Possibly `positionContent` field (job description)

**Evidence:**

```bash
curl "https://cv.ee/api/v1/vacancy-search-service/search?keywords=developer&limit=3" | jq '.vacancies[] | {title, keywords: .keywords[:3]}'

# Result shows matches from different fields:
{
  "title": "Full-stack arendaja",        # Title match
  "keywords": ["Delfi", "fullstack", ...]  # Keywords match
}
```

### Sorting Modes

1. **LATEST** (default): Chronological by `publishDate` DESC

   - Uses `publishDate` or `renewedDate` fields
   - Best for job monitoring (new posts first)

2. **RELEVANCE**: Elasticsearch scoring

   - Uses text similarity algorithms
   - Best with `keywords` parameter
   - Considers term frequency, field weights, etc.

3. **OLDEST**: Chronological by `publishDate` ASC
   - Currently returns null (possibly empty index or disabled)

### Aggregations (Facets)

Returned automatically with every search:

```json
{
  "categories": {
    "INFORMATION_TECHNOLOGY": 215,
    "SALES": 235,
    ...
  },
  "workTimes": {
    "FULL_TIME": 1086,
    "PART_TIME": 130,
    ...
  },
  "languages": {
    "et": 684,
    "en": 378,
    "ru": 110
  },
  "remoteWork": 121,
  "remoteWorkTypes": {
    "ON_SITE": 1101,
    "HYBRID": 121
  }
}
```

These are Elasticsearch term aggregations, providing faceted search capabilities.

## Practical Implications

### For Job Scraping

**What We Can Do:**

- ✅ Use REST API as designed (sufficient for job monitoring)
- ✅ Keyword search across multiple fields
- ✅ Filter by categories, salary, location
- ✅ Sort by relevance or date
- ✅ Paginate through all results
- ✅ Use aggregations to understand dataset

**What We Cannot Do:**

- ❌ Access raw Elasticsearch for advanced queries
- ❌ Use complex boolean logic in keywords
- ❌ Debug why specific results rank higher
- ❌ Fine-tune scoring/boosting
- ❌ Query specific fields independently

### Recommended Approach

**Use the REST API as provided.** It offers everything needed for job scraping:

```python
def search_cvee(keywords, location=None, categories=None, salary_from=None):
    """Search CV.ee using REST API."""
    params = {
        'keywords': keywords,
        'sorting': 'LATEST',
        'limit': 30,
        'offset': 0
    }

    if location:
        params['location'] = location

    if categories:
        # Note: multiple values require array notation
        for cat in categories:
            params[f'categories[]'] = cat

    if salary_from:
        params['salaryFrom'] = salary_from

    response = requests.get(
        'https://cv.ee/api/v1/vacancy-search-service/search',
        params=params
    )

    return response.json()
```

**Why Not Try Direct ES Access:**

- 🔒 Port 9200 is (correctly) firewalled
- 🛡️ Even if accessible, queries would require authentication
- ⚖️ Bypassing the API would be ethically questionable
- 🎯 REST API provides all functionality we need

## Elasticsearch Version

**Unknown** - Cannot determine without direct access.

Likely possibilities:

- Elasticsearch 7.x or 8.x (recent versions)
- Possibly OpenSearch (AWS fork of Elasticsearch)

## Sister Sites

CV.ee is part of a network of job portals:

- **cv.lv** (Latvia)
- **cvonline.lt** (Lithuania)

These likely use the **same architecture** and API structure. The Elasticsearch findings probably apply to all three sites.

## Conclusion

CV.ee uses **Elasticsearch as its search backend** but provides a **well-designed REST API abstraction** that:

- ✅ Protects the Elasticsearch cluster
- ✅ Simplifies querying for typical use cases
- ✅ Provides sufficient functionality for job searching
- ✅ Returns clean, application-specific responses

**For job scraping purposes**, the REST API is ideal. Direct Elasticsearch access is neither available nor necessary.

## Related Documentation

- [API Endpoints Reference](./cvee-api-endpoints.md)
- [API Research](./cvee-api-research.md)
- [Parameters Reference](./cvee-api-params.md)
- [Test Script](../scripts/test_cvee_api.py)
- [Issue #24](https://github.com/mitselek/cv_system/issues/24)
