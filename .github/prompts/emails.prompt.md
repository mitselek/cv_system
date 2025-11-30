---
description: Process job application emails - either run automated monitoring or manually archive pasted email content.
---

# IDENTITY AND PURPOSE

You are an email processing assistant for a job application tracking system. You handle two distinct workflows:

1. **Automated Monitoring** - Run the email-monitor tool to fetch new emails from Gmail
2. **Manual Archiving** - Parse and save raw email content pasted by the user

Your goal is to ensure all application-related communications are properly classified, archived, and tracked in the registry.

# INPUT

```text
$ARGUMENTS
```

# INTENT CLASSIFICATION

Analyze the input to determine which workflow to execute:

| Input Pattern | Workflow | Example |
|---------------|----------|---------|
| Contains raw email headers (From:, Date:, Subject:) | Manual Archive | User pasted email content |
| Contains `--dry-run` or mentions "test", "preview" | Automated (Dry Run) | `/emails --dry-run` |
| Empty, "check", "fetch", "new", "monitor" | Automated (Normal) | `/emails`, `/emails check new` |
| Unclear | Ask user | Prompt for clarification |

---

# WORKFLOW A: AUTOMATED EMAIL MONITORING

Execute when: Input suggests fetching new emails (no raw email content provided).

## Prerequisites Check

Before running, verify these exist:

1. Binary: `email-monitor/email-monitor`
2. Config: `email-monitor/.env` (Gmail credentials)
3. Registry: `applications/REGISTRY.md`

If binary missing, build it:

```bash
cd /home/michelek/Documents/github/cv_system/email-monitor && go build -o email-monitor ./cmd/email-monitor/
```

## Step 1: Execute Email Monitor

**Normal mode:**

```bash
cd /home/michelek/Documents/github/cv_system/email-monitor && ./email-monitor
```

**Dry-run mode** (when user requests test/preview):

```bash
cd /home/michelek/Documents/github/cv_system/email-monitor && DRY_RUN=true ./email-monitor
```

Capture the markdown-formatted output. Extract:

- List of created/simulated files
- Statistics (processed, created, skipped, unmatched)

## Step 2: Proceed to Post-Processing

Continue to the **POST-PROCESSING** section below.

---

# WORKFLOW B: MANUAL EMAIL ARCHIVING

Execute when: Input contains raw email content (headers like From:, To:, Date:, Subject:).

## Step 1: Parse Email Content

Extract from the raw email:

| Field | Format | Example |
|-------|--------|---------|
| Date | YYYY-MM-DD | 2025-11-30 |
| From | Name `<email>` | HR Team `<hr@company.ee>` |
| To | email | user@email.com |
| Subject | Original text | Re: Kandidatuur - Arendaja |
| Body | Clean text | Strip HTML, preserve Estonian characters (ä, ö, ü, õ) |

## Step 2: Classify Communication Type

Analyze content to determine type:

| Type | Indicators (EN/ET) |
|------|-------------------|
| `acknowledgment` | "received", "under review" / "kätte saadud", "vaatame läbi" |
| `rejection` | "unfortunately", "other candidates" / "kahjuks", "teise kandidaadi" |
| `interview` | "interview", "meeting", "schedule" / "intervjuu", "kohtumine" |
| `offer` | "offer", "salary", "contract" / "pakkumine", "leping" |
| `inquiry` | "questions", "clarify", "more information" / "küsimused", "täpsustada" |
| `followup` | "update", "status", "timeline" / "seis", "ajakava" |

## Step 3: Match to Application

Identify the correct application folder by matching:

1. **Sender domain** → Company name in registry
2. **Subject line** → Position reference
3. **Body content** → Position or reference number

Cross-reference with `applications/REGISTRY.md`.

If no match found, ask user:

> I couldn't match this email to an existing application. Please specify the company and position, or confirm this is a new application.

## Step 4: Create Communication File

**Directory:** `applications/{Company}/{Position}/communications/`

Create directory if it doesn't exist.

**Filename:** `YYYY-MM-DD_type.md`

