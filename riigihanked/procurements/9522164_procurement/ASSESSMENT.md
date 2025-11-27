# Procurement 9522164 Assessment: Third-Party Risk Management Platform

**Procurement ID:** 9522164 (Version 9608084)  
**Reference:** 302387  
**Procurer:** Eesti Energia AS  
**Deadline:** 2025-12-02 12:00 EET (4 days remaining)  
**Assessment Date:** 2025-11-28  
**Decision:** **SKIP**

---

## EXECUTIVE SUMMARY

### Recommendation: SKIP (<5% winning probability)

**Critical Mismatch:** This procurement requires a **SaaS platform vendor** with an existing third-party risk management (TPRM) and attack surface monitoring solution. You are a **software developer/integrator**, not a platform vendor. This is a **product reseller procurement**, not a development project.

**Procurement Type:** Platform-as-a-Service (SaaS) license procurement with support  
**Contract Value:** Not disclosed (cost classified)  
**Contract Duration:** 24 months + 12-month optional extension (2+1 years)  
**Evaluation:** 100% price-based (lowest cost wins)

**Why SKIP:**
1. **No qualifying product:** You don't own/resell a TPRM platform
2. **Manufacturer authorization required:** Must have vendor certificate for platform and support services  
3. **Platform must exist at bid submission:** No development allowed
4. **ISO 27001/SOC2 Type II certification required:** For the platform service itself
5. **Wrong business model:** This requires SaaS vendor partnership, not development skills

**Similar to:** Procurement 9526064 (CRM software) - also SKIP for same reason (product vendor required, not developer)

**Alternative Focus:** Continue pursuing development procurements like 9407944 (Java/Spring Boot - CONSIDER status)

---

## PROJECT SCOPE

### Procurement Objective

Acquire 2-year SaaS platform license (2+1 years with extension option) for **third-party cybersecurity risk management and attack surface monitoring** covering:
- Eesti Energia AS (parent company)
- 6 subsidiaries
- Up to 150 third-party vendors (switchable on demand)
- 10 full-access users + unlimited read-only users

### Core Platform Requirements

**1. Third-Party Risk Management:**
- Automated vendor risk profiling and scoring
- Risk score history (minimum 1 year)
- Peer comparison (minimum 7 comparators)
- Risk treatment workflow management
- Pre-defined security questionnaires (ISO, NIST, GDPR, NIS2, etc.)
- Custom questionnaire builder
- Document sharing (certificates, policies, compliance docs)
- Company branding for outbound questionnaires

**2. Attack Surface Monitoring:**
- Continuous asset discovery (IPs, domains)
- Automated daily rescans (minimum 1x per day)
- Manual scan triggering
- Passive and active vulnerability detection
- Typosquatting detection (similar domains monitoring)
- Last successful scan timestamp visibility

**3. Real-Time Alert System:**
- Major data breach notifications
- Cybersecurity incident alerts
- Critical vulnerability warnings

**4. Platform Features:**
- GDPR compliant
- Multi-tenancy (parent + 6 subsidiaries)
- Third/fourth-party auto-detection
- Vendor swapping without additional costs
- Custom dashboards and reports with filtering/tagging
- Data export capabilities
- API integrations with security solutions
- Audit log access

### Technical Requirements (NFR.xlsx - 40 detailed requirements)

**Security (NFR_1.x):**
- **Identity Management:** EntraID (Microsoft Entra ID) integration for SSO/authentication
- **MFA Enforcement:** Multifactor authentication mandatory
- **API Security:** OAuth 2.0, JWT tokens, secure key management
- **Data Protection:** TLS 1.2+ encryption, secrets management (HashiCorp Vault/Secrets Server)
- **OWASP Compliance:** Web/mobile apps follow OWASP best practices
- **Session Management:** Configurable timeouts, revocation, secure storage
- **Error Handling:** Generic error messages (no technical details exposed)

**Compliance (NFR_1.3.x) - MANDATORY:**
- **NFR_1.3.1:** Hosting provider ISO 27001 certified (must provide certificate copy)
- **NFR_1.3.2:** Service itself ISO 27001 OR SOC2 Type II certified (must provide certificate/third-party confirmation)
- **NFR_1.3.3:** Service hosted in EU or GDPR-equivalent territory
- **NFR_1.3.7:** Regular penetration testing, no unresolved high/critical vulnerabilities

