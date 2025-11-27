# Procurement 9224484 Assessment: RTIP Development Framework

**Procurement ID:** 9224484 (Version 9579426)  
**Reference:** 299277  
**Title:** Riigitöötaja iseteenindusportaali (RTIP) arendus- ja hooldustööd  
**Procurer:** Riigi Tugiteenuste Keskus + Rahandusministeeriumi Infotehnoloogiakeskus  
**Assessed:** 2025-11-27  
**Deadline:** 2026-01-06 11:00 (40 days remaining)  
**Status:** SKIP

---

## RECOMMENDATION: SKIP

**Confidence Level:** HIGH

**Primary Reasons:**

1. **SAP ABAP developer requirement (MANDATORY)** - Zero documented experience, cannot fulfill critical role
2. **€5M framework scale** - Project management credibility gap at this financial magnitude
3. **Java/Spring Boot skills gap** - 7/10 proficiency, 8+ years since last hands-on work, insufficient for €5M delivery
4. **Test assignment complexity** - 70% of score, requires working calendar integration in 40 days
5. **Competitive field** - 7-10 established government contractors (Nortal, CGI, Helmes) with RTIP experience

**Bottom Line:** This procurement targets large IT service companies with dedicated SAP teams, current Java/Spring Boot expertise, and €5M+ government framework experience. Attempting to bid would require:

- Assembling 7-person team including SAP ABAP developer (3-4 weeks)
- Refreshing Java/Spring Boot skills to production level (4-6 weeks)
- Completing substantial test assignment (40+ hours)
- Competing against established RTIP contractors with insider knowledge

**Time investment (80-120 hours) vs. success probability (5-15%) makes this non-viable.**

---

## Executive Summary

### Procurement Overview

**Contract Type:** Framework agreement, single supplier, no mini-competitions  
**Value:** €5,000,000 + VAT  
**Duration:** 48 months OR until max value reached (whichever first)  
**Procedure:** Open (Avatud hankemenetlus)  
**CPV:** 72262000-9 (Software development), 72267000-4 (Software maintenance)  
**Users:** ~45,000 employees from ~200 Estonian government institutions  
**System:** State employee self-service portal for HR processes (vacations, business trips, training, expenditures, assets)

### Evaluation Criteria (100 points)

- **30%** - Hourly rate (price-based, lowest wins)
- **70%** - Test assignment quality (client-evaluated, scored: 70/35/15/1 points)

### Critical Requirements

1. **7-person team MANDATORY:**

   - Project Manager
   - Software Architect
   - Analyst
   - Programmer
   - Tester
   - UI Designer
   - **SAP ABAP Developer** ← CRITICAL GAP

2. **Test Assignment (70% of score):**

   - Build working calendar integration (iCal invites for vacation approvals)
   - Submit: Source code, deployment guide, architecture docs, explanation
   - Must meet ALL 13 technical criteria for full 70 points
   - Deadline: 2026-01-06 11:00 (must request source code by 2025-12-31)

3. **Technical Stack:**

   - Spring Boot 2.5.8, Java 1.8
   - PostgreSQL 16
   - Microservices architecture (20+ services)
   - SAP JCO 3.0.9 integration (HEAVY dependency)
   - TARA, SiGa, X-Road integrations
   - Maven, Tomcat 9, RedHat Linux

4. **Work Model:**
   - Agile development, unified team with client
   - Parallel development (contractor + client teams)
   - Code quality checks (Sonarqube, Trivy) on every delivery
   - Estonian language OR full-time translator required

### Your Profile Match

**STRENGTHS:**

- Estonian native speaker (exceeds requirement)
- 15+ years project management experience
- Java 7/10 proficiency (verified: EKI 2017-2018, Justice Ministry 2002-2005)
- Spring Boot experience (EKI EKILEX project 2017-2018)
- PostgreSQL expertise
- System architecture skills
- Government systems experience (Justice Ministry)

**CRITICAL GAPS:**

