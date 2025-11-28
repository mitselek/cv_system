# Email Communication Monitor

Automated email monitoring system for job application communications, written in Go.

## Phase 1: Foundation (MVP) ✅

**Status:** Complete

- ✅ Connect to Gmail via IMAP (TLS/SSL)
- ✅ Authenticate with app-specific passwords
- ✅ Fetch emails from last 7 days
- ✅ Parse email metadata (Date, From, Subject)
- ✅ Extract email body with MIME multipart support
- ✅ Display parsed emails to stdout

## Phase 2: Classification & Storage ✅

**Status:** Complete

- ✅ Keyword-based email classification (acknowledgment, rejection, interview, offer, inquiry, followup)
- ✅ Confidence scores for classification
- ✅ Load applications from `REGISTRY.md`
- ✅ Fuzzy company/application matching
- ✅ Generate markdown files in correct location
- ✅ Dry-run mode (`DRY_RUN=true`)
- ✅ MIME multipart parsing (text/plain preferred over text/html)
- ✅ Quoted-printable and base64 decoding

## Setup

1. **Create Gmail App Password**

   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" as the app
   - Choose "Other (Custom Name)" for the device
   - Name it `email-monitor script`
   - Click "Generate"
   - Copy the 16-character password shown (spaces don't matter)

   > **Note:** You need 2-Step Verification enabled on your Google account to create app passwords.

2. **Configure Credentials**

   Create a `.env` file in the `email-monitor/` directory:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your credentials:

   ```.env
   EMAIL_USER=your.email@gmail.com
   EMAIL_APP_PASSWORD=your-16-char-app-password
   ```

3. **Build and Run**

   ```bash
   go build -o email-monitor ./cmd/email-monitor/
   ./email-monitor
   ```

   For dry-run mode (shows what would be saved without creating files):

   ```bash
   DRY_RUN=true ./email-monitor
   ```

### Example Output

```text
2025/11/28 13:27:49 Loaded 9 applications from registry
2025/11/28 13:27:49 Connecting to imap.gmail.com:993...
2025/11/28 13:27:49 Successfully connected and authenticated
2025/11/28 13:27:49 Searching for emails since 2025-11-21 (7 days)

=== Processing 5 email(s) ===

--- Email 1/5 (UID: 12345) ---
Date: 2025-11-27 14:30:00
From: CV.ee <notification@cv.ee>
Subject: Kandideerimise kinnitus
Classification: Acknowledgment (confidence: 100%)
Match: DataShift OÜ / Project Manager (confidence: 80%, company name in email)
✅ Saved: ../applications/DataShift/Project_Manager/communications/2025-11-27_acknowledgment.md

=== Summary ===
Total emails: 5
Saved: 3
Skipped: 1
Unmatched: 1

🔍 DRY-RUN mode - no files were created
```

## Next Steps (Phase 3)

- [ ] Goroutine worker pool for parallel processing
- [ ] Channel-based pipeline
- [ ] Graceful shutdown handling
- [ ] Retry logic with exponential backoff
- [ ] Comprehensive logging with log levels

## Next Steps (Phase 4)

- [ ] YAML configuration file
- [ ] Daemon mode with configurable interval
- [ ] Registry update functionality (status changes)
- [ ] Track processed emails (avoid duplicates)
- [ ] Unit tests

## Project Structure

```text
email-monitor/
├── cmd/
│   └── email-monitor/
│       └── main.go              # Entry point
├── internal/
│   ├── imap/
│   │   └── client.go            # IMAP connection & fetch
│   ├── parser/
│   │   └── email.go             # Email parsing with MIME support
│   ├── classifier/
│   │   └── classifier.go        # Email type classification
│   ├── matcher/
│   │   └── application.go       # Application matching
│   ├── storage/
│   │   └── markdown.go          # Markdown file generation
│   └── registry/
│       └── registry.go          # REGISTRY.md parser
├── config/
│   └── config.go                # Configuration
├── .env                         # Credentials (not in git)
├── go.mod
└── README.md
```

## Technical Notes

- Uses `github.com/emersion/go-imap/v2` for IMAP operations
- Standard library `net/mail` + `mime/multipart` for email parsing
- Gmail requires app-specific passwords (not regular password)
- Searches emails from last 7 days by default
- Uses `[Gmail]/All Mail` folder to catch all emails

## Classification Keywords

| Type | Keywords (Estonian/English) |
|------|----------------------------|
| Acknowledgment | kätte saanud, received, kinnitame, täname kandideerimise |
| Rejection | kahjuks, teise kandidaadi, unfortunately, not selected |
| Interview | intervjuu, interview, kohtumine, meeting |
| Offer | pakkumine, offer, salary, palk |
| Inquiry | küsimus, question, lisainfo |
| Followup | update, status, jätkuteade |

---

**Created:** 2025-11-28
**Current Phase:** 2/4 Complete
