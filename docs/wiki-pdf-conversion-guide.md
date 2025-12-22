# PDF Conversion System

A Markdown-to-PDF conversion pipeline with YAML frontmatter support for document metadata and professional formatting.

## Overview

Converts Markdown documents into professionally formatted PDFs with:

- **Dynamic footers** from YAML frontmatter (docID, version, date, author)
- **Smart incremental builds** (only regenerate when source changes)
- **Custom LaTeX styling** for professional document layout
- **Optional PDF metadata** for ATS/AI systems

## Tech Stack

### Core Dependencies

| Tool         | Version | Purpose                                  |
| ------------ | ------- | ---------------------------------------- |
| **Pandoc**   | 2.0+    | Markdown → LaTeX → PDF conversion engine |
| **XeLaTeX**  | Any     | PDF rendering engine (Unicode support)   |
| **exiftool** | 12.0+   | PDF metadata (EXIF/XMP) manipulation     |
| **Bash**     | 4.0+    | Orchestration script                     |

### LaTeX Packages

- `fontawesome5` - Icon support for contact links
- `titlesec` - Custom heading spacing
- `needspace` - Prevent orphaned headings
- `fancyhdr` - Header/footer management
- `lastpage` - Page count in footer
- `xcolor`, `colortbl` - Table styling
- `enumitem` - List spacing customization

### File Structure

```text
scripts/
├── convert-to-pdf.sh          # Main conversion script
├── metadata_to_latex.lua      # Pandoc Lua filter (frontmatter → LaTeX macros)
└── .header.tex                # Global LaTeX header template

<your-documents>/
├── document.md                # Source markdown
└── output/
    └── document.pdf           # Generated PDF output
```

**Note:** The directory structure is flexible. Place the `scripts/` folder at your project root and reference it from wherever your markdown files are located.

## YAML Frontmatter Schema

### TypeScript Interface

```typescript
interface DocumentMetadata {
  /** Document identifier (max 24 chars, e.g., "CV-Company-Role") - appears in footer */
  docID: string & { readonly __brand: "MaxLength24" };

  /** Semantic version number (e.g., "1.0", "2.1") - appears in footer */
  version: string;

  /** Document date in ISO format (YYYY-MM-DD) - appears in footer */
  date: string & { readonly __brand: "ISODate" };
  /** Author name - appears in footer */
  author: string;

  /** Optional: PDF metadata for ATS/AI systems (embedded, not visible) */
  pdf_metadata?: {
    /** Document title (visible in PDF viewer properties) */
    title?: string;

    /** Document subject/purpose */
    subject?: string;

    /** Comma-separated keywords for search/ATS */
    keywords?: string;

    /** Creator/author name */
    creator?: string;

    /** Brief summary for AI/ATS parsing (custom XMP field) */
    recommendation?: string;
  };
}
```

### Required Fields

All documents **must** include these fields in YAML frontmatter:

```yaml
---
docID: CV-Company-Role # Required: Document identifier
version: 1.0 # Required: Version number
date: 2025-12-22 # Required: ISO date (YYYY-MM-DD)
author: Your Name # Required: Author name
---
```

### Optional Fields

PDF metadata is **optional** and typically used for ATS optimization:

```yaml
---
docID: CV-Acme-Dev
version: 1.0
date: 2025-12-22
author: Jane Doe

pdf_metadata:
  title: "CV: Senior Developer"
  subject: "Job Application"
  keywords: "Python, PostgreSQL, Docker"
  creator: "Jane Doe"
---
```

## Usage

### Basic Conversion

```bash
# From your document directory
cd path/to/your/documents/

# Convert all .md files in current directory
# (Adjust relative path to scripts/ based on your structure)
../../scripts/convert-to-pdf.sh

# Convert specific file
../../scripts/convert-to-pdf.sh document.md
```

### Command-Line Options

