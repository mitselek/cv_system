---
docID: "EKA-E-ITS-2026"
version: "1.0"
date: "2026-01-02"
author: "Mihkel Putrinš"
pdf_metadata:
  title: "E-ITS Süvaanalüüs: Eesti Kunstiakadeemia IT-osakonna juhi intervjuuks"
  subject: "Põhjalik analüüs Eesti Infoturbestandardist (E-ITS) ja selle rakendamisest väikese avaliku sektori ülikooli kontekstis"
  keywords: "E-ITS, Eesti Infoturbestandard, ISMS, infoturbe haldus, EKA, Eesti Kunstiakadeemia, intervjuu ettevalmistus, küberturvalisus, avalik sektor, IT-juhtimine"
  creator: "Mihkel Putrinš"
  recommendation: "Kohustuslik lugemine EKA IT-osakonna juhi intervjuuks. Sisaldab E-ITS raamistiku põhjalikku analüüsi, eestikeelset terminoloogiat, ISMS elutsüklit, implementeerimise ajakavu, ressursivajadusi ja EKA-spetsiifilisi soovitusi."
---

# E-ITS Süvaanalüüs: Eesti Kunstiakadeemia IT-osakonna juhi intervjuuks

**Dokumendi eesmärk:** Põhjalik arusaam Eesti Infoturbestandardist (E-ITS) ja selle rakendamisest väikese avaliku sektori ülikooli kontekstis.

**Kontekst:** Intervjuu 6. jaanuaril 2026 EKA IT-osakonna juhi ametkohale.

**Koostatud:** 2. jaanuar 2026

---

## Töökuulutus (Kontekst)

