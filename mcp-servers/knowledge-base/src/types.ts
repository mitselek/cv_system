/**
 * Shared types for Knowledge Base MCP server
 */

/**
 * Bilingual text content with Estonian and/or English
 */
export interface Translation {
  et?: string;
  en?: string;
}

/**
 * Tag reference for linking entities
 */
export interface TagReference {
  name: string;
  category: string;
}

/**
 * Skill categories matching EdgeDB enum
 */
export enum SkillCategory {
  ProgrammingLanguage = 'programming_language',
  BackendDevelopment = 'backend_development',
  FrontendDevelopment = 'frontend_development',
  Database = 'database',
  DevOps = 'devops',
  CloudPlatform = 'cloud_platform',
  Framework = 'framework',
  Tool = 'tool',
  Methodology = 'methodology',
  SoftSkill = 'soft_skill',
  DomainKnowledge = 'domain_knowledge',
  Testing = 'testing',
  Security = 'security',
  Other = 'other'
}

/**
 * Verification status matching EdgeDB enum
 */
export enum VerificationStatus {
  Verified = 'verified',
  Draft = 'draft',
  Outdated = 'outdated'
}

/**
 * Project status matching EdgeDB enum
 */
export enum ProjectStatus {
  Active = 'active',
  Archived = 'archived',
  Planned = 'planned',
  Maintenance = 'maintenance'
}
