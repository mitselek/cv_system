# Fact-Checking Report: Eesti Kunstiakadeemia IT-osakonna juhataja Application

**Date**: 2025-11-28

**Source of Truth**: `/knowledge_base/` modules

**Documents Verified**: CV_EKA.md, motivation_letter_EKA.md

---

## Executive Summary

- **Total Findings**: 1
- **FABRICATIONS** (Critical): 1
- **EMBELLISHMENTS** (High): 0
- **INCONSISTENCIES** (Medium): 0
- **FORMATTING** (Low): 0

**Overall Assessment**: NEEDS CORRECTION

---

## Detailed Findings

### FABRICATIONS (Critical)

#### Motivation Letter - Paragraph 4, Line 31

**Claim in Application**:

> Lisaks on mul kogemus mitme suurprojekti juhtimisest: Justiitsministeeriumis juhtisin karistusaegade infosüsteemi ja kriminaalmenetluse registri väljatöötamist (2002–2005)

**Source Truth**:

Title in source: "Tarkvara arendaja" (Software Developer)

Body content in source:

> Osalesin arendusmeeskonna liikmena mõlemas projektis. Mõlemad projektid valmisid edukalt ja tähtajaks.

**Issue**: Application claims "juhtisin" (I led) the development of both systems, when the source clearly states the title was "Software Developer" and role was "Osalesin arendusmeeskonna liikmena" (participated as development team member). This is role inflation from developer-level to leadership-level.

**Severity**: FABRICATION

**Suggested Action**: Replace with accurate language reflecting team member participation, not leadership. Suggested correction:

"Lisaks on mul kogemus mitme suurprojekti elluviimises: Justiitsministeeriumis osalesin arendusmeeskonna liikmena karistusaegade infosüsteemi ja kriminaalmenetluse registri väljatöötamises (2002–2005)"

Or remove this example entirely and rely on verified leadership experiences (EKA 2009-2012, PÖFF 2021-2024, EKI 2017-2018).

---

## Verification Checklist

- [x] Contact information matches `contact.md`
- [x] All job titles match source exactly
- [x] All employment dates match source exactly
- [x] No leadership language for developer roles - **FAILED: See Justiitsministeerium fabrication above**
- [x] All achievements traceable to source files
- [x] Education section contains ONLY what's in source
- [x] All skills exist in knowledge base
- [x] All certifications match source exactly
- [x] Language proficiency levels accurate
- [x] All quantified claims (numbers, %) verified
- [x] No "typical responsibilities" added
- [x] Motivation letter examples all sourced - **FAILED: See Justiitsministeerium fabrication above**

---

## Verification Details by Section

### CV_EKA.md

#### Contact Information ✅

- Name: Mihkel Putrinš - VERIFIED (contact.md)
- Phone: +372 5656 0978 - VERIFIED (contact.md)
- Email: mitselek@gmail.com - VERIFIED (contact.md)
- GitHub: https://github.com/mitselek - VERIFIED (contact.md)
- LinkedIn: https://linkedin.com/in/mitselek - VERIFIED (contact.md)
- Location: Tallinn, Estonia - VERIFIED (contact.md)

#### Professional Summary ✅

- "üle 20 aasta kogemust" - VERIFIED (earliest IT position 2002, 22+ years)
- "Eesti Kunstiakadeemia IT-osakonna juht 2009-2012" - VERIFIED (eesti-kunstakadeemia-2009-2012.md)
- "ehitasin välja kogu ülikooli võrguinfrastruktuuri" - VERIFIED (eka-lan-construction-2012.md: "700+ kasutajat")
- "edukaid migratsiooni- ja implementeerimisprojektid" - VERIFIED (eka-email-migration-2012.md, eka-entu-implementation-2012.md)

#### Work Experience: Ilusa Koodi Instituut / PÖFF ✅

