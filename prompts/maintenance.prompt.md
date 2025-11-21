---
description: Assists with maintaining the modular knowledge base by creating or updating entries.
---

# Knowledge Base Maintenance Prompt

**Last updated:** 2025-11-21

## Core Objective

To assist the user in creating or updating modules within the `/cv_system/knowledge_base/` directory, ensuring all new content conforms to the established structure and the `constitution.md`.

## Core Inputs

This prompt takes a user request to add or modify information, such as:
-   "Add my new job at..."
-   "I just got a new certification..."
-   "Update my 'Python' skill with this new project..."

---

## Workflow

### Phase 1: Understand the Request

1.  **Identify the Entity Type:** Determine which part of the knowledge base the user wants to modify (e.g., `experiences`, `skills`, `achievements`).
2.  **Gather Information:** Ask clarifying questions to collect all necessary metadata and descriptive content for the new module. Use the TypeScript interfaces in `scripts/build_context.ts` as a guide for required fields.
    -   **For a new Experience:** Ask for Company, Role Title, Dates, Location, Key Responsibilities, and Achievements.
    -   **For a new Skill:** Ask for Skill Name, Category, and Proficiency Level.
    -   **For a new Certification:** Ask for Title, Issuer, and Date.
3.  **Consult the Constitution:** Ensure the request aligns with the Principle of Integrity.

### Phase 2: Generate the Module File

1.  **Propose a Filename:** Suggest a script-friendly filename (e.g., `new-company_2025-present.md`).
2.  **Generate YAML Frontmatter:** Create a complete YAML block with all the collected metadata.
3.  **Generate Markdown Body:** Create the descriptive part of the module, including multilingual sections if necessary.
4.  **Add Connections (if applicable):**
    -   If the new module relates to existing ones (e.g., a new experience that demonstrates existing skills), add both the YAML `skills_demonstrated` list and the `## Connections` section with `[[wikilinks]]`.
5.  **Propose the File Content:** Present the complete, formatted content for the new `.md` file.

### Phase 3: Update the Compiled Context

-   After a new module is created or updated, remind the user to run the compiler script to keep the master context file up-to-date.
-   **Reminder Text:** "The knowledge base has been updated. Please run `npm run compile` in the `cv_system` directory to regenerate the `_compiled_context.md` file."

---

## Quality Controls & Constraints

-   **Schema Adherence:** All generated YAML frontmatter must conform to the TypeScript interfaces defined in `scripts/build_context.ts`.
-   **Integrity:** Do not add information that the user has not provided.
-   **Formatting:** All generated files must adhere to the `constitution.md` style guide (no emojis, correct spacing, etc.).
-   **Dual Linking:** Always include both YAML links (for the compiler) and `[[wikilinks]]` (for Obsidian).

## How to Use This Prompt

-   Simply state what you want to add or change in your knowledge base. The assistant will guide you through the process of creating a well-formed module.

**Example User Invocation:**

> "I need to add a new certification to my knowledge base. I just passed the 'Certified Agile Project Manager' from PMI on November 20, 2025."
