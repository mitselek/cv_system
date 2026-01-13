# EdgeDB Schema Redesign - Alignment with Knowledge Base

**Date:** 2026-01-12  
**Issue:** #45  
**Status:** Design Complete → Implementation Phase

## Problem

Current EdgeDB schema doesn't match the rich structure in knowledge base frontmatter files. Key mismatches:

1. **Bilingual fields** - Frontmatter has `title: {et: ..., en: ...}`, DB has single `title` field
2. **Missing metadata** - `repository`, `technologies`, `project`, `context`, `location`, `url`
3. **Missing relationships** - `skills_demonstrated`, `parent_experience`, `achievements`
4. **Field naming** - `company` vs `organization`, `skill_name` vs `name`
5. **Data formats** - `proficiency_level: "9/10"` vs `level: int16`
6. **Verification tracking** - `status`, `last_verified`, `source` not stored

## Current Schema vs Reality

### Experience

**Current DB:**

```esdl
type Experience {
    required property title -> str;
    required property organization -> str;
    required property start_date -> str;
    property end_date -> str;
    property description_et -> str;
    property description_en -> str;
    multi link tags -> Tag;
}
```

**Actual Frontmatter:**

```yaml
id: eesti-keele-instituut-2017-2018
type: employment # Not stored
company: # Field name: company vs organization
  et: Eesti Keele Instituut
  en: Institute of the Estonian Language
dates: # Nested object
  start: "2017-04-12"
  end: "2018-04-30"
title: # Bilingual object
  et: Vanamsüsteemianalüütik
  en: Senior System Analyst
location: Tallinn, Estonia # Not stored
tags: [...]
project: EKI-ASTRA (...) # Not stored
repository: https://... # Not stored
technologies: [...] # Not stored
status: verified # Not stored
last_verified: "2025-11-26" # Not stored
source: Employment contract nr 408 # Not stored
skills_demonstrated: [java, ...] # Not stored
achievements: [...] # Not stored
context: ... # Not stored (e.g., PÖFF)
url: ... # Not stored
```

### Skill

**Current DB:**

```esdl
type Skill {
    required property name -> str;
    property level -> int16;
    property description -> str;
    property evidence_refs -> array<str>;
    multi link tags -> Tag;
}
```

**Actual Frontmatter:**

```yaml
id: python
skill_name: # Field name difference
  et: Python
  en: Python
category: Programming Language # Not stored
proficiency_level: 9/10 # String format, needs parsing
tags: [programming, ...]
status: verified # Not stored
last_verified: "2025-12-20" # Not stored
evidence: [vabamu-..., poff-...] # Field name: evidence vs evidence_refs
```

### Achievement

**Current DB:**

```esdl
type Achievement {
    required property title -> str;
    property date -> str;
    property description -> str;
    multi link tags -> Tag;
}
```

**Actual Frontmatter:**

```yaml
id: poff-intern-hiring-2024
aliases: ["..."] # Not stored
type: achievement # Not stored
parent_experience: ilusa-koodi-... # Not stored - critical relationship!
title: # Bilingual
  et: Juhendas 4 praktikanti...
  en: Mentored 4 interns...
description: # Bilingual
  et: Kõik 4 praktikanti said...
  en: All 4 interns were hired...
tags: [mentoring, ...]
status: verified # Not stored
last_verified: "2025-11-21" # Not stored
```

## Proposed Schema

### Experience (Complete Redesign)

```esdl
type Experience {
    # Core identity
    required property external_id -> str {  # From frontmatter 'id'
        constraint exclusive;
    }

    # Bilingual fields
    required property title_en -> str;
    required property title_et -> str;
    required property company_en -> str;
    required property company_et -> str;

    # Dates
    required property start_date -> str;    # Keep as string (YYYY-MM-DD format)
    property end_date -> str;               # "Present" for ongoing

    # Bilingual descriptions (from markdown body)
    property description_en -> str;
    property description_et -> str;

    # Metadata
    property location -> str;
    property employment_type -> str;        # From frontmatter 'type'
    property context -> str;                # E.g., "PÖFF (Black Nights Film Festival)"

    # External references
    property url -> str;
    property repository -> str;
    property project_name -> str;
    property technologies -> array<str>;

    # Verification tracking
    property status -> str;                 # "verified", etc.
    property last_verified -> str;          # Date
    property source -> str;                 # Evidence description

    # System fields
    property created -> datetime {
        default := datetime_current();
    }

    # Relationships
    multi link tags -> Tag;
    multi link skills_demonstrated -> Skill;
    multi link achievements := .<parent_experience[is Achievement];
}
```

### Skill (Enhanced)