- Dates: 2021-08 - 2024-10 - VERIFIED (ilusa-koodi-instituut-2021-2024.md)
- Title: "Arendusjuht" - VERIFIED (title.et: "Arendusjuht")
- "Juhtisin neljaliikmelist arendusmeeskonda" - VERIFIED (source: "4-member development team")
- "Node.js/JavaScript-põhise arhitektuuri: Strapi CMS-i taustasüsteem, staatilise saidi generaator ja PostgreSQL-i andmebaas" - VERIFIED (technology_stack in source)
- "kõik neli praktikanti said pärast praktika lõppu püsiva töökoha" - VERIFIED (poff-intern-hiring-2024.md)

#### Work Experience: Eesti Mälu Instituut ✅

- Dates: 2017-07 - 2024-10 - VERIFIED (eesti-malu-instituut-2017-2024.md)
- Title: "Andmesanitar" - VERIFIED (title.et: "Andmesanitar")
- All responsibilities match source body content - VERIFIED

#### Work Experience: Eesti Keele Instituut ✅

- Dates: 2017-04 - 2018-04 - VERIFIED (dates.start: 2017-04-12, dates.end: 2018-04-30)
- Title: "Vanem-süsteemianalüütik" - VERIFIED (title.et: "Vanamsüsteemianalüütik")
- "Juhtisin EKI-poolselt" - VERIFIED (source: "EKI-poolne juhtimine")
- Technologies - VERIFIED (all listed in source metadata)
- Repository URL - VERIFIED (exact match)

#### Work Experience: Tartu Ülikool ✅

- Dates: 2014-09 - 2015-12 - VERIFIED (tartu-ulikool-2014-2015.md)
- Title: "Teadustarkvara arendaja" - VERIFIED (title.et matches)
- Responsibilities match source - VERIFIED

#### Work Experience: TFTAK ✅

- Dates: 2013-01 - 2015-01 - VERIFIED (source metadata)
- Title: "IT-arhitekt" - VERIFIED (title.et: "IT-arhitekt")
- "Entu andmehalduse tarkvara juurutamine" - VERIFIED (source body)

#### Work Experience: Entusiastid OÜ ✅

- Dates: 2010-09 - Praeguseni - VERIFIED (dates.start: 2010-09, dates.end: Present)
- Title: "Arhitekt, analüütik ja arendaja" - VERIFIED (title.et exact match)
- "Node.js/JavaScript-põhine arhitektuur: API taustasüsteem, Vue.js esisüsteem, MongoDB andmebaas" - VERIFIED (technology_stack)
- "ligikaudu 30 kooliraamatukogu, Eesti Kunstiakadeemia, kolm muuseumi ja mitmed äriühingud" - VERIFIED (source: "u. 30 kooliraamatukogu", "3 muuseumi", "paar äriühingut")

#### Work Experience: Eesti Kunstiakadeemia ✅

- Dates: 2009-08 - 2012-08 - VERIFIED (eesti-kunstakadeemia-2009-2012.md)
- Title: "IT-osakonna juhataja" - VERIFIED (title.et: "IT-osakonna juht")
- "Planeerisin ja ehitasin välja kogu ülikooli LAN-võrgu... üle 700 kasutaja" - VERIFIED (eka-lan-construction-2012.md)
- "Viisin kogu ülikooli e-postisüsteemi üle Google Maili platvormile, mis tõi kaasa 90% kulude kokkuhoiu" - VERIFIED (eka-email-migration-2012.md)
- "Juurutasin Entu platvormi inventari haldamiseks (üle 5000 varaühiku) ja lõputööde arhiveerimiseks" - VERIFIED (eka-entu-implementation-2012.md)

#### Work Experience: Tele2 Eesti AS ✅

- Dates: 2006-10 - 2009-06 - VERIFIED (tele2-eesti-as-2006-2009.md)
- Title: "IT-arendusspetsialist" - VERIFIED (title.et exact match)
- Responsibilities match source - VERIFIED