- **SAP ABAP development:** NO documented experience (MANDATORY role)
- **Java/Spring Boot currency:** Last hands-on 2017-2018 (8 years ago), proficiency 7/10 insufficient for €5M delivery
- **€5M framework PM credibility:** Project financial scale not documented at required magnitude
- **SAP JCO connector:** Zero experience (system has HEAVY SAP dependency)
- **Microservices at scale:** 20+ services, no documented experience at this complexity
- **Team assembly:** Solo practitioner, would need to recruit 6-7 specialists in 40 days

---

## Procurement Structure

### Contract Scope

**Framework Agreement Model:**

- Single supplier (no mini-competitions)
- Work ordered as either:
  - (a) Hour-based resource allocation
  - (b) Specific deliverable with fixed scope
- Maximum value: €5,000,000 + VAT
- Maximum duration: 48 months from contract signing
- Start date: 2026-02-06 (estimated)

**Work Types:**

1. **Analysis:** System and detailed analysis
2. **Design:** Software solution design
3. **Development:** New features, modifications, bug fixes
4. **Testing:** Test creation, execution, management
5. **Deployment:** Production releases, go-live support
6. **Documentation:** Technical, user, and architecture documentation
7. **Project Management:** Sprint planning, coordination, reporting
8. **Maintenance:** L2/L3 support, performance optimization

### Current RTIP System

**Purpose:** State employee self-service portal for HR processes  
**Users:** ~45,000 employees from ~200 government institutions  
**Functions:**

- Vacations and absences management
- Business trips and training
- Expenditure claims
- Asset management (inventory tracking)

**Architecture:**

- **Monolith (legacy):** Spring Framework 4.3.30, JSP 4.0.1, Java 1.8
- **Microservices (current):** Spring Boot 2.5.8, Java 1.8
  - 8 core modules (HR, Vacations, Business trips, Expenditures, Assets)
  - 10 support modules (Notifications, Assignments, Business rules, Absences, Security, Emails, Event logs, External services, SAP adapter, Mock TARA)
  - 2 background jobs (SAP GUI frontend, SAP Agent backend)
- **Frontend:** JSP 4.0.1 (monolith), Angular 6.1.8 (SAP GUI only)
- **Database:** PostgreSQL 16
- **Server:** Tomcat 9.0.104.0, RedHat Linux
- **Build:** Maven
- **Load Balancer:** Apache HTTP Server + ETCD → future: Haproxy

**Key Integrations:**

- **SAP JCO 3.0.9** (CRITICAL: imports org structures, employees, sends approved data back)
- TARA (authentication)
- SiGa (digital signatures)
- X-Road (address, business, population, education registers)
- SMTP (email notifications)
- Filetransfer (document exchange)

### Test Assignment Requirements

**Problem:** Employees must manually add vacations to calendar  
**Solution:** Auto-send iCal invites when manager approves vacation/absence

**13 Technical Criteria (ALL must be met for 70 points):**

1. Send calendar invite for approved vacation/absence
2. Multi-day vacation as single period (18-22.08.2026 as one block)
3. One invite contains all periods from vacation request
4. Update invites when dates change
5. Send cancellation invites when vacation cancelled
6. Mass approval support (thousands of employees)
7. Send at approval moment (not before)
8. Handle approval failures (digital signature may fail, retry logic needed)
9. Send to employee email in system
10. Title: "Puhkus"/"Puudumine", display: "Out of office"
11. Full-day calendar reservation
12. Timezone-aware (employee location)
13. Calendar sending logged (timestamp, user, action, object)

**Deliverables:**

- **Source code:** Submit via RmIT cloud service (request access by 2026-01-03)
- **Deployment guide:** Independent installation capability
- **Technical documentation:** RmIT architecture standards (component diagram, entity diagram with semantics)
- **Explanation document:** Solution rationale

**Compliance:**

- Must follow RFN-2.9.0 (non-functional requirements)
- Must follow IT-profiil-2.9.0 (IT profile)

**Source Code Access:**

- Request via procurement register with confidentiality form
- Deadline: 2025-12-31 (6 days before bid deadline)
- Requires signed confidentiality agreement from authorized representative

### Team Requirements (7 roles MANDATORY)

**1. Project Manager (Projektijuht):**

- Experience managing development teams
- Stakeholder coordination
- Budget and schedule management
- Agile methodology proficiency

**2. Software Architect (Tarkvaraarhitekt):**