```esdl
type Skill {
    # Core identity
    required property external_id -> str {
        constraint exclusive;
    }

    # Bilingual name
    required property name_en -> str {
        constraint exclusive;
    }
    required property name_et -> str;

    # Proficiency
    property level -> int16;                # Parsed from "9/10" -> 9
    property level_display -> str;          # Keep original "9/10" format

    # Classification
    property category -> str;

    # Description (from markdown body)
    property description -> str;

    # Evidence
    property evidence_refs -> array<str>;

    # Verification
    property status -> str;
    property last_verified -> str;

    # System fields
    property created -> datetime {
        default := datetime_current();
    }

    # Relationships
    multi link tags -> Tag;
    multi link demonstrated_in := .<skills_demonstrated[is Experience];
}
```

### Achievement (Enhanced)

```esdl
type Achievement {
    # Core identity
    required property external_id -> str {
        constraint exclusive;
    }

    # Bilingual fields
    required property title_en -> str;
    required property title_et -> str;
    property description_en -> str;
    property description_et -> str;

    # Metadata
    property date -> str;
    property achievement_type -> str;
    property aliases -> array<str>;

    # Verification
    property status -> str;
    property last_verified -> str;

    # System fields
    property created -> datetime {
        default := datetime_current();
    }

    # Relationships
    multi link tags -> Tag;
    link parent_experience -> Experience;   # Critical: links to experience
}
```

### Tag (Enhanced)

```esdl
type Tag {
    required property name -> str;
    required property category -> str;

    # Normalization tracking
    property aliases -> array<str>;         # Alternative names
    property normalized_from -> array<str>; # What was consolidated

    property created -> datetime {
        default := datetime_current();
    }

    constraint exclusive on ((.name, .category));

    # Backlinks
    multi link experiences := .<tags[is Experience];
    multi link skills := .<tags[is Skill];
    multi link achievements := .<tags[is Achievement];
}
```

## Key Decisions

### 1. Bilingual Strategy

**Proposal:** Store both languages as separate fields (`_en`, `_et` suffix)

**Rationale:**

- Preserves both languages
- Allows language-specific queries
- Simple, no JSON complexity
- Clear field names in queries

**Alternative considered:** JSON field `title: {en: "...", et: "..."}`

- Rejected: Harder to query, type safety issues

### 2. External ID

**Proposal:** Add `external_id` field to store frontmatter `id`

**Rationale:**

- Preserves original identifiers
- Enables traceability to source files
- Unique constraint for data integrity
- EdgeDB generates its own UUIDs internally

### 3. Date Format

**Proposal:** Keep dates as strings (`"2017-04-12"` or `"Present"`)

**Rationale:**

- Matches frontmatter exactly
- Handles "Present" naturally
- Simple date range queries still possible
- No timezone complexity

### 4. Array Fields

**Proposal:** Use native EdgeDB arrays for `technologies`, `evidence_refs`, `aliases`

**Rationale:**

- Native type support
- Queryable
- Simple to populate from YAML arrays

### 5. Relationships

**Proposal:** Proper links instead of string references

**Experience.skills_demonstrated -> Skill**

- Many-to-many: One experience can demonstrate multiple skills
- Backlink: `Skill.demonstrated_in` shows which experiences use this skill

**Achievement.parent_experience -> Experience**

- Many-to-one: Achievement belongs to one experience
- Backlink: `Experience.achievements` lists all achievements

## Migration Strategy

### Phase 1: Schema Update

1. Create new schema file: `dbschema/default.esdl`
2. Run `edgedb migration create`
3. Apply migration: `edgedb migrate`

### Phase 2: Data Import

1. Parse `_compiled_context.md` or individual files
2. Extract all unique tags first (create Tag entries)
3. Import Skills (need tags to exist)
4. Import Experiences (need tags and skills to exist)
5. Import Achievements (need experiences to exist)

### Phase 3: Validation

1. Count: 20 experiences, 18 skills, 13 achievements
2. Verify tag relationships
3. Test MCP tool queries
4. Verify backlinks work

## Design Decisions

### 1. Multilingual Fields - ✅ DECIDED (Revised Implementation)

**Decision:** Use `scalar type Translation` extending JSON with constraint validation

**Original Plan:** Tuple-based scalar type (proven impossible in EdgeDB)

**Why Tuple Approach Failed:**
EdgeDB does not support `scalar type` extending `tuple`. Attempted implementation:

```esdl
scalar type Translation extending tuple<et: optional str, en: optional str>
```

Error: `scalar type 'default::tuple' does not exist`

**Constraint:** Scalar types in EdgeDB can only extend primitive types (`str`, `int64`, `json`, etc.) or enums, not composite types like tuples.

**Final Implementation:**