**Interoperability (NFR_3.x):**
- REST/OpenAPI APIs for synchronous data flows
- Kafka/AMQP with Avro schema for asynchronous flows (desirable)
- API key authentication minimum (OAuth2/OIDC preferred)
- ISO 8601 date/time with timezone (UTC default)

**Documentation (NFR_6.x):**
- Estonian or English language
- User/administrator troubleshooting guides
- User lifecycle management documentation
- Configuration parameter documentation

**Observability (NFR_9.x):**
- Audit logging (who, what, where, source, when in UTC)
- User activity logging (authentication, PII access, permission changes, password changes)
- Tamper-proof logs, access controls, integrity checks
- Backup verification and recovery testing

**Usability (NFR_13.x):**
- HTML5/CSS3 standards compliance
- Internal apps: Edge + Chrome (2 latest versions)
- External apps: Edge, Chrome, Firefox, Safari (2 latest versions)
- Mobile: Same 4 browsers (2 latest versions)
- Browser incompatibility notifications with instructions

### Supplier Requirements

**Mandatory Certifications:**
- Manufacturer authorization/certificate for platform and support services (valid for contract duration)
- ISO 27001 OR SOC2 Type II certification for the service

**Support Requirements:**
- Estonian or English language technical support
- Critical priority: Response within 1 business day (08:00-17:00, weekdays)
- Low priority: Response within 3 business days
- Support channels: Email + vendor-specified environment

**Implementation:**
- Platform available within 5 business days after contract signing
- Initial training completed within 30 days (online)
- Training costs included in license fee

**Documentation:**
- Technical specification/product documentation
- NFR compliance matrix (all 40 requirements)
- Certificates: ISO 27001/SOC2 Type II (NFR_1.3.1, NFR_1.3.2)
- Service Level Agreement (SLA) for product support
- Detailed cost breakdown form

### Evaluation Criteria

**100% price-based:** Lowest cost wins (no quality criteria)
- Total cost for 2-year license (including all fees, training, support)
- Cost form must match bid price on evaluation page

---

## CRITICAL MISMATCH ANALYSIS

### Why This is a SKIP

**1. WRONG PROCUREMENT TYPE**
- **Required:** SaaS platform vendor/reseller
- **Your profile:** Software developer/integrator
- **Gap:** You don't own or represent a TPRM platform

**2. MANUFACTURER AUTHORIZATION REQUIRED**
- **Requirement:** "Valid software support service manufacturer's authorization or certificate for provision of software and software support services"
- **Your status:** No vendor partnerships for TPRM platforms documented
- **Cannot acquire:** Would need 3-6 months to establish vendor relationship, contract negotiation, certification training

**3. PLATFORM MUST EXIST AT BID TIME**
- **Requirement:** "At the time of submitting a tender, the platform must comply with all mandatory requirements"
- **Reality:** Platform must be ready-to-use, not buildable
- **Your offering:** Development skills, not finished platforms

**4. ISO 27001/SOC2 TYPE II CERTIFICATION (SERVICE)**
- **NFR_1.3.2:** "The service must be ISO27001 or SOC2 Type II certified... Subject service must be within the SOA of the certification"
- **Your status:** No ISO 27001/SOC2 certification
- **Gap:** 6-12 months minimum to achieve certification
- **Note:** This is for the SERVICE itself, not just the hosting provider

**5. SPECIFIC TPRM PLATFORM FEATURES**
- **Required capabilities:**
  * Automated vendor risk scoring algorithms
  * Third/fourth-party auto-detection
  * Pre-built security questionnaires (ISO, NIST, GDPR, NIS2)
  * Attack surface scanning infrastructure
  * Typosquatting detection databases
  * Threat intelligence feeds integration
  * Continuous vulnerability databases
- **Development timeline:** 12-18 months for MVP, 24+ months for enterprise-grade
- **Your foundation:** No TPRM/attack surface monitoring expertise