- Architecture documentation per RmIT standards
- Microservices design
- Integration architecture (SAP, TARA, SiGa, X-Road)
- Performance and scalability planning

**3. Analyst (Analüütik):**

- Business analysis capability
- Requirements elicitation
- User story creation
- Acceptance criteria definition

**4. Programmer (Programmeerija):**

- Java 1.8 / Spring Boot 2.5.8
- PostgreSQL
- Maven
- Tomcat
- Estonian language OR translator (client expense)

**5. Tester (Testija):**

- Testing documentation per RmIT standards
- Test automation (Sonarqube, Trivy)
- Integration testing
- Regression testing

**6. UI Designer (Kasutajaliidese disainer):**

- UI design for JSP/Angular system
- RTIP style guide compliance
- Accessibility standards
- User experience optimization

**7. SAP ABAP Developer (SAP ABAP arendaja):** ← **CRITICAL MANDATORY**

- SAP JCO connector expertise
- ABAP programming
- SAP integration patterns
- Data mapping and transformation

**Team Flexibility:**

- One person can fill up to 2 roles IF meeting requirements for both
- Can have more than 7 people, all must meet respective role requirements
- All team members need CV per template, sertificates, consent forms

### Compliance Requirements

**ESPD (European Single Procurement Document):**

- No criminal convictions (organized crime, corruption, fraud, terrorism, money laundering)
- No tax/social security debt
- Not bankrupt or in liquidation
- Self-cleaning possible for some exclusion grounds

**Operational Requirements:**

- Accept all terms in procurement documents
- Request RTIP source code with confidentiality form (by 2025-12-31)
- Submit test assignment via RmIT cloud (request access by 2026-01-03)
- Submit team CVs per template
- No Russian subcontractors >10% (EU sanctions compliance)
- Environmental commitment (digital materials, minimal printing, eco-labels)

**Source Code Access Process:**

1. Submit request via procurement register
2. Attach signed confidentiality form (299277_Konfidentsiaalsuskohustuse_vorm)
3. Wait 3 days for RmIT approval
4. Receive access credentials via encrypted email
5. Download source code (before 2026-01-06 11:00)

---

## Capability Matching

### STRONG MATCHES

**1. Estonian Language (Native)**

- Native speaker (exceeds requirement)
- No translator needed (cost advantage)
- Direct communication with RTK/RmIT stakeholders

**2. Project Management Experience**

- 15+ years documented experience
- PÖFF Development Lead (2021-2024): 4-member team
- EKA IT Head (2009-2012): 700+ users, large-scale projects
- Justice Ministry (2002-2005): Government systems
- Entusiastid OÜ (2010-present): 30+ platform deployments

**Limitation:** Project financial scale not documented at €5M level. Largest documented: EKA (700 users), Justice Ministry (government scale) but no contract values proven.

**3. Government Systems Experience**

- Justice Ministry (2002-2005): Criminal care IS, criminal procedure register
- Experience with government security requirements
- Understanding of public sector workflows

**Limitation:** 20+ years old, different regulatory environment (pre-GDPR, pre-X-Road)

**4. PostgreSQL Expertise**

- Documented database management skills
- Large-scale data management (Eesti Mälu Instituut)
- Database design and architecture

**5. System Architecture Skills**

- Core documented strength
- Entu platform: Architected from scratch
- PÖFF: Technical architecture for international festival platform

**Limitation:** No documented microservices experience at 20+ service scale

### PARTIAL MATCHES

**1. Java / Spring Boot Experience**

- **Eesti Keele Instituut (2017-2018):** EKILEX project

  - Spring Boot 2.6.12
  - Spring Framework 5.3.23
  - Spring Security 5.6.7
  - **Role:** PROJECT MANAGER (not hands-on developer)
  - **Repository:** <https://github.com/keeleinstituut/ekilex>

- **Justiitsministeerium (2002-2005):** Government systems
  - Oracle JDeveloper + Oracle ADF (Java-based)
  - XML-based UI development
  - JSP/JSF
  - **Age:** 20+ years old

**Proficiency:** 7/10 (documented)

**GAPS:**

