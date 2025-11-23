# Fact-Checking Report: Askend Estonia Tarkvaraarenduse Projektijuhi Rakendus

**Date**: 2025-11-22

**Source of Truth**: `/knowledge_base/` modules

**Documents Verified**:

- CV_Askend_Estonia_Tarkvaraarenduse_Projektijuht.md
- motivation_letter_Askend_Estonia.md

---

## Executive Summary

- **Total Findings**: 2
- **FABRICATIONS** (Critical): 0
- **EMBELLISHMENTS** (High): 0
- **INCONSISTENCIES** (Medium): 2
- **FORMATTING** (Low): 0

**Overall Assessment**: NEEDS MINOR CORRECTION

---

## Detailed Findings

### FABRICATIONS (Critical)

None found.

---

### EMBELLISHMENTS (High)

None found.

---

### INCONSISTENCIES (Medium)

#### Education Section - CV Line 153

**Claim in Application**:

> ### Tartu Ülikool ja Tallinna Ülikool
>
> **1990 – 2002**
> Õpitud matemaatikat, loodusteaduslikke aineid ja informaatikat

**Source Truth**:

```yaml
id: university-studies-1990-2002
type: education
dates:
  start: "1990"
  end: "2002"
studies:
  - field:
      et: Matemaatika
      en: Mathematics
    institution: University of Tartu
  - field:
      et: Loodusteaduslikud ained
      en: Natural Sciences
    institution: Tallinn University
  - field:
      et: Informaatika
      en: Computer Science
    institution: University of Tartu
```

**Issue**: Source metadata shows separate fields studied at different institutions, not combined. However, the presentation in CV is a reasonable simplification without fabrication.

**Severity**: INCONSISTENCY (Minor - acceptable simplification)

**Suggested Action**: Optional - could be more specific about which subjects at which institutions, but current format is acceptable.

---

#### Motivation Letter - Line 47

**Claim in Application**:

> Pean ausalt tunnistama, et mul puudub otsene Scrum-metodoloogia kogemus

**Source Truth**:
Knowledge base contains no mention of Scrum methodology.

**Issue**: This is an accurate acknowledgment of a gap, not an inconsistency. This is actually good practice.

**Severity**: NOT AN ISSUE - This is appropriate gap acknowledgment

**Suggested Action**: None - this is best practice honesty.

---

### FORMATTING (Low)

None found.

---

## Verification Checklist

- [x] Contact information matches `contact.md` ✓
- [x] All job titles match source exactly ✓
- [x] All employment dates match source exactly ✓
- [x] No leadership language for developer roles ✓
- [x] All achievements traceable to source files ✓
- [x] Education section contains ONLY what's in source ✓
- [x] All skills exist in knowledge base ✓
- [x] All certifications match source exactly ✓
- [x] Language proficiency levels accurate ✓
- [x] All quantified claims (numbers, %) verified ✓
- [x] No "typical responsibilities" added ✓
- [x] No role inferences beyond source ✓
- [x] Motivation letter examples all sourced ✓

---

## Detailed Verification

### Contact Information (CV & Motivation Letter)

✓ Name: Mihkel Putrinš - MATCHES contact.md
✓ Phone: +372 5656 0978 - MATCHES contact.md
✓ Email: <mitselek@gmail.com> - MATCHES contact.md
✓ GitHub: <https://github.com/mitselek> - MATCHES contact.md
✓ LinkedIn: <https://linkedin.com/in/mitselek> - MATCHES contact.md
✓ Location: Tallinn, Eesti - MATCHES contact.md

### Professional Summary (CV)

✓ "üle 30-aastase kogemusega" - VERIFIED (1986-present = 38+ years)
✓ "juhtinud edukalt arendusmeeskondi" - VERIFIED (ilusa-koodi-instituut-2021-2024, eesti-kunstakadeemia-2009-2012)
✓ "tehnilisi projekte" - VERIFIED (multiple project management roles)
✓ "Tõestatud tulemustele orienteeritus" - VERIFIED (achievements show on-time delivery)

