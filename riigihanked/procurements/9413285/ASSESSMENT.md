# Procurement 9413285 Assessment: ATV and RIHAKE Development Framework

**Assessment Date:** 2025-11-27  
**Procurement ID:** 9413285 (latest version: 9609004)  
**Procurer:** Riigi Infosüsteemi Amet (RIA) - State Information System Authority  
**Title:** Andmete teabevärava ja RIHAKEse arendustööd  
**CPV Code:** 72200000-7 (Software programming and consultancy services)  
**Contract Value:** €1,600,000 (excl. VAT)  
**Contract Duration:** 30 months  
**Submission Deadline:** 2026-01-14 13:00 (48 days remaining)  
**Evaluation:** Mixed - 40% Quality (test work), 40% Team experience, 20% Price

---

## Executive Summary

**RECOMMENDATION: CHALLENGING - CONSIDER**

**Feasibility:** 40-55% (significant technology gaps, strong team assembly challenge)

**Winning Probability:** 20-35% (competitive field, critical DevOps/Java gaps)

**Key Decision:** This is a framework agreement for maintaining RIA's Data Portal (ATV) and data management tool (RIHAKE). You have VERIFIED Java/Spring Boot experience (EKI 2017-2018) and PostgreSQL expertise, but CRITICAL gaps in modern Java ecosystem (Java 21, NestJS, Docker/Kubernetes), X-Road integration, and TARA authentication. 48-day timeline allows team assembly BUT test work quality scoring (40% weight) heavily favors teams with current ATV/RIHAKE familiarity.

**Critical Match:**

- Java + Spring Boot experience VERIFIED (EKI EKILEX 2017-2018, employment contract)
- PostgreSQL database expertise documented
- JavaScript 9/10 proficiency (Angular learnable, similar to React)
- 15+ years development/PM/architect experience
- Native Estonian language (excellent for RIA collaboration)
- System architecture core documented skill

**Critical Gaps:**

- Java currency: Last hands-on 2017-2018 (8-year gap), need refresh to Java 21 + Spring Boot 3.x
- NestJS: NOT documented (TypeScript Node.js framework, alternative platform requirement)
- Docker/Kubernetes: NOT documented (MANDATORY for architect role)
- X-Road integration: NOT documented (MANDATORY for both developer and architect roles)
- TARA/GovSSO authentication: NOT documented (MANDATORY for architect role)
- Hazelcast/Ignite: NOT documented (required for architect)
- Microservices architecture: NOT explicitly documented at production scale
- Security vulnerability management: NOT documented as formal practice
- Team assembly: Need 5-6 specialists in 48 days (tight but feasible)

---

## Project Scope

### Systems Overview

**Andmete teabevärav (ATV) - Data Information Gateway:**

- Public portal providing overview of government-managed data
- Aggregates descriptions from institutional RIHAKE instances
- Enables data reuse discovery
- URL: https://avaandmed.eesti.ee/
- Public code: https://koodivaramu.eesti.ee/andmete-teabevarav

**RIHAKE - Data Management Application:**

- Institution-internal data management tool
- Describes datasets per Data Description Standard
- Creates data and business vocabularies
- Transmits descriptions to ATV via API
- Each institution has own RIHAKE instance

### Contract Scope

Framework agreement for continuing development of ATV and RIHAKE components:

- Pre-analysis and consultation for new features
- Development of new functionalities and integrations
- Enhancement of existing features
- System sustainability maintenance
- Code, documentation, and guide material updates
- Testing and consulting

**Key Deliverables:**

- New component creation (with pre-analysis)
- Feature enhancements based on legislation and user needs
- Usability improvements
- Bug fixes and security patches
- Updated documentation (RIA Confluence)
- Code published to public repositories

### Work Organization

- Agile development (sprints, likely 2-week cycles)
- Weekly planning meetings (MS Teams)
- Task management in JIRA
- Code reviews (team-internal)
- Continuous integration (Jenkins)
- Git-based version control (public repositories)
- Collaboration with RIA's development partners
- RIA may make direct code changes (with agreement)

