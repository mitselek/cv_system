# Procurement 9582704 Assessment: Andmeplatvormi juurutus- ja arendusteenused

**Procurement ID:** 9582704

**Reference:** TBD (Market research phase)

**Procurer:** SA Põhja-Eesti Regionaalhaigla (North Estonia Medical Centre)

**Deadline:** TBD (Currently in market research phase - "Turu-uuring")

**Contract Duration:** ~17 months (3+4+10 month phases)

**Evaluation:** 100% price-based (lowest cost wins)

**Status:** PRE-PROCUREMENT MARKET RESEARCH

---

## Executive Summary

**Feasibility:** CHALLENGING - Requires extensive specialized cloud data platform expertise

**Winning Probability:** 20-30% (team assembly + specialized partner required)

**Critical Requirements:**

- Snowflake data warehouse implementation and migration
- Modern DataOps stack: Airflow + dbt + Airbyte
- Azure ADLS Gen2 data lake architecture
- Tableau integration and BI development
- Change Data Capture (CDC) implementation
- Data catalog and metadata management (lineage, quality)
- 3-phase delivery: PoC (3 months) → Expansion (4 months) → Standardization (10 months)

**Your Profile Match:**

- Database architecture: STRONG (MySQL, PostgreSQL, Oracle, MongoDB)
- Python development: STRONG (9/10)
- Data integration experience: STRONG (multiple source systems)
- ETL/ELT concepts: MODERATE (SSIS experience, not modern DataOps stack)
- **Snowflake:** NO documented experience
- **dbt:** NO documented experience
- **Airflow:** NO documented experience
- **Airbyte:** NO documented experience
- **Azure Data Lake:** NO documented experience
- **Tableau advanced:** LIMITED (basic BI reporting, not deep development)
- **Healthcare domain:** NO experience
- **DataOps/CI/CD for analytics:** NO documented experience

**Strategic Assessment:** This is a MAJOR infrastructure project requiring specialized cloud data platform expertise. Your strong database and Python foundation provides a base, but the Snowflake + modern DataOps ecosystem (dbt, Airflow, Airbyte) represents significant technology gaps. Success requires either intensive upskilling or partnering with a specialized data engineering firm.

**Recommendation:** 25% CONDITIONAL PARTICIPATION as technical partner/advisor IF you can partner with a Snowflake-certified data engineering firm. NOT recommended as prime contractor without significant team augmentation.

---

## Document Status

**Market Research Phase:** This procurement is currently in the preliminary market research stage ("Turu-uuring"). The procurer is seeking market feedback on technical specifications before launching the formal procurement.

**Documents Available:**

1. **Technical Specification (Tehniline kirjeldus):** 34KB detailed requirements
2. **Market Research Questions (Turu-uuringu küsimused):** 1.9KB feedback form

**Key Questions Posed to Market:**

1. Is the technical description clear and understandable?
2. What are the main risks and limitations for participation?
3. What additional suggestions for the technical specification?
4. Is the timeline feasible?
5. What is the expected cost for the data warehouse contract?
6. Can PERH actively develop reports in Tableau during development? Will there be a "code freeze" period?

**Opportunity:** Participating in market research could:

- Provide visibility to procurer
- Influence final specification
- Build relationship before formal tender
- Assess competition landscape
- Demonstrate capability to contribute meaningfully

---

## Critical Requirements Analysis

### 1. MANDATORY TECHNICAL CAPABILITIES

#### Snowflake Data Warehouse (CRITICAL GAP)

**Requirements:**

- Implement and migrate existing 530GB SQL Server data warehouse to Snowflake
- Design dimensional model (star schema) presentation layer
- Hourly data loads (max 15-minute latency)
- RBAC, RLS, CLS security implementation
- Azure AD integration with MFA
- SQL performance optimization for Snowflake architecture
- Cost optimization strategies

**Your Capability:** ❌ NO MATCH

- No Snowflake documentation
- SQL Server experience exists (SSIS background)
- Database design experience: STRONG (multiple platforms)
- Security concepts: MODERATE (E-ITS awareness through applications)