### Work Experience Verification

#### Ilusa Koodi Instituut

✓ Title: "Arendusjuht" - MATCHES source title.et
✓ Dates: "2021-08 – 2024-10" - MATCHES source dates
✓ Location: "Tallinn, Eesti" - MATCHES source location
✓ "Juhtisin 4-liikmelist arendusmeeskonda" - VERIFIED in source body
✓ "PÖFF (Pimedate Ööde Filmifestival)" - VERIFIED in source context
✓ "Kõik 4 praktikanti said peale praktika lõppemist ametlikult tööle" - VERIFIED in achievement poff-intern-hiring-2024

#### Eesti Mälu Instituut

✓ Title: "Andmesanitar" - MATCHES source title.et
✓ Dates: "2017-07 – 2024-10" - MATCHES source dates
✓ Location: "Tallinn, Eesti" - MATCHES source location
✓ URL: <https://mnemosyne.ee> - MATCHES source url
✓ "Skännisin raamatuid" - VERIFIED in source body
✓ "Google tabelites" - VERIFIED in source body
✓ "MySql andmebaasis" - VERIFIED in achievement mem-historian-db-adoption-2024

#### Entusiastid OÜ

✓ Title: "Arhitekt/Analüütik/Arendaja" - MATCHES source title.et
✓ Dates: "2010-09 – Praeguseni" - MATCHES source dates (Present)
✓ Location: "Eesti" - MATCHES source location
✓ URL: <https://entu.ee> - MATCHES source url
✓ "u. 30 kooliraamatukogu" - VERIFIED in source body
✓ "Eesti Kunstiakadeemia" - VERIFIED in source body

#### Tartu Ülikool

✓ Title: "Teadustarkvara arendaja" - MATCHES source title.et
✓ Dates: "2014-09 – 2015-12" - MATCHES source dates
✓ Location: "Tartu, Eesti" - MATCHES source location
✓ Context: "Centre of Estonian Language Resources" - MATCHES source context
✓ URL: <https://keeleressursid.ee/en/> - MATCHES source url

#### TFTAK

✓ Title: "IT-arhitekt" - MATCHES source title.et
✓ Dates: "2013-01 – 2015-01" - MATCHES source dates
✓ Location: "Tallinn, Eesti" - MATCHES source location
✓ "Center of Food and Fermentation Technologies" - VERIFIED in source

#### Eesti Kunstiakadeemia

✓ Title: "IT-osakonna juht" - MATCHES source title.et
✓ Dates: "2009-08 – 2012-08" - MATCHES source dates
✓ Location: "Tallinn, Eesti" - MATCHES source location
✓ "Kogu ülikooli LAN-võrgu planeerimine ja ehitamine" - VERIFIED in achievement eka-lan-construction-2012
✓ "700+ kasutajat" - VERIFIED in source and achievement
✓ "Kogu ülikooli e-mailindus kolitud Google Mail'i" - VERIFIED in achievement eka-email-migration-2012

#### Tele2 Eesti AS

✓ Title: "IT-arendusspetsialist" - MATCHES source title.et
✓ Dates: "2006-10 – 2009-06" - MATCHES source dates
✓ Location: "Tallinn, Eesti" - MATCHES source location

#### Justiitsministeerium

✓ Title: "Tarkvara arendaja" - MATCHES source title.et
✓ Dates: "2002-10 – 2005-10" - MATCHES source dates
✓ Location: "Tallinn, Eesti" - MATCHES source location
✓ "Oracle JDev, Microsoft .NET" - VERIFIED in source body
✓ "Kriminaalhoolduse infosüsteem" - VERIFIED in achievement justiitsministeerium-criminal-care-is-2005
✓ "Kriminaalmenetluse register" - VERIFIED in achievement justiitsministeerium-criminal-procedure-register-2005