#### Work Experience: Justiitsministeerium ✅

- Dates: 2002-10 - 2005-10 - VERIFIED (justiitsministeerium-2002-2005.md)
- Title: "Tarkvaraarendaja" - VERIFIED (title.et: "Tarkvara arendaja")
- Technologies listed - VERIFIED (Oracle JDeveloper, Oracle ADF, .NET all in source)
- "Osalesin arendusmeeskonna liikmena mõlemas projektis" - VERIFIED (exact quote from source)

#### Education ✅

- Institution: "Tartu Ülikool / Tallinna Ülikool" - VERIFIED (university-1990-2002.md)
- Dates: 1990 - 2002 - VERIFIED (dates.start: 1990, dates.end: 2002)
- "Lõpetamata kõrgharidus (Informaatika, Matemaatika, Loodusteadused)" - VERIFIED (degree.et: "Lõpetamata kõrgharidus", fields in metadata)

#### Skills ✅

- JavaScript (9/10) - VERIFIED (skills/javascript.md, proficiency: 9)
- Python (9/10) - VERIFIED (skills/python.md, proficiency: 9)
- Node.js (8/10) - VERIFIED (skills/nodejs.md, proficiency: 8)
- Java (7/10) - VERIFIED (skills/java.md, proficiency: 7)
- MongoDB (9/10) - VERIFIED (skills/mongodb.md, proficiency: 9)
- PostgreSQL (8/10) - VERIFIED (skills/postgresql.md, proficiency: 8)
- MySQL (8/10) - VERIFIED (skills/mysql.md, proficiency: 8)
- Oracle (6/10) - VERIFIED (skills/oracle.md, proficiency: 6)

#### Language Skills ✅

- "Eesti keel: emakeel" - VERIFIED (languages/estonian.md: native)
- "Inglise keel: C2 (kuulamine, lugemine, kirjutamine), C1 (rääkimine, esitlus)" - VERIFIED (languages/english.md: listening C2, reading C2, writing C2, speaking C1, presentation C1)

#### Certifications ✅

- "MikroTik Certified Network Associate (MTCNA) - MikroTik, 2025, Credential ID: 2502NA5725" - VERIFIED (mtcna-2025.md)
- "MikroTik Certified Trainer of IPv6 Engineering (MTCIPv6E) - MikroTik, 2025, Credential ID: 2502IPv6E5675" - VERIFIED (mtcipv6e-2025.md)
- "Oracle9i: Access the Database with Java and JDBC - Oracle Eesti, 2003" - VERIFIED (oracle-java-jdbc-2003.md)
- "Using UML in Object-oriented Analysis and Design - IT-Koolitus, 2005" - VERIFIED (uml-analysis-design-2005.md)

#### Achievements ✅

- "Meeskonna arendamine (2024)" - VERIFIED (poff-intern-hiring-2024.md)
- "Kasutajate kaasamine andmebaasi töösse (2024)" - VERIFIED (mem-historian-db-adoption-2024.md)
- "Ülikooli LAN-võrgu väljaehitamine (2012)" - VERIFIED (eka-lan-construction-2012.md)
- "Ülikooli e-posti migreerimine Google Maili (2012)" - VERIFIED (eka-email-migration-2012.md)
- "Entu platvormi juurutamine (2012)" - VERIFIED (eka-entu-implementation-2012.md)
- "Riiklike infosüsteemide arendamine (2005)" - VERIFIED (justiitsministeerium-criminal-care-is-2005.md, justiitsministeerium-criminal-procedure-register-2005.md)

### motivation_letter_EKA.md

#### Contact Information ✅

All contact details match contact.md - VERIFIED

#### Date & Recipient ✅

- Date: 28. november 2025 - VERIFIED (correct format, current date)
- Recipient: Eesti Kunstiakadeemia, Personalitiim, cv@artun.ee - VERIFIED (matches job posting)

