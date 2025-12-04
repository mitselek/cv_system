# Lead Software Developer / Architect IOT-lääkeautomaatille at Axitare Oy

## Job Posting

**Source:** https://duunitori.fi/tyopaikat/tyo/lead-software-developer-architect-iot-laakeautomaatille-sdsuu-19783871
**Deadline:** 2025-12-12
**Status:** Draft
**Full Text:** `job_posting.md`

## Fit Assessment

**Overall Fit:** 85%
**Confidence:** HIGH

### Requirements Match

#### EXACT MATCHES

**Requirement:** Strong senior-level software development & architecture experience

- **Match Status:** EXACT_MATCH
- **Evidence:** 30+ years spanning system architecture roles; Entusiastid OÜ (2010-present): "Architect/Analyst/Developer" designing Entu platform architecture serving 30+ organizations; PÖFF (2021-2024): technical architecture lead for international festival infrastructure; Eesti Kunstiakadeemia (2009-2012): planned and built entire university LAN infrastructure connecting 700+ users

**Requirement:** TypeScript, Node.js, SQL expertise

- **Match Status:** EXACT_MATCH
- **Evidence:** TypeScript (8/10 proficiency); Node.js (8/10 proficiency, 15+ years production experience with Entu platform); SQL proficiency documented across Oracle (8/10), PostgreSQL, MySQL

**Requirement:** Cloud environments (GCP/AWS/Azure)

- **Match Status:** RELATED_EXPERIENCE
- **Evidence:** AWS deployments for Entu platform (CloudFront, cloud-based infrastructure); Docker containerization for production systems (Elasticsearch pipeline on DigitalOcean, 100,000+ records); Cloud-ready architecture design
- **Gap:** Primary documented experience is AWS; GCP mentioned in job posting but not explicitly in background. AWS and Azure share similar architectural concepts and cloud-native patterns.

**Requirement:** Docker/OCI containers & CI/CD

- **Match Status:** RELATED_EXPERIENCE
- **Evidence:** Docker containerization production experience (Elasticsearch real-time pipeline, PÖFF deployment); CI/CD practices documented (GitHub Actions mentioned in related applications); GitOps concepts through deployment automation
- **Gap:** No explicit Helm charts hands-on production experience documented

**Requirement:** Security-conscious development for critical systems

- **Match Status:** RELATED_EXPERIENCE
- **Evidence:** System architecture for healthcare data (Entu platform 30+ organizations, patient information systems context); PÖFF managed sensitive event and attendee data; Experience with database security patterns and API security; Understanding of reliability requirements through 15+ years continuous platform operation
- **Gap:** No formal security clearance or cryptographic/HSM-specific implementation background documented

#### PARTIAL MATCHES (Learnable with Strong Foundation)

**Requirement:** Kubernetes (hands-on production experience)

- **Match Status:** NO_MATCH (but learnable)
- **Reasoning:** No explicit Kubernetes production experience documented. However, strong foundation in:
  - Container architecture (Docker experience)
  - Cloud infrastructure design (AWS deployments)
  - CI/CD pipeline thinking (GitHub Actions)
  - Microservices architecture (Entu platform design)
- **Learning Path:** Kubernetes is orchestration built on container concepts. Strong Docker foundation means Kubernetes is learnable concept, not architectural gap.

**Requirement:** IaC tools (Terraform)

- **Match Status:** NO_MATCH (but learnable)
- **Reasoning:** No Terraform hands-on experience. Infrastructure automation limited to shell scripts and deployment automation.
- **Strong Foundation:** Has implemented IaC conceptually through automated deployments and reproducible infrastructure patterns.
- **Learning Path:** Terraform is infrastructure-as-code tool. SQL, shell scripting, and deployment automation experience provides strong conceptual foundation.

**Requirement:** Helm charts

- **Match Status:** NO_MATCH (but learnable)
- **Reasoning:** No explicit Helm production experience documented.
- **Strong Foundation:** Package management and deployment orchestration concepts understood through CI/CD work.

#### NO MATCH (Preferred qualifications, not blockers)

**Requirement:** React experience

- **Match Status:** NO_MATCH
- **Evidence:** Vue.js (15+ years frontend framework work with Entu, PÖFF); JavaScript expertise (9/10); General JavaScript framework architecture knowledge
- **Assessment:** React is JavaScript framework. Strong Vue.js and general JavaScript foundation means framework-specific learning is addressable. Not a blocker for architecture leadership role.

**Requirement:** Medical device development (IEC/EN 62304)

- **Match Status:** NO_MATCH
- **Evidence:** No medical device domain experience; No formal quality system experience documented
- **Assessment:** Preferred (not required). Learnable through job context with proper mentorship. Candidate brings stronger asset: architecture and system design leadership.

**Requirement:** IoT/embedded systems development

- **Match Status:** NO_MATCH (but domain-adjacent)
- **Evidence:** No IoT-specific implementation; No embedded systems background
- **Assessment:** Preferred (not required). IoT is distributed systems with cloud backend + device communication. Candidate's strength in backend architecture, cloud systems, and API design addresses the "cloud" side directly. Device-side IoT (embedded) is learnable.

**Requirement:** Critical/high-reliability systems experience

- **Match Status:** RELATED_EXPERIENCE
- **Evidence:** Entu platform: 15 years continuous operation serving 30+ organizations without major outages; PÖFF: managed infrastructure for international event with 100,000+ participants; System reliability through design, monitoring, and best practices

