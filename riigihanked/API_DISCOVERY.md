# API Discovery Guide for riigihanked.riik.ee

## ✅ VERIFIED API ENDPOINTS

**Status:** Complete API workflow discovered and tested  
**Date:** 2025-11-27  
**Base URL:** `https://riigihanked.riik.ee/rhr/api/public/v1`  
**Authentication:** None required (public procurement data)

### Complete Document Download Workflow

#### 1. Get Latest Version ID

```bash
GET /procurement/{procurement_id}/latest-version
```

**Example:**

```bash
curl 'https://riigihanked.riik.ee/rhr/api/public/v1/procurement/9559644/latest-version'
```

**Response:**

```json
{ "value": 9618044 }
```

**Purpose:** Maps procurement ID to current version ID (procurements can have multiple versions due to amendments)

---

#### 2. Get Documents List

```bash
GET /proc-vers/{version_id}/documents/general-info
```

**Example:**

```bash
curl 'https://riigihanked.riik.ee/rhr/api/public/v1/proc-vers/9618044/documents/general-info'
```

**Response:**

```json
{
  "procurementDocuments": [
    {
      "procurementDocumentOldId": 18750020,
      "name": "Vastavustingimused",
      "fileName": "302778_vastavustingimused.pdf",
      "fileSize": 9479,
      "docSubtypeCode": "VASTAVUSTINGIMUSED",
      "statusCode": "PUBLISHED",
      "visibilityCode": "PUBLIC"
    }
  ]
}
```

**Key Fields:**

- `procurementDocumentOldId` - Use this for temp URL generation
- `fileName` - Original filename for saving
- `fileSize` - Size in bytes
- `docSubtypeCode` - Document type
- `visibilityCode` - Filter for "PUBLIC" documents

---

#### 3. Generate Temporary Download URL

```bash
GET /proc-vers/{version_id}/documents/{doc_id}/temp-url
```

**Example:**

```bash
curl 'https://riigihanked.riik.ee/rhr/api/public/v1/proc-vers/9618044/documents/18750020/temp-url'
```

**Response:**

```json
{
  "value": "/filetransfer/client/shared/file/47692eeb-ebf8-435e-9c11-adb7efaa71b5"
}
```

**Purpose:** Returns relative path with UUID token for actual file download (security measure)

---

#### 4. Download File

```bash
GET /filetransfer/client/shared/file/{uuid}
```

**Example:**

```bash
curl -o document.pdf 'https://riigihanked.riik.ee/filetransfer/client/shared/file/47692eeb-ebf8-435e-9c11-adb7efaa71b5'
```

**Response:** Binary file (PDF, DOCX, XLSX, XML, etc.)

---

### Document Type Codes

**Document Subtype Codes (`docSubtypeCode`):**

- `VASTAVUSTINGIMUSED` - Compliance/qualification conditions
- `HINDAMISKRITEERIUMID` - Evaluation criteria
- `HANKEPASS` - Procurement passport with explanations
- `ESPD_XML2` - European Single Procurement Document (XML)
- `CRITERION_QUESTION` - Question forms (often tax/price forms)
- `null` - Usually technical descriptions and annexes

---

### Implementation

**Working Script:** `harvest.py` - Python implementation using discovered endpoints  
**Test Results:** Successfully downloaded all 8 documents for procurement 9559644  
**Rate Limiting:** None observed

---

Since the automated investigation didn't find public API endpoints, we need to inspect the actual network traffic. Here's how:

### Step 1: Open Browser Developer Tools

1. Open the procurement page in your browser:

   ```text
   https://riigihanked.riik.ee/rhr-web/#/procurement/9559644/procurement-versions
   ```

2. Open Developer Tools:
   - **Firefox/Chrome:** Press `F12` or `Ctrl+Shift+I`
   - Go to the **Network** tab
   - Clear any existing requests (trash icon)

### Step 2: Capture API Requests

1. Reload the page (`Ctrl+R` or `F5`)
2. Look for XHR/Fetch requests in the Network tab
3. Filter by:
   - Type: `XHR` or `Fetch`
   - Status: `200` (successful)

### Step 3: Identify Relevant Endpoints

Look for requests that contain:

