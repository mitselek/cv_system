# Riigihanked Registry

Track Estonian public procurements (riigihanked) for participation evaluation.

## Statistics

**Total:** 1  
**Active:** 1  
**Submitted:** 0  
**Won:** 0  
**Passed:** 0

## Procurement Tracking

| Date Added | Procurement ID | Reference | Title                             | Procurer         | Deadline         | Fit Score | Documents | Status       | Notes                                                              |
| ---------- | -------------- | --------- | --------------------------------- | ---------------- | ---------------- | --------- | --------- | ------------ | ------------------------------------------------------------------ |
| 2025-11-27 | 9559644        | 302778    | Veebide arendus - ja hooldus tööd | Eesti Energia AS | 2025-12-12 13:00 | TBD       | ✅ 8/8    | 🔍 Analyzing | Web dev & maintenance, simplified procurement, 15 days to deadline |

## Procurement Details

### 9559644 - Eesti Energia AS Web Development

**Basic Information:**

- **Procurement ID:** 9559644
- **Version ID:** 9618044 (latest)
- **Reference Number:** 302778
- **Title:** Veebide arendus - ja hooldus tööd (Web development and maintenance work)
- **Procurer:** Eesti Energia AS (registry code: 10421629)
- **Procedure Type:** Lihthange (Simplified procurement)
- **Published:** 2025-11-26 15:00
- **Submission Deadline:** 2025-12-12 13:00 (15 days remaining)
- **Status:** Alustatud (Active/Started)

**Documents Downloaded (8 base documents):**

1. ✅ **Lisa 2 Raamlepingu projekt** (62,867 bytes) - Framework agreement project
2. ✅ **Lisa 1 Tehniline kirjeldus** (59,169 bytes) - Technical description
3. ✅ **Nõuded meeskonnale** (29,301 bytes) - Team requirements
4. ✅ **Vastavustingimused** (9,479 bytes) - Compliance conditions
5. ✅ **Hankepass täiendatavate selgitustega** (34,852 bytes) - Procurement passport with clarifications
6. ✅ **Hankepass rahvusvahelises formaadis (ESPD) v2.0 laiendatud** (154,317 bytes) - ESPD XML
7. ✅ **Maksumusvorm** (26,295 bytes) - Tax form (XLSX)
8. ✅ **Hindamiskriteeriumid ja hinnatavad näitajad** (2,955 bytes) - Evaluation criteria

**Location:** `procurements/9559644_Eesti_Energia_Veebid/`

**Key Requirements (to be extracted):**

- Web development and maintenance services
- Framework agreement (raamleping) - likely multi-year contract
- Team requirements specified
- Technical requirements in detailed documents

**Next Steps:**

- [ ] Extract requirements from documents (especially Lisa 1, Nõuded meeskonnale)
- [ ] Calculate fit score against knowledge base
- [ ] Analyze team composition requirements
- [ ] Review evaluation criteria (hindamiskriteeriumid.pdf)
- [ ] Check if individual can participate or company registration required
- [ ] Make participation decision

**Links:**

- Platform: <https://riigihanked.riik.ee/rhr-web/#/procurement/9559644/general-info>
- Documents: <https://riigihanked.riik.ee/rhr-web/#/procurement/9559644/documents>

---

## Notes

**Document Types Discovered:**

- `CRITERION_QUESTION` - Tax form for evaluation
- `HANKEPASS` - Procurement passport with explanations
- `ESPD_XML2` - European Single Procurement Document (XML format)
- `HINDAMISKRITEERIUMID` - Evaluation criteria
- `VASTAVUSTINGIMUSED` - Compliance/qualification conditions
- No subtype code - Usually annexes and technical descriptions

**Procurement Process Understanding:**

1. ✅ Documents harvested automatically via API
2. ⏳ Requirements extraction from DOCX/PDF files
3. ⏳ Fit-score calculation against CV/knowledge base
4. ⏳ Decision: Participate / Skip / Need more info
5. If participating: Prepare bid documents (ESPD, team CVs, references, price offer)

**Last Updated:** 2025-11-27
