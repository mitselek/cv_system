# Email Processing Report - December 4, 2025

**Mode:** Automated Monitoring
**Date:** 2025-12-04
**Time:** 03:56 UTC+2

---

## Summary

Email monitor executed successfully. Scanned emails from UID 16442 to UID 16555 (113 new emails since last run).

### Results

- **Emails processed:** 27
- **Files created:** 2 (both misclassified - deleted)
- **Skipped (keyword-based unknown):** 15
- **Unmatched emails:** 10

### Classification Issues

Two files were created but contained false positives:

1. `Eesti_Kunstiakadeemia/.../2025-12-03_acknowledgment.md` 
   - **Issue:** Newsletter/event invitation (not application-related)
   - **Sender:** maarja.pabut@artun.ee
   - **Subject:** KUTSE: EKA Design Showcase 27. jaanuaril
   - **Action:** ❌ DELETED

2. `IONA/.../2025-12-03_offer.md`
   - **Issue:** Revolut card notification (not job-related)
   - **Sender:** no-reply@revolut.com
   - **Subject:** Mihkel-Mikelis, your virtual card is ready for use 💳
   - **Action:** ❌ DELETED

---

## Registry Status

**No changes required.** No valid application communications received since last run (2025-12-03 12:05).

---

## Assessment

### Positive

✅ Email monitor running reliably
✅ State tracking working (incremental UID updates)
✅ Large email volume processed efficiently (113 emails scanned)

### Areas for Improvement

⚠️ Keyword-based classification has false positives
⚠️ Needs domain filtering to reduce noise (e.g., exclude marketing@, newsletter@)
⚠️ Consider whitelist of known recruiting domains

---

## Next Steps

1. ✅ Monitor continues running daily
2. ✅ Interview prep materials ready for Dec 5 (10:30 & 13:30)
3. 📋 Watch for interview confirmations, follow-ups, or additional communications
4. 🔔 Manual review of any new files created

---

## Known Issues

**Email forwarding UID problem (documented):**
- Brandem Baltic interview invitation (Dec 3) arrived via forwarding
- Forward creates new UID, potentially out of sequential order
- Risk: May miss forwarded emails in future
- Status: Documented in issues-22-23-evaluation.md

**Recommendation:** 
- Consider monitoring both `mitselek@gmail.com` and `mihkel.putrinsh@gmail.com`
- Or implement hybrid UID+date-based filtering

---

