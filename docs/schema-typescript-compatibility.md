# EdgeDB Schema vs TypeScript Interface Compatibility Analysis

**Date:** 2026-01-13  
**Issue:** #46  
**Purpose:** Assess compatibility between existing TypeScript interfaces and proposed EdgeDB schema

## Summary

✅ **Overall Assessment: HIGHLY COMPATIBLE**

The EdgeDB schema design aligns well with existing TypeScript interfaces. Main differences are intentional improvements (proper links vs string IDs, structured types vs JSON).

## Detailed Comparison

### 1. Base Structure

**TypeScript (build_context.ts):**

```typescript
interface MultilingualText {
  et?: string;
  en?: string;
}

interface BaseEntity {
  id: string;
  type: string;
  status: string;
  last_verified: string;
  tags?: string[];
}
```

**EdgeDB Schema:**

```esdl
scalar type Translation extending tuple<et: optional str, en: optional str> {
    constraint expression on (
        len(__subject__.et ?? '') > 0 OR
        len(__subject__.en ?? '') > 0
    );
}

# All types have:
property external_id -> str { constraint exclusive; }
property status -> VerificationStatus;
property last_verified -> str;
multi link tags -> Tag;
```

**Compatibility:**

- ✅ `MultilingualText` → `Translation` (equivalent, EdgeDB adds constraint)
- ✅ `id` → `external_id` (renamed for clarity, EdgeDB has internal UUID)
- ✅ `type` field not needed in EdgeDB (type system handles this)
- ✅ `status` → enum type (improvement over string)
- ✅ `tags` → proper links (improvement over string array)

**Migration:** Map `id` → `external_id`, `type` field can be derived from EdgeDB type

---

### 2. Experience Type

**TypeScript:**

```typescript
interface Experience extends BaseEntity {
  company: string;
  url?: string;
  context?: string;
  dates: DateRange;
  title: MultilingualText;
  location: string;
  description?: MultilingualText;
  achievements?: string[]; // IDs of achievement modules
  skills_demonstrated?: string[]; // IDs of skill modules
}
```

**EdgeDB Schema:**

```esdl
type Experience {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;
    required property company -> Translation;
    property description -> Translation;
    property article -> Translation;  # Markdown body
    property location -> str;
    property context -> str;
    property url -> HttpUrl;
    property dates -> tuple<start: str, end: optional str>;
    property status -> VerificationStatus;
    property last_verified -> str;

    multi link tags -> Tag;
    multi link skills_demonstrated -> Skill;
    multi link achievements := .<parent_experience[is Achievement];
}
```

**Compatibility Issues:**

| Field               | TypeScript         | EdgeDB              | Status          | Notes                                          |
| ------------------- | ------------------ | ------------------- | --------------- | ---------------------------------------------- |
| company             | `string`           | `Translation`       | ⚠️ **MISMATCH** | TS has single string, actual data is bilingual |
| url                 | `string`           | `HttpUrl`           | ✅ Compatible   | EdgeDB adds validation                         |
| dates               | `DateRange` object | `tuple<start, end>` | ✅ Compatible   | Same structure                                 |
| title               | `MultilingualText` | `Translation`       | ✅ Compatible   | Equivalent                                     |
| description         | `MultilingualText` | `Translation`       | ✅ Compatible   | Equivalent                                     |
| article             | Not present        | `Translation`       | ✅ Enhancement  | Body content added                             |
| skills_demonstrated | `string[]`         | `link Skill`        | ✅ Improvement  | Proper links                                   |
| achievements        | `string[]`         | Computed backlink   | ✅ Improvement  | Auto-maintained                                |

**Verdict:** TypeScript interface has bug - `company` should be `MultilingualText` not `string`. EdgeDB schema is correct based on actual frontmatter data.

---

### 3. Skill Type

**TypeScript:**

```typescript
interface Skill extends BaseEntity {
  skill_name: MultilingualText;
  category: string;
  proficiency_level?: string; // e.g., "9/10", "advanced"
  evidence?: string[]; // IDs of experience/achievement modules
}
```

**EdgeDB Schema:**

```esdl
type Skill {
    required property external_id -> str { constraint exclusive; };
    required property name -> Translation;  # skill_name in frontmatter
    property level -> int16;  # Parsed from "9/10"
    property level_display -> str;  # Original "9/10"
    property category -> SkillCategory;  # Enum
    property article -> Translation;
    property status -> VerificationStatus;
    property last_verified -> str;

    multi link tags -> Tag;
    multi link demonstrated_in := .<skills_demonstrated[is Project | Experience];
}
```