**Gap Severity:** CRITICAL - Snowflake is the core platform, requires specialized expertise

#### Modern DataOps Stack (CRITICAL GAP)

**Requirements:**

- **Airflow:** Orchestration, scheduling, monitoring
- **dbt:** SQL-based transformations with automated testing
- **Airbyte:** CDC and data loading from sources
- **CI/CD:** Bitbucket-based deployment pipelines
- **Testing:** Automated data quality and transformation tests

**Your Capability:** ❌ NO MATCH

- Experience: MS SSIS (legacy ETL tool)
- Python: STRONG (could learn Airflow/dbt)
- Version control: Bitbucket documented
- DevOps concepts: MODERATE (not DataOps-specific)

**Gap Severity:** CRITICAL - These are daily-use tools throughout the project

#### Azure Data Lake Architecture (MAJOR GAP)

**Requirements:**

- Azure ADLS Gen2 object storage design
- Apache Iceberg table format
- Data partitioning strategies (time, domain, organization)
- Retention policies and lifecycle management
- Hot/cool/archive storage optimization
- Azure AD authentication and ACLs
- Data encryption (at rest and in transit)

**Your Capability:** ❌ NO MATCH

- Cloud experience: NOT documented
- Azure specifically: NO
- Object storage concepts: NOT demonstrated
- Cost optimization: NOT in cloud context

**Gap Severity:** MAJOR - Core infrastructure component

#### Change Data Capture (MAJOR GAP)

**Requirements:**

- Airbyte CDC setup and configuration
- On-premise to cloud secure networking
- Historical data initial load performance
- Real-time/near-real-time change streaming
- Source system impact assessment
- CDC cluster sizing and optimization
- High availability and fault tolerance

**Your Capability:** ⚠️ PARTIAL MATCH

- Database replication concepts: LIKELY known (DBA background)
- Airbyte specifically: NO
- Network security: MODERATE (IT infrastructure background)
- Performance tuning: DATABASE-LEVEL (not CDC-specific)

**Gap Severity:** MAJOR - Critical for Phase 1 PoC success

#### Data Catalog and Metadata Management (MODERATE GAP)

**Requirements:**

- Automated metadata collection from all layers
- Horizontal data lineage visualization (source → warehouse → BI)
- Vertical lineage (business → technical)
- Column-level lineage through transformations
- Data quality rule definition and testing
- Automated quality monitoring and alerting
- SQL-based quality tests

**Your Capability:** ⚠️ PARTIAL MATCH

- Metadata concepts: MODERATE (database documentation)
- Data quality: MODERATE (data curation at Mälu Instituut)
- Lineage tools: NO experience
- Automation: PYTHON (strong foundation)

**Gap Severity:** MODERATE - Important but learnable with guidance

#### Tableau BI Development (MODERATE GAP)

**Requirements:**

- Advanced dashboard development (15 total: 1 in PoC, 4 in Phase 2, 10 in Phase 3)
- BI style book compliance
- KPI register integration (tooltips, links, metadata)
- Self-service enablement for users
- Training material creation (video tutorials)
- Onboarding documentation

**Your Capability:** ⚠️ PARTIAL MATCH

- Tableau: LIKELY basic use (mentioned in context)
- BI reporting: MODERATE (spreadsheet-based analytics)
- Dashboard design: LIKELY (graphic design background)
- Training delivery: STRONG (taught historians to use MySQL)
- Documentation: STRONG (consistent across projects)

**Gap Severity:** MODERATE - Tableau is teachable, BI concepts understood

### 2. TECHNICAL ENVIRONMENT

#### Core Technologies

| Component | Required | Your Experience | Gap |
|-----------|----------|-----------------|-----|
| Snowflake | Production deployment | None | ❌ CRITICAL |
| Airflow | Orchestration expert | None | ❌ CRITICAL |
| dbt | SQL transformations | None | ❌ CRITICAL |
| Airbyte | CDC implementation | None | ❌ CRITICAL |
| Azure ADLS Gen2 | Data lake design | None | ❌ MAJOR |
| Apache Iceberg | Table format | None | ❌ MAJOR |
| Tableau | Advanced dashboards | Basic/moderate | ⚠️ MODERATE |
| Python | Data processing scripts | 9/10 STRONG | ✅ MATCH |
| SQL | Complex queries | STRONG | ✅ MATCH |
| PostgreSQL/MySQL | Source systems | STRONG | ✅ MATCH |
| Bitbucket | Version control | Known | ✅ MATCH |
| Azure AD | Authentication | Concepts known | ⚠️ PARTIAL |

