# Entu Platform Technology Audit

**Purpose:** Verify Entu platform qualifies as reference project and determine portfolio points

**Reference project requirements:**

- 2000+ contractor hours ✓ (likely exceeds - 15 years continuous development)
- Python-based: ⬜ TO VERIFY
- Client confirmation: ⬜ TO OBTAIN

---

## Technology Criteria Checklist (20 points max per project)

### 1. Publicly Available Application (4 points)

- **Status:** ✓ YES
- **Evidence:** <https://entu.ee>
- **Points:** 4

### 2. TARA/GovSSO Authentication (2 points)

- **Status:** ⬜ TO VERIFY
- **Question:** Do any Entu deployments use TARA or GovSSO for authentication?
- **Likely:** Possible for government client deployments
- **Points:** 0-2 (depends on verification)

### 3. PostgreSQL Database (2 points)

- **Status:** ⬜ TO VERIFY (likely YES)
- **Your expertise:** PostgreSQL documented in knowledge base
- **Assumption:** Entu likely uses PostgreSQL (verify architecture)
- **Points:** 0-2 (likely 2)

### 4. Docker Containerization (4 points)

- **Status:** ⬜ TO VERIFY
- **Current deployment:** Unknown
- **If NO:** Can be implemented (20-30 hours)
- **Points:** 0-4

### 5. Kubernetes Horizontal Scaling (2 points)

- **Status:** ⬜ TO VERIFY
- **Current deployment:** Unknown
- **If NO:** Can be implemented (15-20 hours)
- **Points:** 0-2

### 6. GitLab CI/CD Deployment (2 points)

- **Status:** ⬜ TO VERIFY
- **Current CI/CD:** Unknown (GitHub or GitLab?)
- **If NO:** Can be implemented (10-15 hours)
- **Points:** 0-2

### 7. X-Road Consumer (2 points)

- **Status:** ⬜ TO VERIFY
- **Question:** Do any Entu deployments consume X-Road services?
- **Likely:** Possible for government client deployments
- **Points:** 0-2

### 8. X-Road Provider (2 points)

- **Status:** ⬜ TO VERIFY
- **Question:** Do any Entu deployments provide X-Road services?
- **Likely:** Less common for content management platform
- **Points:** 0-2

---

## Current Estimated Points

**Confirmed:** 4 points (publicly available)  
**Likely:** +2 points (PostgreSQL)  
**Total baseline:** 6 points out of 20

**With DevOps implementation (Docker + K8s + GitLab):** +8 points = **14 points**  
**If TARA/X-Road documented:** +2-6 points = **16-20 points**

---

## Verification Action Items

### Step 1: Technology Stack Verification

- [ ] Check Entu GitHub repository: <https://github.com/entu> (if public)
- [ ] Review Entu documentation: <https://entu.ee>
- [ ] Check deployment documentation
- [ ] Identify backend programming language (Python?)
- [ ] Identify database (PostgreSQL?)
- [ ] Check containerization (Docker?)

### Step 2: Current Deployment Investigation

- [ ] How is Entu currently deployed? (VPS? Cloud? Containers?)
- [ ] Is there existing CI/CD? (GitHub Actions? GitLab CI?)
- [ ] Are there any Kubernetes deployments?

### Step 3: Client Deployment Features

- [ ] List all Entu client deployments
- [ ] Which clients use TARA/GovSSO authentication?
- [ ] Which clients integrate with X-Road?
- [ ] Document specific instances for portfolio

### Step 4: Hours Documentation

- [ ] Calculate total Entu development hours (2010-present)
- [ ] Select 1-3 major client projects with 2000+ hours each
- [ ] Prepare client contact list for confirmation letters

---

## Alternative: If Entu Does NOT Qualify

**Scenario:** Entu is not Python-based OR cannot reach 14+ points

**Backup options:**

1. **PÖFF platform:** Verify if Python-based (2021-2024, within 48 months)
2. **Other Python projects:** Search knowledge base for undocumented Python work
3. **Partnership route:** Find contractor with qualifying Python projects

---

## DevOps Enhancement Plan (if pursuing)

### If Docker/K8s/GitLab NOT currently used

**Implementation timeline:** Days 4-14 (60-85 hours)

**Docker containerization (Days 4-7):**

- [ ] Create Dockerfile for Entu application
- [ ] Configure environment variables
- [ ] Test container build and run locally
- [ ] Document container architecture
- [ ] Push to container registry (Docker Hub or private)

**Kubernetes deployment (Days 8-10):**

- [ ] Set up local K8s cluster (Minikube or K3s for testing)
- [ ] Create deployment.yaml manifest
- [ ] Create service.yaml manifest
- [ ] Create ingress.yaml manifest (if applicable)
- [ ] Test horizontal scaling (replicas ≥2)
- [ ] Document K8s architecture

**GitLab CI/CD pipeline (Days 11-13):**

- [ ] Create GitLab repository (or migrate from GitHub)
- [ ] Create .gitlab-ci.yml file
- [ ] Configure build stage (Docker image build)
- [ ] Configure test stage (automated tests)
- [ ] Configure deploy stage (K8s deployment)
- [ ] Test full pipeline end-to-end
- [ ] Document CI/CD process

**Documentation and evidence (Day 14):**

- [ ] Update technical documentation
- [ ] Take screenshots of running containers
- [ ] Screenshot K8s dashboard showing scaling
- [ ] Screenshot GitLab CI/CD pipeline
- [ ] Prepare portfolio evidence package

---

## Notes

_[Add investigation findings here]_

### Entu Platform Overview

- **Website:** <https://entu.ee>
- **Description:** Content management and data platform
- **Development period:** 2010-present (15 years)
- **Your role:** Architect/Analyst/Developer
- **Deployments:** 30+ organizations documented

### CRITICAL FINDING: Technology Evolution Timeline

**Original Platform (2010-2017):**

- **Language:** Python ✓
- **Database:** MySQL ✗ (NOT PostgreSQL = -2 points)
- **Repository:** https://github.com/entu/entu (archived)
- **Last Updated:** 2017-01-19
- **Status:** ARCHIVED

**Current Platform (2017-present):**

- **Language:** JavaScript/Node.js ✗ (NOT Python = DISQUALIFIED)
- **Database:** MongoDB ✗ (NOT PostgreSQL = DISQUALIFIED)
- **Repository:** https://github.com/entu (organization)
- **Status:** ACTIVE

### Procurement Qualification Analysis

**48-Month Window Requirement:** 2021-11-27 to 2025-11-27

**Python/MySQL Version:**

- Migration date: ~2017 (8 years ago)
- **Status:** ✗ OUTSIDE 48-month window
- **Result:** DISQUALIFIED (too old)

**Node.js/MongoDB Version:**

- Active period: 2017-present (within window)
- **Python requirement:** ✗ NO (JavaScript)
- **PostgreSQL requirement:** ✗ NO (MongoDB)
- **Result:** DISQUALIFIED (wrong technology stack)

### CONCLUSION

**Entu CANNOT be used as reference project because:**

1. **Original Python version** (2010-2017): Outside 48-month window
2. **Current Node.js version** (2017-present): Not Python, not PostgreSQL

**Final Score: 0 points**

Even with Python/MySQL historical context, the platform migration to Node.js/MongoDB in ~2017 means:

- The qualifying Python version is too old (8 years)
- The current version uses disqualifying technologies

**Action Required:** Pursue Partnership Route (see todo list)