**Compatibility Issues:**

| Field             | TypeScript         | EdgeDB                                  | Status         | Notes                              |
| ----------------- | ------------------ | --------------------------------------- | -------------- | ---------------------------------- |
| skill_name        | `MultilingualText` | `Translation` (as `name`)               | ✅ Compatible  | Field name changed for consistency |
| category          | `string`           | `SkillCategory` enum                    | ✅ Improvement | Type safety added                  |
| proficiency_level | `string`           | `level` (int16) + `level_display` (str) | ✅ Enhancement | Parsed for queryability            |
| evidence          | `string[]`         | Computed backlink                       | ✅ Improvement | Auto-maintained                    |

**Verdict:** Fully compatible. EdgeDB improves on TypeScript design.

---

### 4. Achievement Type

**TypeScript:**

```typescript
interface Achievement extends BaseEntity {
  parent_experience: string; // ID of the parent experience
  title: MultilingualText;
  description?: MultilingualText;
}
```

**EdgeDB Schema:**

```esdl
type Achievement {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;
    property description -> Translation;
    property article -> Translation;
    property status -> VerificationStatus;
    property last_verified -> str;

    multi link tags -> Tag;
    link parent_experience -> Experience;  # Proper link
}
```

**Compatibility:**

- ✅ `parent_experience`: string ID → proper link (improvement)
- ✅ `title`, `description`: `MultilingualText` → `Translation` (equivalent)
- ✅ All fields compatible

**Verdict:** Fully compatible.

---

### 5. Education Type

**TypeScript:**

```typescript
interface Education extends BaseEntity {
  dates: DateRange | string; // Can be a range or single year string
  institutions?: string[];
  studies?: Array<{ field: MultilingualText; institution: string }>;
  degree: MultilingualText;
}
```

**EdgeDB Schema:**

```esdl
type Education {
    required property external_id -> str { constraint exclusive; };
    required property dates -> tuple<start: str, end: optional str>;
    property institutions -> array<Translation>;
    property fields -> array<Translation>;
    property degree -> Translation;
    property description -> Translation;
    property article -> Translation;
    property status -> VerificationStatus;
    property last_verified -> str;
}
```

**Compatibility Issues:**

| Field        | TypeScript                    | EdgeDB                  | Status           | Notes                                            |
| ------------ | ----------------------------- | ----------------------- | ---------------- | ------------------------------------------------ |
| dates        | `DateRange \| string`         | `tuple<start, end>`     | ⚠️ **PARTIAL**   | TS allows single string, EdgeDB requires tuple   |
| institutions | `string[]`                    | `array<Translation>`    | ⚠️ **MISMATCH**  | TS has strings, actual data is bilingual objects |
| studies      | `Array<{field, institution}>` | Separate `fields` array | ⚠️ **STRUCTURE** | TS has combined, EdgeDB separates                |
| degree       | `MultilingualText`            | `Translation`           | ✅ Compatible    | Equivalent                                       |

**Verdict:** TypeScript interface doesn't match actual frontmatter structure. Actual data has:

```yaml
institutions:
  - name: { et: "...", en: "..." }
fields:
  - et: "..."
    en: "..."
```

EdgeDB schema matches reality. TypeScript needs update.

---

### 6. Certification Type

**TypeScript:**

```typescript
interface Certification extends BaseEntity {
  title: string;
  issuer: string;
  date: string;
  credential_id?: string;
  url?: string;
}
```

**EdgeDB Schema:**

```esdl
type Certification {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;
    required property issuer -> str;
    required property date -> str;
    property credential_id -> str;
    property url -> HttpUrl;
    property article -> Translation;
    property status -> VerificationStatus;
    property last_verified -> str;
}
```

**Compatibility Issues:**

| Field         | TypeScript | EdgeDB        | Status          | Notes                                        |
| ------------- | ---------- | ------------- | --------------- | -------------------------------------------- |
| title         | `string`   | `Translation` | ⚠️ **MISMATCH** | Decision #8: Use Translation for consistency |
| issuer        | `string`   | `string`      | ✅ Compatible   | -                                            |
| date          | `string`   | `string`      | ✅ Compatible   | -                                            |
| credential_id | `string`   | `string`      | ✅ Compatible   | -                                            |
| url           | `string`   | `HttpUrl`     | ✅ Compatible   | EdgeDB adds validation                       |

**Verdict:** TypeScript has `title` as string (matches current data), EdgeDB uses `Translation` for future-proofing. Compatible via import transformation.

---