#### Security and Compliance

**Requirements:**

- E-ITS (Estonian Information Security Standard) compliance
- RBAC, RLS, CLS security models
- Data masking/pseudonymization for sensitive data
- Audit logging (required by E-ITS)
- Multi-factor authentication
- Data encryption standards

**Your Capability:** ⚠️ PARTIAL MATCH

- E-ITS awareness: YES (referenced in applications)
- Security concepts: MODERATE (not specialist)
- Audit logging: DATABASE-LEVEL (not platform-level)
- Compliance: MODERATE understanding

### 3. PROJECT PHASES AND DELIVERABLES

#### Phase 1: PoC (3 months)

**Deliverables:**

- Snowflake environment setup with security
- CDC from one source system to data lake
- Data lake structure and format definition
- Data warehouse dimensional model
- dbt transformations with automated tests
- Airflow orchestration
- Data catalog with lineage
- 1 Tableau dashboard
- Documentation and training for key users
- PoC evaluation and recommendations

**Your Contribution Potential:** LOW (20%)

- Python scripting: STRONG
- SQL transformations: STRONG
- Documentation: STRONG
- Platform-specific work: DEPENDENT on partner

#### Phase 2: Post-PoC Expansion (4 months)

**Deliverables:**

- 4 Tableau dashboards with KPIs
- User training (10 people, 2h each)
- Risk assessment with InfoSec team
- Development pattern documentation
- Naming conventions and access controls
- BI community creation (forum, Teams)
- KPI registry (initial version)
- BI style book
- Data quality and performance evaluation

**Your Contribution Potential:** MODERATE (40%)

- Training delivery: STRONG (historian onboarding success)
- Documentation: STRONG
- BI community: MODERATE (organizational skills)
- Dashboard development: DEPENDENT on Tableau skills

#### Phase 3: Standardization (10 months)

**Deliverables:**

- 10 additional Tableau dashboards (total 15)
- Expanded KPI registry
- Additional source integrations
- Standardized data models
- CI/CD pipeline implementation
- Audit logging system (E-ITS)
- Self-service BI training (20+ users)
- Video training materials
- Onboarding handbooks
- Next phase roadmap

**Your Contribution Potential:** MODERATE-HIGH (50%)

- CI/CD concepts: MODERATE
- Training program: STRONG
- Documentation: STRONG
- Process standardization: MODERATE
- Platform work: STILL DEPENDENT on partner

---

## YOUR ROLE OPTIONS

### Option 1: Strategic Skip (Recommended if Solo)

**Rationale:**

- Technology stack gap too large for 3-month PoC timeline
- Snowflake + dbt + Airflow + Airbyte learning curve: 6-12 months to proficiency
- PoC failure would damage reputation with major healthcare provider
- Healthcare domain expertise not demonstrated
- Better to pursue procurements matching your core strengths

**When to Skip:**

- Cannot secure Snowflake-certified partner quickly
- No budget for 2-3 FTE data engineering specialists
- Risk appetite low (PoC evaluation is make-or-break)

### Option 2: Partner with Data Engineering Firm (25% RECOMMEND)

**Your Role:** Technical Project Manager + Database/Python Specialist

**Responsibilities:**

- Project coordination and stakeholder management
- Database design consultation (leveraging your SQL expertise)
- Python scripting for custom integrations
- Documentation and training delivery
- Quality assurance and testing support
- PERH relationship management

**Partner Requirements:**

- Snowflake certified consultancy
- Proven dbt + Airflow implementations
- Azure data platform experience (ADLS Gen2)
- Healthcare or large enterprise project portfolio
- 3-5 FTE team capacity

**Your Value Proposition:**