**6. 100% PRICE COMPETITION**
- **Evaluation:** Lowest cost wins (no quality/competence scoring)
- **Competitors:** Established vendors like:
  * SecurityScorecard
  * BitSight
  * RiskRecon
  * Panorays
  * UpGuard
  * Black Kite
  * CyberGRX
- **Pricing:** Enterprise SaaS licenses typically €50k-150k/year for this scale
- **Your position:** Cannot compete on price without existing platform + economies of scale

**7. ENTRA ID (MICROSOFT ENTRA ID) INTEGRATION**
- **NFR_1.1.1-1.1.4:** Mandatory EntraID SSO integration
- **Requirement:** Production-ready integration, not development project
- **Gap:** Would need Microsoft partner program enrollment, integration testing, compliance validation

**8. BUSINESS MODEL MISMATCH**
- **This procurement:** Platform vendor supplies finished SaaS solution
- **Your business:** Custom software development and integration services
- **Analogy:** Like bidding to supply Microsoft Office when you're a web developer

---

## CAPABILITY MATCHING

### Your Strengths (NOT Applicable Here)

**Development Skills (Irrelevant for Platform Resale):**
- ✅ Python development (but platform is pre-built SaaS)
- ✅ Database design (PostgreSQL, MySQL) - not needed for SaaS procurement
- ✅ API integration experience - could help with platform configuration, but not sufficient
- ✅ Government system experience (Justice Ministry) - compliance awareness

**Project Management:**
- ✅ Requirements analysis, technical documentation
- ✅ Client communication and stakeholder management
- But: This is a product sale, not a project

### Critical Gaps (Insurmountable)

**Platform Ownership:**
- ❌ No TPRM/attack surface monitoring platform owned or resold
- ❌ No vendor authorization from SecurityScorecard, BitSight, Panorays, etc.
- ❌ Cannot develop compliant platform in 4 days (deadline)

**Certifications:**
- ❌ No ISO 27001 certification
- ❌ No SOC2 Type II certification
- ❌ No TPRM platform-specific certifications

**TPRM Domain Expertise:**
- ❌ No vendor risk scoring methodologies
- ❌ No attack surface scanning infrastructure
- ❌ No threat intelligence feed partnerships
- ❌ No vulnerability database access
- ❌ No typosquatting detection systems

**Infrastructure:**
- ❌ No SaaS hosting infrastructure (ISO 27001 certified)
- ❌ No EU-hosted GDPR-compliant data centers
- ❌ No 24/7 monitoring and support organization

**Business Relationships:**
- ❌ No established vendor partnerships with TPRM platform manufacturers
- ❌ No reseller agreements with authorized distributors

---

## COMPETITIVE LANDSCAPE

### Likely Competitors

**International TPRM Platform Vendors:**
1. **SecurityScorecard** - Market leader, automated ratings
2. **BitSight** - Continuous monitoring, breach intelligence
3. **Panorays** - Third-party risk platform with automated assessments
4. **RiskRecon** - Mastercard company, financial sector focus
5. **UpGuard** - Attack surface monitoring + vendor risk
6. **Black Kite** - Automated cyber risk assessments
7. **CyberGRX** - Exchange network for vendor risk data

**Regional Resellers:**
- Nordic/Baltic cybersecurity vendors with reseller agreements
- Managed security service providers (MSSPs) offering platform licenses

**Their Advantages:**
- Established platforms with years of development (not starting from zero)
- Manufacturer authorization and support contracts
- ISO 27001/SOC2 Type II certifications already in place
- Threat intelligence partnerships and vulnerability databases
- Proven track record with enterprise clients
- 100% price competition benefits established vendors (economies of scale)

**Your Disadvantage:**
- No platform to offer (4 days to deadline - cannot build or acquire authorization)

---

## STRATEGIC ASSESSMENT

### Why You Cannot Win This

**Structural Barriers (Insurmountable in 4 days):**

1. **No Product:** You don't manufacture or resell TPRM platforms
2. **No Vendor Authorization:** Cannot obtain manufacturer certificate in 4 days
3. **No Certification:** ISO 27001/SOC2 Type II takes 6-12 months minimum
4. **Platform Must Exist:** Cannot bid with development proposal - platform must be ready at submission
5. **Wrong Business Model:** Developer bidding on product resale = auto-disqualification