**Amet:** IT-osakonna juhataja  
**Tööandja:** Eesti Kunstiakadeemia  
**Allikas:** CV.ee (https://cv.ee/et/vacancy/1474717)  
**Kandideerimistähtaeg:** 14. detsember 2025

### Peamised tööülesanded

• IT-osakonna töö ja meeskonna juhtimine  
• IT digiarendusstrateegia ning tegevusplaanide väljatöötamine ja elluviimine  
• Arendusprojektide juhtimine  
• IT-taristu toimivuse ja turvalisuse tagamine  
• IT infrastruktuuri arendamine ja haldamine  
• IT-juhendite ja kasutajate koolitamise korraldamine  
• Digiteenuste tagamine koostöös majasiseste IT-spetsialistide ja väliste teenuspakkujatega  
• IT-alaste andmete kogumine ja analüüsimine  
• **Eesti infoturbestandardi (E-ITS) nõuetele vastava infoturbe juhtimissüsteemi koos vajalike protsesside, dokumentatsiooni ja riskihalduse praktikate juurutamine koostöös väliste ja akadeemia siseste partneritega**  
• Ülikoolide vahelises IT koostöö töörühmades osalemine  
• Kõikide IT-partneritega igapäevase suhtluse ja sujuva koostöö haldamine

### Nõuded kandidaadile

• IT-alane haridus (võib olla omandamisel)  
• Vähemalt 3-aastane töökogemus IT valdkonnas  
• Vähemalt 2-aastane IT sektoris osakonna (meeskonna) juhina töötamise kogemus  
• Soovitatavalt teadmised riigihangete korrast  
• Head teadmised arvutite, serverite, IT süsteemide arhitektuuri jt IT toodete hingeelust  
• Initsiatiivikus, kohusetundlikkus, täpsus ja korrektsus  
• Väga hea eesti ja inglise keele oskus  
• Hea suhtlemis-, meeskonnatöö- ja ajaplaneerimisoskus

**Märkus:** E-ITS on töökuulutuses **konkreetselt nimetatud kui otsene tööülesanne** - selle põhjalik mõistmine on seega ametikoha jaoks **kriitilise tähtsusega**.

---

## Kokkuvõte juhtkonnale

E-ITS ei ole IT-projekt – see on **organisatsiooniline transformatsioon**, mis nõuab:

- **Tippjuhtkonna kohustumust** (rektori ja juhatuse aktiivne osalemine)
- **Kõiki äriprotsesse hõlmavat lähenemist** (mitte ainult IT-süsteemid)
- **Süsteemset riskihaldust** läbi organisatsiooni
- **Pikaajalist pühendumust** (2,5-4 aastat miinimum)
- **Pidevaid ressursse** (mitte ühekordne projekt)
- **Turvakultuuri muutust** (kõik töötajad, koolitused)

**EKA jaoks:** 5-liikmelise IT-meeskonnaga (1144 üliõpilast + 279 töötajat) on E-ITS rakendamine reaalne väljakutse. Õnnestumise eelduseks on:

- Realistlikud ootused (pole võimalik "kiiresti implementeerida")
- Väliskonsultantide kaasamine (puuduvad EKA sisesed kompetentsid)
- Ülikoolidevahelise koostöö kasutamine (teised Eesti ülikoolid on teel)
- Piisav eelarve ja ajaressurss

---

## 1. Mis on E-ITS?

### 1.1 Põhidefinitsioon

**Eesti Infoturbestandard (E-ITS)** on avalikule sektorile **kohustuslik** infoturbe halduse raamistik, mis tagab avalike ülesannete täitmiseks kasutatavate äriprotsesside ja infosüsteemide kõikehõlmava kaitse.

### 1.2 Õiguslik alus

- **Küberturvalisuse seadus § 3** (lõiked 1 ja 4)
- **Ettevõtlus- ja infotehnoloogiaministri määrus nr 101** (16. detsember 2022)
- **Viimane versioon:** 2024 (muudetud 28. august 2025)
- **Reguleeriv asutus:** Riigi Infosüsteemi Amet (RIA)

### 1.3 Kohaldatavus

E-ITS kohaldub:

- Riigi- ja kohaliku omavalitsuse asutustele
- Hallatavad asutused
- Riigitulundusasutused
- Avalik-õiguslikud juriidilised isikud
- Nende struktuuriüksused

**EKA kuulub avalik-õigusliku juriidilise isiku kategooriasse** → E-ITS on kohustuslik.

### 1.4 Päritolu ja seos teiste standarditega

- **Aluseks:** Saksa BSI IT-Grundschutz metoodika
- **Kokkusobivus:** Üldine vastavus EVS-EN ISO/IEC 27001 standardiga (standardturbe puhul)
- **Eripära:** Eestikeelne, Eesti õigusruumile vastav, avaliku sektori vajadusi arvestav

---

## 2. Põhimõisted (eestikeelsed terminid)

### 2.1 Infoturbe põhikomponendid (C-I-A)

| Eestikeelne termin        | Ingliskeelne    | Selgitus                                           |
| ------------------------- | --------------- | -------------------------------------------------- |
| **Konfidentsiaalsus (C)** | Confidentiality | Teabe kättesaamatus volitamata isikutele           |
| **Terviklus (I)**         | Integrity       | Teabe õigsus ja täielikkus, hõlmab autentsust      |
| **Käideldavus (A)**       | Availability    | Teabe kättesaadavus õigel ajal volitatud isikutele |

### 2.2 Organisatsiooni struktuuri mõisted

| Eesti termin    | Saksa/inglise       | Selgitus                                                      |
| --------------- | ------------------- | ------------------------------------------------------------- |
| **Kaitseala**   | Informationsverbund | ISMS käsitlusala – kaitstavad elemendid organisatsioonis      |
| **Sihtobjekt**  | Zielobjekt          | Kaitseala allosa – äriprotsess, rakendus, IT-komponent, hoone |
| **Äriprotsess** | Business process    | Eesmärgi saavutamisele suunatud tegevuste kogum               |
| **Kaitsetarve** | Schutzbedarf        | Vara väärtusest tulenev vajadus seda kaitsta                  |

### 2.3 Kaitsetarbe skaalad

| Skaalal       | Inglise   | Selgitus                                                | Tagajärjed                                                 |
| ------------- | --------- | ------------------------------------------------------- | ---------------------------------------------------------- |
| **Normaalne** | Normal    | Võimalik kahju piiratud ja ohjatav                      | Etalonturbe meetmetest piisab                              |
| **Suur**      | High      | Kahjustuse toimed võivad olla tõsised                   | Etalonturbe ei pruugi piisata, vajalik väline riskianalüüs |
| **Väga suur** | Very high | Katastroofilised toimed, organisatsiooni olemasolu ohus | Etalonturbe ei piisa, kohustuslik põhjalik riskianalüüs    |

### 2.4 ISMS ja dokumentatsioon

| Eesti termin                               | Inglise                                | Selgitus                                                                                  |
| ------------------------------------------ | -------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Infoturbe halduse süsteem (ISMS)**       | Information Security Management System | Süsteem poliitikatest, protseduuridest, juhistest ja ressurssidest infovarade kaitsmiseks |
| **Infoturvapoliitika**                     | Information Security Policy            | Organisatsiooni keskne infoturbealane dokument                                            |
| **Infoturbe meetmete rakendusplaan (IMR)** | -                                      | Dokument turvameetmete loetlemiseks, rakendamiseks, vastutajate määramiseks               |

---

## 3. E-ITSi põhidokumendid

E-ITS 2024 versioon koosneb kolmest põhidokumendist:

### 3.1 E-ITS Nõuded infoturbe halduse süsteemile

**Mis see on:**

- Peadokument, mis esitab nõuded ISMS-ile
- 11 jagu (sissejuhatus + jaotised 5-11)
- Kirjeldab ISMS rajamise, evitamise, käigushoidmise ja täiustamise protsessi

**Põhijaotised:**

1. Sissejuhatus (käsitlusala, sihtgrupp)
2. Kasutatud terminid
3. Jaotiste lühiülevaade
4. E-ITS olemus (ISMS kirjeldus, seos riskihaldusega)
5. Infoturbeprotsessist üldiselt (algatamine, tippjuhtkonna kohustumus)
6. Infoturbeprotsessi kavandamine ja plaanimine
7. Infoturbeprotsessi riskihaldus
8. Infoturvameetmete rakendamine
9. Infoturbe käigushoid
10. Infoturbeprotsessi täiustamine
11. E-ITS auditeerimine

### 3.2 E-ITS Etalonturbe kataloog

**Mis see on:**

- Meetmete kataloog ohtude tõrjeks
- 800+ turvameedet moodulitesse koondatuna
- Allalaaditav .html vormingus tugirakenduse kaudu

**Struktuur:**

- **Protsessimoodulid** (ISMS.1 jt) - organisatsioonilised protsessid
- **Süsteemimoodulid** - tehnilised komponendid (server, võrk, rakendus, jne)
- Iga moodul sisaldab:
  - Kirjeldust
  - Ohuanalüüsi
  - Turvasoovitusi (meetmeid)
  - Vastutajaid (rollid)

### 3.3 E-ITS Auditeerimiseeskiri

**Mis see on:**

- Juhised välise auditi läbiviimiseks
- Auditeerimise protsessi kirjeldus
- Audiitori pädevusnõuded
- Järeldusotsuse andmise kriteeriumid

**Auditi eesmärk:**
Hinnata, kas organisatsiooni ISMS ja rakendatud meetmed on:

- Vastavuses E-ITS nõuetega
- Piisavad äriprotsesside kaitseks
- Kooskõlas organisatsiooni eesmärkidega

---

## 4. Kolm turbeviisi (implementeerimislähenemist)

E-ITS võimaldab valida kolme turbeviisi vahel vastavalt organisatsiooni kaitsetarbele ja küpsusele:

### 4.1 Põhiturve

**Millal sobib:**

- Kaitsetarve on **normaalne**
- Organisatsioon alustab E-ITSiga
- Eesmärk on luua baastase

**Nõuded:**

- Etalonturbe kataloogist rakendatakse **põhimeetmed**
- Põhimeetmed tagavad esmase kaitse
- Väljajätud peavad olema põhjendatud

**Rakendamine:**

- Esmajärjekorras põhimeetmed
- Siis järk-järgult liikumine standardturbe suunas

### 4.2 Standardturve

**Millal kohustuslik:**

- Kaitsetarve on **suur või väga suur**
- Organisatsioon soovib ISO 27001 vastavust
- Äriprotsessid nõuavad kõrget kaitset

**Nõuded:**

- Rakendatakse **põhimeetmed + standardmeetmed**
- Kohustuslik **etalonturbe väline riskianalüüs**
- Suur/väga suur kaitsetarve puhul **kõrgmeetmed ja lisameetmed**
- Väljajätud põhi- ja standardmeetmetest peavad olema põhjendatud

**Tulemus:**

- Üldine vastavus **EVS-EN ISO/IEC 27001** standardiga
- Kõrgem turvatase
- Välise auditi võimalus

### 4.3 Tuumikuturve

**Millal sobib:**

- Keskendutakse **ainult kriitiliste protsesside** kaitsmisele
- Organisatsioonil piiratud ressursid
- Soovitakse fokusseeritud lähenemist

**Iseloom:**

- Kitsam käsitlusala (mitte kogu organisatsioon)
- Süvendatud kaitse valitud äriprotsessidele
- Võib olla esimene samm terviklikuma lähenemise suunas

### 4.4 EKA jaoks soovitus: Standardturve

**Põhjused:**

1. **Õiguslik kohustus:** Avalik sektor, ülikool
2. **Andmete tundlikkus:** Üliõpilaste isikuandmed, teadusandmed
3. **T4EU partnerlus:** Rahvusvaheline andmevahetus, partneri nõuded
4. **Finantsandmed:** Eelarve, palgad, hanked
5. **Tulevikukindlus:** ISO 27001 vastavus avab võimalusi

**Strateegia:**

- **Faas 1 (1. aasta):** Põhiturve rakendamine, baasinfoturbe
- **Faas 2 (2-3 aasta):** Üleminek standardturvele
- **Faas 3 (4. aasta):** Standardturbe täielik rakendamine ja audit

---

## 5. ISMS elutsükkel (11 etappi)

E-ITS nõuded kirjeldavad ISMS elutsüklit 11 jaotises. See on **pideva täiustamise tsükkel** (PDCA - Plan-Do-Check-Act):

### FAAS 1: ALGATAMINE (Jaotis 5)

**5.1 Infoturbeprotsessi algatamine**

- **Tippjuhtkond algatab** protsessi (mitte IT-osakond!)
- Nimetatakse **infoturbejuht** (või juhtkond täidab rolli)
- Määratakse äriprotsessid ja kaitseala

**5.2 Tippjuhtkonna kohustumus (commitment)**

- Tippjuhtkond **vastutab** infoturbe elluviimise eest
- Eraldatakse ressursid (rahalised ja inimesed)
- Regulaarne teavitamine juhtkonnas (turvariskid, intsidentid)

**Kriitilised rollid:**

- **Tippjuhtkond** (rektor, juhatus) - eestvedaja
- **Infoturbejuht** - koordineerija
- **Äriprotsessijuhid** - meetmete rakendajad
- **Kõik töötajad** - kaasatud infoturbeprotsessi

### FAAS 2: KAVANDAMINE JA PLAANIMINE (Jaotis 6)

**6.1 Infoturvapoliitika**

- Organisatsiooni **juhtdokument** infoturbe kohta
- Sisaldab infoturbealast kohustumust, eesmärke, põhimõtteid
- Kinnitab **juhtkond**
- Tehakse teatavaks töötajatele

**6.2 Infoturvaeesmärkid**

- Realistlikud, praktilised, mõõdetavad eesmärgid
- Äriprotsesside kirjeldus
- Kaitseala ja sihtobjektide määramine
- Kaitsetarbe määramine (normaalne/suur/väga suur)

**6.3 Infoturbeprotsessi korraldus**

- Turbekorraldus- ja teavitusstruktuur
- Rollide määramine (infoturbejuht, IT-turbejuht, protsessijuhid)
- Volitused ja vastutusalad

**6.4 Infoturbealane koolitus**

- Kõigi töötajate pädevuse tagamine
- Regulaarsed koolitused (motivatsioon, riskikäitumine)

**6.5-6.7 Ressursid ja dokumenteerimine**

- Juhtkond eraldab ressursid
- Dokumenteerimise reeglid
- Poliitikad, eeskirjad, korrad, protseduurid

### FAAS 3: RISKIHALDUS (Jaotis 7)

**7.1 Riskihalduse põhimõtted**

- Kaitsetarbe määramise põhimõtted
- Kahjustsenaariumid
- Riski aktsepteerimise kriteeriumid

**7.2 Etalonturbe modelleerimine**

- Sihtobjektide vastendamine etalonturbe moodulitega
- Põhi-, standard- või kõrgmeetmete valimine
- Protsessimoodulid + süsteemimoodulid

**7.3 Etalonturbe väline riskianalüüs**

- Kohustuslik suur/väga suur kaitsetarbe puhul
- Ebatüüpsed sihtobjektid
- Lisaturvameetmete määramine

### FAAS 4: RAKENDAMINE (Jaotis 8)

**8.1-8.3 Meetmete rakendamine**

- Tehnilised meetmed kõigile sihtobjektidele
- Organisatsioonilised meetmed kõigisse protsessidesse
- Vastutajate määramine

**8.4-8.5 Infoturbe meetmete rakendusplaan (IMR)**

- Rakendatavad turvameetmed
- Meetme teostatuse määr
- Rakendamise selgitus või mitterakendamise põhjendus
- Vastutajad ja tähtajad

**8.6-8.8 Kinnitamine ja teotsus**

- Juhtkond kinnitab IMR ja aktsepteerib jääkriske
- Meetmete rakendamine vastavalt plaanile
- Regulaarsete tegevuste tõendatavus

### FAAS 5: KÄIGUSHOID (Jaotis 9)

**9.1-9.2 Pideva toimimise tagamine**

- Infoturvaeesmärkide saavutatuse jälgimine
- Ressursside kasutamise mõõtmine
- Reageerimine muutustele

**9.3-9.4 Seire ja registreerimine**

- Infoturbe sündmuste registreerimine
- Dokumenteeritud tulemuste kasutamine täiustamiseks

**9.5 Teavitamine**

- Juhtkonna teavitamine
- Töötajate informeerimine
- Huvipoolte kaasamine

### FAAS 6: TÄIUSTAMINE (Jaotis 10)

**10.1 Infoturbe parendamine**

- Perioodiline infoturbeprotsessi kontroll
- Täiustamise põhjused (organisatsiooni muutused, intsidentid, auditid)
- Juhtkonna otsused täiustamiseks

**10.2 Sõltumatu läbivaatus**

- Regulaarne sõltumatu läbivaatus või siseaudit
- Vastavuse hindamine E-ITS nõuetele
- Ettepanekud täiustamiseks

### FAAS 7: AUDITEERIMINE (Jaotis 11)

**11.1-11.4 Väline audit**

- Auditi eesmärk: hinnata ISMS vastavust E-ITSile
- Kohustuslik (regulatsioon), lepinguline või vabatahtlik
- Järeldusotsus - tõend infoturbe toimivuse kohta

---

## 6. Etalonturbe kataloogi struktuur

### 6.1 Moodulite tüübid

**Protsessimoodulid (P-moodulid):**

- **ISMS.1** - Turbehaldus (ISMS teostusjuhised)
- Organisatsioonilised, juhtimise ja turbekorralduse protsessid
- Kohaldatakse kõigile organisatsioonidele
- Kõik protsessimoodulid kaasatakse rakendusplaani

**Süsteemimoodulid (S-moodulid):**

- Tehnilised komponendid (serveri, võrk, rakendus, andmebaas jne)
- Rakendatakse vastavalt kaitseala määratlusele
- Valitakse vastavalt organisatsiooni tehnilistele vahenditele

### 6.2 Meetmete tasemed

| Tase              | Eestikeelne | Selgitus                                                |
| ----------------- | ----------- | ------------------------------------------------------- |
| **Põhimeede**     | Basic       | Minimaalne turvatase, kohustuslik põhiturve puhul       |
| **Standardmeede** | Standard    | Kõrgendatud turvatase, kohustuslik standardturve puhul  |
| **Kõrgmeede**     | High        | Väga kõrge turvatase, suur/väga suur kaitsetarve korral |
| **Lisameede**     | Additional  | Etalonturbe välise riskianalüüsi tulemusena määratud    |

### 6.3 800+ meetme kataloog

**Meetmete koondamine moodulitesse:**

- Iga moodul sisaldab 10-50 meedet
- Meetmed on klassifitseeritud taseme järgi
- Meetmed vastavad BSI IT-Grundschutz metoodikale

**Näide moodulist:**

- **APP.1 E-post ja gruppvaratöö klient**
  - Põhimeetmed: Turvaseadete konfigureerimine, paroolide kaitse
  - Standardmeetmed: Krüpteerimine, spämmikaitse
  - Kõrgmeetmed: Täiendav logieering, kõrgendatud autentimine

---

## 7. Realistlikud ajakavad ja ressursid

### 7.1 Implementeerimise ajakava (standardturve)

**Faas 1: Ettevalmistus (2-3 kuud)**

- Juhtkonna kohustumus ja otsus E-ITS rakendamiseks
- Infoturbejuhi nimetamine
- Algne koolitus (infoturbejuht, võtmeisikud)
- Konsultandi valimine (vajaduse korral)

**Faas 2: Planeerimine (4-6 kuud)**

- Infoturvapoliitika koostamine ja kinnitamine
- Äriprotsesside kirjeldamine
- Kaitseala ja sihtobjektide määramine
- Kaitsetarbe hindamine
- Infoturvaeesmärkide sõnastamine

**Faas 3: Põhiturbe rakendamine (6-12 kuud)**

- Etalonturbe modelleerimine
- IMR koostamine (põhimeetmed)
- Põhimeetmete rakendamine
- Dokumentatsiooni loomine
- Töötajate koolitus (esimene voor)

**Faas 4: Standardturve rakendamine (12-18 kuud täiendavalt)**

- Standardmeetmete rakendamine
- Etalonturbe väline riskianalüüs (suur kaitsetarve korral)
- Lisameetmete rakendamine
- Täiendav dokumentatsioon
- Süvendatud koolitused

**Faas 5: Audit ja sertifitseerimine (3-6 kuud)**

- Siseaudit või sõltumatu läbivaatus
- Korrigeerivad tegevused
- Välise audiitori kaasamine
- E-ITS audit
- Järeldusotsuse saamine

**KOKKU: 2,5-4 aastat** minimaalselt täielikuks standardturve rakendamiseks.

### 7.2 Inimressursi vajadus

**IT-osakonna koormus:**

- **Infoturbejuht** (IT-osakonna juht EKA puhul): 20-30% FTE pidevalt
- **IT-tehniline personal**: 10-20% FTE implementeerimise ajal
- **Kogu IT-meeskond kokku**: Esmajärjekorras 30-50% ühe FTE-st

**Organisatsioon laiemalt:**

- **Äriprotsessijuhid**: 10-20% FTE planeerimise ja rakendamise ajal
- **Tippjuhtkond**: Kvartaliaruanded, poliitikate kinnitamine (ca 5-10 tundi aastas)
- **Kõik töötajad**: Iga-aastane koolitus 4-8 tundi

**Välised konsultandid:**

- **E-ITS konsultant**: 50-100 tundi kokku (planeerimine, riskianalüüs, audit ettevalmistus)
- **Audiitor**: 20-40 tundi (väline audit)

### 7.3 Rahalised ressursid (orienteeruv)

**Konsultandid:**

- E-ITS konsultant: 5 000 - 15 000 € (olenevalt mahust)
- Välise audit: 3 000 - 8 000 €

**Koolitused:**

- Infoturbejuhi koolitus: 1 000 - 3 000 €
- Töötajate üldkoolitused: 50-100 € per töötaja
- EKA (279 töötajat): ca 15 000 - 28 000 € (esimesed aastad)

**Tehnilised lahendused:**

- Turvameetmete rakendamise tehniline pool (sõltub olemasolevast infrastruktuurist)
- Dokumentatsiooni tööriistad, riskihalduse tarkvara: 1 000 - 5 000 €

**Kokku esmaste aastate eelarve: 25 000 - 60 000 €** (sõltub konsultantide kasutamise mahust ja tehniliste investeeringute vajadusest)

---

## 8. EKA spetsiifilised kaalutlused

### 8.1 EKA tugevused E-ITS kontekstis

**1. Bert Blös (andmekaitsespetsialist, Rektoraadi büroo):**

- Juba organisatsioonis (kuigi Rektoraadi büroost, mitte IT-osakonnast)
- GDPR kogemus kattub E-ITS nõuetega (isikuandmete kaitse)
- Võimalik oluline koostööpartner E-ITS rakendamisel
- Tuleb siduda E-ITS töörühma ühistöö lepinguga

**2. Olemasolevad digitaalsed süsteemid:**

- Tahvel (õppeinfosüsteem)
- Moodle (e-õpe)
- Veebileht ja digitaalse loomingu süsteemid
- Määratletud sihtobjektid - hea alus kaitseala kirjeldamiseks

**3. GDPR vastavuse töö:**

- Andmekaitse põhimõtted vastavad E-ITS nõuetele
- Isikuandmete töötlemise dokumentatsioon - kasulik E-ITS dokumentatsioonis
- Andmete kaitsetarbe määramine - otsene sisend E-ITSi

**4. Ülikoolide võrgustik:**

- Eesti ülikoolide IT-koostöö grupid
- Võimalus õppida teiste ülikoolide kogemustest (TalTech, TÜ, TTÜ jt)
- Jagatud väljakutsed (sarnased äriprotsessid, regulatsioonid)

### 8.2 EKA väljakutsed E-ITS kontekstis

**1. Väike meeskond, suur ulatus:**

- 5 IT-töötajat 1144 üliõpilasele + 279 töötajale
- Tõenäoliselt operatiivse tööga küllastunud
- E-ITS nõuab 30-50% ühe FTE ressurssi pidevalt
- **Küsimus:** Kust tuleb E-ITS jaoks võimsus?

**2. T4EU rahvusvaheline liit:**

- 10-ülikoolide liit (Euroopa kunstiülikoolid)
- Piiriülene andmevahetus
- Partnerluse lepingulised nõuded infoturvele
- Tõenäoliselt suur/väga suur kaitsetarve
- Suurendab E-ITS rakendamise keerukust

**3. Võimalik pärandinfrastruktuur:**

- 2012. aasta süsteemid võivad veel eksisteerida
- Tehniline võlg
- Turvariskid vanematel süsteemidel
- Täiendav koorem nende turvamisele või asendamisele

**4. Avaliku sektori piirangud:**

- Piiratud eelarve
- Hankeseaduse protseduurid konsultantide kaasamisel
- Aeganõudvad otsustusprotsessid

**5. Tippjuhtkonna teadlikkus:**

- Kas rektor/juhatus mõistab, et E-ITS on nende vastutus?
- Kas on olemas "juhtkonna kohustumus"?
- Kas eraldatakse piisavalt ressursse?

### 8.3 Riskid ja ohud EKA-le

**Kui E-ITSi ei rakendata või see ebaõnnestub:**

- **Õiguslik risk:** Küberturvalisuse seaduse rikkumine
- **Regulatoorne risk:** RIA järelevalve, võimalikud sanktsionid
- **Operatsiooniline risk:** Turvaintsidendid, andmelekkeid, süsteemide katkestused
- **Reputatsiooniline risk:** Üliõpilaste/töötajate andmete lekkimise korral usalduse kaotus
- **Rahaline risk:** Intsidentide tagajärgede kõrvaldamine kallim kui ennetamine
- **Partnerlusrisk:** T4EU nõuete mittevastamine võib mõjutada rahvusvahelist koostööd

---

## 9. Intervjuu strateegia

### 9.1 Positsioneerimise põhimõtted

**Olge aus:**

- "Mul ei ole otsest E-ITS rakendamise kogemust."
- "Olen E-ITSi põhjalikult uurinud, sest see on EKA jaoks kriitiline."

**Demonstreerige sügavat arusaamist:**

- "E-ITS ei ole IT-projekt - see on organisatsiooniline transformatsioon, mis nõuab tippjuhtkonna kohustumust."
- "Etalonturbe põhimeetmed on aluseks, kuid standardturve on EKA õiguslikust positsioonist ja T4EU partnerlusest lähtuvalt vajalik."

**Näidake realismi:**

- "Täielik standardturve rakendamine võtab 2,5-4 aastat minimaalselt."
- "Väike meeskond (5 inimest) vajab selget prioritiseerimist ja välise toe kaasamist."

**Pakuge pragmaatilist lähenemist:**

- "Soovitaksin kaasata sertifitseeritud E-ITS konsultandi esialgseks hindamiseks ja plaanimiseks."
- "Ülikoolidevahelise IT-koostöö kasutamine - õppida teiste Eesti ülikoolide kogemustest."
- \"Bert Blös (Rektoraadi büroo) on väärtuslik väline partner - tema GDPR teadmised ja ISMS valdkonnad toetavad E-ITSi, kuid IT-osakonna poolt tuleb ta aktiivselt koostööks kaasata.\"

### 9.2 Konkreetsed vastusevariandid

**Küsimus: "Mis on teie kogemus E-ITSiga?"**

_Vastus:_
"Mul ei ole otsest E-ITS rakendamise kogemust, kuid olen seda raamistikku põhjalikult uurinud, sest avaliku sektori ülikooli jaoks on see kohustuslik ja strateegiliselt kriitilne.

E-ITS põhineb Saksa BSI IT-Grundschutz metoodikal ja on oma olemuselt infoturbe halduse süsteem, mis nõuab tippjuhtkonna kohustumust, süstemaatilist riskihaldust ja kõigi äriprotsesside kaasamist. See ei ole ainult IT-tehniline projekt.

Mul on tugev IT-turvaalane taust üle 20 aasta infrastruktuuritöös, kogemus avaliku sektori IT-st (Justiitsministeerium), ja mõistan ISMS põhimõtteid. Lisaks tunnen EKA keskkonda (töötasin siin 2009-2012).

Minu lähenemine oleks pragmaatiline:

1. Kaasata sertifitseeritud E-ITS konsultant esimeseks hindamiseks ja planeerimiseks
2. Ehitada E-ITS töörühm koos Bert Blösiga (Rektoraadi büroo andmekaitsespetsialist) ja protsessijuhtidega - koordineerimiskokkulepe vajalik
3. Tagada rektori ja juhatuse mõistmine, et see on nende kohustumus, mitte ainult IT-osakonna ülesanne
4. Võtta faasipõhine lähenemine - põhiturve esimese 12-18 kuu jooksul, siis järk-järguline üleminek standardturvele
5. Seada realistlikud ootused - 2,5-4 aastat täielikuks standardturve rakendamiseks"

**Küsimus: "Kuidas tagaksite E-ITS rakendamise väikese meeskonnaga?"**

_Vastus:_
"See on tõeline väljakutse. 5-liikmeline IT-meeskond 1144 üliõpilase ja 279 töötaja jaoks on intensiivne, eriti kui operatiivne töö on prioriteet.

E-ITS rakendamine nõuab 30-50% ühe FTE ressurssi pidevalt, mitte ühekordset projekti. Seega peame looma jätkusuutliku lahenduse:

**Lühiajaline (esimene aasta):**

- IT-osakonna juhi roll hõlmab infoturbejuhi ülesandeid (20-30% ajast)
- Välise konsultandi kaasamine algplaanimiseks ja riskianalüüsi teostamiseks (50-100 tundi)
- E-ITS töörühma moodustamine - kaasates Bert Blösi (Rektoraadi büroost), õppeosakonna esindaja, personaliosakonna esindaja
- Selge prioritiseerimine - mis operatiivtööst saab minimeerida või automatiseerida?

**Keskpikas (2-3 aastat):**

- Kaaluda täiendava infoturbe/nõuete spetsialisti lisamist meeskonda (0,5-1 FTE)
- Või alternatiivina: üks olemasolev IT-töötaja fokuseeritakse turvale ja vastavusele
- Ülikoolidevahelise koostöö kasutamine - õppimine ja vahendite jagamine

**Pikaajaline (3+ aastat):**

- ISMS muutub osa tavapärasest tööprotsessist (mitte eraldi "projekt")
- Automatiseerimine ja tööriistade kasutamine seire jaoks
- Pideva täiustamise kultuur

Oluline on juhtkonna mõistmine, et **kvaliteetne infoturve nõuab investeeringut**. Alternatiiv - jätta E-ITS rakendamata - toob õigusliku, operatiivse ja reputatsioonilisi riske, mis on kallimad kui õigeaegne investeering."

### 9.3 Küsimused EKA-le (ära küsi kõiki, vali kontekstipõhiselt)

**Hetkeseisu kohta:**

1. "Mis on EKA praegune E-ITS vastavuse tase? Kas on tehtud mingit esialgset hindamist?"
2. "Kas juhatus või rektor on arutanud E-ITS rakendamise vajadust ja ajakava?"
3. \"Kuidas Bert Blös (Rektoraadi büroo) saab koordineerida IT-osakonnaga E-ITS ja infoturbehalduse küsimustes?\"

**Juhtkonna toetuse kohta:** 4. "Kuidas rektor suhtub infoturbesse? Kas on arusaam, et E-ITS nõuab tippjuhtkonna kohustumust?" 5. "Mis eelarve on või saab olla eraldatud infoturbe strateegiateks peale igapäevase IT-toe?" 6. "Kas eksisteerib IT-juhtimise struktuur või komitee strateegiliste IT-küsimuste jaoks?"

**Meeskonna võimekuse kohta:** 7. "Milline protsent IT-meeskonna ajast läheb reaktiivsele toele versus strateegilistele projektidele?" 8. "Kas on kaalutud E-ITS/infoturvefookusega võimekuse lisamist?" 9. "Kuidas looksime 30-50% FTE võimsuse E-ITS jaoks praeguse meeskonna suurusega?"

**Ülikoolide koostöö kohta:** 10. "Milline on EKA kaasatus Eesti ülikoolide IT-koostöö töörühmadesse?" 11. "Kas EKA on õppinud teiste ülikoolide E-ITS rakendamise kogemustest?"

**Prioriteetide ja ajakava kohta:** 12. "Kuna E-ITS on kohustuslik, mis on ülikooli vastavuse tähtaja ootus?" 13. "Kuidas infoturve prioritiseerub võrreldes T4EU infrastruktuuriga ja digitaalse transformatsiooniga?" 14. "Kas on väliseid stiimuleid (auditid, partnerlusnõuded), mis loovad E-ITS kiires?" 15. "Miks Kenet lahkub? (Kas E-ITS surve on tegur?)"

### 9.4 Punased lipud (red flags)

Kui kuulete neid, olge ettevaatlik:

- **"Me vajame teid kiiresti E-ITSi rakendama"** → Ebareaalsed ootused (2,5-4 aastat on miinimum)
- **"See on IT-osakonna vastutus"** → Vale - nõuab organisatsioonilist kohustumust
- **"Pole eelarvet konsultantide või lisapersonali jaoks"** → Õige rakendamine vajab ressursse
- **"Turvalisus ei tohi segada akadeemilist vabadust"** → Kultuuriline vastupanu
- **"Eelmine IT-juht ei maininud E-ITSi"** → Organisatsioon võib olla märkimisväärselt maha jäänud

### 9.5 Rohelised lipud (green flags)

Need märgid näitavad head pinnavst:

- **"Rektor/juhatus on arutanud infoturbe strateegiat"** → Juhtkonna teadlikkus
- **\"Oleme alustanud GDPR tööd Bert Blösiga (Rektoraadi büroo)\"** → Alus eksisteerib, koordineerimine vajalik
- **"Oleme avatud väliste konsultantide kaasamisele"** → Realistlik ekspertiisi lõhede kohta
- **"Osaleme ülikoolide IT-koostöö võrgustikes"** → Koostööle orienteeritud, õppiv mõtteviis
- **"Mõistame, et see on mitmeaastane teekond"** → Realistlikud ootused

---

## 10. Järeldused ja soovitused

### 10.1 Põhiteesid E-ITSist

1. **E-ITS on kohustuslik avalikule sektorile**, sealhulgas ülikoolidele nagu EKA.

2. **E-ITS ei ole IT-projekt** - see on organisatsiooniline transformatsioon, mis nõuab tippjuhtkonna kohustumust.

3. **E-ITS põhineb etalonturbe metoodikal** (Saksa BSI IT-Grundschutz), kus tüüpsete sihtobjektide jaoks kasutatakse etalonmeetmeid, ebatüüpsete ja kõrge kaitsetarbega objektide jaoks täiendavat riskianalüüsi.

4. **Kolm turbeviisi:** põhiturve (normaalne kaitsetarve), standardturve (suur/väga suur kaitsetarve, ISO 27001 vastavus), tuumikuturve (kriitiliste protsesside fookus).

5. **EKA jaoks sobib standardturve** õigusliku positsiooni, andmete tundlikkuse ja T4EU partnerluse tõttu.

6. **Realistlik ajakava:** 2,5-4 aastat täielikuks standardturve rakendamiseks.

7. **Ressursivajadus:** 30-50% ühe FTE ressurssi IT-osakonnast pidevalt, lisaks äriprotsessijuhid, juhtkond, kõik töötajad (koolitused).

8. **Kulud:** 25 000 - 60 000 € esmaste aastate jooksul (konsultandid, koolitused, tehnilised lahendused).

### 10.2 EKA-spetsiifilised soovitused

**Tugevustele toetumine:**

- Kaasata Bert Blös (Rektoraadi büroo andmekaitsespetsialist) E-ITS töörühma - tema GDPR kogemus on väärtuslik, kuid ametliku koostöö leping vajalik
- Kasutada olemasoleva GDPR töö dokumentatsiooni E-ITS jaoks
- Ühenduda Eesti ülikoolide IT-koostöö võrgustikuga - õppida teiste kogemustest

**Väljakutsetega tegelemine:**

- Selge prioritiseerimine IT-meeskonnas - E-ITS jaoks aeg tuleb kuskilt võtta
- Kaaluda täiendava infoturbe spetsialisti lisamist (0,5-1 FTE)
- Kaasata sertifitseeritud E-ITS konsultant esialgseks hindamiseks ja planeerimiseks (50-100 tundi)
- Tagada rektori ja juhatuse mõistmine nende rollist (tippjuhtkonna kohustumus)

**Faasipõhine lähenemine:**

- **Aasta 1:** Juhtkonna kohustumuse saavutamine, planeerimine, põhiturve algatamine
- **Aasta 2-3:** Põhiturve rakendamine, üleminek standardturvele
- **Aasta 4:** Standardturve täielik rakendamine, audit, järeldusotsus

### 10.3 Lõppmärkus

E-ITS rakendamine EKA-s on reaalne, kuid väljakutsuv ülesanne. Õnnestumise võtmed:

1. **Realistlikud ootused** - pole võimalik "kiiresti" implementeerida
2. **Juhtkonna toetus** - rektor ja juhatus peavad võtma kohustumuse
3. **Piisavad ressursid** - raha, aeg, inimesed
4. **Väline tugi** - konsultandid, ülikoolide koostöö
5. **Pragmaatiline lähenemine** - faasipõhine, toimiv turve enne täiuslikku

Kui need eeldused on täidetud, on IT-osakonna juhil võimalik edukalt juhtida E-ITS rakendamist, isegi ilma otsese eelneva E-ITS kogemuseta. Võtmeküsimus on: **kas EKA organisatsioon on valmis seda toetama?**

---

## Kasutatud allikad

- **E-ITS portaal:** https://eits.ria.ee/
- **E-ITS nõuded infoturbe halduse süsteemile 2024** (viimati muudetud 28.08.2025)
- **Küberturvalisuse seadus** (Riigi Teataja)
- **Ettevõtlus- ja infotehnoloogiaministri määrus nr 101** (16.12.2022)
- **RIA (Riigi Infosüsteemi Amet)** juhendmaterjalid ja koolitused

---

_Dokument koostatud 2. jaanuar 2026, IT-osakonna juhi intervjuu ettevalmistuseks Eesti Kunstiakadeemias (intervjuu 6. jaanuar 2026)._

_Autor: Põhjalik uurimistöö E-ITS raamistiku ja rakendamise kohta, lähtudes EKA kontekstist ja vajadustest._