```bash
./scripts/convert-to-pdf.sh [OPTIONS] [FILE...]

Options:
  --force, -f          Force regeneration (ignore timestamps)
  --clean, -c          Clean output directory before build
  --output DIR, -o     Specify output directory (default: ./output/)
  --help, -h           Show help message
```

### Smart Incremental Builds

PDFs are automatically regenerated only when:

- Source `.md` file is newer than `.pdf`
- `scripts/.header.tex` has changed
- `scripts/metadata_to_latex.lua` has changed
- `--force` flag is used

```bash
# First run: Regenerates all
./scripts/convert-to-pdf.sh
# Converting: document.md -> document.pdf
# ✓ Created: output/document.pdf (142K)

# Second run: Skips unchanged files
./scripts/convert-to-pdf.sh
# ⊘ Skipped (up-to-date): document.md
```

## Footer Layout

The generated PDF footer displays metadata from frontmatter:

```text
───────────────────────────────────────────────────────────
docID | author          5/15           v2.0 | 2025-12-22
```

**Layout:**

- **Left:** `docID | author`
- **Center:** Current page / Total pages
- **Right:** `vVersion | Date`

## Document Standards

### Naming Conventions

**Document IDs** follow the pattern: `TYPE-COMPANY-ROLE`

```typescript
type DocumentType = "CV" | "ML" | "REF"; // CV, Motivation Letter, References

// Examples:
const docIDs = [
  "CV-Acme-SeniorDev", // Curriculum Vitae
  "ML-Acme-SeniorDev", // Motivation Letter
  "REF-Acme-SeniorDev", // References
];
```

**File naming:**

```text
CV_CompanyName_RoleName.md               # Source markdown
CV_CompanyName_RoleName.pdf              # Generated PDF
motivation_letter_CompanyName_Role.md    # Motivation letter
```

### Version Semantics

Use semantic versioning:

```typescript
interface VersionSemantics {
  "1.0": "Initial submission";
  "1.1": "Minor updates (typo fixes, formatting)";
  "1.2": "Additional minor changes";
  "2.0": "Major revision (new content, restructuring)";
}
```

## Validation Requirements

### Frontmatter Validation

**The conversion script MUST validate frontmatter before processing.** Invalid frontmatter should cause immediate failure with clear error messages.

#### Validation Rules

```typescript
interface ValidationRules {
  docID: {
    required: true;
    maxLength: 24;
    pattern: /^[A-Z0-9-]+$/;  // Uppercase alphanumeric + hyphens
    example: 'DOC-Company-Role';
  };
  version: {
    required: true;
    pattern: /^\d+\.\d+$/;  // Semantic version (e.g., 1.0, 2.3)
    example: '1.0';
  };
  date: {
    required: true;
    pattern: /^\d{4}-\d{2}-\d{2}$/;  // ISO 8601 date
    example: '2025-12-22';
  };
  author: {
    required: true;
    minLength: 1;
    maxLength: 100;
    example: 'John Doe';
  };
}
```

#### Implementation Example

**Bash validation** (add to `convert-to-pdf.sh`):

```bash
validate_frontmatter() {
  local md_file="$1"
  local docid=$(extract_field "$md_file" "docID")
  local version=$(extract_field "$md_file" "version")
  local date=$(extract_field "$md_file" "date")
  local author=$(extract_field "$md_file" "author")

  # Check required fields
  [ -z "$docid" ] && echo "ERROR: Missing required field 'docID'" && return 1
  [ -z "$version" ] && echo "ERROR: Missing required field 'version'" && return 1
  [ -z "$date" ] && echo "ERROR: Missing required field 'date'" && return 1
  [ -z "$author" ] && echo "ERROR: Missing required field 'author'" && return 1

  # Validate docID length (max 24 chars)
  [ ${#docid} -gt 24 ] && echo "ERROR: docID exceeds 24 characters: '$docid'" && return 1

  # Validate docID pattern (uppercase alphanumeric + hyphens)
  echo "$docid" | grep -qE '^[A-Z0-9-]+$' || {
    echo "ERROR: docID must contain only uppercase letters, numbers, and hyphens: '$docid'"
    return 1
  }

  # Validate version pattern (semantic version)
  echo "$version" | grep -qE '^[0-9]+\.[0-9]+$' || {
    echo "ERROR: version must be in format X.Y (e.g., 1.0): '$version'"
    return 1
  }

  # Validate date pattern (ISO 8601)
  echo "$date" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' || {
    echo "ERROR: date must be in ISO format YYYY-MM-DD: '$date'"
    return 1
  }

  return 0
}
```