```esdl
scalar type Translation extending json {
    constraint expression on (
        len(<str>__subject__['et'] ?? '') > 0 OR
        len(<str>__subject__['en'] ?? '') > 0
    ) {
        errmessage := 'At least one language (et or en) must be provided';
    };
}

type Experience {
    required property title -> Translation;
    required property company -> Translation;
    property article -> Translation;
}
```

**Usage Patterns:**

```typescript
// TypeScript/JavaScript (MCP Server, Import Scripts)
// EdgeDB client auto-serializes JS objects to JSON
const result = await client.querySingle(
  `
  INSERT Experience {
    title := <Translation>$title,
    company := <Translation>$company
  }
`,
  {
    title: { en: "Senior Developer", et: "Vanemarendaja" },
    company: { en: "Tech Corp" },
  }
);
```

```python
# Python (Import Scripts)
# Pass dict directly, EdgeDB serializes to JSON
await client.query('''
    INSERT Experience {
        title := <Translation>$title,
        company := <Translation>$company
    }
''', title={"en": "Senior Developer", "et": "Vanemarendaja"},
     company={"en": "Tech Corp"})
```

```esdl
# Query with smart fallback
SELECT Experience {
    title_en := <str>.title['en'],
    title_et := <str>.title['et'],
    display_title := <str>.title['en'] ?? <str>.title['et']
};
```

**Critical: NO JSON.stringify() or to_json() needed!**

- ❌ WRONG: `JSON.stringify({en: 'text'})` → Double-stringified, violates constraint
- ❌ WRONG: `to_json('{"en":"text"}')` → Unnecessary, client handles serialization
- ✅ CORRECT: Pass object directly `{en: 'text'}` → EdgeDB client serializes automatically

**Rationale:**

- **Type safety with validation:** JSON scalar + constraint enforces structure at DB level
- **Performance:** Atomic storage, all translations in single row, zero join overhead
- **Reusability:** Define once, use across all types (Experience, Skill, Achievement, etc.)
- **Constraint enforcement:** "At least one language" validated at database level
- **Flexibility:** JSON structure supports optional fields naturally
- **DRY principle:** Constraint and validation defined in one place

**Benefits over alternatives:**

- **vs Tuple (impossible):** Tuples can't be extended by scalar types in EdgeDB
- **vs Separate properties (`_et`/`_en`):** Not extensible, verbose, no cohesion
- **vs Object type (`type Translation`):** Creates separate entities, performance overhead from joins
- **vs Unconstrained JSON:** Loses validation, no enforcement of required structure

**Trade-offs:**

- ⚠️ **Query syntax overhead:** Must use `<str>.field['en']` bracket notation (mitigatable with computed properties)
- ⚠️ **TypeScript integration:** Default type is `unknown`, requires explicit interface definition
- ✅ **Clean inserts/updates:** No `JSON.stringify()` or `to_json()` needed - pass objects directly
- ✅ **Atomic validation:** Empty object `{}` rejected by constraint
- ✅ **Performance:** Single-row storage, indexable, no joins
- ✅ **Client auto-serialization:** EdgeDB protocol handles JS/Python object → JSON conversion

**TypeScript Interface (for client library):**

```typescript
interface Translation {
  et?: string;
  en?: string;
}
```

**Future-proof:** Adding Ukrainian/French requires updating constraint only:

```esdl
constraint expression on (
    len(<str>__subject__['et'] ?? '') > 0 OR
    len(<str>__subject__['en'] ?? '') > 0 OR
    len(<str>__subject__['ua'] ?? '') > 0 OR
    len(<str>__subject__['fr'] ?? '') > 0
)
```

**Validation Confirmed:** ✅

- Inserted test data: `{"en": "Python Programming", "et": "Pythoni programmeerimine"}` - Success
- Query with fallback: `<str>.name['en'] ?? <str>.name['et']` - Works perfectly
- Empty object `{}` rejected: "JSON index 'et' is out of bounds" - Constraint enforced
- **Client serialization validated:** JS/Python objects passed directly, no `JSON.stringify()` needed

**Production Usage Discovery (2025-01):**

During MCP server implementation and testing, discovered the correct usage pattern:

```typescript
// ❌ INCORRECT (initial assumption from EdgeQL docs)
const title = JSON.stringify({ en: "Python" });
await client.query("INSERT Skill { name := <Translation>to_json($title) }", {
  title,
});
// Result: Double-stringified string violates Translation constraint

// ✅ CORRECT (validated through testing)
const title = { en: "Python" };
await client.query("INSERT Skill { name := <Translation>$title }", { title });
// Result: EdgeDB client auto-serializes object to JSON, constraint satisfied
```

