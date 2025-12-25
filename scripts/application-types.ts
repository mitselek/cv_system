/**
 * TypeScript type definitions for application documents frontmatter
 * Used by PDF conversion pipeline and validation tools
 * 
 * Aligns with: docs/wiki-pdf-conversion-guide.md
 * Used by: scripts/convert-to-pdf.sh, scripts/metadata_to_latex.lua
 */

/**
 * PDF metadata embedded in the document (not visible in rendered PDF)
 * Used by ATS systems and AI parsing tools
 */
export interface PDFMetadata {
  /** Document title (visible in PDF viewer properties) */
  title?: string;

  /** Document subject/purpose (e.g., "Job Application", "Motivation Letter") */
  subject?: string;

  /** Comma-separated keywords for search/ATS optimization */
  keywords?: string;

  /** Creator/author name */
  creator?: string;

  /** Brief summary/recommendation for AI/ATS parsing (custom XMP field) */
  recommendation?: string;
}

/**
 * Required frontmatter fields for all application documents
 * These fields appear in PDF footer and metadata
 */
export interface ApplicationFrontmatter {
  /** 
   * Document identifier (max 24 chars)
   * Format: {Type}-{Company}-{Role}
   * Examples: "CV-Yordas-DataTech", "ML-EKA-ITHead"
   * Appears in PDF footer
   */
  docID: string;

  /** 
   * Semantic version number
   * Examples: "1.0", "2.1", "3.0"
   * Appears in PDF footer
   */
  version: string;

  /** 
   * Document date in ISO format (YYYY-MM-DD)
   * Appears in PDF footer
   */
  date: string;

  /** 
   * Author name
   * Appears in PDF footer
   */
  author: string;

  /** 
   * Optional: PDF metadata for ATS/AI systems
   * Embedded in PDF file, not visible in rendered document
   */
  pdf_metadata?: PDFMetadata;
}

/**
 * Type guard to validate ApplicationFrontmatter at runtime
 */
export function isValidApplicationFrontmatter(obj: any): obj is ApplicationFrontmatter {
  if (!obj || typeof obj !== 'object') return false;

  // Check required fields
  if (typeof obj.docID !== 'string' || obj.docID.length === 0 || obj.docID.length > 24) {
    return false;
  }

  if (typeof obj.version !== 'string' || obj.version.length === 0) {
    return false;
  }

  // Validate ISO date format (YYYY-MM-DD)
  if (typeof obj.date !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(obj.date)) {
    return false;
  }

  if (typeof obj.author !== 'string' || obj.author.length === 0) {
    return false;
  }

  // Validate optional pdf_metadata if present
  if (obj.pdf_metadata !== undefined) {
    if (typeof obj.pdf_metadata !== 'object' || obj.pdf_metadata === null) {
      return false;
    }

    const meta = obj.pdf_metadata;
    if (meta.title !== undefined && typeof meta.title !== 'string') return false;
    if (meta.subject !== undefined && typeof meta.subject !== 'string') return false;
    if (meta.keywords !== undefined && typeof meta.keywords !== 'string') return false;
    if (meta.creator !== undefined && typeof meta.creator !== 'string') return false;
    if (meta.recommendation !== undefined && typeof meta.recommendation !== 'string') return false;
  }

  return true;
}

/**
 * Document type prefixes for docID generation
 */
export enum DocumentType {
  CV = 'CV',
  MotivationLetter = 'ML',
  CoverLetter = 'CL',
  Portfolio = 'PF',
  Reference = 'REF',
}

/**
 * Helper to generate docID from components
 * 
 * @example
 * generateDocID(DocumentType.CV, "Yordas Group", "Data Technician")
 * // Returns: "CV-Yordas-DataTech" (truncated to 24 chars if needed)
 */
export function generateDocID(
  type: DocumentType,
  company: string,
  role: string
): string {
  // Simplify company name (remove "OÜ", "Ltd", common suffixes)
  const cleanCompany = company
    .replace(/\s+(OÜ|OU|Ltd|Limited|Inc|Corp|AS|Group)\.?$/i, '')
    .trim();

  // Simplify role (take key words)
  const cleanRole = role
    .replace(/\s+(Specialist|Engineer|Developer|Manager|Lead|Senior|Junior)/gi, '')
    .trim();

  // Generate base docID
  const docID = `${type}-${cleanCompany}-${cleanRole}`
    .replace(/\s+/g, '-')  // Replace spaces with hyphens
    .replace(/[^a-zA-Z0-9-]/g, '') // Remove special chars
    .substring(0, 24); // Enforce max length

  return docID;
}

/**
 * Validation result for frontmatter checking
 */
export interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

/**
 * Comprehensive validation with detailed error messages
 */
export function validateFrontmatter(obj: any): ValidationResult {
  const result: ValidationResult = {
    valid: true,
    errors: [],
    warnings: [],
  };

  if (!obj || typeof obj !== 'object') {
    result.valid = false;
    result.errors.push('Frontmatter must be an object');
    return result;
  }

  // Required fields validation
  if (!obj.docID) {
    result.valid = false;
    result.errors.push('Missing required field: docID');
  } else if (typeof obj.docID !== 'string') {
    result.valid = false;
    result.errors.push('docID must be a string');
  } else if (obj.docID.length > 24) {
    result.valid = false;
    result.errors.push(`docID too long (${obj.docID.length} chars, max 24)`);
  } else if (obj.docID.length === 0) {
    result.valid = false;
    result.errors.push('docID cannot be empty');
  }

  if (!obj.version) {
    result.valid = false;
    result.errors.push('Missing required field: version');
  } else if (typeof obj.version !== 'string') {
    result.valid = false;
    result.errors.push('version must be a string');
  }

  if (!obj.date) {
    result.valid = false;
    result.errors.push('Missing required field: date');
  } else if (typeof obj.date !== 'string') {
    result.valid = false;
    result.errors.push('date must be a string');
  } else if (!/^\d{4}-\d{2}-\d{2}$/.test(obj.date)) {
    result.valid = false;
    result.errors.push('date must be in ISO format (YYYY-MM-DD)');
  } else {
    // Validate date is actually valid
    const dateObj = new Date(obj.date);
    if (isNaN(dateObj.getTime())) {
      result.valid = false;
      result.errors.push('date is not a valid date');
    }
  }

  if (!obj.author) {
    result.valid = false;
    result.errors.push('Missing required field: author');
  } else if (typeof obj.author !== 'string') {
    result.valid = false;
    result.errors.push('author must be a string');
  }

  // Optional pdf_metadata validation
  if (obj.pdf_metadata !== undefined) {
    if (typeof obj.pdf_metadata !== 'object' || obj.pdf_metadata === null) {
      result.valid = false;
      result.errors.push('pdf_metadata must be an object');
    } else {
      const meta = obj.pdf_metadata;
      const allowedKeys = ['title', 'subject', 'keywords', 'creator', 'recommendation'];
      const actualKeys = Object.keys(meta);
      
      actualKeys.forEach(key => {
        if (!allowedKeys.includes(key)) {
          result.warnings.push(`Unknown pdf_metadata field: ${key}`);
        }
        if (typeof meta[key] !== 'string') {
          result.valid = false;
          result.errors.push(`pdf_metadata.${key} must be a string`);
        }
      });
    }
  }

  return result;
}
