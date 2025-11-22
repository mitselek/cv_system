---
description: Workflow for applying Estonian grammar corrections to application documents using Gemini CLI
---

# Gemini Estonian Correction Workflow

**Last updated:** 2025-11-22

## Automatic Method (Recommended)

From the `/cv_system` root directory, run:

```bash
gemini --yolo 'please apply prompts/gemini_correction_workflow.prompt.md to application documents in folder applications/[Company]/[Position]/'
```

Replace `[Company]/[Position]` with the actual folder path (e.g., `Askend_Estonia/Tarkvaraarenduse_Projektijuht`).

**What this does:**
1. Gemini reads the correction workflow prompt
2. Applies Estonian grammar corrections to CV and motivation letter
3. Fixes case agreement (genitive, partitive, illative)
4. Corrects verb conjugation
5. Uses natural professional phrasing
6. Overwrites original files with corrected versions

**Expected behavior:**
- You may see some file path errors (this is normal - Gemini CLI workspace limitations)
- At the end, Gemini will confirm corrections were applied
- Verify by checking the file timestamps

## Instructions for Gemini

Correct all Estonian grammar and style errors in any CV, motivation letter and email draft or template you see in the specified folder.

**Fix:**
- Case agreement (genitive, partitive, illative)
- Verb conjugation
- Natural professional phrasing
- Compound words and spelling

**Preserve:**
- HTML metadata headers (<!-- ... -->)
- Markdown formatting
- Technical terms and proper nouns
- Contact information

Fix documents in place. Return only confirmations, no document content in chat.

## Manual Interactive Method

If the automatic method fails:

### Step 1: Start Gemini
```bash
cd /home/michelek/Documents/github/cv_system/applications/[Company]/[Position]
gemini
```

### Step 2: Paste this prompt:

```
Correct all Estonian grammar and style errors in CV_*.md and motivation_letter_*.md files in this directory.

Fix: case agreement, verb conjugation, natural phrasing, spelling
Preserve: HTML metadata, Markdown formatting, technical terms, contact info

Fix documents in place.
```

## Fallback: Pipe Method

For single files:

```bash
cd applications/[Company]/[Position]
cat CV_*.md | gemini --yolo 'Correct Estonian grammar: fix case agreement, verb forms, natural phrasing. Return only corrected document.' > CV_corrected.md && mv CV_corrected.md CV_*.md
```

## Verification

After corrections:
1. Check file modification timestamps
2. Verify HTML metadata headers intact
3. Confirm no Gemini commentary added
4. Read Estonian text for naturalness

## Next Step

Generate PDFs:

```bash
cd applications/[Company]/[Position]
../../../scripts/convert-to-pdf.sh CV_*.md motivation_letter_*.md
```

---

**Note:** Gemini CLI may show file path errors but corrections are typically applied successfully. Always verify file contents after running.