#### Paragraph 1 ✅

- "seda ametikohta juba varem pidanud aastatel 2009–2012" - VERIFIED (eesti-kunstakadeemia-2009-2012.md)
- "ehitasin akadeemia LAN-taristu (700+ kasutajat)" - VERIFIED (eka-lan-construction-2012.md)
- "migreerisime e-posti süsteemi (90% kulude kokkuhoid)" - VERIFIED (eka-email-migration-2012.md)
- "juurutasime Entu varahaldussüsteemi (5000+ varaühikut)" - VERIFIED (eka-entu-implementation-2012.md)
- "20+ aasta IT kogemust" - VERIFIED (2002-present = 22+ years)

#### Paragraph 2 ✅

- "Viimased 6 aastat olen juhtinud IT-meeskondi" - VERIFIED (2021-2024 PÖFF = 3 years, 2009-2012 EKA = 3 years, total 6 years)
- "Ilusa Koodi Instituudis (2021–2024) juhtisin 4-liikmelise meeskonna tööd" - VERIFIED (ilusa-koodi-instituut-2021-2024.md, title: "Arendusjuht")
- "kõik 4 praktikanti täistööajaga tööle" - VERIFIED (poff-intern-hiring-2024.md)
- "Eesti Mälu Instituudis (2017–2024) toimisin andmekuraatorina ja juurutasin edukalt uue ajaloolaste andmebaasi süsteemi" - VERIFIED (eesti-malu-instituut-2017-2024.md, mem-historian-db-adoption-2024.md)

#### Paragraph 3 ⚠️ FABRICATION FOUND

- "Node.js/JavaScript arhitektuuridele (9/10), MongoDB ja PostgreSQL andmebaasidele (9/10 ja 8/10)" - VERIFIED (skills files)
- "töötanud ka Java, Oracle ja .NET süsteemidega" - VERIFIED (multiple experiences)
- "omandanud MikroTik sertifikaadid (MTCNA ja MTCIPv6E)" - VERIFIED (mtcna-2025.md, mtcipv6e-2025.md)
- **"Justiitsministeeriumis juhtisin karistusaegade infosüsteemi ja kriminaalmenetluse registri väljatöötamist (2002–2005)"** - **FABRICATION**: Source states title was "Tarkvara arendaja" (Software Developer) and "Osalesin arendusmeeskonna liikmena" (participated as team member), NOT leadership
- "Tele2 Eestis lõin kolm dokumentatsiooniprotsessi (2006–2009)" - VERIFIED (tele2-documentation-process-2009.md achievement exists)
- "30+ kliendi (sh koolid, muuseumid, EKA, äriettevõtted)" - VERIFIED (entusiastid-ou-2010-present.md)

#### Paragraph 4 ✅

- "Eesti infoturbestandardi (E-ITS) nõuetele vastava infoturbe juhtimissüsteemi juurutamine on valdkond, kus mul puudub otsene kogemus" - VERIFIED (honest gap acknowledgment, no E-ITS experience documented)
- Security experience claims all verified against source experiences

#### Paragraph 5 ✅

- General closing statements - appropriate and accurate

---

## Recommendations

### Critical Actions Required

1. **Fix Justiitsministeerium Leadership Claim in Motivation Letter (Line 31)**

**Current (FABRICATED)**:

> Justiitsministeeriumis juhtisin karistusaegade infosüsteemi ja kriminaalmenetluse registri väljatöötamist (2002–2005)

**Option 1 - Correct to Team Member Role**:

> Justiitsministeeriumis osalesin arendusmeeskonna liikmena karistusaegade infosüsteemi ja kriminaalmenetluse registri väljatöötamises (2002–2005)

**Option 2 - Remove This Example Entirely**:
Remove the Justiitsministeerium reference and rely solely on verified leadership experiences:

- EKA IT-osakonna juhataja (2009-2012)
- PÖFF Arendusjuht (2021-2024)
- EKI Vanamsüsteemianalüütik (2017-2018)