#### Soov Kirjastus OÜ

✓ Title: "Projektijuht (IT)" - MATCHES source title.et (lowercase in source)
✓ Dates: "1993-01 – 1993-01" - MATCHES source dates
✓ Location: "Eesti" - MATCHES source location
✓ "Soovilehe telefonineiudele liidesega andmebaas" - VERIFIED in source body

#### BalticWindow OY

✓ Title: "Arvutigraafik-kujundaja" - MATCHES source title.et
✓ Dates: "1998-01 – 2010-01" - MATCHES source dates
✓ Location: "Eesti" - MATCHES source location
✓ URL: <http://www.balticwindow.fi> - MATCHES source url

#### Oopus-Arvutite AS

✓ Title: "Arendusjuht" - MATCHES source title.et
✓ Dates: "1993-01 – 1995-01" - MATCHES source dates
✓ Location: "Eesti" - MATCHES source location

#### KBFI

✓ Title: "Laborant" - MATCHES source title.et
✓ Dates: "1986-01 – 1990-01" - MATCHES source dates
✓ Location: "Eesti" - MATCHES source location
✓ URL: <https://kbfi.ee> - MATCHES source url
✓ "e-coliga kääritajates" - VERIFIED in source body
✓ "raskes vees" - VERIFIED in source body
✓ <https://www.tftak.eu/> - VERIFIED in source body

### Education Verification

#### Tartu Ülikool ja Tallinna Ülikool

✓ Dates: "1990 – 2002" - MATCHES source dates
✓ "matemaatikat, loodusteaduslikke aineid ja informaatikat" - MATCHES source fields (acceptable simplification)

#### Secondary Education

✓ Dates: "1979 – 1990" - MATCHES source dates
✓ Institution names: MATCHES source institutions list
✓ "Keskharidus" - MATCHES source degree

### Skills Verification

#### Juhtimine ja projektiüürimine

✓ Projektijuhtimine - EXISTS in knowledge base (project-management)
✓ Meeskonna juhtimine - EXISTS in knowledge base (team-leadership)
✓ IT-juhtimine - EXISTS in knowledge base (it-management)
✓ Mentorlus - VERIFIED through achievements (poff-intern-hiring-2024)

#### Tehnilised oskused

✓ Andmebaaside haldus (MySQL, PostgreSQL, Oracle, MongoDB) - EXISTS in knowledge base (database-management)
✓ Süsteemiarhitektuur - EXISTS in knowledge base (system-architecture)
✓ Andmete kureerimine - EXISTS in knowledge base (data-curation)
✓ Python (9/10) - MATCHES source proficiency_level
✓ JavaScript (9/10) - MATCHES source proficiency_level

#### Tabelarvutus

✓ Google Sheets: 10/10 - MATCHES source proficiency.google_sheets
✓ MS Excel: 8/10 - MATCHES source proficiency.excel
✓ Apps Script automatiseerimine - VERIFIED in source description
✓ Reaalajas andmebaasiga ühendused - VERIFIED in source description

#### Keeleoskus

✓ Eesti keel: Emakeel (native) - MATCHES source proficiency
✓ Inglise keel: C2, C1 - MATCHES source proficiency (C2 for reading/listening/writing, C1 for speaking/presentation)
✓ Läti keel: C2 - MATCHES source proficiency
✓ Vene keel: B2 - MATCHES source proficiency

### Achievements Verification