### Technology Stack

**RIHAKE Components:**

- **Frontend:** Angular, rihake-fe (user interface, Nginx server)
- **Backend:** Java Spring, rihake-be
- **Authentication:** Keycloak SSO server (TARA integration)
- **Database:** PostgreSQL Patroni cluster (isolated databases)

**ATV Stack (inferred from RIHAKE integration):**

- API-based architecture
- Receives JSON from RIHAKE instances
- Public search interface
- Organization representative role management

**Development Infrastructure:**

- Supplier's own dev/test environment
- RIA's continuous integration environment (Jenkins)
- Code repository: Public (Koodivaramu/GitHub)
- Documentation: RIA Confluence
- Task tracking: JIRA

**Required Technology Competencies (across team):**

- Java, Angular, JavaScript, PostgreSQL
- NPM, Jenkins (or similar CI)
- X-Road integration and service development
- Docker, Kubernetes, Hazelcast/Ignite
- React, Python, Maven, Gradle
- Public code repository publishing
- Security vulnerability management

---

## Requirements Analysis

### Mandatory Team Composition (8 roles, 1.3-1.5 FTE)

#### Role 1: Project Manager (Projektijuht)

**Requirements:**

- 24+ months experience as software development project manager
- Participated as PM in 1+ info system creation/modification project (within last 60 months)
- Project minimum: 2000 hours total, PM worked 100+ hours

**YOUR FIT:** STRONG MATCH

- 15+ years IT project management (exceeds 24 months)
- PÖFF (2021-2024): 4-member development team leadership (within 60 months)
- EKA (2009-2012): University-scale projects (700+ users)
- Justice Ministry (2002-2005): Government systems
- **GAP:** Need to calculate and document 2000+ hour projects

**Estonian Language:** Native speaker, exceeds C1 requirement

---

#### Role 2: System Analyst (Analüütik)

**Requirements:**

- 36+ months experience as system analyst
- Participated as analyst in 2+ info system projects (within last 60 months)
- Projects must implement specific functionality (see below)
- One project minimum: 3500 hours total, analyst worked 300+ hours

**Functionality Requirements (both projects must have ALL three):**

1. User interface based on different user roles and query system
2. Electronic message formation and sending
3. Electronic message reception, validation, and storage

**YOUR FIT:** PARTIAL MATCH

- Analyst experience: Documented (Entu deployments, requirements gathering)
- **STRONG:** Role-based interfaces (Entu platform, multiple roles)
- **WEAK:** Electronic message formation/sending NOT explicitly documented
- **GAP:** Electronic message reception/validation NOT documented
- **GAP:** 3500-hour project with 300+ analyst hours NOT documented

**YOUR STATUS:** CAN POTENTIALLY COVER with project hour documentation, but electronic messaging functionality is questionable

---

#### Role 3: Developers (Arendajad) - 3 positions

**Requirements (each developer):**

- 36+ months programming experience
- Participated in 2+ info system projects (within last 60 months)
- At least one project: 3500 hours total, developer worked 500+ hours, developed on supported platform (Java OR NestJS), uses relational database, runs in high-availability/clustered mode

**Mandatory Technology Experience:**

- Java
- Angular
- JavaScript
- PostgreSQL
- NPM
- Jenkins (or similar CI)
- X-Road integration and/or service development
- Publishing software to public code repositories
- Security vulnerability management experience

**YOUR FIT (for 1 developer position):** PARTIAL MATCH

- Programming: 15+ years (exceeds 36 months)
- **STRONG:** JavaScript 9/10, PostgreSQL documented
- **PARTIAL:** Java 7/10 (EKI 2017-2018, but 8-year gap)
- **WEAK:** Angular NOT documented (have React, learnable)
- **GAP:** X-Road integration NOT documented (CRITICAL)
- **GAP:** High-availability/clustered mode development NOT documented
- **GAP:** Security vulnerability management NOT formal practice
- **GAP:** Public code repository publishing NOT documented
- **GAP:** NPM, Jenkins NOT documented