**TypeScript validation** (for programmatic use):

```typescript
function validateDocumentMetadata(data: any): data is DocumentMetadata {
  const errors: string[] = [];

  // Required fields
  if (!data.docID) errors.push("Missing required field: docID");
  if (!data.version) errors.push("Missing required field: version");
  if (!data.date) errors.push("Missing required field: date");
  if (!data.author) errors.push("Missing required field: author");

  // docID validation
  if (data.docID) {
    if (data.docID.length > 24) {
      errors.push(`docID exceeds 24 characters: "${data.docID}"`);
    }
    if (!/^[A-Z0-9-]+$/.test(data.docID)) {
      errors.push(
        `docID must contain only uppercase letters, numbers, and hyphens: "${data.docID}"`
      );
    }
  }

  // Version validation
  if (data.version && !/^\d+\.\d+$/.test(data.version)) {
    errors.push(`version must be in format X.Y (e.g., 1.0): "${data.version}"`);
  }

  // Date validation
  if (data.date && !/^\d{4}-\d{2}-\d{2}$/.test(data.date)) {
    errors.push(`date must be in ISO format YYYY-MM-DD: "${data.date}"`);
  }

  if (errors.length > 0) {
    throw new Error(`Frontmatter validation failed:\n${errors.join("\n")}`);
  }

  return true;
}
```

#### Error Messages

Validation failures should produce clear, actionable error messages:

```text
✗ ERROR: Frontmatter validation failed for document.md
  - docID exceeds 24 characters: "CV-VeryLongCompanyName-SeniorDev"
  - version must be in format X.Y (e.g., 1.0): "v1.0"
  - date must be in ISO format YYYY-MM-DD: "22-12-2025"

Please fix the frontmatter and try again.
```

## Complete Example

```markdown
---
docID: DOC-ACME-SENIORDEV
version: 1.0
date: 2025-12-22
author: Jane Doe
---

# Jane Doe

**Email:** jane.doe@example.com  
**Phone:** +1 555-0123  
**GitHub:** github.com/janedoe

## Professional Summary

Experienced software engineer specializing in Python backend development...

## Experience

### Senior Developer - Tech Startup (2020-2025)

- Led team of 5 developers on Django/PostgreSQL stack
- Deployed microservices to AWS ECS with 99.9% uptime
```

**Generated Footer:**

```text
DOC-ACME-SENIORDEV | Jane Doe    1/2    v1.0 | 2025-12-22
```

## Troubleshooting

### Validation Errors

If conversion fails with validation errors, check your frontmatter:

```yaml
---
docID: DOC-COMPANY-ROLE # ✓ Max 24 chars, uppercase + hyphens
version: 1.0 # ✓ Semantic version X.Y
date: 2025-12-22 # ✓ ISO format YYYY-MM-DD
author: Jane Doe # ✓ Required, 1-100 chars
---
```

**Common validation errors:**

```yaml
docID: cv-company-role          # ✗ Must be uppercase
docID: CV-VeryLongCompanyName-SeniorDeveloper  # ✗ Exceeds 24 chars
version: v1.0                   # ✗ Must be X.Y format (no 'v' prefix)
date: 22/12/2025                # ✗ Must be ISO format YYYY-MM-DD
```