- Last hands-on Java: 2002-2005 (22-25 years ago)
- Spring Boot experience: PROJECT MANAGEMENT (2017-2018), not development
- Current requirement: Spring Boot 2.5.8, Java 1.8 (production-level hands-on)
- **Gap size:** 8+ years since last Spring Boot exposure, 20+ years since last Java development
- **Risk:** Cannot credibly lead €5M Java development with 7/10 proficiency and 8+ year gap

**2. Maven / Tomcat**

- Justice Ministry likely used Maven (Oracle ADF standard)
- Basic proficiency likely but not explicitly documented

**Gap:** No recent experience documented

### WEAK MATCHES

**1. Microservices Architecture**

- System architecture experience verified
- Entu platform likely has service-oriented design
- REST API development documented

**Limitation:** No explicit microservices experience at 20+ service scale, no documented experience with:

- Service discovery (ETCD → Haproxy migration)
- Inter-service messaging
- Distributed transactions
- Circuit breakers, bulkheads
- Microservices monitoring

**2. UI Design**

- Graphic design background (30+ years)
- Layout and visual design expertise
- User-centric design from design background

**Limitation:** NOT a UI designer for software systems. Graphic design ≠ UI/UX design for JSP/Angular applications. Would need dedicated UI designer on team.

### NO MATCH / CRITICAL GAPS

**1. SAP ABAP Development** ← **MANDATORY ROLE, CANNOT FULFILL**

- **ZERO documented experience:**
  - NO SAP ABAP programming
  - NO SAP JCO connector work
  - NO SAP integration projects
  - NO ERP system experience beyond Entu

**Search Results:** Semantic search for "SAP integration ABAP JCO connector ERP system experience" returned ZERO matches in knowledge base.

**Impact:** CANNOT fulfill mandatory 7th team role. Must recruit SAP ABAP developer:

- **Where to find:** Estonian SAP consulting firms (CGI, Columbus, Nortal SAP practice)
- **Availability:** Limited pool, likely already committed
- **Timeline:** 40 days insufficient to recruit, onboard, align
- **Risk:** SAP developer becomes single point of failure

**2. SAP JCO Connector Integration** ← **CRITICAL SYSTEM DEPENDENCY**

Current RTIP has HEAVY SAP dependency:

- Imports organization structures from SAP
- Imports employee data from SAP
- Sends approved vacation/absence data TO SAP
- Sends business trip approvals TO SAP
- Sends training approvals TO SAP
- Sends expenditure claims TO SAP

**Gap:** Zero experience with SAP integration patterns, data mapping, SAP error handling, SAP authentication/authorization.

**Test Assignment Impact:** Calendar integration must work WITH digital signature workflow that INCLUDES SAP data sync. Cannot test solution without understanding SAP integration failure modes.

**3. Test Assignment Completion** ← **70% OF SCORE**

**Requirements:**

- 40 hours estimated development time
- Architecture documentation per RmIT standards
- Deployment guide for independent installation
- Explanation document (solution rationale)
- Must request source code by 2025-12-31 (13 days from assessment)
- Must request RmIT cloud access by 2026-01-03 (17 days from assessment)
- Submission deadline: 2026-01-06 11:00 (40 days from assessment)

**Challenges:**

1. **Source code familiarization:** 20+ microservices, understand vacation approval workflow
2. **Digital signature integration:** SiGa workflow may fail, need retry logic
3. **Timezone handling:** Employee location awareness, UTC conversions
4. **Bulk operations:** Thousands of employees, performance optimization
5. **Calendar iCal format:** RFC 5545 compliance, multi-period handling
6. **Logging requirements:** Admin audit trail (timestamp, user, action, object)
7. **Architecture documentation:** RmIT standards (component diagram, entity diagram with semantics)

**Time Analysis:**

- Source code study: 8-10 hours
- Calendar integration development: 20-30 hours
- Testing (local environment setup): 4-6 hours
- Documentation (architecture + deployment + explanation): 8-12 hours
- **TOTAL:** 40-58 hours

**Conflicts:**

- Other commitments (existing projects, applications)
- Holiday period (2025-12-23 to 2026-01-01)
- 40-day window crosses New Year