**YOUR STATUS:** Can cover 1 developer role IF Java refreshed and X-Road trained, but need 2 additional developers

---

#### Role 4: Architect (Arhitekt)

**Requirements:**

- **EITHER:** 60+ months as info system architect
- **OR:** 24+ months as senior developer AND 36+ months as architect
- Participated as architect in 2+ info system projects (within last 60 months)
- Projects must implement X-Road functionality (see below)
- At least one project: 4500 hours total, architect worked 500+ hours, developed on supported platform (Java OR NestJS), uses relational database, runs in high-availability cluster

**Functionality Requirements (both projects must have ALL three):**

1. X-Road service usage and creation
2. Microservices-based architecture usage, machine interface creation
3. TARA and/or GovSSO integration

**Mandatory Technology Experience:**

- Docker
- Kubernetes
- Hazelcast OR Ignite (distributed caching/computing)
- Security vulnerability management

**YOUR FIT:** WEAK MATCH

- **STRONG:** 15+ years architect experience (Entusiastid OÜ title: "Architect/Analyst/Developer")
- **STRONG:** System architecture documented core skill
- **STRONG:** Entu platform: Architected from scratch
- **STRONG:** PostgreSQL relational database
- **GAP:** X-Road service usage/creation NOT documented (CRITICAL BLOCKER)
- **GAP:** Microservices architecture NOT explicitly documented at production scale
- **GAP:** TARA/GovSSO integration NOT documented (CRITICAL BLOCKER)
- **GAP:** Docker NOT documented
- **GAP:** Kubernetes NOT documented (CRITICAL for architect role)
- **GAP:** Hazelcast/Ignite NOT documented
- **GAP:** High-availability cluster development NOT documented
- **GAP:** 4500-hour project with 500+ architect hours NOT documented

**YOUR STATUS:** CANNOT fulfill architect role without X-Road, TARA/GovSSO, and Kubernetes experience. These are MANDATORY functional requirements.

---

#### Role 5: Tester (Testija)

**Requirements:**

- 24+ months experience as info system tester
- Participated in 2+ info system projects (within last 60 months)
- At least one project: 2000 hours total, tester worked 200+ hours
- Basic-level security vulnerability detection and testing experience (testing fixes after security testing)

**YOUR FIT:** UNCLEAR

- Testing mentioned in various projects
- NOT documented as dedicated 24-month tester role
- Security testing NOT documented

**YOUR STATUS:** NEED DEDICATED TESTER (cannot cover)

---

#### Role 6: Usability Expert (Kasutatavuse ekspert)

**Requirements:**

- 24+ months experience as info system usability expert
- Participated in 1+ info system project (within last 60 months)
- Project minimum: 2000 hours total, usability expert worked 100+ hours

**YOUR FIT:** WEAK

- UX/UI experience: Graphic design background (1993-2010)
- **GAP:** NOT documented as modern usability expert (user testing, accessibility, interaction design)
- **GAP:** 2000-hour project as usability expert NOT documented

**YOUR STATUS:** NEED DEDICATED USABILITY EXPERT (cannot cover)

---

### Team Technology Coverage (Collective Requirements)

**Developers + Architect must collectively have experience with:**

- React (in addition to Angular/Java/JavaScript/PostgreSQL/etc.)
- Python
- Maven
- Gradle

**YOUR FIT:**

- React: Documented (JavaScript 9/10 includes modern frameworks)
- Python: 9/10 proficiency (STRONG)
- Maven: NOT documented (Java build tool)
- Gradle: NOT documented (Java/Kotlin build tool)

**YOUR STATUS:** Python + React covered, Maven/Gradle learnable (standard Java tools)

---

### Role Overlap Rules

**ALLOWED:**

- PM + Analyst (same person can cover both)
- PM + Tester (same person can cover both)

**NOT ALLOWED:**

- Any other role combinations
- Parallel role coverage beyond PM+Analyst or PM+Tester

**YOUR VIABLE ROLE OPTIONS:**

1. PM only (STRONG MATCH)
2. PM + Analyst (PARTIAL MATCH, electronic messaging gap)
3. Developer (PARTIAL MATCH, X-Road gap)

