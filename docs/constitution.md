# The Constitution of the Job Application System

**Version:** 1.0  
**Last updated:** 2025-11-21T12:00:00+02:00

## 1. Preamble

This document defines the governing principles, standards, and workflows for the modular job application system. Its purpose is to ensure that all components of the system - the knowledge base, the tooling, and the AI interactions - work together to produce honest, high-quality, and professional application materials efficiently and consistently. This Constitution is the single source of truth for how the system operates.

---

## 2. Core Principles

All components and workflows must adhere to these four foundational principles:

1. **Principle of Integrity:** Honesty is the highest priority. All information regarding skills, experience, and achievements must be derived from the verified `knowledge_base`. Fabrication or misrepresentation is strictly forbidden. The system's primary function is to present the truth in the most effective way possible.

   **Zero-Tolerance Policy:** A single unverifiable claim invalidates the entire application. If fabrication is discovered, the complete application must be regenerated from scratch.

   **Verification Requirements:**
   - Before writing ANY detail, verify it exists in the source file
   - Quote exact source text, do not paraphrase or embellish
   - Use ONLY: names, dates, titles, locations AS WRITTEN in source
   - When in doubt → OMIT the detail entirely
   - Better to have sparse content than fabricated content

   **Forbidden Embellishments (even if "reasonable"):**
   - Specializations not mentioned in source
   - Skill focus areas not documented  
   - "With focus on..." unless explicitly stated
   - Descriptive phrases about education content
   - Inferred details based on job titles
   - "Logical" additions that "make sense"

2. **Principle of Structure:** All data and processes must be systematic and well-defined. The knowledge base is modular, and workflows are broken down into logical, repeatable steps. This ensures clarity, maintainability, and predictable outcomes.

3. **Principle of Quality:** All outputs must meet the highest professional standards. This is enforced through mandatory, non-negotiable quality gates, including linguistic checks, strict formatting rules, and visual consistency.

4. **Principle of Automation:** Repetitive and rule-based tasks should be automated to ensure efficiency and reduce manual error. Human effort should be focused on strategy, tailoring, and refinement, not on tedious compilation or formatting.

---

## 3. The Knowledge Base (`/knowledge_base/`)

The `knowledge_base` is the single source of truth for all personal, professional, and educational information.

### 3.1. Structure

- The knowledge base is organized into subdirectories by entity type (e.g., `/experiences`, `/skills`, `/achievements`, `/education`, `/certifications`).
- Each piece of information (a single job, a single skill) is stored as a separate `.md` file.
- Filenames must be unique, descriptive, and script-friendly (e.g., `company-name_start-end.md`).

### 3.2. Content and Schema

- Each file must begin with a YAML frontmatter block containing structured metadata (e.g., `id`, `type`, `title`, `dates`).
- The body of the file contains descriptive, narrative content in Markdown.
- Multilingual content (Estonian and English) is supported and should be clearly delineated.

### 3.3. Relationships

- Relationships between nodes (e.g., an experience demonstrating a skill) are defined in two ways:
    1. **For Tooling (Primary):** In the YAML frontmatter using keys like `skills_demonstrated: [skill-id]`. This is for the compiler script.
    2. **For Visualization (Secondary):** In a `## Connections` section at the end of the file using Obsidian-style `[[wikilinks]]`. This is for visual exploration.

---

## 4. Tooling & Workflows (`/scripts/`)

The use of the following scripts is mandatory to ensure consistency and quality.

### 4.1. The Compiler (`build_context.py` - *to be created*)

- **Purpose:** To read the entire `knowledge_base` and consolidate it into a single, structured, and LLM-friendly Markdown block. This compiled file serves as the consolidated, version-controlled source of truth for all LLM interactions.
- **Function:** This script is the primary interface between the distributed knowledge base and any consuming agent (e.g., an LLM). It should be run whenever the knowledge base is updated.
- **Output:** The script will save its output to `/knowledge_base/_compiled_context.md`. This file should be committed to version control. It is the designated input for all application-generation prompts.

### 4.2. PDF Generation (`/scripts/pdf`)

- **Mandate:** All professional documents (CVs, cover letters) intended for submission must be generated using this script.
- **Mechanism:** The script uses `pandoc` with `xelatex` and the official LaTeX header template at `/templates/.header.tex` to ensure professional formatting and consistent, metadata-driven footers.
- **Output:** Generated PDFs are placed in a `delivery/` subdirectory within the current working directory.

### 4.3. Email Monitoring Tool (Golang)

- **Purpose:** A Golang-based tool that monitors and retrieves the latest application-related emails from the email account.
- **Function:** Provides quick access to correspondence related to job applications, including acknowledgments, interview requests, and status updates.
- **Integration:** This tool helps track application progress and maintain accurate records in the application registry.
- **Output:** Email data is presented in a structured format for easy review and action.

---

## 5. LLM Interaction Protocol

All interactions with Large Language Models (LLMs) for the purpose of generating application materials will adhere to the following protocol.

### 5.1. Input Requirements

- The primary context for the LLM must be the output of the **Compiler** script. Do not feed the LLM outdated, monolithic CV templates.
- The prompt must also include the target job advertisement.
- The prompt should reference this Constitution for its core rules.

### 5.2. Output Requirements

- The LLM's primary task is **synthesis and tailoring**, not invention. It must select, reframe, and order information from the provided context to best match the job ad.
- All generated output must strictly adhere to the Formatting & Style Guide defined below.
- Estonian language quality checks (spelling, grammar, style) are performed internally during the application generation process, as specified in the generation prompt.

### 5.3. Mandatory Verification Protocol

Before finalizing ANY application document:

1. **Pre-Generation Check:**
   - Confirm understanding that fabrication = complete restart
   - Acknowledge that "helpful embellishments" violate integrity
   - Commit to conservative interpretation of source data

2. **During Generation:**
   - For education sections with no body content in source:
     - Institution name (as written)
     - Dates (as written)
     - Degree title (as written)
     - STOP - add nothing else
   - For experiences with minimal source content:
     - Use only explicit statements from source
     - Do not infer responsibilities from job titles
     - Do not add "typical" activities for that role

3. **Self-Audit (Required):**
   - Re-read each section of generated CV
   - For each claim, mentally cite the source file
   - Flag any sentence that cannot be directly quoted from source
   - Remove all flagged content immediately

4. **Conservative Fallback Rule:**
   - When uncertain if detail exists in source: OMIT IT
   - When uncertain if phrasing is faithful: USE SIMPLER VERSION
   - When uncertain if connection is documented: DON'T MAKE IT

---

## 6. Formatting & Style Guide

This guide is the definitive standard for all generated documents and prompts.

1. **No Emojis:** Emojis are strictly forbidden in all professional documents, prompts, scripts, and commit messages.
2. **Strict Markdown Linting:** All generated Markdown must be lint-compliant. This includes, but is not limited to:
    - A single blank line before and after all headings.
    - A single blank line before and after all lists.
    - A single blank line before and after all code blocks.
    - No trailing whitespace.
    - A single newline character at the end of the file.
3. **Metadata Headers:** All generated CVs and Cover Letters must begin with an HTML comment header containing the `docID`, `version`, `date`, and `author` for automated processing by the `pdf` script.
4. **Professional Tone:** The language must be professional, clear, and concise.
5. **Recursive Quality:** Any prompt generated by this system must itself include these constitutional rules, ensuring that all standards propagate through all levels of generation.