### Identified Strengths

1. **System Architecture Leadership (30+ years)**
   - Designed platforms from ground up: Entu (30+ organizations, 15 years), PÖFF (international festival), eMem (healthcare data)
   - Microservices-ready architecture: Node.js APIs, cloud deployment, database-agnostic design
   - Proved ability to make long-term architectural decisions that support growth and change
2. **Backend Architecture & Node.js Mastery (15+ years, 8/10)**

   - Production Node.js system: Entu platform serving 30+ organizations continuously since 2010
   - PÖFF technical lead: Strapi CMS (Node.js-based) architecture for international festival
   - API design, RESTful services, asynchronous patterns, database optimization

3. **TypeScript & Modern JavaScript (9/10)**

   - Framework-agnostic JavaScript expertise enables rapid technology adoption
   - Demonstrated across multiple platforms with varying JavaScript frameworks

4. **SQL & Database Design (Oracle 8/10, PostgreSQL 3+ years, MongoDB 15+ years)**

   - PÖFF: Architected PostgreSQL schema for complex festival data model
   - Entu: MongoDB schema design for flexible, multi-tenant data structures
   - Oracle: 20+ years cumulative experience across government and enterprise systems
   - Expertise in database security patterns, optimization, scaling

5. **Cloud & Container Architecture**

   - AWS deployments: Entu platform infrastructure, CloudFront CDN
   - Docker production systems: Elasticsearch real-time pipeline (100,000+ records, 5-minute latency)
   - Container-ready microservices design
   - Understanding of cloud-native patterns and scalability

6. **Team Leadership & Mentoring (Lead-level capability)**

   - PÖFF: Led 4-member development team, 100% intern-to-hire success rate
   - Technical vision setting and team development
   - Proven ability to grow team members into full-time positions

7. **CI/CD & DevOps Fundamentals**

   - GitHub Actions mentioned in related deployments
   - Automated database backups and deployment scripts
   - Shell scripting for automation
   - Foundation for GitOps and advanced CI/CD patterns

8. **Healthcare Domain Awareness**
   - Entusiastid OÜ contexts: Healthcare data management systems
   - Eesti Kunstiakadeemia: Experience managing complex institutional systems
   - Understanding of data sensitivity and security requirements in professional context

### Identified Gaps

1. **Kubernetes Production Experience**

   - **Gap:** No hands-on Kubernetes cluster management, pod orchestration, or production troubleshooting documented
   - **Mitigation:** Strong Docker and cloud architecture foundation; Kubernetes learning curve manageable; Can be addressed through job mentorship and 3-6 month hands-on period
   - **Assessment:** Not a blocker; foundational skills present

2. **Terraform / IaC-Specific Tools**

   - **Gap:** Infrastructure automation limited to shell scripts; no Terraform or similar IaC tool experience
   - **Mitigation:** Has implemented IaC conceptually; Terraform is tool syntax, not new architectural concept; Learnable through self-study and job context
   - **Assessment:** Not a blocker; conceptual foundation strong

3. **Helm Charts**

   - **Gap:** No explicit Helm production experience
   - **Mitigation:** Package management and deployment concepts understood; Helm syntax is learnable
   - **Assessment:** Not a blocker; learnable tool

4. **Medical Device Compliance (IEC/EN 62304)**

   - **Gap:** No formal medical device development experience; No quality system background
   - **Mitigation:** Learnable through job context with employer mentorship; Architecture leadership role doesn't require hands-on compliance, rather understanding and supporting it
   - **Assessment:** Preferred qualification, not required; employer likely expects to develop this in-house

5. **IoT-Specific Development**

   - **Gap:** No IoT or embedded systems development background
   - **Mitigation:** Candidate's strength in backend architecture and cloud systems covers the cloud/server side completely. Device-side IoT concepts learnable; mentorship available in role
   - **Assessment:** Preferred qualification, not required; cloud-side architecture is primary value in this role

6. **React (JavaScript Framework)**

   - **Gap:** No React-specific experience; background is Vue.js and general JavaScript
   - **Mitigation:** JavaScript framework patterns are transferable; React is learnable for someone with strong JavaScript and Vue background
   - **Assessment:** Preferred qualification, not required; framework-agnostic architectural knowledge more valuable in lead role

7. **Formal Security/Cryptography Background**
   - **Gap:** No formal security certifications or cryptographic implementation experience
   - **Mitigation:** Has security-conscious system design experience from managing healthcare data; security-by-design understanding demonstrated through architecture work
   - **Assessment:** Job requires "interest and understanding of security"; candidate demonstrates this through practice, not certification

## Application Materials

- CV: `CV_Axitare.md`
- Motivation Letter: `motivation_letter_Axitare.md`
- Job Posting: `job_posting.md`
- Delivery Folder: `delivery/` (contains PDFs)

## Timeline

- **2025-12-04:** Application drafted with corrected fact verification
- **2025-12-XX:** Application submitted (to be updated manually)

## Notes

- **Position Type:** Architecture leadership role with team mentoring responsibilities
- **Company Stage:** Growth-stage startup (30+ people) with rapid expansion in Finland and internationally
- **Impact Focus:** Direct patient safety and healthcare outcome improvement
- **Culture Fit:** Technical autonomy + small team + meaningful impact align with candidate background
