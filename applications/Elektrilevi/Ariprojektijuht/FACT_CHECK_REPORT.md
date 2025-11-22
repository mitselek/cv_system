# Fact-Checking Report: Elektrilevi Äriprojektijuht Application

**Date**: 2025-11-22
**Source of Truth**: `/knowledge_base/` modules
**Documents Verified**: CV_Elektrilevi_Ariprojektijuht.md, motivation_letter_Elektrilevi.md

---

## Executive Summary

- **Total Findings**: 7
- **FABRICATIONS** (Critical): 1
- **EMBELLISHMENTS** (High): 2
- **INCONSISTENCIES** (Medium): 2
- **FORMATTING** (Low): 2

**Overall Assessment**: NEEDS CORRECTION

---

## Detailed Findings

### FABRICATIONS (Critical)

#### Justiitsministeerium Section - CV Line 108 & Motivation Letter Line 41

**Claim in CV**:
> **Tehnoloogiad:** Oracle JDev, Microsoft .NET, projektide koordineerimine, sidusrühmade haldus

**Claim in Motivation Letter**:
> Justiitsministeeriumis juhtisin kahe riiklikult olulise registri (Kriminaalhoolduse Infosüsteem ja Kriminaalmenetluse Register) arendusprojekte.

**Source Truth** (justiitsministeerium-2002-2005.md):

```yaml
title:
  et: Tarkvara arendaja
  en: Software Developer
```

Body content:

- Oracle JDev
- Microsoft .NET
- Saavutused: Kriminaalhoolduse infosüsteem, Kriminaalmenetluse register

**Source Truth** (achievement files):

- "Osalesin arendusmeeskonna liikmena" (Participated as team member)
- No mention of "projektide koordineerimine" or "sidusrühmade haldus"

**Issue**:

1. CV adds "projektide koordineerimine, sidusrühmade haldus" to technologies section - NOT in source
2. Motivation letter claims "juhtisin" (led) projects when source clearly states role was "Tarkvara arendaja" (Software Developer) and achievement describes "Osalesin arendusmeeskonna liikmena" (participated as team member)

**Severity**: FABRICATION

**Suggested Action**:

- CV: Remove "projektide koordineerimine, sidusrühmade haldus" from technologies
- Motivation letter: Change "juhtisin kahe riiklikult olulise registri...arendusprojekte" to "Osalesin arendusmeeskonna liikmena kahe riiklikult olulise registri arendusprojektides"

---

### EMBELLISHMENTS (High)

#### Professional Summary - CV Line 17

**Claim in Application**:
> Kogenud IT-projektijuht, kellel on enam kui 15-aastane kogemus keerukate ärisüsteemide juurutamisel, meeskondade koordineerimisel...

**Source Truth**:

- Employment dates from 2010-present (Entusiastid), 2009-2012 (EKA), 2021-2024 (PÖFF)
- Actual project management role titles:
  - Entusiastid: "Arhitekt/analüütik/arendaja" (NOT project manager)
  - EKA: "IT-osakonna juht" (YES - management)
  - PÖFF: "Arendusjuht" (YES - leadership)
  - Soov Kirjastus 1993: "projektijuht (IT)" (YES - but only 1 year in 1993)

**Issue**: Claiming "15+ years" of project management when only ~6 years have explicit project/team management titles (EKA 2009-2012 = 3 years, PÖFF 2021-2024 = 3 years). Entusiastid role is architect/analyst/developer, not project manager, though it involves implementations.

**Severity**: EMBELLISHMENT

**Suggested Action**: Rephrase to "15+ aastat IT-süsteemide juurutuskogemust, sealhulgas 6+ aastat meeskondade ja projektide otsest juhtimist" (15+ years IT system implementation experience, including 6+ years direct team and project management)

---

#### Tele2 Section - CV Line 93

**Claim in Application**:
> Ehitasin nullist üles ja juhtisin tehnilise dokumentatsiooni meeskonda.

