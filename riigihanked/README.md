# Riigihanked Research & Participation

## Overview

This folder contains research and tooling for participating in Estonian public procurements (riigihanked).

**Platform:** <https://riigihanked.riik.ee/>

## Current Status

**Phase:** Document Analysis & Requirement Extraction  
**Last Updated:** 2025-11-27

**Completed:**

- ✅ Project structure created
- ✅ API endpoints discovered and documented (see `API_DISCOVERY.md`)
- ✅ Python harvester script implemented (`harvest.py`)
- ✅ First procurement documents downloaded (9559644 - Eesti Energia, 8 documents)
- ✅ Procurement registry created (`REGISTRY.md`)

**In Progress:**

- ⏳ Requirement extraction from downloaded documents
- ⏳ Fit-score algorithm development

**Active Procurement:**

- **ID:** 9559644
- **Title:** Veebide arendus - ja hooldus tööd (Web development and maintenance)
- **Procurer:** Eesti Energia AS
- **Deadline:** 2025-12-12 13:00 (15 days remaining)
- **Documents:** 8/8 downloaded to `procurements/9559644_Eesti_Energia_Veebid/`

**Next Steps:**

- Extract requirements from DOCX/PDF files (especially technical description & team requirements)
- Build fit-score algorithm comparing requirements to knowledge base
- Research participation requirements (company registration, certifications)
- Make participation decision for procurement 9559644

## Strategy

### 1. Document Harvesting

- Identify relevant IT/software development procurements
- Extract base documents (terms, requirements, deadlines)
- Store in structured format for analysis

### 2. Matching Against Profile

- Compare procurement requirements with knowledge base
- Assess fit scores similar to job applications
- Identify qualification gaps

### 3. Participation Decision

- Evaluate effort vs. opportunity
- Check deadline feasibility
- Assess competition level

## Technical Approach

### API Discovery

The riigihanked.riik.ee platform appears to be a JavaScript SPA. Need to:

1. Inspect network traffic to find API endpoints
2. Check if there's a public API documentation
3. Determine authentication requirements

### Document Structure

Typical procurement includes:

- **Hanke alusdokumendid** (Base documents)
  - Technical requirements
  - Terms and conditions
  - Submission deadlines
  - Evaluation criteria
- **Hanke lisa dokumendid** (Additional documents)
- **Questions and answers**

## Next Steps

1. ✅ Create research folder structure
2. ⏳ Investigate API endpoints
3. ⏳ Build document harvester script
4. ⏳ Create procurement tracking registry
5. ⏳ Develop fit-score algorithm for procurements

## Files

- `README.md` - This file
- `harvest.py` - Script to harvest procurement documents (to be created)
- `REGISTRY.md` - Track procurements of interest (to be created)
- `procurements/` - Downloaded procurement documents (to be created)

---

**Created:** 2025-11-27
**Last Updated:** 2025-11-27
