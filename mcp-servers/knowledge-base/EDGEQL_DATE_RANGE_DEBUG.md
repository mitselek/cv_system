# EdgeQL Date Range Query Debugging

**Date:** 2026-01-12  
**Issue:** Experience search by date range missing experiences with NULL/undefined end_date

## Problem Statement

Date range filter should return experiences that overlap with the query range `[2022-01-01, 2023-12-31]`:

- **Expected:** 2 results (exp2 + exp3)
- **Actual:** 1 result (exp2 only)

### Test Data

```typescript
exp1: Node.js Developer
  - start: 2020-01-01
  - end: 2021-12-31
  - org: TechCorp
  - tags: [nodejs, teamwork]

exp2: Python Engineer
  - start: 2022-01-01
  - end: 2023-06-30  ← Correctly returned
  - org: DataCorp
  - tags: [python]

exp3: Full Stack Developer
  - start: 2023-07-01
  - end: undefined (NOT SET IN addExperience CALL)  ← MISSING FROM RESULTS
  - org: TechCorp
  - tags: [nodejs, python]
```

## Key Discovery from Debug Output

**FINDING:** When calling `searchExperiences({})` with NO filters, **all 3 experiences ARE returned correctly:**

```javascript
ALL experiences: [
  {
    title: 'Full Stack Developer',  // ← This IS exp3!
    startDate: '2023-07-01',
    endDate: null,                   // ← NULL value
    endDateType: 'object',           // typeof null === 'object'
    endDateIsNull: true,             // ← CONFIRMED
    endDateIsUndefined: false,
    endDateIsEmptyString: false
  },
  {
    title: 'Python Engineer',        // ← exp2
    startDate: '2022-01-01',
    endDate: '2023-06-30',
    endDateType: 'string'
  },
  {
    title: 'Node.js Developer',      // ← exp1
    startDate: '2020-01-01',
    endDate: '2021-12-31',
    endDateType: 'string'
  }
]
```

**CONFIRMED:** exp3 exists with `endDate: null`

**THE REAL PROBLEM:** When date range filter `{start: '2022-01-01', end: '2023-12-31'}` is applied, only exp2 is returned (exp3 disappears from results)

## EdgeDB Schema

```esdl
type Experience {
    required property title -> str;
    required property organization -> str;
    required property start_date -> str;
    property end_date -> str;  # OPTIONAL - no 'required'
    property description_et -> str;
    property description_en -> str;
    property created -> datetime {
        default := datetime_current();
    };
    multi link tags -> Tag;
}
```

## Current Failing Query (with debug output)

```edgeql
SELECT Experience {
  id,
  title,
  organization,
  start_date,
  end_date,
  description_en,
  description_et,
  tags: { name } ORDER BY .name,
  created
}
FILTER
  .start_date <= <str>$range_end AND
  ((.end_date ?? '') = '' OR .end_date >= <str>$range_start)

ORDER BY .start_date DESC
```

**Params:**

```json
{
  "range_start": "2022-01-01",
  "range_end": "2023-12-31"
}
```

**Current result:** Only exp2 (Python Engineer) returned
**Expected:** exp2 AND exp3 (Full Stack Developer with NULL end_date)

## EdgeQL NULL Semantics - Need to Understand

Key question: **What does `EXISTS` actually check in EdgeDB?**

From EdgeDB conceptual model:

- EdgeDB has NO NULL values - everything is a SET
- Empty set `{}` is distinct from a set containing a value
- Optional properties can be:
  1. **Not set** (empty set `{}`)
  2. **Set to a value** (e.g., `'2023-06-30'`)

**HYPOTHESIS:** When we insert `endDate: null` from TypeScript, EdgeDB might be converting it to empty set `{}`, BUT the ?? coalescing operator might not catch empty sets correctly in comparisons.

## Test to Run

Test EdgeQL behavior directly:

```edgeql
# Create test experience with no end_date
INSERT Experience {
  title := 'Test No End',
  organization := 'TestCorp',
  start_date := '2023-01-01'
  # NO end_date field
};

# Test 1: Does this match?
SELECT Experience FILTER (.end_date ?? '') = '';

# Test 2: Does EXISTS work on empty set?
SELECT Experience FILTER NOT EXISTS .end_date;

# Test 3: What is the actual value?
SELECT Experience { title, end_date, has_end := EXISTS .end_date };
```

