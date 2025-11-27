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

**Total Assessed:** 5  
**Analyzing:** 1  
**Skip:** 3  
**FEASIBLE:** 1  
**Submitted:** 0  
**Won:** 0  
**Lost:** 0

## Procurement Tracking

| Date       | ID      | Reference | Title                              | Procurer                    | Deadline   | Status     | Notes                                          |
|------------|---------|-----------|------------------------------------|-----------------------------|------------|------------|------------------------------------------------|
| 2025-11-27 | 9559644 | 302778    | Veebide arendus ja hooldus         | Eesti Energia AS            | 2025-12-12 | Analyzing  | Drupal web dev, 40% conditional recommendation |
| 2025-11-27 | 9590504 | 303108    | Välise kvaliteedihindaja teenus    | Eesti Maaülikool            | 2025-12-02 | Skip       | PhD required, academic QA - impossible         |
| 2025-11-27 | 9582704 | -         | Andmelao arendusteenus             | Põhja-Eesti Regionaalhaigla | 2025-12-04 | Skip       | Market research, Snowflake expertise gap       |
| 2025-11-27 | 9449264 | 301632    | Kliendiportaali ja puidumüügi keskkond | Riigimetsa Majandamise Keskus | 2025-12-30 | Skip    | ISO 27001 blocker, GIS tech gap, team assembly |
| 2025-11-27 | 9534824 | 302531    | Pythoni baasil tarkvaraarendused   | KeMIT (Climate Ministry IT) | 2025-12-22 | FEASIBLE   | Python 9/10 MATCH, 70-80% win prob, DevOps gaps addressable |

## Notes

- Each procurement has detailed assessment in `procurements/{id}_{name}/ASSESSMENT.md`
- Documents stored in `procurements/{id}_{name}/originals/` and `extracted/`
- Use `harvest.py` to download new procurements: `python3 harvest.py download {ID}`

**Last Updated:** 2025-11-27