### 7. Language Type (Missing from TypeScript)

**TypeScript:** ❌ No interface defined

**Actual Frontmatter:**

```yaml
language_name: { et: "...", en: "..." }
proficiency:
  listening: C2
  reading: C2
  speaking: C1
  presentation: C1
  writing: C2
evidence: [...]
```

**EdgeDB Schema:**

```esdl
scalar type LanguageProficiency extending tuple<
    listening: str,
    reading: str,
    speaking: str,
    presentation: str,
    writing: str
>;

type Language {
    required property external_id -> str { constraint exclusive; };
    required property name -> Translation;
    property proficiency -> LanguageProficiency;
    property article -> Translation;
    property status -> VerificationStatus;
    property last_verified -> str;

    multi link tags -> Tag;
    multi link demonstrated_in -> Experience;
}
```

**Verdict:** ✅ EdgeDB schema complete, TypeScript interface missing (needs to be added).

---

### 8. Hobby Type (Missing from TypeScript)

**TypeScript:** ❌ No interface defined

**Actual Frontmatter:**

```yaml
title: { et: "...", en: "..." }
category: technical-creative # Only 1/5 files
tools: [...]
```

**EdgeDB Schema:**

```esdl
type Hobby {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;
    property tools -> array<str>;
    property article -> Translation;
    property status -> VerificationStatus;
    property last_verified -> str;

    multi link tags -> Tag;
}
```

**Verdict:** ✅ EdgeDB schema complete, TypeScript interface missing (needs to be added).

---

### 9. Project Type (Missing from TypeScript)

**TypeScript:** ❌ No interface defined

**Actual Frontmatter:**

```yaml
title: { et: "...", en: "..." }
status: active | completed | archived
technologies: [...]
skills_demonstrated: [...]
url: ...
repository: ...
```

**EdgeDB Schema:**

```esdl
scalar type ProjectStatus extending enum<active, completed, archived>;

type Project {
    required property external_id -> str { constraint exclusive; };
    required property title -> Translation;
    property description -> Translation;
    property article -> Translation;
    property status -> ProjectStatus;
    property url -> HttpUrl;
    property repository -> HttpUrl;
    property technologies -> array<str>;
    property last_verified -> str;

    multi link tags -> Tag;
    multi link skills_demonstrated -> Skill;
}
```

**Verdict:** ✅ EdgeDB schema complete, TypeScript interface missing (needs to be added).

---

## Issues Found in TypeScript Interfaces

### Critical Mismatches

1. **Experience.company** - `string` → should be `MultilingualText`
2. **Education.institutions** - `string[]` → should be `Array<{name: MultilingualText}>`
3. **Education.studies** - structure doesn't match actual frontmatter

### Missing Interfaces

4. **Language** - No interface (5 files exist)
5. **Hobby** - No interface (5 files exist)
6. **Project** - No interface (~5 files exist)

### Design Improvements in EdgeDB

- String IDs → Proper links (referential integrity)
- String enums → Enum types (type safety)
- String URLs → HttpUrl scalar (validation)
- Split fields → Separate structured types (proficiency, dates)
- Added `article` field for markdown bodies

## Recommendations

### 1. Update TypeScript Interfaces (build_context.ts)

```typescript
interface Experience extends BaseEntity {
  company: MultilingualText; // Fix: was string
  // ... rest
}

interface Education extends BaseEntity {
  institutions?: Array<{ name: MultilingualText }>; // Fix: was string[]
  fields?: MultilingualText[]; // Fix: was studies
  // ... rest
}

// Add missing interfaces:
interface Language extends BaseEntity {
  /* ... */
}
interface Hobby extends BaseEntity {
  /* ... */
}
interface Project extends BaseEntity {
  /* ... */
}
```

### 2. Import Script Mapping

The Python import script must handle:

- `id` → `external_id`
- String IDs in arrays → Proper links (lookup by external_id)
- String company → Extract from bilingual field
- Parse `proficiency_level: "9/10"` → `level: 9`, `level_display: "9/10"`

### 3. MCP Server Types

Update MCP server service interfaces to match EdgeDB schema (already closer to correct structure).

## Conclusion

✅ **EdgeDB schema is CORRECT** - matches actual frontmatter data  
⚠️ **TypeScript interfaces have BUGS** - don't match reality  
✅ **Migration is STRAIGHTFORWARD** - clear mapping path

The EdgeDB schema design improves upon TypeScript interfaces with better type safety, proper relationships, and validation. TypeScript interfaces need updates to match both reality and EdgeDB schema.