✓ "Meeskonna arendamine (2024)" - MATCHES poff-intern-hiring-2024
✓ "Kasutajate kaasamine andmebaasi töösse (2024)" - MATCHES mem-historian-db-adoption-2024
✓ "Kogu ülikooli LAN-võrgu ehitamine (2012)" - MATCHES eka-lan-construction-2012
✓ "Ülikooli e-maili migreerimine Google Maili (2012)" - MATCHES eka-email-migration-2012
✓ "90% kulude kokkuhoid" - VERIFIED in achievement description
✓ "Entu platvormi juurutamine (2012)" - MATCHES eka-entu-implementation-2012
✓ "üle 5000 varaühiku" - VERIFIED in achievement description
✓ "üle 500 dokumendi aastas" - VERIFIED in achievement description
✓ "Riiklike infosüsteemide arendamine (2005)" - MATCHES both justice ministry achievements
✓ "Mõlemad projektid valmisid edukalt tähtajaks" - VERIFIED in achievement descriptions
✓ "Kuulutuste andmebaasi arendamine (1993)" - MATCHES soov-kirjastus-classifieds-db-1993

### Certifications Verification

✓ MikroTik Certified IPv6 Engineer (MTCIPv6E) - MATCHES mtcipv6e-2025
✓ Mikrotikls SIA, 2025-10-26 - MATCHES source issuer and date
✓ MikroTik Certified Network Associate (MTCNA) - MATCHES mtcna-2025
✓ Mikrotikls SIA, 2025-02-09 - MATCHES source issuer and date
✓ Using UML in Object-oriented Analysis and Design - MATCHES uml-analysis-design-2005
✓ IT-Koolitus, 2005 - MATCHES source issuer and date
✓ Oracle9i: Access the Database with Java and JDBC - MATCHES oracle-java-jdbc-2003
✓ Oracle Eesti, 2003 - MATCHES source issuer and date
✓ Programming with Microsoft ADO .NET - MATCHES ado-net-2003
✓ IT-Koolitus, 2003 - MATCHES source issuer and date

### Hobbies Verification

✓ 3D modelleerimine ja printimine - EXISTS in knowledge base (3d-modeling-printing)
✓ Onshape ja FeatureScript - VERIFIED in source tools
✓ Astronoomia ja füüsika uurimine - EXISTS in knowledge base (astronomy-and-physics)
✓ Laulmine segakoorides - EXISTS in knowledge base (choir-singing)
✓ Muusika komponeerimine - EXISTS in knowledge base (music-composition)

### Motivation Letter Verification

✓ "üle 30-aastane kogemus" - VERIFIED (1986-present)
✓ "2021-2024" at Ilusa Koodi Instituut - MATCHES source dates (2021-08 to 2024-10)
✓ "4-liikmelist arendusmeeskonda" - VERIFIED in source
✓ "PÖFF" description - VERIFIED in source
✓ "Kõik 4 praktikanti said peale praktika lõppemist ametlikult tööle" - VERIFIED in achievement
✓ "2009-2012" at EKA - MATCHES source dates (2009-08 to 2012-08)
✓ "700+ kasutajat" - VERIFIED in achievement
✓ "üle 700 postkasti" migration - VERIFIED in achievement eka-email-migration-2012
✓ "90% kulude kokkuhoiu" - VERIFIED in achievement description
✓ "2002-2005" at Justice Ministry - MATCHES source dates (2002-10 to 2005-10)
✓ "arendusmeeskonna liikmena" - CORRECT (title was "Software Developer", not lead)
✓ "Mõlemad projektid valmisid edukalt tähtajaks" - VERIFIED in achievements
✓ Google Sheets 10/10, Excel 8/10 - VERIFIED in skills
✓ "2017-2024" at EMI - MATCHES source dates (2017-07 to 2024-10)
✓ "2010-praeguseni" at Entusiastid OÜ - MATCHES source dates
✓ "u. 30 kooliraamatukogu" - VERIFIED in source
✓ MySql database work with historians - VERIFIED in achievement
✓ Language skills (Estonian native, English C2/C1) - VERIFIED in languages
✓ "Scrum-metodoloogia kogemus" gap acknowledgment - APPROPRIATE (not in source)
✓ Education 1990-2002 incomplete - MATCHES source degree status
✓ MTCNA (2025-02) and MTCIPv6E (2025-10) - VERIFIED in certifications

