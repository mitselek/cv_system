# Riigihanked Registry

Simple tracking of Estonian public procurements (riigihanked) for participation evaluation.

## Guidelines

**Purpose:** Track procurements from discovery through decision/outcome.

**How to Use:**

1. Add new row when procurement is downloaded and assessed
2. Update "Status" as situation evolves
3. Keep "Notes" brief - detailed analysis goes in `ASSESSMENT.md` inside procurement folder
4. Update statistics section when status changes

**Status Values:**

- **Analyzing** - Documents downloaded, assessment in progress
- **Consider** - Assessment complete, decision pending
- **Skip** - Decided not to participate (with reason in Notes)
- **Preparing** - Decided to participate, preparing bid
- **Submitted** - Bid submitted, awaiting results
- **Won** - Contract awarded
- **Lost** - Not selected

## Statistics

**Total Assessed:** 16  
**Analyzing:** 1  
**Consider:** 2  
**Skip:** 12  
**FEASIBLE:** 1  
**Submitted:** 0  
**Won:** 0  
**Lost:** 0

## Procurement Tracking

| Date       | ID      | Title                              | Procurer                    | Deadline   | Status     | Notes                                          |
|------------|---------|------------------------------------|-----------------------------|------------|------------|------------------------------------------------|
| 2025-11-27 | 8960884 | Common IT Platform (gas)           | Elering AS                  | 2025-12-03 | Skip       | Gas transmission TSO system, AS4/ActiveMQ/ELK/Keycloak gaps, 50% interviews, 6d prep insufficient, <5% win prob |
| 2025-11-27 | 9514425 | E-kataloogi arendustööd            | RIK                         | 2025-12-12 | Consider   | €150k Java/Spring Boot framework, 50-60% feasible, 30-40% win prob, need tester, DevOps gaps, 15d timeline tight |
| 2025-11-28 | 9530644 | Läbipääsusüsteemi uuendamine       | Eesti Rahvusringhääling     | 2025-11-28 | Skip       | Hardware installation (not dev), Inner Range cert required (advanced+basic), <24h deadline, 0% match |
| 2025-11-28 | 9522164 | IKT kolmanda osapoole riski- ja turvalisuse haldamise lahendus | Eesti Energia AS | 2025-12-02 | Skip | TPRM SaaS platform vendor required (not dev), ISO 27001/SOC2 Type II cert, manufacturer auth needed, product resale not development, <1% win prob |
| 2025-11-27 | 9479004 | Andmelaohaldus ja analüüs          | Eesti Rahvusraamatukogu     | 2025-11-29 | Skip       | CISA audit cert required (9mo), Snowflake (none) |
| 2025-11-27 | 9559644 | Veebide arendus ja hooldus         | Eesti Energia AS            | 2025-12-12 | Analyzing  | Drupal web dev, 40% conditional recommendation |
| 2025-11-27 | 9590504 | Välise kvaliteedihindaja teenus    | Eesti Maaülikool            | 2025-11-02 | Skip       | PhD required, academic QA - impossible         |
| 2025-11-27 | 9582704 | Andmelao arendusteenus             | Põhja-Eesti Regionaalhaigla | 2025-12-04 | Skip       | Market research, Snowflake expertise gap       |
| 2025-11-27 | 9449264 | Kliendiportaali ja puidumüügi keskkond | Riigimetsa Majandamise Keskus | 2025-12-30 | Skip    | ISO 27001 blocker, GIS tech gap, team assembly |
| 2025-11-27 | 9534824 | Pythoni baasil tarkvaraarendused   | KeMIT (Climate Ministry IT) | 2025-12-22 | FEASIBLE   | Python 9/10 MATCH, 70-80% win prob, DevOps gaps addressable |
| 2025-11-27 | 9525405 | Tehnopoli kodulehe arendus         | SA Tehnopol                 | 2025-12-01 | Skip       | WordPress/PHP gap, web design req, 4-day deadline, better alt exists (9534824) |
| 2025-11-27 | 9390245 | Info- ja küberturvalisuse teenused | ESTDEV                      | 2025-12-16 | Skip       | €27M framework, 8+ specialists, 40+ intl projects, cybersec certs, dev cooperation - structural mismatch |
| 2025-11-27 | 9526064 | CRM tarkvara                       | Tallinna Kultuurikatel      | 2025-12-01 | Skip       | Product procurement (not dev), CRM vendor status required, Entu not CRM, Scoro migration impossible, <5% win prob |
| 2025-11-27 | 9407944 | Illegaali Rändepaketi taustakontroll | SMIT (Police/Border Guard) | 2025-12-16 | Consider   | €530k Java/Spring Boot, 50-60% feasible with team, 30-40% win prob, needs Java refresh + 2-3 person team, 5mo intensive |
| 2025-11-27 | 9224484 | RTIP arendus- ja hooldustööd       | RTK + RmIT                  | 2026-01-06 | Skip       | €5M framework, SAP ABAP mandatory (0% exp), Java 7/10 + 8yr gap, 70% test assignment vs insiders, 7-person team in 40d, 5-15% win prob |
| 2025-11-27 | 9565284 | Ukraine veterans platform          | e-Governance Academy        | 2025-12-03 | Skip       | EstDev Ukraine project, 9-person team, Kubernetes/BPMN/Diia/Trembita gaps, Ukrainian lang barrier, 10-20% win prob, 6d insufficient |

## Notes

- Each procurement has detailed assessment in `procurements/{id}_{name}/ASSESSMENT.md`
- Documents stored in `procurements/{id}_{name}/originals/` and `extracted/`
- Use `harvest.py` to download new procurements: `python3 harvest.py download {ID}`

**Last Updated:** 2025-11-27
