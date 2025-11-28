# Save Communication Prompt

## Purpose
Archive email communications related to job applications by parsing raw email content and saving it in a structured format to the appropriate application folder.

## Input
User provides one or more raw emails (copy-pasted from email client), which may include:
- Email headers (From, To, Date, Subject)
- Email body (plain text or HTML)
- Quoted reply chains
- Various encodings (UTF-8, ISO-8859-1, etc.)

## Process

### 1. Parse Email(s)
Extract from each email:
- **Date**: Convert to YYYY-MM-DD format
- **From**: Sender name and email
- **To**: Recipient (for verification)
- **Subject**: Email subject line
- **Body**: Clean text content (strip HTML if present)

### 2. Classify Communication Type
Determine type based on content analysis:
- `acknowledgment` - Confirmation of receipt, application under review
- `rejection` - Position filled, not selected, or similar
- `interview` - Interview invitation or scheduling
- `offer` - Job offer
- `inquiry` - Questions about application or candidate
- `followup` - Status updates, additional information requests

### 3. Match to Application
Identify the correct application folder by:
1. Sender email domain → Company name
2. Subject line → Position reference
3. Body content → Position or reference number

Cross-reference with `applications/REGISTRY.md` to find the exact folder path.

### 4. Generate Output

#### Filename Convention
```
YYYY-MM-DD_type.md
```
Examples:
- `2025-11-27_acknowledgment.md`
- `2025-11-28_interview.md`
- `2025-11-29_rejection.md`

#### File Location
```
applications/{Company}/{Position}/communications/
```

#### Content Format
```markdown
# Communication: [Type in Title Case]

**Date:** YYYY-MM-DD
**From:** Sender Name <email@domain.com>
**Subject:** Original subject line

---

[Clean email body content]

[If there are relevant quotes or reply chains, include them with proper formatting]
```

## Output Actions

1. **Create** communications subfolder if it doesn't exist
2. **Save** each email as a separate markdown file
3. **Update** `applications/REGISTRY.md` if status change is warranted:
   - Acknowledgment → Add note about expected response time
   - Rejection → Change status to "Rejected"
   - Interview → Change status to "Interview"
   - Offer → Change status to "Offer"

## Example

### Input (Raw Email)
```
From: hr@company.ee
To: user@email.com
Date: Wed, 27 Nov 2025 14:30:00 +0200
Subject: Re: Kandidatuur - Tarkvaraarendaja

Tere!

Täname Teid kandideerimise eest. Teie avaldus on kätte saadud ja 
vaatame selle läbi kahe nädala jooksul.

Lugupidamisega,
HR Meeskond
```

### Output File
**Path:** `applications/Company/Tarkvaraarendaja/communications/2025-11-27_acknowledgment.md`

```markdown
# Communication: Acknowledgment

**Date:** 2025-11-27
**From:** HR Meeskond <hr@company.ee>
**Subject:** Re: Kandidatuur - Tarkvaraarendaja

---

Tere!

Täname Teid kandideerimise eest. Teie avaldus on kätte saadud ja vaatame selle läbi kahe nädala jooksul.

Lugupidamisega,
HR Meeskond
```

## Multiple Emails
When processing multiple emails:
1. Parse each email separately
2. Match each to its respective application
3. Create all communication files
4. Provide summary of actions taken

## Notes
- Preserve original language (Estonian/English) of email content
- Strip email signatures and legal disclaimers if excessive
- Handle encoded characters (ä, ö, ü, õ) properly
- If application folder cannot be determined, ask user for clarification