### PDF Not Regenerating

Force regeneration if timestamps are incorrect:

```bash
./scripts/convert-to-pdf.sh --force document.md
```

### LaTeX Compilation Errors

Install required LaTeX packages:

```bash
# Debian/Ubuntu
sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-latex-extra

# macOS
brew install --cask mactex-no-gui
```

## Processing Pipeline

```text
Markdown Source (YAML frontmatter + Markdown content)
    ↓
[1] Lua Filter (metadata_to_latex.lua)
    → Extracts: docID, version, date, author
    → Generates: LaTeX macros (\def\docid{...})
    ↓
[2] Pandoc Markdown → LaTeX
    → Loads: scripts/.header.tex (global styling)
    → Injects: Lua-generated macros
    → Converts: Markdown to LaTeX
    ↓
[3] XeLaTeX LaTeX → PDF
    → Compiles: LaTeX to PDF
    → Renders: Footer with \docid, \docversion, etc.
    ↓
[4] exiftool Post-Processing (optional)
    → Extracts: pdf_metadata from frontmatter
    → Injects: EXIF/XMP tags into PDF
    ↓
Final PDF (with footer + optional metadata)
```

## Development Guide

### Adding New Frontmatter Fields

To add new fields to the system:

**1. Update TypeScript Interface:**

```typescript
interface DocumentMetadata {
  docID: string;
  version: string;
  date: string;
  author: string;

  // Add new field
  company?: string; // Optional company name
}
```

**2. Update Lua Filter** (`scripts/metadata_to_latex.lua`):

```lua
function Meta(m)
  -- Existing macros
  add_macro('docid', m.docID)
  add_macro('docversion', m.version)
  add_macro('docdate', m.date)
  add_macro('docauthor', m.author)

  -- Add new macro
  add_macro('doccompany', m.company)

  return m
end
```

**3. Update LaTeX Header** (`scripts/.header.tex`):

```latex
% Define default value
\providecommand{\doccompany}{}

% Use in footer (example: add to left side)
\fancyfoot[L]{\small \ifx\doccompany\empty\docid\else\doccompany: \docid\fi}
```

**4. Use in Documents:**

```yaml
---
docID: CV-Acme-Dev
version: 1.0
date: 2025-12-22
author: Jane Doe
company: Acme Corp # New field
---
```

### File Dependencies

```typescript
interface ConversionDependencies {
  script: "./scripts/convert-to-pdf.sh";
  luaFilter: "./scripts/metadata_to_latex.lua";
  globalHeader: "./scripts/.header.tex";
  dependencies: ["pandoc", "xelatex", "exiftool"];
}

// Regeneration triggers
const regenerateWhen = {
  sourceModified: "*.md file newer than *.pdf",
  scriptModified: "convert-to-pdf.sh changed",
  filterModified: "metadata_to_latex.lua changed",
  headerModified: ".header.tex changed",
  forceFlag: "--force option used",
};
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Generate PDFs

on:
  push:
    paths:
      - "documents/**/*.md" # Adjust path to your document directory

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended

      - name: Generate PDFs
        run: |
          # Adjust 'documents' to your directory structure
          find documents -name "*.md" -type f | while read -r file; do
            dir=$(dirname "$file")
            cd "$dir"
            # Adjust relative path to scripts/ based on your structure
            ../../scripts/convert-to-pdf.sh --force
            cd -
          done

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: pdfs
          path: documents/**/output/*.pdf # Adjust output path
```

## References

- [Pandoc Manual](https://pandoc.org/MANUAL.html) - Markdown conversion documentation
- [XeLaTeX](https://www.tug.org/xelatex/) - Unicode-compatible LaTeX engine
- [LaTeX fancyhdr Package](https://ctan.org/pkg/fancyhdr) - Header/footer customization

---

**Last Updated:** 2025-12-22  
**Maintainer:** cv_system development team