**Even With Unlimited Time:**

Building a competitive TPRM platform from scratch would require:
- **Development:** 24-36 months for enterprise-grade platform
- **Threat Intelligence:** Partnerships with threat data providers (6-12 months negotiation)
- **Scanning Infrastructure:** Attack surface monitoring infrastructure (12+ months)
- **Vulnerability Databases:** Access to CVE feeds, exploit databases (licensing + integration)
- **Risk Algorithms:** Proprietary risk scoring methodologies (12-18 months R&D)
- **Certifications:** ISO 27001 (6-12 months), SOC2 Type II (6-12 months)
- **Team:** 8-15 cybersecurity specialists (TPRM domain experts, not generalist developers)
- **Investment:** €500k-2M for MVP, €2M-5M for enterprise platform
- **Market:** Competing with established vendors with 5-10 years head start

**Alternative Partnership Route (Also Not Viable in 4 Days):**
- Contact TPRM vendors for reseller agreements: 2-3 months negotiation
- Complete vendor certification training: 1-2 months
- Establish support infrastructure: 1-2 months
- Obtain manufacturer authorization: Requires proven track record

### Opportunity Cost

**Time investment if attempted:** 40-60 hours
- Understanding TPRM domain
- Researching vendor partnerships
- Attempting to acquire authorization (will fail)
- Preparing impossible bid (will be rejected)

**Better use of time:**
- Continue Java/Spring Boot skill refresh for procurement 9407944 (CONSIDER status)
- Pursue other development procurements where your skills match
- Build team partnerships for future development opportunities

---

## RECOMMENDATION

### Decision: SKIP (Firm)

**Reasoning:**
1. **Product mismatch:** Requires SaaS platform vendor, you are developer
2. **Certification gap:** ISO 27001/SOC2 Type II for service required (6-12 months)
3. **Authorization gap:** Manufacturer certificate required (cannot obtain in 4 days)
4. **Platform gap:** Solution must exist at bid time (no development allowed)
5. **Domain gap:** TPRM/attack surface monitoring is specialized cybersecurity field
6. **Price competition:** 100% cost-based = established vendors with economies of scale win
7. **Winning probability:** <1% (effectively zero - bid would be non-compliant)

**Similar Past Decision:**
- **Procurement 9526064 (CRM Software):** Also SKIP for same reason (product vendor required, not developer)
- **Reasoning:** "This is a product/vendor procurement, not a development project. User lacks: CRM product licensing rights, vendor authorization, ready-made CRM system."

**This is the same situation:** Platform vendor procurement, not development opportunity.

---

## ALTERNATIVE STRATEGIES

### None Viable for This Procurement

**Why Partnership Won't Work:**
- 4 days to deadline = insufficient time for vendor negotiations
- Manufacturer authorization requires established relationship (3-6 months minimum)
- Certification requirements (ISO 27001/SOC2) cannot be met by partnering with developer
- 100% price competition = vendor will bid directly (no margin for intermediary)

### Focus on Better-Fit Opportunities

**Current Pipeline:**
- **Procurement 9407944 (Java/Spring Boot):** CONSIDER status (50-60% feasibility)
  * Development project (your core strength)
  * No product vendor requirement
  * Technology matches your foundation
  * Team assembly feasible
  * Priority: Refresh Java skills, identify 2-3 partner developers

**Future Procurement Targets:**
- Software development projects (not product sales)
- System integration work (your experience)
- API development (your strength)
- Database-centric applications (your expertise)
- Government/public sector (your track record)

**Avoid:**
- SaaS platform resale procurements
- Product vendor selections (CRM, ERP, TPRM, etc.)
- Certifications-heavy opportunities (ISO 27001, SOC2) where service certification required
- Hardware/infrastructure procurements
- 100% price-based competitions where you lack economies of scale

---

## LESSONS LEARNED

### Procurement Type Recognition

**RED FLAGS for SKIP:**
1. "Right to use" / "License" language = product sale, not development
2. "Manufacturer authorization required" = vendor resale, not custom build
3. "Platform must exist at bid time" = no development allowed
4. Service certification required (ISO 27001 for the product) = established vendor only
5. 100% price-based evaluation = commoditized product, no room for custom development value
6. Specific platform features list = pre-built solution expected

