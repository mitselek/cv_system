# E-ITS (Eesti Infoturbestandard) Deep Dive Research

**Research Date:** 2026-01-02

**Purpose:** Comprehensive understanding of E-ITS requirements for EKA IT Department Head interview preparation

**Source:** https://eits.ria.ee/ (Riigi Infosüsteemi Amet - RIA)

---

## Executive Summary

**E-ITS** (Estonian Information Security Standard) is the **mandatory** information security framework for all Estonian public sector organizations, including universities like EKA. It's based on the German BSI IT-Grundschutz methodology and provides a comprehensive approach to information security management.

**Critical Understanding:** E-ITS is NOT just IT security - it's an **Information Security Management System (ISMS)** that requires:

- Top management commitment (not just IT department)
- Risk-based approach to all business processes
- Comprehensive documentation and policy framework
- Regular audits and continuous improvement
- Integration into organizational culture

---

## What is E-ITS?

### Legal Foundation

- **Governing Law:** Küberturvalisuse seadus (Cybersecurity Act) § 3
- **Regulatory Authority:** Riigi Infosüsteemi Amet (RIA)
- **Mandate:** ALL public sector organizations must comply
- **Latest Version:** 2024 (updated August 28, 2025)
- **Minister's Decree:** No. 101 (December 16, 2022)

### Core Components (3 Main Documents)

1. **E-ITS Nõuded infoturbe halduse süsteemile** (ISMS Requirements)

   - Establishes requirements and guidelines for ISMS
   - 11 main sections covering lifecycle from planning to audit

2. **E-ITS Etalonturbe kataloog** (Reference Security Catalog)

   - Pre-analyzed security measures organized in modules
   - Best practices for typical threats and assets
   - 800+ specific security measures

3. **E-ITS Auditeerimiseeskiri** (Audit Guidelines)
   - Instructions for external audit
   - Compliance verification process

### International Equivalence

- **Based on:** German BSI IT-Grundschutz
- **Compatible with:** ISO/IEC 27001 (achieving E-ITS standard-level compliance = ISO 27001 general alignment)
- **Estonian-specific:** Tailored to Estonian legal framework and language

---

## Core Concepts & Terminology

### CIA Triad (Foundation)

- **C** - Konfidentsiaalsus (Confidentiality)
- **I** - Terviklus (Integrity)
- **A** - Käideldavus (Availability)

### Key Terms

| Estonian                         | English                                | Definition                                                                 |
| -------------------------------- | -------------------------------------- | -------------------------------------------------------------------------- |
| Infoturbe halduse süsteem (ISMS) | Information Security Management System | Systematic approach to managing information security                       |
| Infoturvapoliitika               | Information Security Policy            | Central security document defining direction and goals                     |
| Kaitseala                        | Protection scope                       | Elements to be protected (infrastructure, processes, personnel, tech)      |
| Sihtobjekt                       | Target object                          | Any asset requiring protection (process, application, component, building) |
| Kaitsetarve                      | Protection requirement                 | Need to protect assets based on value (normal, high, very high)            |
| Turbeviis                        | Security approach                      | Method for implementing E-ITS (basic, standard, core)                      |
| Etalonturbe                      | Reference security                     | Pre-analyzed security measures for typical threats                         |
| Meetme rakendusplaan (IMR)       | Measure Implementation Plan            | Document listing and justifying security measures                          |

### Protection Requirement Levels

1. **Normaalne** (Normal)

   - Limited, manageable damage potential
   - Reference security measures sufficient
   - **Approach:** Põhiturve (Basic Security)

2. **Suur** (High)

   - Serious damage potential
   - Reference measures may not suffice
   - External risk analysis required
   - **Approach:** Standardturve (Standard Security)

3. **Väga Suur** (Very High)
   - Catastrophic damage potential
   - Threatens organizational existence
   - Mandatory comprehensive risk analysis
   - Custom measures required
   - **Approach:** Standardturve with extensive external risk analysis

---

## Implementation Approaches (Turbeviis)

### 1. Põhiturve (Basic Security)

- **When:** Normal protection requirements
- **What:** Essential baseline measures first
- **Goal:** Foundation for progression to standard security
- **Who:** Small organizations, starting implementation
- **Catalog:** "Esmased turvameetmed" (Primary Security Measures)