**Source Truth** (tele2-eesti-as-2006-2009.md):

```yaml
title:
  et: IT-arendusspetsialist
  en: Software Developer
```

Body content:

- Arvelduse ja kliendihaduse erilahendused
- Saavutused: Dokumenteerimise võimalikkuse tutvustamine korporatsioonis

Achievement (tele2-documentation-process-2009.md):

- "Tutvustasin dokumenteerimise võimalikkust ja väärtust korporatsioonis"

**Issue**: CV claims "ehitasin nullist üles ja juhtisin tehnilise dokumentatsiooni meeskonda" but source only mentions "introducing documentation culture". No mention of building or leading a team. Title is "Software Developer", not manager.

**Severity**: EMBELLISHMENT

**Suggested Action**: Change to match source more closely: "Tutvustasin dokumenteerimise võimalikkust ja väärtust korporatsioonis, toetades dokumentatsiooniprotsesside standardiseerimist"

---

### INCONSISTENCIES (Medium)

#### Language Proficiency - CV Line 236

**Claim in Application**:
> **Läti keel:** B2 (lugemine/rääkimine/kuulamine), B1 (kirjutamine).

**Source Truth** (latvian.md):

```yaml
proficiency:
  listening: C2
  reading: C2
  speaking: C2
  presentation: C2
  writing: C2
```

**Issue**: CV downgrades Latvian proficiency from C2 (all skills) to B2/B1. This is reverse embellishment - unnecessarily understating the skill.

**Severity**: INCONSISTENCY (but incorrect direction - underselling rather than overselling)

**Suggested Action**: Update CV to match source: "Läti keel: C2 (kõik osaoskused)"

---

#### Motivation Letter - Line 41

**Claim in Application**:
> Justiitsministeeriumis juhtisin kahe riiklikult olulise registri (Kriminaalhoolduse Infosüsteem ja Kriminaalmenetluse Register) arendusprojekte. Need nõudsid tihedat koostööd ärikasutajate, IT-meeskondade, partnerite ja juhtkonna vahel.

**Source Truth**:

- Title: "Tarkvara arendaja" (Software Developer)
- Achievement files: "Osalesin arendusmeeskonna liikmena"

**Issue**: Same as fabrication above - claiming leadership role when source indicates developer/team member role.

**Severity**: FABRICATION (duplicate of above)

**Suggested Action**: Change to "Justiitsministeeriumis osalesin arendusmeeskonna liikmena kahe riiklikult olulise registri arendusprojektides."

---

### FORMATTING (Low)

#### Dates Format - Throughout CV

**CV Format**:
> **2010 – praegu**
> **2021 – 2024**

**Source Format**:

```yaml
dates:
  start: '2010-09'
  end: 'Present'
```

**Issue**: CV uses Estonian "praegu" vs source "Present", and doesn't include months

**Severity**: FORMATTING

**Suggested Action**: None needed - Estonian CV appropriately translates "Present" to "praegu" and year-only format is standard for CV presentation

---

#### Entusiastid Count - CV Line 28 & Motivation Letter Line 34

**Claim in Application** (CV):
> Juurutanud Entu platvormi enam kui 30 organisatsioonis

**Claim in Application** (Motivation Letter):
> Entu andmehaldusplatvormi enam kui 30 juurutuse käigus

**Source Truth** (entusiastid-ou-2010-present.md):

Body content (et):

- Entut kasutavad oma igapäevatöös:
  - u. 30 kooliraamatukogu üle Eesti
  - Eesti Kunstiakadeemia [multiple systems]
  - 3 muuseumi
  - paar äriühingut

**Issue**: Source says "u. 30 kooliraamatukogu" (approximately 30 school libraries) PLUS EKA PLUS 3 museums PLUS couple businesses = MORE than 30 total. CV/letter claim "30+" is actually conservative and accurate.