**GREEN FLAGS for PURSUE:**
1. "Development services" / "Custom software" = development project
2. Technology stack specified (Java, Python, React) = programming work
3. "Analysis, design, implementation" phases = full SDLC project
4. Team competence scoring criteria = quality matters, not just price
5. "Integration with existing systems" = your API/integration strength
6. Hourly rate or time-and-materials = service procurement, not product sale

### Business Model Clarity

**You are:**
- Software developer (custom solutions)
- System integrator (connecting systems)
- Technical consultant (analysis and design)
- Project manager (delivery coordination)

**You are NOT:**
- SaaS platform vendor
- Product manufacturer
- Certified reseller (without manufacturer agreements)
- Infrastructure provider (data centers, hosting)
- Cybersecurity platform specialist

**Stay in Your Lane:**
- Bid on development projects
- Skip product/platform procurements
- Partner when team skills needed
- Avoid certification-heavy procurements where you lack credentials

---

## NEXT STEPS

### Immediate Actions (Next 48 Hours)

**1. SKIP This Procurement (Confirmed)**
- No bid submission
- No further time investment
- Document decision for future reference

**2. Focus on Procurement 9407944 (Java/Spring Boot - CONSIDER)**
- Continue Java skill refresh
- Research Estonian Java developer communities
- Identify 2-3 potential team partners
- Review X-Road integration documentation
- Check deadline and prepare bid timeline

**3. Monitor Pipeline for Development Opportunities**
- Check riigihanked.riik.ee weekly for new procurements
- Filter for software development services
- Avoid product/platform/license procurements
- Prioritize government/public sector (your strength)

**4. Strengthen Core Capabilities**
- Java/Spring Boot refresh (for 9407944 and similar)
- X-Road integration learning (Estonian e-government standard)
- API security best practices (recurring requirement)
- OWASP compliance understanding (frequently required)

### Long-Term Strategic Adjustments

**1. Build Developer Network**
- Connect with Estonian Java/Python developers
- Form informal partnerships for team-based bids
- Share procurement opportunities
- Mutual support for skill gaps

**2. Target Your Niche**
- Government/public sector development projects
- Database-centric applications (your strength)
- System integration work (your experience)
- API development and microservices
- Legacy system modernization (your Justice Ministry experience)

**3. Avoid Mismatches**
- Product vendor procurements (CRM, ERP, TPRM, etc.)
- Platform-as-a-Service sales
- Certification-heavy requirements (ISO 27001 service certification)
- 100% price-based competitions where you lack product economies of scale
- Highly specialized domains (cybersecurity platforms, attack surface monitoring)

**4. Consider Strategic Certifications (Long-Term)**
- ISO 27001 certification if pursuing consulting work (6-12 months)
- AWS/Azure certifications if cloud work increases
- TOGAF or enterprise architecture if targeting consulting
- But: Only if clear ROI from multiple procurement opportunities

---

## CONCLUSION

**SKIP this procurement firmly.** This is a product vendor selection for an existing SaaS platform, not a development project. You lack:
1. TPRM platform ownership or reseller authorization
2. Manufacturer certificates for platform and support
3. ISO 27001/SOC2 Type II certification for the service
4. TPRM/attack surface monitoring domain expertise
5. Viable path to compliance within 4-day deadline

**Winning probability: <1% (effectively zero)**

This is identical to procurement 9526064 (CRM software - SKIP): Both require product vendors with existing platforms, not developers offering to build solutions.

**Redirect focus** to development procurements like 9407944 (Java/Spring Boot backend - CONSIDER status, 50-60% feasibility), where your software development skills are the primary requirement, not platform ownership.

**Document this assessment** as template for rapid SKIP decisions on future product/platform procurements. Key lesson: **"Manufacturer authorization required" + "Platform must exist" + "Service certification" = SKIP for developer without vendor partnerships.**

---

**Assessment completed:** 2025-11-28  
**Assessor:** AI Assistant  
**Based on:** Procurement documents (14 files), knowledge base analysis, comparative procurement history  
**Confidence level:** HIGH (clear structural mismatch, no ambiguity)