### 2. Standardturve (Standard Security)

- **When:** High or very high protection requirements
- **What:** Basic + standard measures + external risk analysis
- **Goal:** Comprehensive security aligned with ISO 27001
- **Who:** Most public sector organizations (like universities)
- **Requirements:**
  - All basic measures implemented
  - Standard measures applied
  - External risk analysis for high-risk objects
  - Optional: Advanced measures for very high requirements

### 3. Tuumikuturve (Core Security)

- **When:** Specific protection scope, not whole organization
- **What:** Focused protection for critical processes only
- **Goal:** Targeted security for highest-value assets
- **Who:** Organizations with clear critical infrastructure subset

**EKA Reality:** Likely should pursue **Standardturve** given:

- Public sector university = mandatory compliance
- Educational processes (student data = high protection requirement)
- Research data (potentially high or very high protection)
- International partnerships (T4EU) = external data sharing risks
- Financial systems, HR data = high protection requirements

---

## ISMS Lifecycle (Plan-Do-Check-Act)

E-ITS follows continuous improvement cycle:

```text
┌──────────────────────────────────────┐
│  1. INITIATE & COMMIT                │
│  - Top management commitment         │
│  - Appoint Information Security Lead │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│  2. PLAN                             │
│  - Security policy                   │
│  - Security objectives               │
│  - Protection scope definition       │
│  - Risk assessment                   │
│  - Measure selection                 │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│  3. IMPLEMENT (DO)                   │
│  - Apply security measures           │
│  - Document everything               │
│  - Train staff                       │
│  - Resource allocation               │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│  4. MONITOR (CHECK)                  │
│  - Ongoing operations                │
│  - Incident management               │
│  - Effectiveness measurement         │
│  - Change response                   │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│  5. IMPROVE (ACT)                    │
│  - Process improvement               │
│  - Independent review                │
│  - Internal audit                    │
│  - Management review                 │
└──────────┬───────────────────────────┘
           │
┌──────────▼───────────────────────────┐
│  6. AUDIT (Optional but Recommended) │
│  - External E-ITS audit              │
│  - Compliance verification           │
│  - Audit conclusion                  │
└──────────────────────────────────────┘
```

---

## Top Management Responsibilities (Critical!)

**This is NOT just an IT project** - E-ITS explicitly requires **top management commitment**.

### Management Must:

1. **Initiate** the information security process
2. **Appoint** Information Security Lead (Infoturbejuht)
3. **Approve** security policy, objectives, and resource allocation
4. **Receive** regular security reports on:

   - Security risks and their impacts
   - Security incidents
   - Regulatory requirements and compliance status
   - Current security state
   - Process improvement recommendations
   - Stakeholder commitments and feedback

5. **Accept** residual risks explicitly and regularly
6. **Integrate** security into ALL business processes

### What This Means for EKA

- **Rector** must be committed, not just IT department
- E-ITS implementation requires **board-level** approval
- IT department head role includes **reporting to top management**
- Security policy must come from **institution leadership**, not IT
- Budget and resources come from **university budget**, not just IT budget

**Interview Implication:** When discussing E-ITS, frame it as **organizational transformation**, not just IT project. Emphasize need for **management buy-in** and **cross-functional collaboration**.

---

## Implementation Requirements (Section-by-Section)

### Section 5: General Information Security Process

- Top management initiates process
- Appoint Information Security Lead (Infoturbejuht)
- Management commitment documented
- Regular security training for ALL staff
- Security awareness integrated into organizational culture

### Section 6: Planning and Design

**6.1 Security Policy (Infoturvapoliitika)**

- Central security document
- Defines organization's security goals and principles
- Must consider:
  - Organizational objectives and strategy
  - Legal framework (GDPR, sector-specific regulations)
  - Client/partner requirements
  - Industry security standards
- Approved by top management
- Reviewed at least annually

**6.2 Security Objectives (Infoturvaeesmärgid)**

- Realistic, practical, measurable, time-bound
- Aligned with business processes
- Based on:
  - Business process descriptions
  - Asset inventory
  - Protection requirements (C-I-A assessment)
  - Risk analysis
  - Existing security documentation