**Cannot realistically cover:** Architect (X-Road/TARA/Kubernetes MANDATORY), Tester, Usability Expert

---

## Capability Matching

### Strong Matches

**1. Project Management (STRONG)**

- 15+ years PM experience (PÖFF 2021-2024, EKA 2009-2012, Justice 2002-2005)
- Team leadership: 4-member team at PÖFF
- Government sector experience: Justice Ministry
- Stakeholder management: 30+ Entu deployments
- Estonian native: Excellent for RIA collaboration

**2. PostgreSQL Expertise (STRONG)**

- Documented database management (Entu platform, Eesti Mälu Instituut)
- Relational database design
- Large-scale data (700+ users at EKA)

**3. JavaScript/Frontend Development (STRONG)**

- JavaScript 9/10 proficiency
- Modern frameworks: React documented
- Angular learnable (similar architecture to React)
- 15+ years web development

**4. System Architecture (STRONG)**

- Core documented skill
- Entu platform: Architected from scratch
- PÖFF: Technical architecture
- 15+ years system design

**5. Python Development (STRONG)**

- 9/10 proficiency (bonus team requirement)
- 15+ years experience
- Full-stack capability

---

### Gaps Requiring Mitigation

**1. X-Road Integration (CRITICAL BLOCKER)**

- NOT documented in knowledge base
- Mandatory for developer role (service usage/creation)
- Mandatory for architect role (both projects must demonstrate X-Road)
- Estonian government systems foundational requirement
- **Impact:** Cannot fulfill architect role, weak developer role
- **Mitigation:** X-Road training + demo project (6-12 months), OR partner with X-Road specialist

**2. TARA/GovSSO Authentication (CRITICAL BLOCKER)**

- NOT documented
- Mandatory for architect role (both projects must demonstrate)
- National eID service integration
- **Impact:** Cannot fulfill architect role
- **Mitigation:** TARA integration training (2-4 weeks), OR partner with auth specialist

**3. Java/Spring Boot Currency (MAJOR GAP)**

- Last hands-on: 2017-2018 (8 years ago)
- Need refresh to Java 21, Spring Boot 3.x ecosystem
- Proficiency 7/10 (not 9/10 needed for competitive edge)
- **Impact:** Weak developer position, cannot lead Java development
- **Mitigation:** Java refresher course (4-8 weeks), OR partner with current Java developer

**4. Docker/Kubernetes (MAJOR GAP)**

- NOT documented
- Mandatory for architect role
- Required for modern cloud-native development
- **Impact:** Cannot fulfill architect role, weak modern development credibility
- **Mitigation:** Docker/K8s hands-on training (4-8 weeks), OR partner with DevOps specialist

**5. Microservices Architecture (MODERATE GAP)**

- NOT explicitly documented at production scale
- Architect role requires demonstrating microservices usage
- **Impact:** Cannot prove architect functional requirement
- **Mitigation:** Document if Entu has microservices, OR partner with microservices architect

**6. NestJS (MODERATE GAP)**

- NOT documented (TypeScript Node.js framework)
- Alternative to Java for "supported platform" requirement
- Could compensate for Java gap
- **Impact:** Cannot use NestJS path as Java alternative
- **Mitigation:** Learn NestJS (2-4 weeks for JavaScript 9/10 developer), OR focus on Java path

**7. Security Vulnerability Management (MODERATE GAP)**

- NOT documented as formal practice
- Mandatory for developer and architect roles
- **Impact:** Cannot demonstrate security hygiene process
- **Mitigation:** Implement OWASP practices, document security testing workflow

**8. Team Assembly (MAJOR CHALLENGE)**

**Need to hire/partner:**

- 2-3 additional developers (36+ months experience, X-Road, Java/Angular)
- 1 architect (IF not covering yourself, 60+ months experience, X-Road/TARA/Docker/K8s)
- 1 tester (24+ months, security testing)
- 1 usability expert (24+ months)

**Total:** 5-6 specialists in 48 days

**Timeline:** 48 days allows recruitment (30-45 days feasible), but quality matters