**Risk:** Cannot complete test assignment to 70-point standard while maintaining other commitments AND without SAP integration understanding.

**4. €5M Framework Agreement Project Management**

**Your documented PM experience:**

- PÖFF: 4-member team, 3 years, contract value NOT documented
- EKA: 700+ users, large projects, contract values NOT documented
- Entusiastid OÜ: 30+ deployments, individual project values NOT documented (likely <€50k each)
- Justice Ministry: Government scale, but 2002-2005 (20+ years ago), values NOT documented

**Gap:** Cannot prove €5M+ project management scale. Framework agreement procurement expects PM credentials like:

- Led €1M+ software projects (documented with contract references)
- Managed 10+ person development teams
- Multi-year government framework experience
- Formal PM certification (PMP, PRINCE2, Agile)

**5. Agile/Scrum Methodology**

- General project management: STRONG
- Agile/Scrum: NOT explicitly documented
- Scrum certification: NOT documented

**Gap:** RmIT requires:

- Agile development principles
- Sprint-based delivery
- Unified team model (contractor + client working together)
- Likely 2-week sprint cycles

**6. Team Assembly (40 days)**

**Need to recruit:**

1. Software Architect (microservices at scale)
2. Analyst (government HR domain)
3. Programmer (Java/Spring Boot current proficiency)
4. Tester (automation, RmIT standards)
5. UI Designer (JSP/Angular, RTIP style guide)
6. **SAP ABAP Developer** (CRITICAL, limited availability)

**Challenges:**

- 40 days = 6 weeks including holidays
- SAP developer pool very limited (maybe 50-100 in Estonia)
- Established contractors (Nortal, CGI) likely have SAP teams committed
- CV template + consent forms + certifications per person
- Team coordination and bid preparation (20+ hours)

**Risk:** Cannot assemble credible 7-person team in 40 days with RTIP-relevant experience.

**7. Competitive Landscape** ← **MARKET REALITY**

**Expected bidders:**

- **Nortal AS:** Estonia's largest IT company, likely current RTIP contractor
- **CGI Eesti AS:** Global IT services, SAP practice, government frameworks
- **Helmes AS:** Estonian IT services, government systems experience
- **Playtech Estonia:** Large development teams, enterprise systems
- **Fujitsu Estonia:** Global IT services, government sector
- **Tieto Estonia:** Nordic IT services, public sector
- **Proekspert AS:** Estonian IT consultancy, enterprise applications

**Their advantages:**

- Existing RTIP system knowledge (insider advantage)
- Established SAP ABAP teams (dedicated practice)
- €5M+ framework experience (proven credentials)
- Relationships with RTK/RmIT (trust, track record)
- Bench of Java/Spring Boot developers (ready to deploy)
- Test assignment can be completed by existing team (no learning curve)
- ISO certifications, formal PM methodologies

**Your position:**

- Solo practitioner competing against 100-500 person companies
- No RTIP insider knowledge
- No SAP team
- Must assemble team from scratch
- Test assignment requires 40-58 hours focused effort
- 7/10 Java proficiency vs their 9-10/10 teams

**Win Probability Estimate:**

