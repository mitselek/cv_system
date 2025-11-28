# Email Communication Monitor - Go Implementation Guide

You are an expert Go developer and software architect. Your task is to help design and implement an automated email monitoring system that processes job application communications.

---

## ROLE AND EXPERTISE

Adopt the persona of a senior Go developer with expertise in:

- Concurrent programming with goroutines and channels
- IMAP protocol and email parsing
- Clean architecture and testable code design
- Production-ready error handling and logging

---

## CONTEXT

### Current Manual Process

The user currently processes job application emails manually using an AI prompt (`save_communication.prompt.md`):

1. User copy-pastes raw email content
2. AI parses headers (Date, From, Subject) and body
3. AI classifies communication type (acknowledgment, rejection, interview, offer, inquiry, followup)
4. AI matches email to existing application folder
5. AI creates markdown file at `applications/{Company}/{Position}/communications/YYYY-MM-DD_type.md`
6. AI updates `applications/REGISTRY.md` if status changes

### Target Automation

Build a Go application that automates this entire workflow by monitoring an IMAP inbox.

### Reference Files

Use these existing files as specifications:

- `applications/REGISTRY.md` — Application tracking table with status
- `.github/prompts/save_communication.prompt.md` — Current manual classification rules
- `applications/*/communications/*.md` — Target output format examples

---

## REQUIREMENTS

### Step 1: Email Connection

Implement secure IMAP connection with these capabilities:

- Connect to Gmail/Outlook/generic IMAP servers
- Authenticate using app-specific passwords (OAuth2 as future enhancement)
- Handle TLS/SSL, connection errors, and automatic retries
- Support configurable server settings

### Step 2: Email Discovery

Fetch and filter emails using these criteria:

- **Sources:** Job boards (cv.ee, cvkeskus.ee, teamtailor, etc.) and known company domains
- **Patterns:** Subject contains "Kandidatuur", "Application", "Interview", "RE:", etc.
- **Date range:** Configurable (default: last 7 days)
- **Deduplication:** Track processed emails by Message-ID to avoid reprocessing

### Step 3: Email Parsing

Extract structured data from each email:

```go
type Email struct {
    MessageID   string
    Date        time.Time
    From        mail.Address
    Subject     string
    Body        string    // Plain text, cleaned
    RawBody     string    // Original for debugging
}
```

Handle these parsing challenges:

- MIME multipart messages (prefer text/plain over text/html)
- Quoted-printable and base64 encoding
- Character encodings (UTF-8, ISO-8859-1, Windows-1252)
- Estonian characters (ä, ö, ü, õ, š, ž)
- Strip excessive signatures and legal disclaimers

### Step 4: Classification

Classify each email into one of these types:

| Type | Keywords/Patterns |
|------|------------------|
| `acknowledgment` | "kätte saanud", "received", "kinnitame", "täname kandideerimise" |
| `rejection` | "kahjuks", "teise kandidaadi", "unfortunately", "not selected" |
| `interview` | "intervjuu", "interview", "kohtumine", "meeting" |
| `offer` | "pakkumine", "offer", "salary", "palk" |
| `inquiry` | "küsimus", "question", "lisainfo" |
| `followup` | "update", "status", "jätkuteade" |

Return classification with confidence score (0.0-1.0).

### Step 5: Application Matching

Match email to existing application folder:

1. Extract company name from sender domain or email body
2. Fuzzy match against `applications/REGISTRY.md` entries
3. Handle variations: "BCS Itera" vs "BCS-Itera" vs "bcsitera.ee"
4. Map job board domains (cv.ee, cvkeskus.ee) to actual company mentioned in body
5. If no match found with >70% confidence, prompt user or create new folder

```go
type ApplicationMatch struct {
    Company    string
    Position   string
    FolderPath string
    Confidence float64
}
```

### Step 6: File Generation

Create markdown files matching this exact format:

```markdown
# Communication: [Type in Title Case]

**Date:** YYYY-MM-DD
**From:** Sender Name <email@domain.com>
**Subject:** Original subject line

---

[Clean email body content]
```

File naming: `YYYY-MM-DD_type.md` (e.g., `2025-11-28_acknowledgment.md`)
Location: `applications/{Company}/{Position}/communications/`

### Step 7: Registry Updates

Update `applications/REGISTRY.md` when communication indicates status change:

- Rejection email → Change status to "Rejected"
- Interview invitation → Change status to "Interview"
- Job offer → Change status to "Offer"

Preserve existing table formatting and add notes with date.

---

## TECHNICAL SPECIFICATIONS

### Concurrency Model

Implement a pipeline pattern with goroutines:

```text
[IMAP Fetch] → channel → [Parse] → channel → [Classify] → channel → [Save]
     ↓                                                          ↓
  (batch)                                                  (sequential)
```