---

## Strategic Assessment

### Competitive Landscape

**Likely Competitors:**

1. **Current ATV/RIHAKE maintainers:**
   - Companies already working on these systems
   - **Advantage:** Deep system knowledge, test work (40% weight) heavily favors them
   - **Advantage:** Existing team, proven track record, RIA relationship

2. **Established Government IT Contractors:**
   - Trinidad Wiseman, Nortal, CGI, Webmedia, Helmes
   - **Advantage:** X-Road experience portfolio, TARA integrations, Docker/K8s standard
   - **Advantage:** Large teams with specialist depth

3. **RIA-Focused Contractors:**
   - Companies specializing in RIA projects
   - **Advantage:** RIA process familiarity, Jenkins CI experience, Koodivaramu publishing

**Your Competitive Position:**

- **Strengths:** Native Estonian, government experience, PostgreSQL/JavaScript strong, PM credibility
- **Weaknesses:** X-Road gap, Java currency, Docker/K8s gap, team assembly from scratch
- **Test work disadvantage:** 40% weight on test work quality favors teams with ATV/RIHAKE exposure
- **Price competitiveness:** Only 20% weight, cannot win on price alone

**Market Reality:**

- Framework agreements for established systems favor continuity
- Test work (40% weight) = incumbents have structural advantage
- RIA likely prefers proven partners
- 48 days allows team assembly BUT test work quality matters MORE than team CVs (40% vs 40% weight)

**Estimated Market Position:** Bottom half (5th-10th out of 10-15 bidders)

---

### Participation Options

**Option 1: Lead as PM, Partner for Architect/DevOps (30-40% feasible)**

**What you bring:**

- Project Manager: 15+ years, native Estonian, government experience
- Potentially Analyst role (IF electronic messaging documented/stretched)
- Potentially 1 Developer role (IF Java refreshed + X-Road trained)

**What you need:**

- **CRITICAL:** Architect with X-Road/TARA/Docker/Kubernetes (60+ months experience)
- **CRITICAL:** 2 additional Java/Angular developers with X-Road
- Tester with security testing (24+ months)
- Usability expert (24+ months)
- Total: 5 specialists in 48 days

**Test work strategy:**

- Architect leads technical approach
- Your PM role: Realistic planning, resource allocation
- Developer input: ATV/RIHAKE architecture analysis from public repos
- **RISK:** No ATV/RIHAKE familiarity = lower test work score (40% weight)

**Viability:** 30-40% FEASIBLE

- 48 days allows partnership negotiations
- But finding architect with ALL mandatory competencies (X-Road, TARA, Docker, K8s, Hazelcast, microservices) is challenging
- Test work quality unknown without system exposure

---

**Option 2: Join as Subcontractor (20-30% feasible)**

**Approach:**

- Contact current ATV/RIHAKE maintainers or RIA-focused contractors
- Offer PM or developer capacity
- Accept subcontractor rates (30-40% lower)

**Your value proposition:**

- Native Estonian PM with government experience
- PostgreSQL expertise (if they lack DBA)
- Python capability (bonus team requirement)

**Viability:** 20-30% FEASIBLE

**Why low:**

- Established contractors likely have full teams
- Framework agreements favor prime contractors
- 48 days insufficient for subcontractor negotiations + their bid prep
- Limited unique value (they have PMs, developers, X-Road specialists)

---

**Option 3: SKIP - Focus on Better-Fit Procurements (RECOMMENDED)**

**Rationale:**

1. **CRITICAL BLOCKERS:**
   - X-Road integration NOT documented (mandatory for architect + developer)
   - TARA/GovSSO NOT documented (mandatory for architect)
   - Docker/Kubernetes NOT documented (mandatory for architect)
   - Microservices production experience NOT documented (mandatory for architect)

2. **STRUCTURAL DISADVANTAGE:**
   - Test work quality = 40% of score (favors incumbents with ATV/RIHAKE exposure)
   - Team experience = 40% of score (need high-hour specialists)
   - Price = only 20% of score (cannot win on price)