**Key Insight:** The JSON approach is **cleaner than expected** because EdgeDB's protocol handles serialization automatically. The original concern about "messy double-stringification" was based on incorrect usage assumptions.

**Potential Enhancements (see issue #48):**

1. **Global utility function** for DRY translation fallback:

   ```esdl
   function get_text(t: Translation, lang: str) -> str
     using (<str>t[lang] ?? <str>t['et'] ?? <str>t['en'] ?? '');
   ```

2. **Computed properties** to hide JSON syntax from queries:

   ```esdl
   type Skill {
     required property name -> Translation;
     property display_name := get_text(.name, 'en');
   }
   ```

These would reduce query verbosity while preserving all benefits of JSON storage.

### 2. URL Validation - ✅ DECIDED

**Decision:** Use strict `scalar type HttpUrl` with proper URL format validation

**Implementation:**

```esdl
scalar type HttpUrl extending str {
    constraint regexp(r'^https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&''()*+,;=%]+$') {
        errmessage := 'Invalid HTTP/HTTPS URL format';
    };
}

type Experience {
    property url -> HttpUrl;
    property repository -> HttpUrl;
}
```

**Rationale:**

- **Validation at database level:** Prevents invalid URLs from being stored
- **Semantic clarity:** `HttpUrl` type communicates intent
- **Reusability:** Define once, use across Experience, Skill, Tag types
- **Type safety:** Database enforces URL format constraints

**Import Pipeline Preprocessing:**
Markdown-wrapped URLs in frontmatter (e.g., `<https://github.com/entu>`) will be cleaned during import:

```python
# Import script preprocessing
def clean_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return None
    # Strip markdown angle brackets
    return raw_url.strip('<>').strip()
```

**Files with markdown-wrapped URLs:**

- `entusiastid-ou-2010-present.md`: `<https://entu.ee>`
- `ilusa-koodi-instituut-2021-2024.md`: `<https://github.com/poff-bnff/web2021>`

These will be automatically corrected during import, ensuring database integrity.

### 3. Status Enums - ✅ DECIDED

**Decision:** Use separate enums for different semantic domains

**Implementation:**

```esdl
# For Experience, Skill, Achievement - verification tracking
scalar type VerificationStatus extending enum<
    verified,
    draft,
    outdated
>;

# For Projects - lifecycle tracking
scalar type ProjectStatus extending enum<
    active,
    completed,
    archived
>;

type Experience {
    property status -> VerificationStatus {
        default := VerificationStatus.verified;
    };
}

type Skill {
    property status -> VerificationStatus {
        default := VerificationStatus.verified;
    };
}

type Achievement {
    property status -> VerificationStatus {
        default := VerificationStatus.verified;
    };
}

type Project {
    property status -> ProjectStatus {
        default := ProjectStatus.active;
    };
}
```

**Rationale:**

- **Semantic clarity:** Different entity types have different status lifecycles
- **Type safety:** Prevents invalid status assignments (can't set Experience to "active")
- **Domain-appropriate:** VerificationStatus for curated knowledge, ProjectStatus for work items
- **Extensible:** Can add domain-specific statuses without affecting other types

**Current data mapping:**

- **VerificationStatus.verified:** All 51 experiences/skills/achievements currently use this
- **ProjectStatus.active:** 9 projects (ongoing)
- **ProjectStatus.completed:** 3 projects (finished)
- **ProjectStatus.archived:** 2 projects (no longer maintained)

### 4. Skill Category Taxonomy - ✅ DECIDED

**Decision:** Use flat enum `SkillCategory` (not hierarchical)

**Implementation:**

```esdl
scalar type SkillCategory extending enum<
    # Technical Skills
    programming_language,
    backend_development,
    framework,
    database_programming,
    database_management,

    # Data Skills
    data_engineering,
    data_extraction,
    data_curation,

    # Management & Leadership
    management,

    # Tools & Methods
    development_tools,
    technical
>;

type Skill {
    required property name -> Translation;
    property category -> SkillCategory;  # Flat, no hierarchy
    multi link tags -> Tag;              # Detailed facets (separate from category)
}
```

**Rationale:**

- **Flat structure:** Categories are peer-level, no parent/child relationships
- **CV organization:** Category defines which CV section the skill appears in
- **Separate from tags:** Category = high-level bucket, Tags = detailed facets
- **Type safety:** Enum prevents typos and enforces consistent categorization
- **Simple queries:** Direct filtering without recursive traversal

**Import mapping:**

```python
CATEGORY_MAP = {
    "Programming Language": SkillCategory.programming_language,
    "Backend Development": SkillCategory.backend_development,
    "Framework": SkillCategory.framework,
    "Database Programming": SkillCategory.database_programming,
    "Database Management": SkillCategory.database_management,
    "Data Engineering": SkillCategory.data_engineering,
    "Data Extraction": SkillCategory.data_extraction,
    "Data": SkillCategory.data_curation,  # "Data" maps to data_curation
    "Management": SkillCategory.management,
    "Development Tools": SkillCategory.development_tools,
    "Technical": SkillCategory.technical,
    "technical": SkillCategory.technical,  # Normalize case inconsistency
}
```

**Current data:** 18 skills across 11 categories (now normalized to 14 enum values)

### 5. Technologies Array - ✅ DECIDED

**Decision:** Use simple string array (normalize later if needed)

**Implementation:**

```esdl
type Experience {
    property technologies -> array<str>;
}
```

**Rationale:**

- **Pragmatic start:** String array meets current needs (4/20 experiences use this field)
- **Preserves specificity:** Can store versions ("Spring Boot 2.6.12") and compound names
- **Simple import:** No normalization headaches during initial data migration
- **Display-focused:** Technologies are primarily for CV listings, not complex analytics
- **Future-proof:** Can migrate to normalized Technology type later if needed

**Import handling:**

```python
# Simple array - import as-is
technologies: ['Java JDK 17', 'Spring Boot 2.6.12', 'Postgres 15.4']

# Structured stack - flatten during import
technology_stack:
  backend: ['Node.js', 'Strapi CMS']
  frontend: ['Pug', 'Stylus']
# → technologies: ['Node.js', 'Strapi CMS', 'Pug', 'Stylus']
```

**Query pattern:**

```edgeql
# Find experiences using Spring Boot (any version)
SELECT Experience FILTER any(.technologies LIKE '%Spring Boot%');
```

**Migration path:** If technology analytics become important later, can create Technology type and migrate array data into links.

### 6. Evidence Linking - ✅ DECIDED

**Decision:** Use proper links with computed backlinks (Project → Skill direction)

**Implementation:**

```esdl
type Project {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;
    property status -> ProjectStatus;

    # Store the relationship in this direction
    multi link skills_demonstrated -> Skill;
}

type Skill {
    required property external_id -> str { constraint exclusive; };
    required property name -> Translation;

    # Computed backlink - database maintains this automatically
    multi link demonstrated_in := .<skills_demonstrated[is Project];
}
```

**Usage:**

```edgeql
# Insert Project with skills (single statement)
INSERT Project {
    external_id := 'vabamu-migration',
    title := (et := 'Vabamu migratsioon', en := 'Vabamu Migration'),
    skills_demonstrated := (
        SELECT Skill FILTER .external_id IN {'python', 'data-processing'}
    )
}

# Query from Project side (stored direction)
SELECT Project {
    title,
    skills_demonstrated: { name }
};

# Query from Skill side (computed backlink - works automatically!)
SELECT Skill {
    name,
    demonstrated_in: { title, status }
} FILTER .external_id = 'python';
```

**Rationale:**

- **Referential integrity:** Can't link to non-existent entities
- **No sync issues:** Computed backlinks eliminate manual bidirectional sync problems
- **Type safety:** Links are validated at database level
- **Semantic clarity:** "Project uses Skills" is natural direction
- **Rich queries:** Navigate both directions with ease

**Import order:**

1. Import all Skills first (without evidence)
2. Import all Projects (link to existing skills via `skills_demonstrated`)
3. Backlinks (`demonstrated_in`) work automatically - no additional steps needed

**Frontmatter mapping:**

```python
# projects/vabamu-museum-migration.md
skills_demonstrated: [python, data-processing]  # → Used directly

# skills/python.md
evidence: [vabamu-migration, poff-scripts]  # → Ignore during import, use backlink instead
```

### 7. Markdown Body Storage - ✅ DECIDED

**Decision:** Use `Translation` type for all article/body fields (consistent with frontmatter)

**Implementation:**

```esdl
scalar type Translation extending tuple<et: optional str, en: optional str> {
    constraint expression on (
        len(__subject__.et ?? '') > 0 OR
        len(__subject__.en ?? '') > 0
    );
};

type Experience {
    required property title -> Translation;      # Frontmatter
    required property company -> Translation;    # Frontmatter
    property description -> Translation;         # Frontmatter
    property article -> Translation;             # Markdown body content
}

type Skill {
    required property name -> Translation;       # Frontmatter
    property article -> Translation;             # Markdown body content
}

type Achievement {
    required property title -> Translation;      # Frontmatter
    property description -> Translation;         # Frontmatter (short)
    property article -> Translation;             # Markdown body content (if present)
}

type Project {
    required property title -> Translation;      # Frontmatter
    property article -> Translation;             # Markdown body content
}
```

**Rationale:**

- **Consistency:** Same type for all multilingual content (frontmatter + body)
- **Uniform structure:** All types have `property article -> Translation`
- **Optional fields:** Empty tuple element `{et: None, en: "..."}` for single-language content
- **Future-proof:** Bodies can transition from single to bilingual without schema changes
- **Type safety:** Database enforces "at least one language" constraint

**Import handling:**

```python
# Bilingual body (experiences, some skills)
## et
Eesti keeles sisu...

## en
English content...
# → article: {et: "Eesti keeles sisu...", en: "English content..."}

# English-only body (most skills, projects)
### Overview
Technical details...
# → article: {et: None, en: "### Overview\nTechnical details..."}

# Empty body (achievements)
# (only frontmatter description present)
# → article: {et: None, en: None}  # or omit field entirely
```

**Data distribution:**

- **Experiences (20):** All have bilingual bodies (`## et` / `## en` sections)
- **Skills (18):** Mixed - some bilingual (`### et` / `### en`), some English-only
- **Achievements (13):** Mostly no body (description in frontmatter only)
- **Projects:** Currently English-only, but schema supports future bilinguality

**Consistency with Decision #1:**
Both frontmatter metadata and markdown body content use the same `Translation` type, ensuring uniform handling of multilingual data throughout the system.

### 12. Date Format Validation - ✅ DECIDED

**Current usage:** Dates appear in multiple formats and granularities across frontmatter:

```yaml
dates:
  start: "2017-04-12"      # Full date
  end: "2018-04-30"        # Full date
date: "2025-02"            # Year-month (education)
date: "2005"               # Year only (certification)
last_verified: "2025-12-20"  # Full date
```

**Decision:** Create flexible `IsoDate` scalar type supporting multiple granularities.

**Implementation:**

```esdl
scalar type IsoDate extending str {
    constraint regexp(r'^\d{4}(-\d{2}(-\d{2})?)?$') {
        errmessage := 'Date must be in YYYY, YYYY-MM, or YYYY-MM-DD format';
    };
}
```

**Supported formats:**

- `YYYY` - Year only (e.g., "2005")
- `YYYY-MM` - Year and month (e.g., "2025-02")
- `YYYY-MM-DD` - Full date (e.g., "2025-12-20")

**Usage across all types:**

```esdl
# Experience
property dates -> tuple<start: IsoDate, end: optional IsoDate>;
required property last_verified -> IsoDate;

# Certification
required property date -> IsoDate;

# Achievement
property date -> IsoDate;

# Education
property dates -> tuple<start: IsoDate, end: optional IsoDate>;
```

**Rationale:**

- DRY principle - Define constraint once, reuse everywhere
- Clear semantic meaning - `IsoDate` is self-documenting
- **Flexible granularity** - Handles year-only certifications, year-month education periods
- Consistent validation - All dates validated at database level
- Simple queries - `FILTER .last_verified < <IsoDate>'2024-01-01'`
- Matches frontmatter convention exactly (ISO 8601 prefix formats)

**Alternative considered:** `cal::local_date` rejected - loses string format flexibility, can't represent year-only or year-month dates.

### 13. Verification Tracking - ✅ DECIDED

**Current usage:** All verified entries have `last_verified` field.

**Decision:** Make `last_verified` required using `IsoDate` type (see Decision #12).

**Rationale:**

- Data quality tracking is essential (CV accuracy depends on freshness)
- Required field enforces verification workflow
- Uses `IsoDate` for consistent format validation
- Queryable for finding stale entries: `SELECT Experience FILTER .last_verified < <IsoDate>'2024-01-01'`

## Design Decisions Complete

All 13 schema design decisions have been finalized:

### Core Design (1-7)

**#1 Multilingual fields** - `scalar type Translation` with tuple (frontmatter)  
**#2 URL validation** - `scalar type HttpUrl` with regex constraint  
**#3 Status enums** - Separate `VerificationStatus` and `ProjectStatus`  
**#4 Skill categories** - Flat `SkillCategory` enum  
**#5 Technologies** - String array (normalize later if needed)  
**#6 Evidence linking** - Proper links with computed backlinks (Project → Skill)  
**#7 Markdown body storage** - `Translation` type for article fields (consistent with frontmatter)

### Additional Entity Types (8-11)

**#8 Certification titles** - Use `Translation` type (future-proof for Estonian equivalents)  
**#9 Education arrays** - `array<Translation>` for institutions/fields (type-safe, preserves structure)  
**#10 Language proficiency** - Structured `LanguageProficiency` tuple + evidence links to Experience  
**#11 Hobby categories** - Drop `category` field, use Tag system exclusively

### Data Quality & Validation (12-13)

**#12 Date format validation** - `scalar type IsoDate` with YYYY, YYYY-MM, YYYY-MM-DD formats (reusable)  
**#13 Verification tracking** - Required `last_verified` using `IsoDate` type

### Entity Type Coverage

| Entity        | Count   | Status                |
| ------------- | ------- | --------------------- |
| Experience    | 20      | Designed              |
| Skill         | 18      | Designed              |
| Achievement   | 13      | Designed              |
| Project       | ~5      | Designed              |
| Certification | 5       | Designed              |
| Education     | 2       | Designed              |
| Language      | 5       | Designed              |
| Hobby         | 5       | Designed              |
| Tag           | N/A     | Designed (shared)     |
| **Total**     | **73+** | **All types covered** |

## Additional Entity Types

### Inventory

**Discovered in knowledge base:**

| Type          | Count | Fields                                              | Complexity |
| ------------- | ----- | --------------------------------------------------- | ---------- |
| Certification | 5     | title, issuer, date, credential_id                  | Simple     |
| Education     | 2     | institutions (array), fields (array), degree, dates | Complex    |
| Language      | 5     | language_name, proficiency (breakdown), evidence    | Medium     |
| Hobby         | 5     | title, category, tools (array)                      | Simple     |

### 8. Certifications - ✅ DECIDED

**Frontmatter structure:**

```yaml
id: mtcna-2025
type: certification
title: MikroTik Certified Network Associate (MTCNA) # Currently single-language
issuer: Mikrotikls SIA
date: "2025-02-09"
credential_id: 2502NA5725 # Optional
status: verified
last_verified: "2025-11-21"
```

**Decision:** Use `Translation` type for consistency with all other entity titles, even though current data is English-only. During import, populate `{et: None, en: "Official Title"}`.

**Rationale:**

- Consistency with all entity types (Experience, Skill, Project, etc.)
- Future-proof for Estonian equivalents (e.g., "MikroTik Sertifitseeritud Võrguadministraator")
- Optional fields handle current single-language reality

**Schema:**

```esdl
type Certification {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;
    required property issuer -> str;         # Organization name
    required property date -> str;           # Issue date (YYYY-MM-DD or YYYY)
    property credential_id -> str;           # Optional verification ID
    property status -> VerificationStatus;
    property last_verified -> str;
    property article -> Translation;         # Body content

    property created -> datetime {
        default := datetime_current();
    }
}
```

### 9. Education - ✅ DECIDED

**Frontmatter structure:**

```yaml
id: university-studies-1990-2002
type: education
dates:
  start: "1990"
  end: "2002"
institutions: # ARRAY of bilingual objects
  - name:
      et: Tartu Ülikool
      en: University of Tartu
  - name:
      et: Tallinna Ülikool
      en: Tallinn University
fields: # ARRAY of bilingual fields of study
  - et: Matemaatika
    en: Mathematics
  - et: Informaatika
    en: Computer Science
degree:
  et: Lõpetamata kõrgharidus
  en: Incomplete Higher Education
description:
  et: Matemaatika, informaatika...
  en: Mathematics, computer science...
```

**Decision:** Use `array<Translation>` for institutions and fields. This preserves bilinguality while maintaining type safety and queryability.

**Rationale:**

- Type-safe (not JSON) with full compile-time checking
- Preserves array structure for multiple institutions/fields
- Preserves bilinguality for each element
- Queryable: `SELECT Education FILTER 'University of Tartu' IN .institutions.en`
- Consistent with Translation pattern used elsewhere

**Schema:**

```esdl
type Education {
    required property external_id -> str { constraint exclusive; };
    required property dates -> tuple<start: str, end: optional str>;

    # Arrays of bilingual content
    property institutions -> array<Translation>;   # Multiple universities
    property fields -> array<Translation>;         # Multiple study fields

    property degree -> Translation;                # Bilingual degree name
    property description -> Translation;           # Frontmatter description
    property article -> Translation;               # Body content

    property status -> VerificationStatus;
    property last_verified -> str;

    property created -> datetime {
        default := datetime_current();
    }
}
```

### 10. Languages - ✅ DECIDED

**Frontmatter structure:**

```yaml
id: english
type: language
language_name:
  et: Inglise keel
  en: English
proficiency: # STRUCTURED breakdown
  listening: C2
  reading: C2
  speaking: C1
  presentation: C1
  writing: C2
tags: [language, communication, international]
evidence: # Links to experiences
  - entusiastid-ou-2010-present
  - ilusa-koodi-instituut-2021-2024
```

**Decision:** Use structured tuple type `LanguageProficiency` for type safety and queryability. Evidence links point to Experience entities (proper links with backlinks).

**Rationale:**

- Type-safe access: `.proficiency.speaking` with compile-time checking
- Queryable: `SELECT Language FILTER .proficiency.speaking = 'C2'`
- Preserves all 5 CEFR skill categories (listening, reading, speaking, presentation, writing)
- Proper links to Experience (not string references) with referential integrity
- Computed backlinks from Experience side (no manual sync)

**Schema:**

```esdl
scalar type LanguageProficiency extending tuple<
    listening: str,      # CEFR levels: A1, A2, B1, B2, C1, C2
    reading: str,
    speaking: str,
    presentation: str,
    writing: str
>;

type Language {
    required property external_id -> str { constraint exclusive; };
    required property name -> Translation;           # language_name in frontmatter
    property proficiency -> LanguageProficiency;     # Structured breakdown
    property status -> VerificationStatus;
    property last_verified -> str;
    property article -> Translation;                 # Body content

    property created -> datetime {
        default := datetime_current();
    }

    # Relationships
    multi link tags -> Tag;
    multi link demonstrated_in -> Experience;        # Evidence links
}
```

### 11. Hobbies - ✅ DECIDED

**Frontmatter structure:**

```yaml
id: 3d-modeling-printing
type: hobby
title:
  et: 3D modelleerimine ja printimine
  en: 3D modeling and printing
category: technical-creative # String value (only 1/5 files)
tools:
  - Onshape
  - FeatureScript
  - 3D printers
tags: [hobby, 3d-modeling, prototyping, CAD]
```

**Decision:** Drop `category` field entirely, use Tag system exclusively.

**Rationale:**

- Only 1/5 hobbies uses `category` field (redundant)
- Tag system already provides classification (`[hobby, 3d-modeling, prototyping, CAD]`)
- Tags are more flexible (multiple categories possible)
- Consistent with other entity types (Experience, Skill use tags for classification)
- If CV needs "hobby type" grouping, can query by specific tags or tag categories

**Data analysis:** 5 hobby files examined - all have bilingual titles and tags; only 1 has `category`, `tools`, and verification fields (all optional).

**Schema:**

```esdl
type Hobby {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;          # Bilingual title
    property tools -> array<str>;                    # Tool names
    property status -> VerificationStatus;
    property last_verified -> str;
    property article -> Translation;                 # Body content

    property created -> datetime {
        default := datetime_current();
    }

    # Relationships
    multi link tags -> Tag;                          # Classification via tags
}
```

## Design Decisions Summary - ALL COMPLETE ✅

All 11 schema design decisions finalized:

### Core Entity Design (1-7)

✅ **#1 Multilingual fields** - `scalar type Translation` with tuple (frontmatter)  
✅ **#2 URL validation** - `scalar type HttpUrl` with regex constraint  
✅ **#3 Status enums** - Separate `VerificationStatus` and `ProjectStatus`  
✅ **#4 Skill categories** - Flat `SkillCategory` enum  
✅ **#5 Technologies** - String array (normalize later if needed)  
✅ **#6 Evidence linking** - Proper links with computed backlinks (Project → Skill)  
✅ **#7 Markdown body storage** - `Translation` type for article fields (consistent with frontmatter)

### Additional Entity Types (8-11)

✅ **#8 Certification titles** - Use `Translation` type (future-proof for Estonian equivalents)  
✅ **#9 Education arrays** - `array<Translation>` for institutions/fields (type-safe, preserves structure)  
✅ **#10 Language proficiency** - Structured `LanguageProficiency` tuple + evidence links to Experience  
✅ **#11 Hobby categories** - Drop `category` field, use Tag system exclusively

### Data Quality (12)

✅ **#12 Verification tracking** - Required `last_verified` with YYYY-MM-DD format constraint

| Project | ~5 | ✅ Designed |
| Certification | 5 | ✅ Designed |
| Education | 2 | ✅ Designed |
| Language | 5 | ✅ Designed |
| Hobby | 5 | ✅ Designed |
| Tag | N/A | ✅ Designed (shared) |
| **Total** | **73+** | **All types covered** |

## Next Steps

1. ✅ Identify all entity types (20 exp, 18 skills, 13 achv, ~5 projects, 5 certs, 2 edu, 5 langs, 5 hobbies)
2. ✅ Design schema for all entity types (11 decisions completed)
3. **NEXT:** Implement complete EdgeDB schema in `dbschema/default.esdl`
4. Create EdgeDB migration (`edgedb migration create`)
5. Apply migration (`edgedb migrate`)
6. Build Python import script (parse frontmatter + markdown bodies)
7. Import all 73+ knowledge base entries
8. Verify data integrity and relationships
9. Test MCP tools with new schema
10. Update MCP server TypeScript types to match new schema

---

**Status:** Design phase complete ✅ Ready for implementation!
