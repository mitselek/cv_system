# Action Plan: CV System Development

**Last Updated:** 2025-11-21

## 1. Primary Objective

To build a modular, script-driven system for managing CV content and generating tailored application materials. The system is designed to work in tandem with an LLM, providing it with a clean, structured, and comprehensive context of all professional experience, skills, and achievements.

## 2. Current State

We have successfully completed the initial data structuring and project setup phase. The current state is as follows:

- **Project Directory:** A self-contained project has been created at `/cv_system/`.
- **Knowledge Base:** The `/knowledge_base` is fully populated with modular Markdown files for:
  - Experiences
  - Skills
  - Achievements
  - Education
  - Certifications
- **Relationships:** Links between entities (experiences, skills, achievements) have been established in both YAML frontmatter (for tooling) and Markdown wikilinks (for Obsidian visualization).
- **Constitution:** A `constitution.md` file has been created in `/docs/`, defining the rules, standards, and architecture of the system.
- **Compiler Script (COMPLETED):**
  - A TypeScript-based compiler script, `scripts/build_context.ts`, has been created.
  - The project is set up with `package.json` and `tsconfig.json`.
  - **✓ RESOLVED:** The script compiles successfully and generates `_compiled_context.md` (1380 lines).
  - The compiled context includes all experiences, skills, achievements, education, and certifications.

- **Core Prompts (COMPLETED):**
  - `prompts/generate_application.prompt.md` - Comprehensive application generation workflow with honest fit assessment
  - `prompts/maintenance.prompt.md` - Knowledge base maintenance and module creation guidance

## 3. Immediate Next Step

The core infrastructure is now complete. The next priority is to **complete the knowledge base** with remaining personal information sections:

  1. **Languages** - Estonian (native), English (C1/C2), Russian (B2)
  2. **Hobbies/Interests** - Extract from original CV templates
  3. **GitHub Projects** - (optional) Can be added later as part of skill evidence

## 4. Broader Plan (Subsequent Steps)

With the core system functional, the remaining steps are:

1. **Test the System (PRIORITY):**

   - Select a real job posting from your applications pipeline
   - Run the `generate_application.prompt.md` with the compiled context
   - Validate that the output matches your quality standards
   - Compare with your existing template-based applications

2. **Analyze GitHub Repositories (OPTIONAL):**

   - Begin the exploratory task of analyzing the user's GitHub profile to extract a deeper, evidence-based understanding of technical skills, interests, and project contributions.
   - This will likely involve creating new `skill` and `project` modules in the knowledge base.

3. **Refine and Iterate:**

   - Based on test results, refine prompts and knowledge base structure
   - Add any missing sections (Languages, Hobbies) if they prove important
   - Optimize the compiled context format for LLM consumption
   - Consider adding analytics tracking (which experiences/skills get used most)