**6.3 Security Organization**

- Define roles and responsibilities
- Role competency requirements
- Authority and accountability
- Internal/external communication structure
- Documented and communicated to staff

**Example Roles:**

- Information Security Lead (Infoturbejuht)
- Process Owners (Protsessijuhid)
- IT Security Lead (IT-turbejuht) - for large orgs
- Data Protection Officer (already exists at EKA: Bert Blös in Rector's Office)
- IT Coordination Committee

**6.4 Security Training**

- All staff must receive regular security training
- Motivate staff to follow security requirements
- Handle information and tools correctly
- Avoid risky behavior
- Respond appropriately to incidents

**6.5 Resource Allocation**

- Financial and non-financial resources
- Staff time allocation for security duties
- Management must accept security workload

**6.6 Management Approval**

- Formal sign-off on policy, objectives, resources

**6.7 Documentation**

- All policies, procedures, decisions documented
- Version control required
- Reviewed annually
- Accessible to authorized personnel
- Protected from unauthorized access

### Section 7: Risk Management

**7.1 Risk Management Fundamentals**

- Define protection requirement determination principles
- Define risk acceptance criteria
- Protection requirements (C-I-A) for all target objects
- Document risk management process

**7.2 Reference Security Modeling (Etalonturbe modelleerimine)**

- Map each target object to catalog module(s)
- Consider security approach, protection level, lifecycle
- All process modules must be included (or exclusions justified)
- For normal protection: implement basic measures first
- For high/very high: basic + standard + external risk analysis

**7.3 External Risk Analysis**

- Required for:
  - High or very high protection requirements
  - No suitable catalog module exists
  - Usage differs from catalog descriptions
  - Reference measures insufficient (residual risk not acceptable)
  - Object critical to multiple organizational processes
- Document process, circumstances, results
- Define additional measures based on protection needs

### Section 8: Implementing Security Measures

**8.1-8.3 Implementation**

- Technical measures for all target objects
- Organizational measures integrated into ALL processes
- Process owners responsible (IT Security Lead coordinates/advises)

**8.4 Measure Assessment**

- One-time and recurring costs
- Suitability, feasibility, sufficiency
- Effectiveness and interdependencies

**8.5 Measure Implementation Plan (IMR)**
Must document:

- Measures to be applied (with IDs from catalog)
- Implementation status (not started, in progress, complete, not applicable)
- Justification (how implemented, why excluded, what's partial)
- Responsible parties
- Implementation deadlines
- Next review dates

**8.6-8.8 Execution**

- Management accepts residual risks and approves plan
- Measures implemented per plan
- Recurring activities must be traceable, comparable, consistent, timely

### Section 9: Ongoing Operations

**9.1 Monitoring & Measurement**

- Objective achievement
- Measure effectiveness
- Resource utilization

**9.2 Change Management**

- Respond to changes in:
  - Organizational objectives
  - Regulations and contracts
  - Security environment
- Process owners ensure timely information flow

**9.3 Incident Management**

- Monitor system/process operations
- Respond to significant security events
- Register important incidents

**9.4 Continuous Improvement**

- Use monitoring, reviews, audits to identify improvements
- Feed results back into risk management

**9.5 Communication**

- Report to:
  - Top management
  - Role holders
  - All staff
  - External stakeholders

### Section 10: Process Improvement

**10.1 Improvement Activities**

- Periodic review of process, policy, objectives
- Reasons for improvement:
  - Organizational changes
  - Policy/objective changes
  - Security environment changes
  - Regulatory changes
  - Scope/protection requirement changes
  - Incident/audit findings

**10.2 Independent Review**

- Regular independent assessment
- Can be internal audit or external expert
- Assess compliance with:
  - E-ITS requirements
  - Organization's security policy
- Avoid conflict of interest (reviewer ≠ implementer)
- Document results for improvement and traceability

### Section 11: Auditing

**11.1-11.3 E-ITS Audit**

- Assesses ISMS compliance with E-ITS
- Evaluates sufficiency for business process protection
- Required for:
  - **Mandatory** - legal/regulatory obligations
  - **Contractual** - partner requirements
  - **Voluntary** - organizational goals

**11.4 Audit Conclusion**

- Formal evidence of security effectiveness
- Can be used for:
  - Regulatory compliance demonstration
  - Partner confidence
  - Continuous improvement input

---

## Reference Security Catalog (Etalonturbe kataloog)

### Structure

The catalog contains **800+ pre-analyzed security measures** organized into **modules**.

### Module Types

1. **Process Modules (ISMS.\*)**

   - Security management
   - Organization and personnel
   - MANDATORY for all organizations

2. **System Modules**
   - Applications
   - IT systems
   - Infrastructure
   - Networks
   - Industrial control systems
   - Applied as needed based on scope

### Measure Hierarchy

Each module contains measures at different levels:

- **Põhimeetmed** (Basic Measures) - Essential baseline, priority 1
- **Standardmeetmed** (Standard Measures) - Comprehensive protection, priority 2
- **Kõrgmeetmed** (Advanced Measures) - For very high protection requirements

### Example Modules (Relevant to EKA)

- **ISMS.1** - Security Management
- **ORP.1** - Organization and Human Resources
- **ORP.2** - Personnel
- **ORP.3** - Awareness and Training
- **ORP.4** - Identity and Access Management
- **CON.1** - Cryptography
- **OPS.1.1.2** - Archiving
- **OPS.1.1.3** - Patch Management
- **OPS.1.1.5** - Logging
- **OPS.1.1.6** - Data Backup
- **OPS.2.1** - Outsourcing
- **APP.1.1** - E-mail/Groupware
- **APP.3.1** - Web Applications
- **APP.3.2** - Web Servers
- **APP.3.3** - Content Management Systems
- **APP.3.6** - DNS Servers
- **APP.4.3** - Relational Databases
- **APP.5.1** - Groupware
- **SYS.1.1** - General Servers
- **SYS.1.3** - Unix Servers
- **SYS.2.1** - General Clients
- **SYS.2.2.3** - Clients under Linux/Unix
- **SYS.2.3** - Clients under macOS
- **SYS.2.4** - Clients under Windows
- **SYS.3.1** - Laptops
- **SYS.3.2.2** - Smartphones and Tablets
- **SYS.4.3** - Embedded Systems
- **NET.1.1** - Network Architecture and Design
- **NET.1.2** - Network Management
- **NET.2.1** - WLAN Operation
- **NET.2.2** - WLAN Usage
- **NET.3.1** - Routers and Switches
- **NET.3.2** - Firewalls
- **NET.4.1** - TLS-based Connections
- **INF.1** - General Building
- **INF.2** - Data Center
- **INF.3** - Electrotechnical Infrastructure
- **INF.9** - Mobile Workplace
- **INF.10** - Home Office

---

## Implementation Resources & Tools

### E-ITS Support Application (Tugirakendus)

- **URL:** https://www.eits.ria.ee/webapp/volur_2024_latest.html
- **Purpose:** Web-based tool to help organizations start implementation
- **Features:**
  - Browse catalog
  - Generate measure implementation plans
  - Export documentation
  - Track progress

### Organizational Maturity Assessment

- **URL:** https://hindamine.eits.ria.ee/
- **Purpose:** Self-assessment of security management maturity
- **Use:** Identify current state and improvement areas

### E-Courses

- **"Infoturbest juhtidele"** (Security for Managers)
- **Platform:** Digiriigi Akadeemia
- **URL:** https://digiriigiakadeemia.ee/
- **Target:** Top management and executives

### Documentation Templates

- Security policy templates
- Procedure guidelines
- Implementation plan formats
- Available through E-ITS portal

### External Consultants

- RIA maintains list of certified E-ITS consultants
- Can assist with:
  - Implementation planning
  - Risk analysis
  - Documentation
  - Audit preparation
  - Training

---

## Timeline & Effort Estimation

### Small University (EKA-sized) Realistic Timeline

**Phase 1: Preparation (2-3 months)**

- Management commitment secured
- Information Security Lead appointed (IT head)
- Initial training completed
- High-level scope defined

**Phase 2: Planning (4-6 months)**

- Security policy drafted and approved
- Business processes documented
- Asset inventory compiled
- Protection scope defined
- Target objects identified and assessed
- Security objectives set
- Risk assessment framework established

**Phase 3: Implementation - Basic Security (6-12 months)**

- Basic measures from catalog applied
- Documentation created
- Staff training conducted
- Technical measures deployed
- Organizational procedures established

**Phase 4: Implementation - Standard Security (12-18 months additional)**

- Standard measures applied
- External risk analysis for high-value assets
- Advanced measures for critical systems
- Full documentation completed
- Internal review conducted

**Phase 5: Audit Preparation & Execution (3-6 months)**

- Independent internal review
- Gap analysis and remediation
- External audit scheduled
- Audit conducted
- Conclusion received

**Total Timeline: 2.5-4 years** for full standard-level implementation in small university

**Effort:**

- **IT Department:** 30-50% of one FTE continuously
- **Information Security Lead:** 20-30% of one FTE (likely IT head)
- **Process Owners:** 10-20% of time during implementation
- **Management:** Quarterly reviews + policy approval
- **All Staff:** Annual training (4-8 hours)
- **External Consultant:** Optional but recommended (50-100 hours total)

### What Makes This HARD for Small Teams

1. **Documentation Burden** - Everything must be documented
2. **Cross-Functional Nature** - IT can't do this alone
3. **Continuous Effort** - Not a one-time project
4. **Culture Change** - Security awareness for ALL staff
5. **Resource Constraints** - Small teams wear many hats

---

## Audit Process

### Types of Audits

1. **Mandatory Audit**

   - Required by law or regulation
   - Public sector organizations typically required

2. **Contractual Audit**

   - Required by partners or service agreements
   - Common in international partnerships

3. **Voluntary Audit**
   - Organization chooses to verify compliance
   - Demonstrates commitment
   - Can be used for ISO 27001 alignment

### Audit Scope Levels

- **Põhiturve audit** (Basic Security) - Basic measures compliance
- **Standardturve audit** (Standard Security) - Full E-ITS compliance (≈ ISO 27001)

### Audit Process

1. **Pre-Audit**

   - Organization requests audit
   - Auditor reviews documentation
   - Audit plan created

2. **On-Site Audit**

   - Document review
   - Interviews with management, process owners, staff
   - Technical verification
   - Observation of procedures

3. **Audit Report**

   - Findings documented
   - Non-conformities identified
   - Recommendations provided

4. **Audit Conclusion**

   - Positive: Compliance confirmed
   - Conditional: Minor issues, re-audit needed
   - Negative: Major gaps, significant work required

5. **Follow-Up**
   - Address findings
   - Re-audit if needed
   - Continuous improvement

### Certified Auditors

- RIA maintains list of certified E-ITS auditors
- Must use certified auditor for official audit conclusion
- Can use consultants for pre-audit/gap analysis

---

## EKA-Specific Considerations

### Existing Foundation at EKA

**Positive Assets:**

1. **Data Protection Officer** - Bert Blös (Rector's Office) already in place - coordinate with him on data protection aspects

   - Essential for E-ITS (GDPR compliance overlaps)
   - Can lead data protection aspects
   - Expertise in privacy = foundation for security

2. **IT Team** - 5 people total

   - Robert Luig (senior specialist) - likely lead technical implementation
   - Support specialists - can implement technical measures
   - Team already manages infrastructure

3. **Digital Systems in Place**
   - Tahvel (student info system)
   - Moodle (LMS)
   - Google Workspace (email)
   - Document management (WebDesktop)
   - Digital repository (Digivaramu)
   - **These ALL need E-ITS assessment and protection!**

### Critical Challenges for EKA

1. **Small Team, Big Scope**

   - 5 IT staff for 1,144 students + 279 employees + ~721 hourly staff
   - E-ITS requires 30-50% FTE continuously
   - Team likely fully saturated with operations
   - **Risk:** No capacity for strategic E-ITS work

2. **T4EU International Complexity**

   - 10-university alliance
   - Cross-border data sharing
   - Multiple jurisdictions (EU, but different implementations)
   - Student/staff mobility data
   - Research collaboration data
   - **Risk:** High or very high protection requirements likely

3. **Legacy Infrastructure Unknown**

   - 2012 infrastructure may still be in use
   - 13 years of technical debt possible
   - Security patches, OS updates, software EOL?
   - **Risk:** Major remediation needed before E-ITS possible

4. **Limited Budget**

   - Public sector university
   - Procurement regulations
   - Competing priorities (teaching, research, facilities)
   - **Risk:** Insufficient resources for proper implementation

5. **Cultural Resistance**
   - Academic freedom culture
   - Faculty autonomy
   - "Security as inconvenience" mindset
   - **Risk:** Low adoption, weak security culture

### Opportunities at EKA

1. **Clean Slate Advantage**

   - No prior E-ITS implementation = no bad habits
   - Can implement correctly from start
   - Your 2012 experience = understanding of current state foundation

2. **Management Support Potential**

   - University leadership may understand compliance necessity
   - GDPR already familiar concept
   - International partnerships (T4EU) create business case
   - Research funding may require security compliance

3. **Existing Processes**

   - GDPR compliance already underway (Bert Blös)
   - Quality management systems may exist (accreditation)
   - IT governance structures may be in place
   - **Leverage:** Build E-ITS on existing management systems

4. **Inter-University Cooperation**
   - Job requirement: "ülikoolide vahelises IT koostöö töörühmades osalemine"
   - Other Estonian universities implementing E-ITS
   - Knowledge sharing opportunities
   - Shared challenges, shared solutions
   - **Leverage:** Learn from University of Tartu, TalTech, etc.

---

## Interview Strategy for E-ITS Discussion

### Opening Positioning

**BAD:** "I don't have E-ITS experience but I'm willing to learn."

**GOOD:** "I'm aware that E-ITS is mandatory for public sector organizations like EKA. While I don't have direct implementation experience, I understand that E-ITS is fundamentally an organizational transformation requiring top management commitment, cross-functional collaboration, and a systematic approach to risk management. As IT department head, my role would be to coordinate technical implementation while ensuring management understands their essential leadership role in the process."

### Key Messages to Convey

1. **E-ITS is Management Responsibility, Not Just IT**

   - "E-ITS explicitly requires top management commitment. The rector and board must lead this initiative - IT department coordinates, but we can't do it alone."
   - Shows understanding that this isn't just an IT project

2. **Foundation Exists at EKA**

   - "EKA has critical foundations already: Bert Blös as data protection officer, existing digital systems, and international partnership security awareness through T4EU."
   - Shows you've done homework and see opportunities

3. **Realistic Implementation Approach**

   - "For an organization like EKA, reaching standard-level E-ITS compliance realistically takes 2.5-4 years with sustained effort. We should start with basic security (põhiturve) and build systematically toward full compliance."
   - Shows realistic expectations, not naive optimism

4. **External Support Will Be Needed**

   - "I'd propose working with an E-ITS certified consultant for initial planning and gap analysis, then leverage inter-university IT cooperation for ongoing knowledge sharing. This accelerates learning and reduces risk."
   - Shows pragmatic approach, willingness to seek expert help

5. **Resource Implications Must Be Addressed**
   - "E-ITS implementation requires approximately 30-50% of one FTE continuously, plus cross-functional involvement from process owners. We need to discuss how to create this capacity within current team size or whether additional resources are needed."
   - Shows business acumen and honesty about requirements

### Questions to Ask (Critical)

**About Current State:**

1. "What is EKA's current level of E-ITS compliance? Has any assessment been done?"
2. "Has there been any discussion at management level about E-ITS requirements?"
3. "Does Bert Blös (data protection officer) have any involvement in security management beyond GDPR?"
4. "What security incidents or concerns have been raised in recent years?"

**About Management Support:** 5. "How does the rector view information security? Is there awareness of E-ITS requirements at board level?" 6. "What budget exists or can be allocated for security initiatives beyond BAU operations?" 7. "Is there an IT governance structure or committee that addresses strategic IT matters?"

**About Team Capacity:** 8. "What percentage of the current IT team's time is consumed by reactive support versus strategic projects?" 9. "Has there been consideration of adding E-ITS/security-focused capacity to the team?" 10. "How does the university handle projects that require cross-functional involvement?"

**About Inter-University Cooperation:** 11. "What is EKA's level of engagement with other Estonian universities' IT cooperation working groups?" 12. "Are there any shared services or collaborative security initiatives with partner universities?" 13. "Has EKA learned from other universities' E-ITS implementations?"

**About Priorities:** 14. "Given E-ITS is mandatory for public sector, what is the university's timeline expectation for compliance?" 15. "How does security rank among other IT priorities like digital transformation and T4EU support?" 16. "Are there any external drivers (audits, partnerships, regulations) creating urgency for E-ITS?"

### Red Flags to Watch For

1. **"We need you to implement E-ITS quickly"**

   - Reality: 2.5-4 years minimum for proper implementation
   - Risk: Unrealistic expectations

2. **"This is an IT department responsibility"**

   - Reality: Requires top management and cross-functional effort
   - Risk: IT department set up to fail alone

3. **"We don't have budget for consultants or additional staff"**

   - Reality: Proper implementation requires resources
   - Risk: Impossible mandate without support

4. **"Security policies should not interfere with academic freedom"**

   - Reality: E-ITS requires organizational discipline
   - Risk: Cultural resistance will block implementation

5. **"Previous IT head didn't mention E-ITS"**
   - Reality: Mandatory requirement since 2022
   - Risk: Institution may be significantly behind on compliance

### Green Flags to Look For

1. **"Rector/board has discussed information security strategy"**

   - Shows management awareness and commitment

2. **"We've started GDPR compliance work with Bert Blös"**

   - Shows foundation exists and organization can handle security frameworks

3. **"We're open to external consultants for specialized needs"**

   - Shows realistic understanding of expertise gaps

4. **"We participate actively in inter-university IT cooperation"**

   - Shows collaborative approach and learning mindset

5. **"We understand this is a multi-year journey"**
   - Shows realistic expectations

---

## Bottom Line for Interview

### Your E-ITS Gap is Real BUT Not Disqualifying

**Why:**

1. **No one has full E-ITS implementation experience at universities yet** - it's relatively new (2022 decree, 2024 version)
2. **Your general IT security background transfers** - network security, system administration, infrastructure protection
3. **Your ISMS understanding is solid** - you grasp that this is organizational transformation
4. **Your willingness to learn and seek expert help is mature** - better than false confidence
5. **Your broader experience compensates** - 20+ years IT, public sector, university environment, team leadership

### Address the Gap Proactively

**Say This:**
"E-ITS implementation is one of my priority learning areas. I've researched the framework thoroughly - I understand it's based on BSI IT-Grundschutz, requires top management commitment, and involves systematic risk management across organizational processes. I've identified that EKA has foundational advantages including Bert Blös as data protection officer and existing digital systems. My approach would be to:

1. **Partner with certified E-ITS consultant** for initial assessment and planning
2. **Engage actively in inter-university IT cooperation** to learn from peers
3. **Build cross-functional E-ITS working group** with process owners and management
4. **Take phased approach** - basic security first, build toward standard compliance
5. **Ensure top management understands their essential leadership role**

I don't claim expertise I don't have, but I'm committed to acquiring it quickly with the right support structure."

### This Demonstrates:

- Intellectual honesty (not pretending to know what you don't)
- Research thoroughness (you've done deep homework)
- Strategic thinking (organizational approach, not just technical)
- Pragmatism (external help, peer learning, realistic timeline)
- Leadership (management engagement, cross-functional collaboration)
- Growth mindset (committed to learning)

---

## Conclusion

E-ITS is mandatory, complex, resource-intensive, and multi-year journey. Success requires:

1. Top management commitment and resources
2. Cross-functional collaboration across all processes
3. Systematic risk management approach
4. Comprehensive documentation
5. Continuous monitoring and improvement
6. Cultural transformation toward security awareness
7. External expertise where needed
8. Realistic timeline (2.5-4 years minimum)

For EKA IT department head role, E-ITS will be a **major strategic initiative**. It's not the only responsibility, but it's mandatory and will consume significant leadership attention. The role requires balancing E-ITS implementation with T4EU infrastructure support, digital transformation, team management, and daily operations - a challenging portfolio requiring strong prioritization and stakeholder management skills.

**Your advantage:** You understand the complexity realistically, not naively. This positions you as a credible leader who can set appropriate expectations and build necessary support structures, rather than someone who will over-promise and under-deliver.