**Severity**: FORMATTING (accurate representation)

**Suggested Action**: None needed - claim is verified

---

## Verification Checklist

- [x] Contact information matches `contact.md` - VERIFIED
- [x] All job titles match source exactly - VERIFIED
- [x] All employment dates match source exactly - VERIFIED (format adapted appropriately)
- [ ] No leadership language for developer roles - **FAILED** (Justiitsministeerium, Tele2)
- [x] All achievements traceable to source files - VERIFIED
- [x] Education section contains ONLY what's in source - VERIFIED
- [x] All skills exist in knowledge base - VERIFIED
- [x] All certifications match source exactly - VERIFIED
- [ ] Language proficiency levels accurate - **FAILED** (Latvian understated)
- [x] All quantified claims (numbers, %) verified - VERIFIED
- [ ] No "typical responsibilities" added - **FAILED** (projektide koordineerimine, sidusrühmade haldus at Justiitsministeerium)
- [ ] No role inferences beyond source - **FAILED** (Tele2 team building claim)
- [ ] Motivation letter examples all sourced - **FAILED** (Justiitsministeerium leadership claim)

---

## Recommendations

Based on findings, recommend:

1. **CRITICAL - Fix Justiitsministeerium fabrications**:
   - CV: Remove "projektide koordineerimine, sidusrühmade haldus" from technologies section
   - Motivation letter: Change "juhtisin kahe riiklikult olulise registri...arendusprojekte" to "osalesin arendusmeeskonna liikmena kahe riiklikult olulise registri arendusprojektides"

2. **HIGH - Fix professional summary embellishment**:
   - Change "15+ aastane kogemus...IT-projektijuht" to more accurate "15+ aastat IT-süsteemide juurutuskogemust, sealhulgas 6+ aastat meeskondade ja projektide otsest juhtimist"

3. **HIGH - Fix Tele2 team building claim**:
   - Replace "Ehitasin nullist üles ja juhtisin tehnilise dokumentatsiooni meeskonda" with "Tutvustasin dokumenteerimise võimalikkust ja väärtust korporatsioonis"

4. **MEDIUM - Correct Latvian language proficiency**:
   - Update from "B2/B1" to "C2 (kõik osaoskused)" to match source

5. **Regenerate PDFs** after corrections

---

## Source Files Referenced

- `/knowledge_base/_compiled_context.md`
- `/knowledge_base/contact.md`
- `/knowledge_base/experiences/entusiastid-ou-2010-present.md`
- `/knowledge_base/experiences/ilusa-koodi-instituut-2021-2024.md`
- `/knowledge_base/experiences/eesti-kunstakadeemia-2009-2012.md`
- `/knowledge_base/experiences/justiitsministeerium-2002-2005.md`
- `/knowledge_base/experiences/tele2-eesti-as-2006-2009.md`
- `/knowledge_base/experiences/tartu-ulikool-2014-2015.md`
- `/knowledge_base/experiences/tftak-2013-2015.md`
- `/knowledge_base/experiences/soov-kirjastus-1993.md`
- `/knowledge_base/experiences/eesti-malu-instituut-2017-2024.md`
- `/knowledge_base/achievements/justiitsministeerium-criminal-care-is-2005.md`
- `/knowledge_base/achievements/justiitsministeerium-criminal-procedure-register-2005.md`
- `/knowledge_base/achievements/tele2-documentation-process-2009.md`
- `/knowledge_base/achievements/eka-lan-construction-2012.md`
- `/knowledge_base/achievements/eka-email-migration-2012.md`
- `/knowledge_base/achievements/eka-entu-implementation-2012.md`
- `/knowledge_base/achievements/poff-intern-hiring-2024.md`
- `/knowledge_base/languages/latvian.md`
- `/knowledge_base/education/secondary-education-1979-1990.md`
- `/knowledge_base/education/university-studies-1990-2002.md`