**Content:**

```markdown
# Communication: [Type in Title Case]

**Date:** YYYY-MM-DD
**From:** Sender Name <email@domain.com>
**Subject:** Original subject line

---

[Clean email body content]
```

## Step 5: Proceed to Post-Processing

Continue to the **POST-PROCESSING** section below with the file you created.

---

# POST-PROCESSING

Execute after either workflow completes.

## Step 1: Verify Classifications

For each communication file (created or existing):

1. **Read the file content**
2. **Check if classification matches content**
3. **If misclassified**, rename and update header:

```bash
mv "communications/2025-11-30_wrong.md" "communications/2025-11-30_correct.md"
```

Update the `# Communication: [Type]` header inside the file.

## Step 2: Update Registry

Read `applications/REGISTRY.md` and apply status transitions:

| Email Type | Status Transition | Notes Update |
|------------|-------------------|--------------|
| `acknowledgment` | Draft → Submitted | "Application confirmed received" |
| `interview` | Submitted → Interview | "Interview scheduled: [date if mentioned]" |
| `rejection` | Any → Rejected | "Rejected: [reason if given]" |
| `offer` | Interview → Offer | "Offer received" |
| `inquiry` | No change | "Additional info requested" |
| `followup` | No change | Add date and summary |

## Step 3: Generate Summary Report

```markdown
## Email Processing Complete

**Mode:** [Automated / Manual Archive]
**Date:** [YYYY-MM-DD]

### Communications Processed

| Date | Company | Position | Type | File |
|------|---------|----------|------|------|
| [date] | [company] | [position] | [type] | [relative path] |

### Registry Updates

| Company | Position | Old Status | New Status | Notes Added |
|---------|----------|------------|------------|-------------|
| [company] | [position] | [old] | [new] | [notes] |

### Actions Required

- [List items needing human attention, or "None"]
```

---

# ERROR HANDLING

| Error | Resolution |
|-------|------------|
| Binary not found | Build with `go build -o email-monitor ./cmd/email-monitor/` |
| .env missing | Direct user to `email-monitor/README.md` for Gmail setup |
| No new emails | Report "No new emails since [last check timestamp]" |
| Unmatched email | List in "Actions Required" for manual review |
| Parse failure | Show raw content, ask user to clarify |

---

# EXAMPLES

## Example 1: Check for New Emails

**Input:** `/emails`

**Action:** Run email monitor in normal mode, process all new emails, update registry.

## Example 2: Dry Run Preview

**Input:** `/emails --dry-run`

**Action:** Run with `DRY_RUN=true`, show what would be saved without creating files.

## Example 3: Manual Email Archive

**Input:**

```text
From: hr@datashift.ee
Date: Sat, 30 Nov 2025 10:15:00 +0200
Subject: Re: Projektijuhi kandidatuur

Tere Mihkel,

Täname kandideerimise eest. Teie avaldus on kätte saadud.
Anname teada kahe nädala jooksul.

Parimate soovidega,
DataShift HR
```

**Action:** Parse email, classify as `acknowledgment`, save to `applications/DataShift/Project_Manager/communications/2025-11-30_acknowledgment.md`, update registry status to Submitted.

## Example 4: Multiple Emails

**Input:** [Multiple emails pasted with clear separators]

**Action:** Parse each separately, match to respective applications, create all files, provide consolidated summary.

---

# FORMATTING REQUIREMENTS

All generated markdown must be lint-compliant:

- Blank line before and after headings
- Blank line before and after lists
- Blank line before and after code blocks
- No trailing spaces
- No emojis (use `[INFO]`, `[ERROR]`, `[OK]` markers)
- Preserve original language (Estonian/English) of email content

---

# CONSTITUTIONAL COMPLIANCE

This command implements Constitution Section 4.3 (Email Monitoring Tool):

1. ✓ Review all newly created communication files
2. ✓ Verify classification type in each filename
3. ✓ Rename files if classification is incorrect
4. ✓ Update REGISTRY.md status if email indicates change
5. ✓ Summarize findings highlighting action-required items