## Attempts Made

### Attempt 1: `IS NOT SET` syntax (FAILED)

```edgeql
.end_date IS NOT SET OR .end_date >= <str>$range_start
```

**Error:** EdgeQL syntax error - `IS NOT SET` not valid

### Attempt 2: `NOT EXISTS` syntax (CURRENT)

```edgeql
NOT EXISTS .end_date OR .end_date >= <str>$range_start
```

**Status:** No syntax error, but exp3 not found

### Attempt 3: Empty params handling (FIXED DIFFERENT ISSUE)

```typescript
// Only pass params if we actually have any
const results =
  Object.keys(params).length > 0
    ? await this.client.query<any>(query, params)
    : await this.client.query<any>(query);
```

**Result:** Fixed "query parameters" error when searching with no filters

## Hypothesis

**PRIMARY HYPOTHESIS:** exp3 is not being created successfully OR is missing its end_date debug info in the output.

Evidence:

- Debug shows "ALL experiences" returns only 2 items (should be 3)
- exp3Id is being set (no creation error thrown)
- Need to verify: Does exp3 actually exist in database?

## Next Steps to Try

### 1. Verify exp3 Creation

```typescript
console.log("Created exp3:", exp3);
console.log("exp3 has id:", exp3.id);
console.log("exp3.endDate:", exp3.endDate);
```

### 2. Check Database Directly

```bash
docker exec -it cv_system-edgedb-1 edgedb query \
  "SELECT Experience { title, start_date, end_date } ORDER BY .start_date"
```

### 3. Alternative EdgeQL Syntax

If exp3 exists but end_date is empty string instead of NULL:

```edgeql
(.end_date ?? '') = '' OR .end_date >= <str>$range_start
```

### 4. Check addExperience Implementation

Does it handle missing endDate field correctly?

```typescript
// Look at experience.ts addExperience method
// Verify optional field handling
```

### 5. Type System Issue?

Maybe TypeScript/EdgeDB type mismatch on optional fields:

```typescript
// Check if we need explicit undefined:
endDate: undefined; // vs not including the field at all
```

## BREAKTHROUGH - Actual Debug Output

```javascript
Created exp3: {
  id: '0b61a98e-efa6-11f0-be68-831b8101b409',
  title: 'Full Stack Developer',
  organization: 'TechCorp',
  startDate: '2023-07-01',
  endDate: null,  // ← NULL in database
  description: 'Both frontend and backend',
  tags: [ 'search-nodejs', 'search-python' ],
  language: 'en',
  created: '2026-01-12T11:01:28.304Z'
}

ALL experiences: [
  {
    title: 'Full Stack Developer',  // ← exp3 EXISTS!
    startDate: '2023-07-01',
    endDate: null,
    endDateType: 'object',  // ← typeof null === 'object' in JavaScript
    endDateIsNull: true,    // ← CONFIRMED: it's NULL
    endDateIsUndefined: false,
    endDateIsEmptyString: false
  },
  // ... exp2 and exp1 also returned
]
```

**FINDING:** exp3 is created successfully and IS in the database with `endDate: null`.

**NEW PROBLEM:** When date range filter is applied, exp3 disappears from results!

This means the EdgeQL query `NOT EXISTS .end_date` is NOT matching NULL values.

## Status

- [x] Fixed tag AND logic (count-based approach working - 9/10 tests passing)
- [x] Verified exp3 creation - it exists with `endDate: null`
- [ ] **CURRENT ISSUE:** `NOT EXISTS .end_date` doesn't match NULL in EdgeDB
- [ ] Need different NULL check syntax

## New Hypothesis

**EdgeDB Behavior:** `NOT EXISTS .end_date` checks if the property is **not set in the schema**, not if the value is NULL.

When we insert with `endDate: null`, the property EXISTS (it's set to NULL), so `NOT EXISTS` returns FALSE.

## Solution to Try

Replace `NOT EXISTS .end_date` with explicit NULL check:

```edgeql
.end_date ?= <str>{} OR .end_date >= <str>$range_start
```

Or:

```edgeql
(.end_date ?? '') = '' OR .end_date >= <str>$range_start
```

Or check EdgeDB docs for proper NULL comparison.
