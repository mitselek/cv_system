# CV System Compilation Guide

## Purpose

You are assisting with a professional CV (Curriculum Vitae) compilation system. This system transforms a modular knowledge base of career information into a unified context document optimized for Large Language Model (LLM) consumption. The compiled output enables AI-powered generation of tailored CVs, cover letters, and professional documents.

## System Architecture

### Technology Stack

- **Runtime**: Node.js
- **Language**: TypeScript
- **Package Manager**: npm
- **Data Format**: Markdown files with YAML frontmatter
- **Output**: Single consolidated Markdown file (`_compiled_context.md`)

### Core Components

1. **Knowledge Base**: Modular Markdown files organized by information type
2. **Compiler Script**: TypeScript code (`scripts/build_context.ts`) that processes and consolidates files
3. **Compiled Context**: Single Markdown file containing all professional information

## Building and Running

The project uses `npm` for package management and running scripts.

- **Install dependencies:**

  ```bash
  npm install
  ```

- **Build the project:**
  This command transpiles the TypeScript code to JavaScript.

  ```bash
  npm run build
  ```

- **Run the compiler:**
  This command executes the compiled JavaScript code, which reads the knowledge base and generates the `_compiled_context.md` file.

  ```bash
  npm run start
  ```

- **Compile (build and run):**
  This is a convenience script that does both building and running in one command.

  ```bash
  npm run compile
  ```

## Development Conventions

The core of this project is the `knowledge_base` directory. This directory contains several subdirectories, each representing a different type of information (e.g., `experiences`, `skills`, `achievements`).

Each piece of information is stored in its own Markdown file. The file format is a YAML frontmatter block followed by the main content in Markdown.

### File Structure Example

```text
knowledge_base/
├── experiences/
│   ├── company-a_2020-2022.md
│   └── company-b_2018-2020.md
├── skills/
│   ├── typescript.md
│   └── python.md
└── _compiled_context.md
```

### Markdown File Format

Each Markdown file must contain a YAML frontmatter section and a Markdown body.

**Example (`knowledge_base/experiences/eesti-malu-instituut_2017-2024.md`):**

```yaml
---
id: eesti-malu-instituut-2017-2024
type: employment
company: Eesti Mälu Instituut
url: https://mnemosyne.ee
dates:
  start: "2017-07"
  end: "2024-10"
title:
  et: Andmesanitar
  en: Data Curator
location: Tallinn, Estonia
tags:
  - Data Curation
  - Data Cleansing
  - Database Management
  - History
  - Research
skills_demonstrated:
  - data-curation
  - database-management
achievements:
  - mem-historian-db-adoption-2024
status: verified
last_verified: "2025-11-21"
---
### et

- Skännida raamatud [Memento raamatud](https://www.memento.ee/trukised/memento-raamatud) ja moodustada nende põhjal andmebaas [eMem](https://github.com/memoriaal/eMem) ning ehitada sellele veebiväljund [Memoriaal](https://www.memoriaal.ee).
- Memento raamatutele on aja jooksul lisandunud veel kümneid allikaid, mille nimekirjad on tulnud olemasolevatega kokku viia; suuresti toimub töö Google tabelites, kus loon igaks ülesandeks ajaloolastele spetsiaalse töökeskkonna andmete otsimiseks ja võrdlemiseks.
- Ka on mul õnnestunud panna ajaloolased toimetama andmetega otse MySql andmebaasis - nad teevad päringuid ja isegi loovad seal kontrollitud keskkonnas sisu; selle üle olen ma eriti uhke.

### en

- Scanning books and creating a database.
- Data cleansing and integration from various sources.
- Working with large datasets to ensure data quality.
- I'm particularly proud of my success in in getting historians to work directly with the database often without recognizing that they can now add MySQL to their CV :)
```

The `scripts/build_context.ts` script reads all the `.md` files in the `knowledge_base` subdirectories, parses the YAML frontmatter, and concatenates the content into the `knowledge_base/_compiled_context.md` file.