- Strong Python (automation, custom tools)
- Database architecture experience (multiple platforms)
- Training and onboarding expertise
- Local market knowledge
- Cost-effective compared to full consulting rates

**Win Probability:** 20-30% (competitive market, price-based evaluation)

**Risk:** Partner relationship quality, task ownership clarity, revenue share negotiation

### Option 3: Team Assembly as Prime Contractor (NOT RECOMMENDED)

**Required Team:**

1. **Snowflake Architect** (1 FTE): Core platform design
2. **Data Engineer - dbt/Airflow** (1-2 FTE): DataOps implementation
3. **Azure Data Platform Engineer** (1 FTE): ADLS Gen2, Iceberg
4. **BI Developer - Tableau** (1 FTE): Dashboard development
5. **You - Technical PM** (0.5-0.75 FTE): Coordination, documentation, training

**Why Not Recommended:**

- Hiring/contracting: 4-5 specialists in ≤1 month before PoC start
- Knowledge transfer overhead: No existing team culture
- Financial risk: Prime contractor liability
- Management complexity: Coordinating specialists in unfamiliar tech stack
- Competitive disadvantage: Established consultancies have ready teams

**Win Probability:** 5-10% (too many moving parts)

### Option 4: Participate in Market Research Only (STRATEGIC)

**Action:** Submit thoughtful responses to the 6 market research questions

**Value:**

- Demonstrate analytical capability
- Build relationship with PERH procurement team
- Influence final specification (could add requirements matching your strengths)
- Assess competition (who else responds?)
- Learn more about procurer's expectations
- No commitment beyond time investment (2-4 hours)

**Risk:** Low (minimal time, potential insight gain)

**Recommendation:** YES - Do this regardless of participation decision

---

## COMPETITIVE ANALYSIS

### Market Landscape

**Likely Competitors:**

1. **Snowflake-certified consultancies** (e.g., Elisa, Telia, Proekspert, Nordic consulting firms)
2. **Big 4 consulting** (Deloitte, PwC, EY, KPMG) with data platform practices
3. **Specialized data engineering firms** with healthcare portfolio
4. **Estonian IT companies** with cloud data practice (Nortal, Helmes, Playtech)

### Your Competitive Advantages

1. **Local Market Knowledge:** Estonian language, E-ITS familiarity
2. **Healthcare Sector Proximity:** Can quickly understand PERH context
3. **Training and Onboarding Strengths:** Proven ability to teach technical concepts (historians → MySQL)
4. **Cost-Effectiveness:** Lower rates than Big 4 or Nordic consultancies
5. **Python Expertise:** Custom tools, integration scripts, automation
6. **Database Architecture:** Multi-platform experience, design patterns

### Your Competitive Disadvantages

1. **No Snowflake Portfolio:** Cannot show healthcare data warehouse references
2. **No DataOps Tooling:** Competitors have years of dbt/Airflow projects
3. **Solo/Small Team:** Cannot mobilize 5-person team quickly
4. **No Azure Credentials:** Competitors have Microsoft partnerships
5. **No Healthcare Domain:** Competitors may have EMR integration experience
6. **No Data Catalog Tools:** Competitors know Alation, Collibra, etc.

### Realistic Winning Probability

**Scenario: Partner with Data Engineering Firm**

- Base probability: 40% (assuming capable partner)
- Snowflake gap discount: -10% (partner must be VERY strong)
- Price-based evaluation: -10% (competing against established firms)
- Healthcare domain: -5% (no prior references)
- Training/documentation strengths: +5%

**Result:** 20-30% chance

**Scenario: Prime Contractor with Team**

- Base probability: 20%
- Team assembly risk: -10%
- PoC failure risk: -5%

**Result:** 5-10% chance

---

## COST-BENEFIT ANALYSIS

### Time Investment Estimate

**Market Research Phase:**

- Read technical specification: 2-3 hours
- Research Snowflake/dbt/Airflow ecosystem: 4-8 hours
- Prepare market research responses: 2-4 hours
- **Subtotal:** 8-15 hours

**Bid Preparation (if proceeding):**

