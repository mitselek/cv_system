---
description: Generate comprehensive job applications using the compiled knowledge base, with integrity controls and honest fit assessment.
---

# Application Generation Prompt (V2 - Knowledge Base)

**Last updated:** 2025-11-21

## Core Objective

To generate a complete, honest, and professional job application by synthesizing a **Job Advertisement** with the candidate's verified professional background from a **Compiled Context File**. This process follows the established `/cv_system/docs/constitution.md` to ensure integrity, quality, and consistency.

## Core Inputs

This prompt requires one primary input from the user:

1.  **The Job Advertisement:** The full text of the job posting the user wants to apply for.

The prompt will automatically access:

2.  **The Compiled Context:** The full content of the `/cv_system/knowledge_base/_compiled_context.md` file, which is the single source of truth for the candidate's skills, experiences, and achievements.
3.  **Contact Information:** The content of the `/cv_system/knowledge_base/contact.md` file from the knowledge base, containing verified contact details.

---

## Workflow

### Phase 1: Research & Analysis

Before generating any application materials, conduct a comprehensive analysis based *only* on the provided inputs.

#### 1.1. Source Material Analysis (Compiled Context)
-   Read the **Compiled Context** from `/cv_system/knowledge_base/_compiled_context.md` - this is the **ONLY** source of truth for the candidate's background.
-   Read the **Contact Information** from `/cv_system/knowledge_base/contact.md` - this is the **ONLY** source for personal contact details (name, email, phone, etc.).
-   These files contain a structured list of all validated work history, skills, achievements, education, certifications, and contact information.
-   **CRITICAL INTEGRITY CONSTRAINT:** Never invent, embellish, or infer information not explicitly present in these source files. Adhere strictly to the `/cv_system/docs/constitution.md`'s Principle of Integrity.

#### 1.2. Job Advertisement Analysis
-   Analyze the provided job posting thoroughly.
-   Identify key requirements, responsibilities, and preferred qualifications.
-   Note the company name, position title, application deadline, and any specific submission instructions.

#### 1.3. Honest Fit Assessment
-   Conduct an objective assessment by comparing the Job Advertisement against the Compiled Context.
-   **Skills Match:** Compare required skills against the `skills` section of the context.
-   **Experience Alignment:** Assess how `experiences` and `achievements` in the context transfer to the new role.
-   **Identify Gaps:** Clearly note any required qualifications from the job ad that are **not** supported by evidence in the context file.

### Phase 2: Application Generation

Based on the analysis, generate a complete set of application documents.

#### 2.1. Folder Structure
-   Propose the creation of the standard folder structure: `applications/[Company_Name]/[Position_Title]/`

#### 2.2. Content Generation Requirements

**1. `README.md`**
-   **Company & Position Summary:** Briefly summarize the role.
-   **Honest Fit Assessment:** Provide a percentage score and a breakdown of strengths and critical gaps, based *only* on the provided context.
-   **Application Strategy:** Recommend a strategy (e.g., "Emphasize direct experience," "Focus on transferable skills," or "Honest career transition").

**2. `tookuulutus.md`**
-   Copy the complete, original job posting text provided by the user.

**3. Adapted CV (`CV_[CompanyName]_[PositionTitle].md`)**
-   **CRITICAL:** Add the standard HTML comment metadata header in this exact format:
    ```html
    <!--
    docID: CV-CompanyName-Position
    version: 1.0
    date: YYYY-MM-DD
    author: [Full Name from contact.md]
    -->
    ```
-   **CRITICAL:** Use contact information from the `contact.md` file - never invent or guess contact details.
-   Select the most relevant `experiences`, `skills`, and `achievements` from the Compiled Context that align with the job ad.
-   Arrange the selected items to highlight the candidate's suitability.
-   **DO NOT** add any information not present in the Compiled Context or Contact files.
-   Format the CV professionally, adhering to the `constitution.md` style guide (no emojis, correct spacing, etc.).

**4. Motivation Letter (`motivation_letter_[CompanyName].md`)**
-   **CRITICAL:** Add the standard HTML comment metadata header in this exact format:
    ```html
    <!--
    docID: ML-CompanyName-Position
    version: 1.0
    date: YYYY-MM-DD
    author: [Full Name from contact.md]
    -->
    ```
-   **CRITICAL:** Use contact information from the `contact.md` file for the letterhead and signature.
-   Draft a professional and authentic letter that connects specific `experiences` and `achievements` from the Compiled Context to the requirements in the job ad.
-   If there are significant gaps, adopt an honest tone that emphasizes learning ability and transferable skills.
-   Demonstrate genuine interest based on the details in the job ad.

**5. Application Registry**
-   If `/cv_system/applications/REGISTRY.md` does not exist, create it with proper structure including headers and status definitions.
-   Add a new row to the registry table with: date, company, position, fit percentage, link to README, deadline, status, and brief notes.

---

## 3. Quality Controls & Constraints

-   **Integrity:** All generated content must be verifiable against the provided `_compiled_context.md` and `contact.md` files.
-   **No Invented Information:** Never create or guess contact details, names, or any personal information not explicitly provided in the source files.
-   **No Emojis in ANY Generated Files:** Strictly adhere to the "No Emojis" rule from the `constitution.md`. This applies to ALL files including README.md, CV, motivation letter, and any other generated content. Use plain text markers instead (e.g., "STRENGTH:", "GAP:", "NOTE:").
-   **Markdown Linting:** All generated Markdown files must be perfectly formatted (blank lines around headings/lists, no trailing spaces, etc.).
-   **PDF Metadata Headers:** All CVs and Motivation Letters must include the HTML comment header with docID, version, date, and author fields for the `/cv_system/scripts/convert-to-pdf.sh` script.
-   **Estonian Language:** If the application is in Estonian, remind the user that running the `/cv_system/scripts/estonian-spellcheck.sh` script is a **mandatory** next step.
-   **PDF Generation:** After creating all files, inform the user they can generate PDFs by running:
    ```bash
    cd /cv_system/applications/[Company]/[Position]
    ../../../scripts/convert-to-pdf.sh CV_*.md motivation_letter_*.md
    ```

## How to Use This Prompt

1.  **Provide the Job Ad:** Paste the full text of the job advertisement.
2.  **The system will automatically read:**
    - `/cv_system/knowledge_base/_compiled_context.md` for professional background
    - `/cv_system/knowledge_base/contact.md` for contact information
3.  **Execute:** The LLM will perform the analysis and generate all the necessary application files.

**Example User Invocation:**

> "Please generate an application for this job posting. Follow the instructions in `/cv_system/prompts/generate_application.prompt.md`."
>
> **Job Ad:**
> `[...paste job ad here...]`