3. **TEAM ASSEMBLY CHALLENGE:**
   - Need 5-6 specialists in 48 days
   - Architect with X-Road+TARA+K8s+Hazelcast is rare profile
   - Quality matters more than quantity (experience hour scoring)

4. **COMPETITIVE REALITY:**
   - Incumbents have test work advantage
   - Established contractors have X-Road portfolios
   - Your gaps = bottom-half positioning

5. **OPPORTUNITY COST:**
   - 48 days = significant bid prep time
   - 30-month framework = long commitment
   - Better procurements likely available (Python-focused, single-system, new development)

**Better alternatives:**

- Procurement 9488324 (next in queue): Assess Python/JavaScript fit
- Target Python-based government systems (your 9/10 strength)
- Build X-Road portfolio first (6-12 month investment), THEN target RIA/government frameworks
- Focus on new system development (not maintenance of established systems)

---

## Cost-Benefit Analysis

### Bid Preparation Estimate (if proceeding)

**Effort Hours:**

- X-Road research and demo project prep: 40-60 hours
- Public repo analysis (ATV/RIHAKE architecture): 20-30 hours
- Team recruitment (5-6 specialists): 60-80 hours (interviews, negotiations)
- Test work preparation (schedule + implementation plan): 30-40 hours
- CV compilation and project hour documentation: 20-30 hours
- Proposal writing and pricing: 15-25 hours

**Total:** 185-265 hours (5-7 weeks full-time equivalent)

**Problem:** Only 48 days available (6.8 weeks), tight for quality execution

---

### Financial Analysis

**Contract Value:** €1,600,000 over 30 months

**Framework structure:** No volume guarantee, call-off based

**Revenue Uncertainty:**

- Framework ≠ guaranteed work
- Depends on RIA's needs and your team availability
- Incumbents may continue dominating call-offs

**Team Cost Estimate (assuming 40% framework utilization):**

- 8 team members × €5,000/month avg × 30 months × 40% = €480,000
- Project management overhead: €100,000
- Infrastructure (dev environments, tools): €20,000
- Training (X-Road, TARA, security): €30,000
- **Total 30-month cost:** €630,000

**Revenue requirement:** >€800,000 to be profitable

**Risk factors:**

- No volume guarantee
- Test work quality determines call-off preference
- Incumbent advantage = you may get 20-30% of work even if winning framework
- Team idle time = cost without revenue

**Financial Viability:** MODERATE RISK (framework structure + incumbent advantage)

---

### Win Probability Factors

**Positive Factors:**

- Native Estonian (+5%)
- PostgreSQL expertise (+5%)
- Government experience (+5%)
- 15+ years PM/architect (+5%)
- Python capability (bonus requirement) (+5%)

**Negative Factors:**

- X-Road NOT documented (-15%)
- TARA/GovSSO NOT documented (-10%)
- Docker/Kubernetes NOT documented (-10%)
- No ATV/RIHAKE familiarity (-10%)
- Java 8-year gap (-5%)
- Team from scratch (-10%)

**Net Probability:** 20-35% (low-moderate)

**Breakeven threshold:** Need top 3 finish to make financial sense

**Reality:** Likely 5th-10th place finish = UNPROFITABLE even if selected for framework

---

## Recommendation

**CHALLENGING - CONSIDER (but leaning toward SKIP)**

### Proceed IF ALL Conditions Met:

1. **X-Road specialist partnership secured** (architect with X-Road, TARA, Docker, K8s, Hazelcast, microservices experience, 60+ months portfolio)
2. **2-3 Java/Angular developers recruited** (36+ months, X-Road experience, available immediately)
3. **Tester + Usability Expert hired** (24+ months each, available immediately)
4. **Test work strategy viable** (team can produce quality schedule + plan without ATV/RIHAKE access)
5. **Java refresher completed OR positioned as PM only** (clear on which role you're covering)
6. **Financial model viable** (confident framework will provide 40%+ utilization)
7. **Timeline realistic** (confident 48 days sufficient for team assembly + quality test work)

### Skip IF ANY Condition Fails:

1. **Cannot find X-Road+TARA+K8s architect** in 30 days (CRITICAL: architect is keystone role)
2. **Cannot recruit 2+ Java/Angular developers** with X-Road in 30 days
3. **Test work quality uncertain** without ATV/RIHAKE exposure (40% score weight)
4. **Java refresh incomplete** AND cannot position as PM-only
5. **Better procurement emerges** (Python-focused, new development, single-system)
6. **Timeline stress** (bid quality compromised by 48-day rush)
7. **Financial model weak** (framework utilization <40% likely)

---

## Next Steps (If Proceeding - 48-day timeline)

### Week 1 (Days 1-7): Critical Validation

**Days 1-2: Architecture Role Decision**

- [ ] Research X-Road architect availability (LinkedIn, Meetups, forums)
- [ ] Contact 5-7 potential architect partners
- [ ] Qualify: X-Road portfolio (show 2+ projects), TARA integration, Docker/K8s production, Hazelcast/Ignite
- [ ] IF no architect by Day 7 → **ABORT** (keystone role, cannot proceed without)

**Days 3-4: Java Currency Assessment**

- [ ] Take Java 21 + Spring Boot 3.x crash course (Udemy, Pluralsight)
- [ ] Review modern Java ecosystem (Maven, Gradle, JUnit 5, jOOQ)
- [ ] Decision: Position as Developer OR PM-only
- [ ] IF Developer: Commit to 4-week Java refresh + X-Road training

**Days 5-7: Project Hour Documentation**

- [ ] Calculate Entu platform hours (15 years × estimate hours/month)
- [ ] Calculate PÖFF hours (3 years development lead)
- [ ] Document 2000+ hour projects for PM role
- [ ] Document 3500+ hour projects for Analyst/Developer roles (if covering)
- [ ] Verify high-availability/clustered mode for developer requirement

---

### Week 2-3 (Days 8-21): Team Assembly

**Days 8-14: Developer Recruitment**

- [ ] Post jobs: "Java/Angular Developer - X-Road Integration (RIA Framework)"
- [ ] Target: 2-3 candidates with 36+ months, X-Road, Java/Angular/PostgreSQL
- [ ] Interview focus: X-Road projects (show portfolio), high-availability systems
- [ ] Verify: Public code repository publishing experience
- [ ] Secure commitments by Day 21

**Days 8-14: Specialist Recruitment (parallel)**

- [ ] Post jobs: "Software Tester - Security Testing" (24+ months, 2000-hour projects)
- [ ] Post jobs: "Usability Expert - Info Systems" (24+ months, 2000-hour projects)
- [ ] Interview 3-5 candidates each
- [ ] Verify: Project portfolios, hour documentation
- [ ] Secure commitments by Day 21

**Days 15-21: Team Configuration**

- [ ] Finalize role assignments (who covers PM, Analyst, 3× Developer, Architect, Tester, UX)
- [ ] Ensure no illegal role overlaps (only PM+Analyst or PM+Tester allowed)
- [ ] Collect all CVs using official CV-vorm.docx template
- [ ] Verify ALL mandatory competencies covered (Java, Angular, JavaScript, PostgreSQL, NPM, Jenkins, X-Road, Docker, K8s, Hazelcast, React, Python, Maven, Gradle)

---

### Week 4-5 (Days 22-35): Test Work Preparation

**Days 22-28: ATV/RIHAKE Architecture Analysis**

- [ ] Clone public repos: https://koodivaramu.eesti.ee/andmete-teabevarav
- [ ] Review rihake-fe (Angular), rihake-be (Java Spring), rihake-sso (Keycloak)
- [ ] Analyze API documentation: https://andmed.eesti.ee/api/dataset-docs
- [ ] Review Andmekirjelduse Standard v3.0 (data description standard)
- [ ] Map 10 test work tasks to ATV/RIHAKE architecture

**Days 29-35: Schedule + Implementation Plan Development**

- [ ] Create realistic Gantt chart for €600k test work scope
- [ ] Break down 10 tasks: analysis, development, testing, documentation hours
- [ ] Assign roles to tasks (who does what, overlaps, dependencies)
- [ ] Include buffers, holidays, analysis phases, security vulnerability management
- [ ] Write implementation plan: quality measures, tools, CI/CD, security, collaboration with RIA partners
- [ ] Review test work scoring criteria: formatting (4p), comprehensiveness (9p), realism (9p+9p+9p)
- [ ] Target: 30+ out of 40 points (need 15+ for viability)

---

### Week 6-7 (Days 36-48): Finalization

**Days 36-42: Pricing Strategy**

- [ ] Calculate hourly rates (development vs maintenance)
- [ ] Balance: Competitive pricing (20% weight) vs sustainable margins
- [ ] Account for: Junior vs senior rates, role-based pricing, framework long-tail risk
- [ ] Verify: Rates align with team assembly costs + 30% margin

**Days 43-46: Proposal Compilation**

- [ ] Complete Estonian-language compliance forms
- [ ] Prepare 8 CVs in official CV-vorm.docx format (ALL in Estonian)
- [ ] Document experience hours (team experience scoring: 40% weight)
- [ ] Calculate additional experience points (2 points per 12 months beyond minimum)
- [ ] Attach test work: Schedule + implementation plan
- [ ] Prepare evidence documents (employment contracts, project confirmations)

**Days 47-48: Final Review & Submission**

- [ ] Review ALL mandatory requirements (vastavustingimused.pdf)
- [ ] Verify: No illegal role overlaps, all technologies covered, Estonian C1 confirmed
- [ ] Check: Test work quality (aim 30+/40 points), team experience (aim 25+/40 points)
- [ ] Submit via e-procurement system
- [ ] **Deadline: 2026-01-14 13:00**

**Critical deadline:** 48 days remaining (6.8 weeks)

---

## Conclusion

This is a **CHALLENGING procurement** with **20-35% win probability** due to critical X-Road/TARA/Kubernetes gaps and structural test work disadvantage (40% weight favors incumbents).

### Why Consider:

- Strong PM credentials (15+ years, native Estonian, government sector)
- PostgreSQL + JavaScript expertise match core requirements
- Java/Spring Boot verified (though 8-year gap)
- Python bonus requirement = competitive edge
- 48 days allows team assembly (barely)
- €1.6M contract = significant revenue opportunity

### Why Skip (Recommended):

- **X-Road integration NOT documented** = cannot cover architect or developer role without training
- **TARA/GovSSO NOT documented** = architect role blocker
- **Docker/Kubernetes NOT documented** = architect role blocker
- **Test work disadvantage** = 40% score weight favors teams with ATV/RIHAKE exposure
- **Team assembly challenge** = 5-6 specialists in 48 days (tight, quality matters)
- **Competitive disadvantage** = likely bottom-half finish (5th-10th place)
- **Opportunity cost** = 185-265 prep hours + 30-month commitment + better procurements available

### Better-Fit Alternative:

- **Procurement 9488324** (next in queue): Assess technology stack
- **Python-focused government systems:** Leverage 9/10 proficiency
- **New system development:** Not maintenance of established systems (incumbents disadvantaged)
- **Single-system procurements:** Less complexity, focused team needs
- **X-Road portfolio building:** 6-12 month investment → unlock government IT market

### Strategic Development:

1. **Build X-Road integration portfolio** (demo project + small contract, 200-500 hours)
2. **Complete Docker/Kubernetes training** (hands-on course, 40-60 hours)
3. **Refresh Java to Java 21 + Spring Boot 3.x** (crash course, 40-60 hours)
4. **Implement TARA authentication** (demo project, 20-40 hours)
5. **Target NEXT RIA framework** (12-24 months future, enter as proven X-Road contractor)

**Final Recommendation:** **SKIP** this procurement, invest 6-12 months building X-Road + modern Java portfolio, target future RIA frameworks from position of strength.

---

**Assessment completed:** 2025-11-27  
**Time invested:** 4 hours  
**Confidence level:** HIGH (clear capability gaps, structural disadvantages identified)