- Partner identification and negotiation: 20-40 hours
- Technical proposal writing: 20-30 hours
- Pricing model development: 10-15 hours
- Presentations/clarifications: 5-10 hours
- **Subtotal:** 55-95 hours

**Total Investment:** 63-110 hours (1.5-2.5 weeks full-time)

### Financial Parameters

**Contract Value (Estimated):**

- Based on scope: €300,000 - €600,000 total (3 phases)
- Market research question: "What would be expected cost?"
- Your share (if partner): 20-30% = €60,000 - €180,000

**Break-Even Analysis:**

- Bid prep cost (110 hours × €50/hour): €5,500
- Win probability (partner scenario): 25%
- Expected value: €180,000 × 0.25 = €45,000
- ROI: (€45,000 - €5,500) / €5,500 = 7x (POSITIVE if partner is strong)

**Risk Factors:**

- Partner relationship: Could fail during delivery
- PoC evaluation: Pass/fail gate at 3 months
- Price pressure: Lowest cost wins (margin compression)
- Timeline overruns: Fixed-price risk

---

## STRATEGIC RECOMMENDATION

### PRIMARY: PARTICIPATE IN MARKET RESEARCH (100%)

**Action Steps:**

1. **Read full technical specification carefully** (2-3 hours)
2. **Research modern data platform ecosystem** (4-8 hours)
   - Snowflake architecture and pricing
   - dbt best practices
   - Airflow vs. alternatives
   - Data catalog tools (Atlan, DataHub, Alation)