- Procurement ID (`9559644`)
- Keywords like: `procurement`, `document`, `tender`, `hanke`

Common patterns to look for:

```text
GET /api/procurements/9559644
GET /api/v1/procurement/9559644/details
GET /api/tender/9559644/documents
GET /rhr-web/rest/procurements/9559644
```

### Step 4: Inspect Request Details

For each promising request, click on it and check:

**Headers tab:**

- Request URL (copy this!)
- Request Method (GET, POST, etc.)
- Authorization headers (if any)

**Response tab:**

- Check if it's JSON data
- Look for document URLs, procurement details, etc.

**Preview tab:**

- See the structured data

### Step 5: Find Document Download URLs

Look specifically for:

- Document list endpoints
- Direct PDF/DOC download URLs
- File attachment endpoints

### Step 6: Record Your Findings

Create a file `API_ENDPOINTS.md` with your discoveries:

```markdown
## Discovered Endpoints

### Get Procurement Details

- **URL:** [paste URL here]
- **Method:** GET
- **Auth Required:** Yes/No
- **Response:** JSON with procurement details

### Get Documents List

- **URL:** [paste URL here]
- **Method:** GET
- **Response:** Array of documents with download URLs

### Download Document

- **URL Pattern:** [paste URL pattern here]
- **Example:** [paste example URL]
```

## Alternative: Use Browser's Copy as cURL

1. Right-click on a successful API request in Network tab
2. Select **Copy → Copy as cURL**
3. Paste into a text file
4. This gives you the complete request with headers

Example cURL command structure:

```bash
curl 'https://riigihanked.riik.ee/api/...' \
  -H 'Accept: application/json' \
  -H 'Authorization: Bearer ...' \
  # ... more headers
```

## What to Look For

### Procurement Data

- Title, reference number
- Contracting authority
- Deadline
- Budget/value
- Status

### Documents

- Technical specifications
- Terms and conditions
- Templates
- Previous Q&A

### Useful Metadata

- Categories/CPV codes
- Publication date
- Submission requirements

---

---

## ✅ DISCOVERED: URL Structure for Procurement 9559644

Based on the HTML menu structure, the following sections are available:

### Frontend Routes (Angular SPA)

Base pattern: `https://riigihanked.riik.ee/rhr-web/#/procurement/{procurement_id}/{section}`

1. **Hanke üldandmed** (General Information)
   - URL: `#/procurement/9559644/general-info`
2. **Hankijad** (Procurers/Contracting Authorities)
   - URL: `#/procurement/9559644/procurers`
3. **Hanke lisaandmed** (Additional Data)
   - URL: `#/procurement/9559644/additional-data`
4. **Kõrvaldamise alused ja kvalifitseerimistingimused** (Exclusion Grounds & Qualification)
   - URL: `#/procurement/9559644/procurement-passport`
5. **Vastavustingimused** (Compliance Conditions)
   - URL: `#/procurement/9559644/qualification-conditions`
6. **Hindamiskriteeriumid ja hinnatavad näitajad** (Evaluation Criteria)
   - URL: `#/procurement/9559644/evaluation`
7. **Alltöövõtjate kontrollimise tingimused** (Subcontractor Verification)
   - URL: `#/procurement/9559644/subcontractor-passport`
8. **Hanke teated** (Procurement Notices)
   - URL: `#/procurement/9559644/notices`
9. **Hanke versioonid** (Procurement Versions)
   - URL: `#/procurement/9559644/procurement-versions`
10. **Dokumendid** (Documents) ⭐ **MOST IMPORTANT**
    - URL: `#/procurement/9559644/documents?group=B`
    - This is where "hanke alusdokumendid" should be!

### Next Step: Find API Endpoint

The Angular app loads data via API. Likely patterns:

```curl
GET /rhr-web/api/procurements/9559644
GET /rhr-web/rest/procurement/9559644
GET /rhr-web/api/procurement/9559644/documents
```

**Action Required:**

1. Open: `https://riigihanked.riik.ee/rhr-web/#/procurement/9559644/documents?group=B`
2. Open DevTools Network tab
3. Look for XHR/Fetch requests that load document data
4. Share the API endpoint URL you find
