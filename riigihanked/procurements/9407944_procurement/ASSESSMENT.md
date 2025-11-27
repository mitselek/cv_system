# Procurement 9407944 Assessment: Illegaal2 Background Check Module

**Assessment Date:** 2025-11-27

**Procurement ID:** 9407944 (version 9558984)

**Reference:** 301189

**Procurer:** Siseministeeriumi infotehnoloogia- ja arenduskeskus (SMIT)

**Title:** Illegaali Rändepaketi taustakontroll (Illegaal2 Background Check Migration Package)

**CPV Code:** 72240000-9 (System analysis and programming services)

**Contract Value:** €530,000

**Contract Duration:** 5 months (fixed deadline: 25.05.2026)

**Submission Deadline:** 2025-12-16 11:00 (19 days remaining)

**Evaluation:** 100% price (lowest wins)

## Executive Summary

**RECOMMENDATION: CHALLENGING - CONSIDER WITH TEAM**

**Feasibility:** 50-60% (POSSIBLE with right team)

**Winning Probability:** 30-40% (MEDIUM competition)

**Key Decision:**

This is a **Java/Spring Boot backend development** project for Estonian Police and Border Guard's immigration system. You have verified Java experience (Oracle ADF 2002-2005, Spring Boot management 2017-2018) but would need to demonstrate current hands-on Spring Boot development capability and assemble a 2-3 person team for the 5-month intensive sprint-based project.

**Critical Match:** Java 7/10, Spring Boot verified, PostgreSQL, Estonian government experience, Estonian native speaker

**Critical Gaps:** Current Java hands-on development (last role was PM 2017-2018), no documented Scrum/Agile team experience, microservices architecture experience not explicitly documented

## Project Scope

**System:** Illegaal2 - Police and Border Guard immigration/deportation case management system (350+ users nationwide)

**Task:** Build new Background Check module implementing EU Regulation 2024/1358 for third-country nationals screening at external borders

**Core Functionality:**

1. New standalone Background Check API (Java 21, Spring Boot 3.4+, PostgreSQL, jOOQ)
2. Integration with existing Illegaal2 modules (REST, RabbitMQ)
3. X-Road integrations: Border control (PIKO), Identity verification (IT 2.0), ABIS (biometrics), asylum register (RAKS)
4. Angular 13 frontend components
5. Data migration workflows, document generation, statistics reporting

**Phased Delivery:** Minimum 3 phases (first phase 20% fixed, last phase minimum 35%)

**Technology Stack:**

- Java 21+, Spring Boot 3.4+, jOOQ 3.19+, PostgreSQL 15+
- Angular 13 TypeScript frontend
- Gradle 8.5+ (Kotlin DSL), Flyway 10.18+, JUnit 5
- X-Road (SOAP/REST), RabbitMQ messaging
- OpenAPI 3.0 API-first design
- Microservices architecture

## Requirements Analysis

### Mandatory Technical Skills

**Java/Spring Boot (CRITICAL):**

- Java 21+ development
- Spring Boot 3.4+ (current version 2.5-2.7 in existing modules)
- jOOQ for database access (NOT JPA/Hibernate)
- OpenAPI 3.0 specification and code generation

**YOUR FIT:** Java 7/10 verified (Oracle ADF 2002-2005, Spring Boot PM 2017-2018). Gap: Need to demonstrate current hands-on Spring Boot 3.x development, jOOQ experience.

**Database & Architecture:**

- PostgreSQL 15+ with Flyway migrations
- Microservices architecture
- REST API design
- RabbitMQ messaging

**YOUR FIT:** PostgreSQL documented, architecture experience (Entu platform), REST APIs verified. Gap: RabbitMQ and microservices patterns not explicitly documented.

**Integration:**

- X-Road SOAP/REST integrations (Estonian government data exchange layer)
- Multiple external system integrations

**YOUR FIT:** Government systems experience (Justice Ministry 2002-2005), but X-Road integration NOT documented.

**Development Process (MANDATORY):**

- Scrum/Agile: 2-week sprints with demos
- Atlassian stack: JIRA, Confluence, Bitbucket
- GitLab CI/CD (Bamboo)
- SonarQube code quality (80%+ test coverage)
- Code reviews, pull requests
- Estonian language communication

**YOUR FIT:** Estonian native, project management verified. Gap: Scrum team experience, Atlassian tools, CI/CD pipelines not explicitly documented.

### Team Requirements

**Minimum viable team:** 2-3 developers for 5-month intensive project

**Role options for you:**

1. **Technical Lead / Senior Developer** (if demonstrating current Java hands-on skills)
2. **Project Manager / Scrum Master** (leveraging PM experience, partnering with Java developers)

**Need to assemble:**

- 1-2 Java/Spring Boot developers with microservices experience
- Angular/TypeScript frontend developer (or full-stack)
- Optional: DevOps specialist for CI/CD setup

## Capability Matching

### Strong Matches

**Government systems experience:**

- Justice Ministry (2002-2005): Criminal care information system
- Oracle JDeveloper + Oracle ADF (Java enterprise framework)
- XML-based UI development, JSP/JSF

**Java/Spring Boot foundation:**

- EKI (2017-2018): Spring Boot 2.6 project management/oversight
- Oracle Java JDBC certification (2003)
- 4 years documented Java work (2002-2005 development, 2017-2018 PM)

**Estonian language & domain:**

- Native Estonian speaker (critical for daily communication)
- Government sector experience
- Understanding of Estonian e-government ecosystem

**Database & backend:**

- PostgreSQL expertise documented
- System architecture experience (Entu platform)
- 15+ years backend development

### Gaps Requiring Mitigation

**Current Java hands-on (CRITICAL):**