---

## Recommendations

The application is **excellent** and demonstrates strong adherence to the constitution principles:

1. ✅ **Zero fabrications** - All claims are sourced from knowledge base
2. ✅ **Accurate role representation** - Justice Ministry role correctly described as team member, not lead
3. ✅ **Honest gap acknowledgment** - Scrum experience gap appropriately disclosed
4. ✅ **Conservative education presentation** - Incomplete degree status clearly stated
5. ✅ **All quantifications verified** - Every number traced to source

**Minor recommendation**: Education section simplification is acceptable but could optionally be more specific about which institutions taught which subjects if desired for future applications.

**Overall**: This application exemplifies best practices in honest, source-based CV generation. No corrections required.

---

## Source Files Referenced

- `/knowledge_base/_compiled_context.md`
- `/knowledge_base/contact.md`
- `/knowledge_base/experiences/ilusa-koodi-instituut-2021-2024.md`
- `/knowledge_base/experiences/eesti-malu-instituut-2017-2024.md`
- `/knowledge_base/experiences/entusiastid-ou-2010-present.md`
- `/knowledge_base/experiences/tartu-ulikool-2014-2015.md`
- `/knowledge_base/experiences/tftak-2013-2015.md`
- `/knowledge_base/experiences/eesti-kunstakadeemia-2009-2012.md`
- `/knowledge_base/experiences/tele2-eesti-as-2006-2009.md`
- `/knowledge_base/experiences/justiitsministeerium-2002-2005.md`
- `/knowledge_base/experiences/soov-kirjastus-1993.md`
- `/knowledge_base/experiences/balticwindow-oy-1998-2010.md`
- `/knowledge_base/experiences/oopus-arvutite-1993-1995.md`
- `/knowledge_base/experiences/kbfi-1986-1990.md`
- `/knowledge_base/skills/project-management.md`
- `/knowledge_base/skills/team-leadership.md`
- `/knowledge_base/skills/it-management.md`
- `/knowledge_base/skills/database-management.md`
- `/knowledge_base/skills/system-architecture.md`
- `/knowledge_base/skills/data-curation.md`
- `/knowledge_base/skills/python.md`
- `/knowledge_base/skills/javascript.md`
- `/knowledge_base/skills/spreadsheet-tools.md`
- `/knowledge_base/achievements/poff-intern-hiring-2024.md`
- `/knowledge_base/achievements/mem-historian-db-adoption-2024.md`
- `/knowledge_base/achievements/eka-lan-construction-2012.md`
- `/knowledge_base/achievements/eka-email-migration-2012.md`
- `/knowledge_base/achievements/eka-entu-implementation-2012.md`
- `/knowledge_base/achievements/justiitsministeerium-criminal-care-is-2005.md`
- `/knowledge_base/achievements/justiitsministeerium-criminal-procedure-register-2005.md`
- `/knowledge_base/achievements/soov-kirjastus-classifieds-db-1993.md`
- `/knowledge_base/education/university-1990-2002.md`
- `/knowledge_base/education/secondary-1979-1990.md`
- `/knowledge_base/certifications/mtcipv6e-2025.md`
- `/knowledge_base/certifications/mtcna-2025.md`
- `/knowledge_base/certifications/uml-analysis-design-2005.md`
- `/knowledge_base/certifications/oracle-java-jdbc-2003.md`
- `/knowledge_base/certifications/ado-net-2003.md`
- `/knowledge_base/languages/estonian.md`
- `/knowledge_base/languages/english.md`
- `/knowledge_base/languages/latvian.md`
- `/knowledge_base/languages/russian.md`
- `/knowledge_base/hobbies/3d-modeling-printing.md`
- `/knowledge_base/hobbies/astronomy-physics.md`
- `/knowledge_base/hobbies/choir-singing.md`
- `/knowledge_base/hobbies/music-composition.md`
