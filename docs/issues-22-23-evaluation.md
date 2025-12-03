# Issues #22 and #23 - Evaluation Report

**Date:** December 3, 2025  
**Evaluator:** GitHub Copilot  
**Status:** Analysis Complete

---

## Issue #22: Filter out marketing/digest emails

**Title:** Email Monitor: Filter out marketing/digest emails  
**Priority:** Medium  
**Estimated Effort:** Small (1-2 hours)  
**Status:** ✅ Ready to implement

### Problem Statement

The email-monitor tool currently processes ALL emails and attempts to classify them as application communications. This results in:

- Marketing emails from info@cvkeskus.ee (job portal digests)
- Music course promotions from charles@betterpiano.com
- Educational newsletters from aa@artun.ee (EKA)

These should be filtered out before classification to avoid:

- False positives in communication tracking
- Cluttered candidate files
- Wasted processing time

### Current Implementation

**Location:** `email-monitor/cmd/email-monitor/main.go`

Current flow:

1. Fetch emails from IMAP
2. Parse each email
3. Classify (returns "unknown" for non-matching content)
4. Match to application
5. Save if matched

**Issue:** Marketing emails get to step 3-4 before being rejected, wasting cycles.

### Proposed Solution

Add a pre-filter step before classification:

```go
// In config/config.go
type ProcessingConfig struct {
    LookbackDays     int
    DryRun           bool
    MarketingSenders []string  // NEW
}

// In main.go, before classification
func isMarketingEmail(from string, marketingList []string) bool {
    for _, sender := range marketingList {
        if strings.Contains(strings.ToLower(from), strings.ToLower(sender)) {
            return true
        }
    }
    return false
}

// Usage in processing loop:
if isMarketingEmail(email.From.Address, cfg.Processing.MarketingSenders) {
    skipped++
    log.Printf("Skipped marketing email from: %s", email.From.Address)
    continue
}
```

### Configuration

Add to `config/config.go` default settings:

```go
MarketingSenders: []string{
    "info@cvkeskus.ee",
    "charles@betterpiano.com",
    "aa@artun.ee",
    "noreply@",
    "no-reply@",
    "donotreply@",
},
```

Optionally support `.env` override:

```text
MARKETING_SENDERS=info@cvkeskus.ee,charles@betterpiano.com,aa@artun.ee
```

### Implementation Checklist

- [ ] Add `MarketingSenders []string` to `ProcessingConfig`
- [ ] Load from environment variable (comma-separated)
- [ ] Implement `isMarketingEmail()` helper function
- [ ] Add filter check before classification in main.go
- [ ] Add separate counter for marketing emails
- [ ] Update statistics output to show marketing skipped
- [ ] Add log message when marketing email detected (VERBOSE mode)
- [ ] Update README.md with new feature
- [ ] Add test cases for marketing filter

### Testing

```bash
# Test with known marketing sender
# Add test email with From: info@cvkeskus.ee
# Verify it's skipped before classification
```

### Benefits

- ✅ Cleaner processing (skip early)
- ✅ Better statistics (separate marketing count)
- ✅ Configurable (easy to add/remove senders)
- ✅ Performance improvement (less parsing/matching)

### Risks

- ⚠️ May accidentally filter legitimate emails if sender matches
- ⚠️ Requires maintenance as new marketing senders appear

**Mitigation:** Use VERBOSE mode to log skipped emails for review.

---

## Issue #23: Preserve outgoing emails in communications

**Title:** Update emails.prompt.md to preserve outgoing emails in communications  
**Priority:** High  
**Estimated Effort:** Medium (3-4 hours)  
**Status:** ⚠️ Needs clarification

### Problem Statement

The current `.github/prompts/emails.prompt.md` prompt instructs removal of outgoing application emails. However, outgoing emails are valuable for:

- Tracking what was sent and when
- Maintaining complete communication history
- Reviewing application materials sent
- Following up based on what was promised

**Current behavior:** Only incoming emails are saved.

### Current Implementation

**Location:** `.github/prompts/emails.prompt.md`

The prompt currently:

1. Focuses on incoming emails (From: company → To: applicant)
2. Classifies based on incoming communication patterns
3. Does not distinguish between incoming/outgoing