- **Price (30%):** Competitive (solo overhead lower)
- **Test Assignment (70%):** 5-15% (cannot match established contractors' quality)
- **Overall:** 5-15% win probability

---

## Strategic Assessment

### Cost-Benefit Analysis

**BID PREPARATION INVESTMENT:**

1. **Test Assignment:** 40-58 hours

   - Source code study: 8-10 hours
   - Development: 20-30 hours
   - Testing: 4-6 hours
   - Documentation: 8-12 hours

2. **Team Assembly:** 20-30 hours

   - SAP ABAP developer recruitment: 8-10 hours
   - Architect/Analyst/Tester recruitment: 6-8 hours
   - UI Designer recruitment: 2-4 hours
   - CV collection, consent forms: 4-8 hours

3. **Bid Preparation:** 20-30 hours
   - ESPD form completion
   - Team CV template completion
   - Confidentiality forms
   - Pricing strategy (hourly rate optimization)
   - Bid coordination with team

**TOTAL: 80-118 hours**

**OPPORTUNITY COST:**

- 80-118 hours @ €50-80/hour = €4,000-9,440 forgone income
- Holiday period work (reduced personal time)
- Distraction from other applications/projects

**EXPECTED VALUE:**

- Win probability: 5-15%
- Contract value: €5M over 48 months = €1.25M/year
- Gross margin: 20-30% = €250k-375k/year
- Expected value: €1M × 10% × 25% = €25k-37k

**BUT:**

- Must deliver with 7-person team (high coordination overhead)
- Must subcontract SAP developer (€80-120/hour)
- Must maintain quality with 7/10 Java proficiency (high risk)
- Framework agreement = long-term commitment (48 months)

**CONCLUSION:** €4k-9k investment for 5-15% chance at €25k-37k expected value = NEGATIVE expected return when accounting for execution risk.

### Participation Options

**Option 1: Lead Contractor Bid (NOT RECOMMENDED)**

**What you bring:**

- Project Manager role (if scale credibility proven)
- Estonian native language
- Government systems experience

**What you need:**

- Assemble 7-person team (40 days)
- Find SAP ABAP developer (CRITICAL, limited pool)
- Complete test assignment (40-58 hours)
- Refresh Java/Spring Boot to production level (4-6 weeks)
- Document €5M PM scale

**Viability:** 5-15% FEASIBLE

**Why this doesn't work:**

- SAP ABAP developer unavailable or prohibitively expensive
- Test assignment cannot reach 70-point standard (competing against insider teams)
- €5M PM credibility gap vs established contractors
- 40 days insufficient for team assembly + test assignment + bid prep
- Execution risk: 7/10 Java proficiency insufficient for €5M delivery

---

**Option 2: Subcontractor/Partner Role (NOT RECOMMENDED)**

**What you bring:**

- Project Manager / Scrum Master
- Analyst role
- System architecture consultation

**What established contractor brings:**

- SAP ABAP team
- Java/Spring Boot developers
- Test assignment completion
- €5M PM credentials
- RTIP insider knowledge

**Viability:** 20-30% FEASIBLE

**Why this doesn't work:**

- Established contractors (Nortal, CGI, Helmes) already have PM/Analyst teams
- Your value-add unclear (they have government PM experience)
- Subcontractor margin reduces income (€40-60/hour vs €80-120/hour prime)
- 40 days insufficient to identify partner + negotiate terms + integrate into bid
- Partner likely prefers own team (trust, experience, proven)

---

**Option 3: Strategic SKIP (RECOMMENDED)**

**Reasons:**

1. **SAP ABAP requirement is HARD BLOCKER** - Cannot fulfill mandatory role, cannot recruit in 40 days
2. **Test assignment is 70% of score** - Cannot compete against insider teams with RTIP knowledge
3. **€5M scale mismatch** - Project management credibility gap vs established contractors
4. **Java/Spring Boot currency gap** - 7/10 proficiency + 8-year gap insufficient for production delivery
5. **Time investment doesn't justify risk** - 80-118 hours for 5-15% win probability = negative expected value
6. **Competitive field** - 7-10 established contractors with insider advantage

**Better opportunities:**

- **Procurement 9534824** (Python development for environmental systems): 70-80% win probability, Python 9/10 is PRIMARY requirement
- **Procurement 9407944** (Illegaal2 module): 30-40% win probability, Java required but smaller scale (€530k)
- **Job applications:** DataShift PM (70% fit), BCS Itera ERP PM (75% fit) = immediate income

---

## Participation Requirements Checklist

### Technical Skills Coverage

**Java / Spring Boot (REQUIRED):**

- [ ] Current hands-on production experience (Spring Boot 2.5.8, Java 1.8)
- [ ] Microservices architecture (20+ services)
- [ ] Maven build tool
- [ ] Tomcat application server

**YOUR STATUS:** 40% (7/10 proficiency, 8-year gap, project management not development)

**SAP Integration (REQUIRED):**

- [ ] SAP ABAP programming
- [ ] SAP JCO connector (3.0.9)
- [ ] SAP data mapping and transformation
- [ ] SAP error handling and retry logic

**YOUR STATUS:** 0% (ZERO documented experience, MANDATORY role cannot be fulfilled)

**Integrations (REQUIRED):**

- [ ] TARA authentication
- [ ] SiGa digital signatures
- [ ] X-Road data exchange
- [ ] SMTP email (iCal invites)

**YOUR STATUS:** 50% (government systems experience, but no documented TARA/SiGa/X-Road work)

**Database (REQUIRED):**

- [x] PostgreSQL 16

**YOUR STATUS:** 100% (documented expertise)

**Architecture (REQUIRED):**

- [ ] Microservices patterns (service discovery, inter-service messaging)
- [ ] Load balancing (Apache HTTP + ETCD → Haproxy migration)
- [ ] Event-driven architecture
- [ ] Distributed transactions

**YOUR STATUS:** 30% (system architecture strength, but no documented microservices at 20+ service scale)

### Team Assembly

**7 Roles (ALL MANDATORY):**

- [ ] Project Manager
- [ ] Software Architect
- [ ] Analyst
- [ ] Programmer
- [ ] Tester
- [ ] UI Designer
- [ ] **SAP ABAP Developer** ← CRITICAL BLOCKER

**YOUR STATUS:** 1/7 roles can be credibly fulfilled (Project Manager with scale gap caveat)

**Recruitment Needs:**

- [ ] Software Architect (microservices at scale)
- [ ] Analyst (government HR domain knowledge)
- [ ] Programmer (Java/Spring Boot current production proficiency)
- [ ] Tester (automation, RmIT standards, Sonarqube/Trivy)
- [ ] UI Designer (JSP/Angular, RTIP style guide compliance)
- [ ] **SAP ABAP Developer** (limited pool, likely committed to established contractors)

**Timeline:** 40 days (including holidays) = INSUFFICIENT

### Test Assignment Feasibility

**Requirements (ALL must be met for 70 points):**

- [ ] Send calendar invite for approved vacation
- [ ] Multi-day vacation as single period
- [ ] One invite with all periods
- [ ] Update invites when dates change
- [ ] Cancellation invites
- [ ] Mass approval support (thousands)
- [ ] Send at approval moment
- [ ] Handle digital signature failures (retry)
- [ ] Send to employee email
- [ ] Correct titles ("Puhkus"/"Puudumine")
- [ ] Full-day calendar reservation
- [ ] Timezone-aware
- [ ] Logging (timestamp, user, action, object)

**YOUR STATUS:** 20% feasible (calendar functionality basic understanding, but 13 criteria require deep RTIP knowledge + SAP integration understanding)

**Deliverables:**

- [ ] Source code (working implementation)
- [ ] Deployment guide (independent installation)
- [ ] Architecture documentation (RmIT standards: component + entity diagrams)
- [ ] Explanation document (solution rationale)

**Time Required:** 40-58 hours (conflicts with holiday period + other commitments)

### Compliance Requirements

**ESPD (European Single Procurement Document):**

- [x] No criminal exclusion grounds
- [x] No tax/social security debt
- [x] Not bankrupt/liquidation
- [x] EU sanctions compliance (no Russian subcontractors >10%)

**YOUR STATUS:** 100% (standard compliance, no issues)

**Operational Requirements:**

- [ ] Request source code with confidentiality form (by 2025-12-31) - 13 days
- [ ] Request RmIT cloud access for test assignment (by 2026-01-03) - 17 days
- [ ] Team CVs per template with consent forms
- [ ] Certificates for team members (where applicable)
- [ ] Environmental commitment confirmation

**YOUR STATUS:** 50% (operational requirements manageable, but timeline compressed)

### Financial/Scale Requirements

**Project Management Scale:**

- [ ] €5M framework agreement PM credentials
- [ ] Documented €1M+ software projects
- [ ] Multi-year government framework experience

**YOUR STATUS:** 30% (15+ years PM experience, but scale not documented at €5M level)

**Team Scale:**

- [ ] 7-person team management capability
- [ ] Multi-role coordination (PM, Architect, Analyst, Dev, Test, UI, SAP)

**YOUR STATUS:** 40% (4-person team at PÖFF documented, 7-person team at €5M scale NOT documented)

---

## CONCLUSION

**STRATEGIC SKIP STRONGLY RECOMMENDED**

### Primary Blockers (Any one sufficient to skip)

1. **SAP ABAP Developer (MANDATORY):** Zero documented experience, cannot fulfill critical role, cannot recruit in 40 days from limited Estonian pool

2. **Test Assignment (70% of score):** Cannot compete against established contractors with RTIP insider knowledge + SAP integration expertise

3. **€5M Framework Scale:** Project management credibility gap vs Nortal/CGI/Helmes with proven €5M+ government frameworks

4. **Java/Spring Boot Currency:** 7/10 proficiency + 8-year gap insufficient for production delivery, competing against 9-10/10 teams

5. **Competitive Field:** 7-10 established contractors with:
   - Existing RTIP knowledge
   - Dedicated SAP teams
   - €5M+ frameworks
   - RTK/RmIT relationships

### Time Investment vs. Expected Value

**Investment Required:** 80-118 hours (test assignment 40-58h + team assembly 20-30h + bid prep 20-30h)

**Win Probability:** 5-15%

**Expected Value:** €25k-37k (€1M contract × 10% win × 25% margin)

**Opportunity Cost:** €4k-9k foregone income + holiday period + other opportunities

**CONCLUSION:** Negative expected return when accounting for execution risk and alternative opportunities.

### Better Alternatives

**IMMEDIATE PRIORITY:**

1. **Procurement 9534824** (Python development): 70-80% win probability, €2M/48 months, Python 9/10 PRIMARY requirement, 25 days remaining
2. **Job applications:** DataShift PM (70% fit), BCS Itera ERP PM (75% fit) = immediate income stream

**SKILL DEVELOPMENT (if considering future RTIP-like opportunities):**

1. **SAP ABAP training** (6-12 months): SAP Learning Hub, community courses
2. **Spring Boot currency refresh** (3-6 months): Build 2-3 production projects, upgrade to Spring Boot 3.x
3. **Microservices architecture** (3-6 months): Kubernetes, service mesh, distributed patterns
4. **€5M PM credentials** (1-2 years): Document large project values, obtain PMP/PRINCE2, lead €1M+ projects

**TIMELINE:** 12-24 months preparation before credibly bidding €5M government frameworks

---

## Next Steps

### RECOMMENDED: Strategic Skip

**Actions:**

1. **Do NOT request RTIP source code** (avoid confidentiality commitment)
2. **Do NOT invest time in test assignment**
3. **Focus on procurement 9534824** (Python, 25 days, 70-80% win probability)
4. **Continue job applications** (DataShift, BCS Itera, Elektrilevi = immediate income)

**Rationale:**

- SAP ABAP requirement is HARD BLOCKER (cannot fulfill mandatory role)
- Test assignment 70% score unachievable against insider competition
- 80-118 hour investment for 5-15% win probability = poor ROI
- Better opportunities available (Python procurement, job applications)

### IF CONSIDERING FUTURE RTIP-LIKE BIDS (12-24 month horizon)

**Priority 1: SAP ABAP capability (CRITICAL)**

- Partner with SAP consultancy (Columbus, CGI SAP practice, Nortal SAP team)
- Complete SAP Learning Hub courses (ABAP fundamentals, JCO connector)
- Build 1-2 SAP integration reference projects

**Priority 2: Java/Spring Boot currency refresh**

- Upgrade from Spring Boot 2.6 to 3.x
- Build 2-3 microservices projects (10+ services each)
- Document production deployments (Docker, Kubernetes)
- Contribute to open source Spring projects

**Priority 3: €5M PM credentials**

- Document existing project values (reconstruct EKA/Justice contracts)
- Obtain formal PM certification (PMP, PRINCE2, Agile/Scrum)
- Lead €500k-1M projects to build scale credentials

**Priority 4: Government integration skills**

- TARA authentication integration (practice project)
- SiGa digital signatures integration
- X-Road data exchange (test environment)

**Timeline:** 12-24 months before attempting €5M framework bid

---

**Assessment completed:** 2025-11-27  
**Confidence level:** HIGH (comprehensive analysis, clear blockers, sound strategic recommendation)  
**Recommendation:** SKIP - Focus on procurement 9534824 (Python) and job applications (DataShift, BCS Itera)