3. **Prepare thoughtful market research responses** (2-4 hours)
   - Question 1: Clarity assessment (be constructive, not critical)
   - Question 2: Risks - highlight team assembly, PoC timeline pressure, source system dependencies
   - Question 3: Suggestions - emphasize training/onboarding, documentation standards, knowledge transfer
   - Question 4: Timeline - feasible IF experienced team, tight for learning curve
   - Question 5: Cost estimate - research market rates (don't undercut yourself)
   - Question 6: Code freeze - recommend clear coordination process, testing environments
4. **Submit via RHR platform**
5. **Monitor for formal procurement announcement**

**Value:** Build relationship, influence spec, assess feasibility with minimal commitment

### CONDITIONAL: PURSUE FORMAL BID (25%)

**Conditions to Proceed:**

1. **Partner Secured:** Snowflake-certified firm with proven healthcare/large enterprise portfolio
2. **Clear Role Definition:** Your scope = PM + Python + training + documentation (no Snowflake core work)
3. **Risk Mitigation:** PoC phase structured as separate evaluation gate
4. **Fair Revenue Share:** 20-30% minimum for your contribution
5. **Team Capacity:** You have 50-75% availability for 17 months
6. **Financial Buffer:** Can afford 110 hours bid prep + 3-month risk period

**If ALL conditions met:** Proceed with bid preparation

**If ANY condition fails:** Strategic skip, focus on better-fit procurements

### RECOMMENDED: STRATEGIC SKIP FOR FORMAL BID (75%)

**Reasons to Skip:**

1. **Technology Gap Too Large:** Snowflake + dbt + Airflow + Airbyte = 6-12 months to proficiency
2. **PoC Timeline Pressure:** 3 months is unforgiving for learning curve
3. **Better Opportunities Available:** Seek PostgreSQL/MySQL-centric procurements
4. **Team Assembly Risk:** Cannot mobilize specialists quickly
5. **Reputation Protection:** PERH is major healthcare provider, failure would impact future opportunities

**Better-Fit Procurement Types for You:**

- PostgreSQL/MySQL database migration or optimization
- Python-based system integration projects
- Data quality and ETL for traditional databases
- Training and documentation for existing IT systems
- Custom application development (Python/JavaScript)

---

## NEXT STEPS (Market Research Phase)

### Immediate Actions (Days 1-3)

- [ ] Read "Tehniline kirjeldus.docx" in detail (highlight unclear sections)
- [ ] Research Snowflake architecture basics (understand vocabulary)
- [ ] Research dbt, Airflow, Airbyte (understand workflow)
- [ ] Identify 2-3 potential data engineering partners (Elisa, Proekspert, Helmes)

### Research Phase (Days 4-7)

- [ ] Study data catalog tools (Atlan, DataHub, Alation)
- [ ] Review E-ITS requirements for audit logging and security
- [ ] Research Azure ADLS Gen2 and Iceberg format
- [ ] Calculate realistic cost estimate (€300k-€600k range)

### Market Research Response Preparation (Days 8-10)

- [ ] Draft responses to all 6 questions (constructive, professional tone)
- [ ] Review for clarity and completeness
- [ ] Prepare as PDF or structured document
- [ ] Submit via RHR teabevahetus (information exchange)

### Partnership Exploration (Days 11-14, if pursuing bid)

- [ ] Contact 2-3 Snowflake-certified consultancies
- [ ] Discuss partnership model (subcontractor vs. joint venture)
- [ ] Request their healthcare/data platform references
- [ ] Negotiate revenue share and role boundaries
- [ ] Assess cultural fit and communication style

### Bid Preparation (Days 15-30, if ALL conditions met)

- [ ] Technical proposal writing (with partner)
- [ ] Pricing model development
- [ ] Reference projects compilation
- [ ] Team CVs preparation
- [ ] Risk mitigation plan
- [ ] Training and documentation plan (your strength)

---

## ALTERNATIVE OPPORTUNITIES TO CONSIDER

Instead of this highly specialized cloud data platform project, focus on procurements that leverage your core strengths:

### Strong Match Criteria

1. **PostgreSQL/MySQL-centric projects**
   - Database optimization
   - Migration from legacy systems
   - Performance tuning
   - Backup and recovery strategy

2. **Python integration projects**
   - System integration middleware
   - ETL for traditional databases
   - Data quality automation
   - Custom reporting tools

3. **Data governance and quality**
   - Data cleansing workflows
   - Master data management (MDM)
   - Metadata documentation
   - Data dictionary creation

4. **Training and onboarding**
   - Database user training
   - Developer onboarding programs
   - Documentation standardization
   - Knowledge transfer projects

5. **Small-medium system implementations**
   - CRM/ERP integrations
   - Document management systems
   - Inventory/asset tracking (like Entu)
   - Archival and cataloging systems

### Search Terms for Better-Fit Procurements

- "Andmebaasi" (database)
- "PostgreSQL" or "MySQL"
- "Andmekvaliteet" (data quality)
- "ETL" (not "ELT" or "DataOps")
- "Python arendus" (Python development)
- "Integratsioon" (integration)
- "Koolitus" (training)
- "Dokumenteerimine" (documentation)

---

## CONCLUSION

Procurement 9582704 is a sophisticated cloud data platform implementation requiring specialized Snowflake and modern DataOps expertise that significantly exceeds your current documented capabilities. The technology gap (Snowflake, dbt, Airflow, Airbyte, Azure ADLS) is too large to close within the 3-month PoC timeline.

**RECOMMENDED PATH:**

1. **Participate in market research** (8-15 hours) - builds relationship, influences spec, minimal risk
2. **Monitor for partnership opportunities** - IF strong Snowflake-certified firm approaches you
3. **Focus bid efforts on PostgreSQL/Python/training-centric procurements** - higher win probability, better capability match
4. **Use this as learning opportunity** - understand modern data platform landscape for future positioning

**VALUE DELIVERED BY THIS ASSESSMENT:**

- Saved 55-95 hours of bid preparation on low-probability opportunity
- Identified technology upskilling priorities (Snowflake, dbt, Airflow) for future positioning
- Clarified strategic focus: Traditional databases + Python + training vs. cloud data platforms
- Preserved reputation by avoiding PoC failure risk with major healthcare provider

**PERSONAL NOTE:**

Your strengths (database architecture, Python, training, documentation) are valuable and in-demand. This particular procurement requires bleeding-edge cloud data platform specialization that established consultancies have been building for 3-5 years. Don't force a bad fit. Better to excel in PostgreSQL/Python procurements than struggle with Snowflake/dbt. Market research participation is still worthwhile for relationship-building and ecosystem learning.

Focus your energy on procurements where you can deliver with confidence, not where you'd be learning on the job under 3-month PoC pressure.