**Note:** The email-monitor Go tool itself doesn't filter by direction - it processes all emails in the Gmail account.

### Challenge: Gmail Sent Mail

Gmail stores sent emails separately:

- **[Gmail]/All Mail** - Contains both sent and received
- **[Gmail]/Sent Mail** - Only sent emails
- Current config: `Folder: "[Gmail]/All Mail"`

**Problem:** The tool already has access to sent emails, but:

1. Classification patterns are designed for incoming emails
2. Matching logic assumes sender = company (but for sent, sender = user)
3. No "sent" or "application_sent" communication type exists

### Proposed Solution

#### 1. Add Outgoing Communication Types

**Location:** `email-monitor/internal/classifier/classifier.go`

```go
const (
    Acknowledgment CommType = "acknowledgment"
    Rejection      CommType = "rejection"
    Interview      CommType = "interview"
    Offer          CommType = "offer"
    Inquiry        CommType = "inquiry"
    Followup       CommType = "followup"
    ApplicationSent CommType = "application_sent"  // NEW
    FollowupSent    CommType = "followup_sent"     // NEW
    Unknown         CommType = "unknown"
)
```

#### 2. Detect Email Direction

**Location:** `email-monitor/cmd/email-monitor/main.go`

```go
func isOutgoingEmail(from string, userEmail string) bool {
    return strings.EqualFold(from, userEmail)
}
```

#### 3. Update Classification Logic

**Two approaches:**

**Option A: Separate classification function**

```go
func ClassifyOutgoing(subject, body string) Classification {
    // Look for application-related keywords
    // "attached CV", "interested in", "applying for"
    // Return ApplicationSent or FollowupSent
}
```

**Option B: Direction-aware classification**

```go
func Classify(subject, body string, isOutgoing bool) Classification {
    if isOutgoing {
        return classifyOutgoing(subject, body)
    }
    // existing classification logic
}
```

#### 4. Update Matching Logic

**Challenge:** For outgoing emails:

- Sender = user (not company)
- Recipient = company

**Solution:** Match based on:

- To: field (company domain)
- Subject line (position reference)
- Body content (company name mention)

```go
func MatchApplication(
    from string,
    fromName string,
    to string,        // NEW
    subject string,
    body string,
    apps []Application,
    isOutgoing bool,  // NEW
) *Match {
    if isOutgoing {
        // Match by To: field instead of From:
        return matchByRecipient(to, subject, body, apps)
    }
    // existing logic
}
```

#### 5. Update Prompt

**Location:** `.github/prompts/emails.prompt.md`

Update classification table:

| Type               | Indicators (EN/ET)                                          | Direction |
| ------------------ | ----------------------------------------------------------- | --------- |
| `application_sent` | "attached CV", "applying for" / "CV lisatud", "kandideerin" | Outgoing  |
| `followup_sent`    | "following up", "checking status" / "järelepärimine"        | Outgoing  |
| `acknowledgment`   | "received", "under review" / "kätte saadud"                 | Incoming  |
| ...                | ...                                                         | ...       |

Update registry update rules:

| Email Type         | Direction | Status Transition     | Notes Update               |
| ------------------ | --------- | --------------------- | -------------------------- |
| `application_sent` | Outgoing  | Draft → Submitted     | "Application sent: [date]" |
| `followup_sent`    | Outgoing  | No change             | "Follow-up sent: [date]"   |
| `acknowledgment`   | Incoming  | Submitted → (confirm) | "Confirmed received"       |
| ...                | ...       | ...                   | ...                        |

### Implementation Checklist

#### Phase 1: Core Detection (High Priority)

- [ ] Add user email to config (from EMAIL_USER env var)
- [ ] Implement `isOutgoingEmail()` helper
- [ ] Add direction detection in main processing loop
- [ ] Log outgoing emails separately (VERBOSE mode)
- [ ] Update statistics to show "outgoing: X"

#### Phase 2: Classification (Medium Priority)

- [ ] Add `ApplicationSent` and `FollowupSent` types to classifier
- [ ] Implement outgoing classification patterns
- [ ] Update `Classify()` to accept direction parameter
- [ ] Add tests for outgoing classification