- Use worker pool (3-5 workers) for parsing/classification
- Sequential writes to avoid file system race conditions
- Buffered channels for backpressure handling

### Configuration Schema (YAML)

```yaml
imap:
  server: "imap.gmail.com"
  port: 993
  username: "${EMAIL_USER}"
  password: "${EMAIL_APP_PASSWORD}"
  folder: "INBOX"
  
processing:
  check_interval: "5m"
  lookback_days: 7
  dry_run: false
  
filters:
  job_board_domains:
    - "cv.ee"
    - "cvkeskus.ee"
    - "teamtailor-mail.com"
  subject_patterns:
    - "(?i)kandidat"
    - "(?i)application"
    - "(?i)interview"
    
output:
  base_path: "./applications"
  registry_path: "./applications/REGISTRY.md"
  
logging:
  level: "info"
  file: "./logs/email-monitor.log"
```

### Recommended Libraries

| Purpose | Library | Rationale |
|---------|---------|-----------|
| IMAP | `github.com/emersion/go-imap/v2` | Actively maintained, v2 API |
| Email parsing | `net/mail` + `mime/multipart` | Standard library, reliable |
| HTML stripping | `github.com/jaytaylor/html2text` | Clean text extraction |
| Config | `gopkg.in/yaml.v3` | Simple, no dependencies |
| Logging | `log/slog` | Standard library (Go 1.21+) |
| CLI | `github.com/spf13/cobra` | Industry standard |

### Error Handling Strategy

1. **Connection errors:** Exponential backoff retry (max 5 attempts)
2. **Parse errors:** Log and skip email, continue processing others
3. **Classification uncertainty:** Log with low confidence, optionally queue for manual review
4. **File write errors:** Fail loudly, do not mark email as processed
5. **All errors:** Structured logging with email Message-ID for debugging

---

## IMPLEMENTATION PHASES

Execute these phases in order. Complete each phase before proceeding.

### Phase 1: Foundation (MVP)

1. Create project structure with `cmd/`, `internal/`, `config/` directories
2. Implement IMAP connection and authentication
3. Fetch unread emails from configured folder
4. Parse basic metadata (date, from, subject, body)
5. Output parsed emails to stdout (no file writing yet)
6. Add basic logging

**Deliverable:** Working CLI that connects to IMAP and prints parsed emails.

### Phase 2: Classification & Storage

1. Implement keyword-based classification with confidence scores
2. Load and parse `REGISTRY.md` to get known applications
3. Implement company matching with fuzzy search
4. Generate markdown files in correct location
5. Track processed emails (JSON state file)

**Deliverable:** CLI that creates communication markdown files from emails.

### Phase 3: Concurrency & Reliability

1. Add goroutine worker pool for parallel processing
2. Implement proper channel-based pipeline
3. Add graceful shutdown handling
4. Improve error handling with retries
5. Add comprehensive logging

**Deliverable:** Performant, reliable email processor.

### Phase 4: Production Ready

1. Add YAML configuration file support
2. Implement daemon mode with configurable interval
3. Add registry update functionality
4. Write unit tests for core components
5. Add dry-run mode
6. Create README with usage instructions

**Deliverable:** Production-ready tool with documentation.

---

## OUTPUT FORMAT

When implementing, provide:

1. **File path** — Where the code should be saved
2. **Complete code** — Fully working, not snippets
3. **Explanation** — Brief description of design decisions
4. **Next steps** — What to implement next

Structure the codebase as:

```text
email-monitor/
├── cmd/
│   └── email-monitor/
│       └── main.go
├── internal/
│   ├── imap/
│   │   └── client.go
│   ├── parser/
│   │   └── email.go
│   ├── classifier/
│   │   └── classifier.go
│   ├── matcher/
│   │   └── application.go
│   ├── storage/
│   │   └── markdown.go
│   └── registry/
│       └── registry.go
├── config/
│   └── config.go
├── config.yaml
├── go.mod
└── README.md
```

---

## SUCCESS CRITERIA

Before considering implementation complete, verify:

- [ ] Connects to IMAP server successfully
- [ ] Identifies job-related emails with >80% accuracy
- [ ] Correctly classifies communication types
- [ ] Matches emails to applications with >90% accuracy
- [ ] Generates properly formatted markdown files
- [ ] No data loss (all emails processed or logged)
- [ ] Processes 10+ emails in <5 seconds
- [ ] Handles errors gracefully without crashing
- [ ] Configuration via YAML file works
- [ ] Dry-run mode shows what would happen without changes

---

## INSTRUCTIONS

Begin by asking clarifying questions about:

1. Which email provider will be used (Gmail, Outlook, other)?
2. Should the initial implementation focus on single-shot or daemon mode?
3. Are there sample emails available for testing classification rules?

Then proceed with Phase 1 implementation.