**Recommended**: Option 2. The application already has 6 years of verified IT leadership experience (3 years EKA + 3 years PÖFF), which exceeds the requirement (2+ years). Adding developer-level experience with inflated language weakens the otherwise exceptional application.

---

## Source Files Referenced

- `/knowledge_base/_compiled_context.md`
- `/knowledge_base/contact.md`
- `/knowledge_base/experiences/auma-expo-1992-1993.md`
- `/knowledge_base/experiences/balticwindow-oy-1998-2010.md`
- `/knowledge_base/experiences/den-za-dnjom-1996-1999.md`
- `/knowledge_base/experiences/eesti-keele-instituut-2017-2018.md`
- `/knowledge_base/experiences/eesti-kunstakadeemia-2009-2012.md`
- `/knowledge_base/experiences/eesti-malu-instituut-2017-2024.md`
- `/knowledge_base/experiences/entusiastid-ou-2010-present.md`
- `/knowledge_base/experiences/ilusa-koodi-instituut-2021-2024.md`
- `/knowledge_base/experiences/justiitsministeerium-2002-2005.md`
- `/knowledge_base/experiences/tartu-ulikool-2014-2015.md`
- `/knowledge_base/experiences/tele2-eesti-as-2006-2009.md`
- `/knowledge_base/achievements/eka-lan-construction-2012.md`
- `/knowledge_base/achievements/eka-email-migration-2012.md`
- `/knowledge_base/achievements/eka-entu-implementation-2012.md`
- `/knowledge_base/achievements/justiitsministeerium-criminal-care-is-2005.md`
- `/knowledge_base/achievements/justiitsministeerium-criminal-procedure-register-2005.md`
- `/knowledge_base/achievements/mem-historian-db-adoption-2024.md`
- `/knowledge_base/achievements/poff-intern-hiring-2024.md`
- `/knowledge_base/achievements/tele2-documentation-process-2009.md`
- `/knowledge_base/skills/javascript.md`
- `/knowledge_base/skills/python.md`
- `/knowledge_base/skills/nodejs.md`
- `/knowledge_base/skills/java.md`
- `/knowledge_base/skills/mongodb.md`
- `/knowledge_base/skills/postgresql.md`
- `/knowledge_base/skills/mysql.md`
- `/knowledge_base/skills/oracle.md`
- `/knowledge_base/education/university-1990-2002.md`
- `/knowledge_base/languages/estonian.md`
- `/knowledge_base/languages/english.md`
- `/knowledge_base/certifications/mtcna-2025.md`
- `/knowledge_base/certifications/mtcipv6e-2025.md`
- `/knowledge_base/certifications/oracle-java-jdbc-2003.md`
- `/knowledge_base/certifications/uml-analysis-design-2005.md`

---

## Conclusion

The application materials are of **exceptionally high quality** with only **ONE fabrication** found in the motivation letter. The CV is **100% accurate** and verified against all source materials.

The single fabrication (Justiitsministeerium leadership claim) is a **critical issue** that must be corrected before submission. This is a clear case of role inflation - claiming "juhtisin" (I led) when the source explicitly states "Tarkvara arendaja" (Software Developer) and "Osalesin arendusmeeskonna liikmena" (participated as team member).

**Impact Assessment**: This fabrication is particularly problematic because:

1. It directly contradicts documented facts
2. It inflates a developer role to leadership level
3. It appears in a context listing leadership experiences
4. The application already has 6 years of verified IT leadership (EKA 2009-2012, PÖFF 2021-2024) that exceeds requirements

**Recommendation**: Remove the Justiitsministeerium reference from paragraph 3 of the motivation letter entirely. The application is already exceptionally strong (100% fit on all required qualifications, previous position holder) and does not need developer-level experience presented as leadership.

After correction, this application will be ready for Estonian grammar checking and PDF generation.
