---
description: Run email monitor to fetch application-related emails and process the results according to the constitution.
---

# Check Emails Command

**Purpose:** Run the email monitoring tool, parse results, verify classifications, and update application tracking.

User input:

$ARGUMENTS

## Prerequisites

Before running, verify:

1. The email-monitor binary exists at `email-monitor/email-monitor`
2. Configuration file `email-monitor/.env` contains valid Gmail credentials
3. The `applications/REGISTRY.md` file exists

If the binary doesn't exist, build it first:

```bash
cd email-monitor && go build -o email-monitor ./cmd/email-monitor/
```

## Workflow

Given the user's request (which may include flags like `--dry-run`), execute the following phases:

### Phase 1: Run Email Monitor

1. **Determine run mode:**
   - If user mentions "dry run", "test", or "preview": Set `DRY_RUN=true`
   - If `$ARGUMENTS` contains `--dry-run`: Set `DRY_RUN=true`
   - Otherwise: Run in normal mode (creates files)

2. **Execute the tool:**

   ```bash
   cd /home/michelek/Documents/github/cv_system/email-monitor && ./email-monitor
   ```

   Or for dry-run:

   ```bash
   cd /home/michelek/Documents/github/cv_system/email-monitor && DRY_RUN=true ./email-monitor
   ```

3. **Capture and parse output:**
   - The tool outputs markdown-formatted results
   - Extract the list of created/simulated files
   - Note the statistics (processed, created, skipped, unmatched)

### Phase 2: Review Created Communications

For each file listed in the output:

1. **Read the communication file** from the path shown

2. **Analyze the email content** to verify:
   - Is the classification type in the filename correct?
   - Does the email content match the assigned type?

3. **Classification definitions:**

   | Type | Content Indicators |
   |------|-------------------|
   | `acknowledgment` | Receipt confirmation, "application received", "under review", "kätte saanud" |
   | `rejection` | "unfortunately", "other candidates", "kahjuks", "teise kandidaadi" |
   | `interview` | Interview invitation, meeting request, "intervjuu", "kohtumine" |
   | `offer` | Job offer, salary discussion, "pakkumine" |
   | `inquiry` | Questions about candidate, request for more info |
   | `followup` | Status update, timeline extension |

### Phase 3: Correct Misclassifications

If any classification is incorrect:

1. **Rename the file** to the correct type:

   ```bash
   mv "communications/2025-11-30_wrong_type.md" "communications/2025-11-30_correct_type.md"
   ```

2. **Update the header** inside the file:

   ```markdown
   # Communication: [Correct Type in Title Case]
   ```

3. **Document the correction** in your response

### Phase 4: Update REGISTRY.md

Based on email content, update application statuses:

1. **Read** `applications/REGISTRY.md`

2. **For each communication**, determine if status change is warranted:

   | Email Type | Status Transition |
   |------------|-------------------|
   | `acknowledgment` | Draft → Submitted (if not already) |
   | `interview` | Submitted → Interview |
   | `rejection` | Any → Rejected |
   | `offer` | Interview → Offer |

3. **Update the Notes column** with:
   - Date of communication
   - Key information (e.g., "Interview scheduled for 2025-12-05")
   - Contact person if mentioned

4. **Update Statistics section** if totals changed

### Phase 5: Summary Report

Present findings to the user:

```markdown
## Email Check Complete

**Run Mode:** [Normal / Dry-Run]
**Emails Processed:** [X]
**Files Created:** [Y]

### Communications Saved

| Date | Company | Type | Status Update |
|------|---------|------|---------------|
| [date] | [company] | [type] | [action taken] |

### Classification Corrections

- [List any files that were renamed, or "None required"]

### Registry Updates

- [List any status changes made, or "No changes needed"]

### Action Required

- [List any items needing human attention, e.g., "Unmatched email from unknown sender"]
```

## Error Handling

**If binary not found:**

```bash
cd /home/michelek/Documents/github/cv_system/email-monitor && go build -o email-monitor ./cmd/email-monitor/
```

Then retry the email check.

**If .env missing or invalid:**

Inform user that Gmail credentials need to be configured per `email-monitor/README.md`.

**If no new emails:**

Report "No new emails since last check" and show last check timestamp if available.

## Constitutional Compliance

This command implements Section 4.3 of the Constitution (Email Monitoring Tool):

1. Review all newly created communication files - CHECK
2. Verify classification type in each filename - CHECK
3. Rename files if classification is incorrect - CHECK
4. Update REGISTRY.md status if email indicates change - CHECK
5. Summarize findings highlighting action-required items - CHECK

## Examples

### Example 1: Normal Run

**User:** `/check-emails`

**Action:** Run email monitor, process results, update registry.

### Example 2: Dry Run

**User:** `/check-emails --dry-run`

**Action:** Run with `DRY_RUN=true`, show what would be saved without creating files.

### Example 3: With Context

**User:** `/check-emails just the new ones from today`

**Action:** Run normally (tool already tracks state and only fetches new emails).

## Notes

- The tool maintains state in `.email-monitor-state.json` to avoid duplicate processing
- Each run only fetches emails newer than the last processed UID
- Gmail app password required (not regular password)
- Tool uses `[Gmail]/All Mail` folder to catch all application-related emails

## Markdown Formatting Requirements

All output must be lint-compliant:

- Add blank line before and after each heading
- Add blank line before and after each list
- Add blank line before and after each code block
- No trailing spaces
- No emojis in formal output (use text markers like [INFO], [ERROR])

**RECURSIVE REQUIREMENT**: If this prompt generates other prompts, include these markdown formatting requirements.