- Last hands-on Java role: 2002-2005 (20+ years ago)
- 2017-2018: Project manager role, not developer
- Need to demonstrate Spring Boot 3.x, Java 21, jOOQ capability

**Mitigation:** Partner with current Java developers, OR update skills via crash course, OR position as PM/Technical Lead

**Microservices & modern DevOps:**

- Microservices architecture not explicitly documented
- Docker/Kubernetes not documented
- CI/CD pipelines not documented
- X-Road integration not documented

**Mitigation:** Team includes specialists with these skills

**Agile/Scrum team delivery:**

- Scrum Master role not documented
- Atlassian tools (JIRA/Confluence) not documented
- Sprint-based delivery experience not explicitly documented

**Mitigation:** Leverage 15+ years project management, position as learner of formal Scrum framework

## Strategic Assessment

### Competitive Landscape

**Likely bidders:**

- Estonian software consultancies with government experience (Nortal, CGI, Helmes, Trinidad Wiseman)
- Small-medium Java shops with SMIT/government portfolio
- Teams that previously worked on Illegaal2 (insider advantage)

**Your positioning:**

- **Strength:** Native Estonian, government experience, Java foundation, can lead or develop
- **Weakness:** Need to assemble team, outdated hands-on Java (if developer role), no documented Scrum delivery

**Realistic winning probability:** 30-40%

**Why medium probability:**

- €530k contract attractive to many qualified teams
- 100% price-based evaluation = cost competition critical
- Established players have existing Java teams ready to deploy
- Your advantage: Lower overhead (small team), deep technical understanding, government sector fit

### Participation Options

**Option 1: Technical Lead with Junior/Mid Java Developers**

- You: Architecture, code reviews, X-Road integration design, client communication
- Team: 1-2 Java developers handle bulk of Spring Boot development
- Risk: Your Java must be sharp enough to lead effectively
- Timeline: 2 weeks to assemble team, verify Java skills, prepare portfolio

**Option 2: Project Manager / Scrum Master with Senior Java Developer**

- You: Project planning, SMIT communication, sprint management, delivery coordination
- Partner: Senior Java developer leads technical implementation
- Risk: Less technical control, dependent on partner's capability
- Timeline: 2 weeks to find right technical partner, align on approach

**Option 3: Strategic Pass**

- Focus on Python procurement 9534824 (70-80% win probability, better skill match)
- Build Java portfolio with smaller projects before tackling €530k government contract
- Timeline: Immediate focus shift

## Cost-Benefit Analysis

**Bid preparation effort:** 40-60 hours

- Team assembly/partnership: 20-30 hours
- Technical assessment: 10-15 hours
- Project plan creation: 10-15 hours

**Expected value:**

- Win probability: 30-40%
- Contract value: €530,000
- Expected value: €159k-212k
- Your share (if 2-person team): €80k-106k

**Competition:**

- Python procurement 9534824: 70-80% win, €50k-200k value, perfect skill match
- This Java procurement: 30-40% win, €530k value, requires team/skills verification

**Risk assessment:**

- **High risk:** 5-month intensive delivery, fixed deadline (25.05.2026), no extensions
- **Medium risk:** Team management, ensuring quality with tight timeline
- **Low risk:** Technology mismatch (Java foundation exists, just needs refresh)

## Recommendation

**CONDITIONAL PARTICIPATION:**

**Proceed IF:**

1. Can assemble 1-2 qualified Java/Spring Boot developers within 1 week
2. Can demonstrate sufficient Java hands-on capability (crash course or partner validation)
3. Python procurement 9534824 submitted first (higher priority)
4. Comfortable with intensive 5-month sprint-based delivery

**Skip IF:**

1. Cannot assemble team quickly
2. Java skills too outdated to lead effectively
3. Risk profile too high compared to Python opportunity
4. Prefer to focus energy on 9534824 (FEASIBLE, 70-80% win)

## Next Steps (If Proceeding)

**Week 1 (Nov 27 - Dec 3): Team Assembly**

- Contact Java developers for partnership/hiring
- Verify Spring Boot 3.x, jOOQ, microservices experience
- Align on roles (you as Tech Lead or PM)
- Refresh Java/Spring Boot skills (online courses, hands-on practice)

**Week 2 (Dec 4-10): Portfolio & Technical Prep**

- Document relevant references (Justice Ministry, EKI, Entu if applicable)
- Create project plan: phases, timeline, team composition, risk mitigation
- Review Illegaal2 architecture document thoroughly
- Prepare technical approach document

**Week 3 (Dec 11-15): Bid Finalization**

- Price calculation (team costs, overhead, margin)
- Risk mitigation strategies in project plan
- Final review with team
- Submit by Dec 16 11:00

**Critical deadline:** 19 days remaining = aggressive timeline for team assembly

## Conclusion

This is a **solid opportunity IF you can quickly assemble a qualified team**. Your Java foundation (7/10) and government experience are relevant, but the 5-month intensive delivery and need for current Spring Boot 3.x/microservices skills make this **riskier than Python procurement 9534824**.

**Recommended strategy:** Submit 9534824 first (higher win probability, better skill match), then assess bandwidth and team availability for 9407944. Don't chase both simultaneously unless team assembly goes very smoothly.

**Final note:** €530k contract is substantial, but competition will be fierce. Price-based evaluation means lowest cost wins, favoring established teams with ready capacity. Your best competitive angle: smaller overhead, government sector understanding, and ability to move fast with lean team.

---

**Assessment completed:** 2025-11-27

**Time invested:** 2 hours (download, analysis, writing)

**Confidence level:** MEDIUM (Java capability requires validation, team assembly feasibility unclear)