#### Phase 3: Matching (Medium Priority)

- [ ] Update matcher to accept `To:` field
- [ ] Implement `matchByRecipient()` function
- [ ] Update `MatchApplication()` signature
- [ ] Add tests for outgoing matching

#### Phase 4: Storage (Low Priority)

- [ ] Verify storage handles new communication types
- [ ] Update filename generation for "application_sent"
- [ ] Test markdown generation

#### Phase 5: Prompt Update (Low Priority)

- [ ] Update `.github/prompts/emails.prompt.md`
- [ ] Add outgoing email examples
- [ ] Update registry transition rules
- [ ] Add manual archive instructions for outgoing

### Testing Strategy

```bash
# Test 1: Detect outgoing email
# Forward a sent application email to test account
# Run email-monitor with VERBOSE=true
# Verify it's detected as outgoing

# Test 2: Classify outgoing
# Verify it gets "application_sent" classification

# Test 3: Match by recipient
# Verify it matches to correct application by To: field

# Test 4: Save correctly
# Verify filename is "2025-12-03_application_sent.md"
```

### Benefits

- ✅ Complete communication history
- ✅ Track what was sent vs received
- ✅ Better application timeline
- ✅ Registry updates reflect actual actions

### Risks

- ⚠️ **High complexity** - Multiple components to update
- ⚠️ **Matching accuracy** - Outgoing emails may lack clear company identifiers
- ⚠️ **False positives** - Personal emails to companies
- ⚠️ **Performance** - More emails to process

**Mitigation:**

- Implement in phases (detect first, then classify, then match)
- Use dry-run mode extensively during development
- Add verbose logging for debugging

### Open Questions

1. **Should we filter non-application outgoing emails?**

   - Example: Personal emails to company contacts
   - Suggestion: Add keyword filter ("CV", "application", "position")

2. **How to handle reply chains?**

   - "Re: Interview invitation" from user
   - Should this be "followup_sent" or separate type?

3. **What about BCC/CC'd emails?**
   - User CC'd on company-to-recruiter emails
   - Should these be saved?

### Recommendation

**For Issue #23:** Break into 2 separate issues:

1. **Issue #23a: Detect and log outgoing emails** (Quick win)

   - Just add detection and logging
   - No classification or saving yet
   - Gather data on volume and patterns

2. **Issue #23b: Full outgoing email support** (Larger effort)
   - Add classification types
   - Update matching logic
   - Update prompt
   - Requires Issue #23a insights

---

## Priority Recommendation

**Issue #22: High Priority** ✅

- Small effort, immediate benefit
- Reduces noise and improves performance
- Easy to implement and test
- Low risk

**Issue #23: Medium Priority** ⚠️

- High value, but complex implementation
- Recommend phased approach (detect → classify → match)
- Consider breaking into 2 issues
- Higher risk, needs thorough testing

### Suggested Order

1. **First:** Implement Issue #22 (marketing filter)

   - Clean up incoming email processing
   - Get baseline working well

2. **Second:** Implement Issue #23a (detect outgoing)

   - Add detection and logging only
   - Gather data on patterns

3. **Third:** Implement Issue #23b (full support)
   - Based on learnings from #23a
   - Full classification and storage

---

## Summary

| Issue | Status  | Effort | Risk | Priority | Ready?             |
| ----- | ------- | ------ | ---- | -------- | ------------------ |
| #22   | Clear   | Small  | Low  | High     | ✅ Yes             |
| #23   | Complex | Medium | Med  | Medium   | ⚠️ Needs breakdown |

Both issues are valuable and well-defined. Issue #22 is ready for immediate implementation. Issue #23 should be split into detection and full support phases.

---

**Next Steps:**

1. Implement Issue #22 (marketing filter) - Ready to go
2. Create Issue #23a (detect outgoing emails) - Subset of #23
3. Defer Issue #23b (full outgoing support) - After #23a learnings
4. Update original Issue #23 with phase breakdown

**Estimated Total Time:**

- Issue #22: 1-2 hours
- Issue #23a: 2-3 hours
- Issue #23b: 4-6 hours
- **Total: 7-11 hours**
