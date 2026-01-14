/**
 * MCP Server Entry Point for Knowledge Base
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { EdgeDBClient } from './edgedb.js';
import { ExperienceService } from './services/experience.js';
import { SkillService } from './services/skill.js';
import { AchievementService } from './services/achievement.js';
import { TagService } from './services/tag.js';
import { ProjectService } from './services/project.js';
import { scheduleAutoCompile } from './compileHook.js';
import { CertificationService } from './services/certification.js';
import { EducationService } from './services/education.js';
import { LanguageService } from './services/language.js';
import { HobbyService } from './services/hobby.js';
import { type TagReference, SkillCategory, VerificationStatus, ProjectStatus } from './types.js';

function slugifyExternalId(input: string): string {
  return input
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-+/g, '-');
}

const server = new Server(
  {
    name: 'cv-system-knb-mcp',
    version: '0.1.0'
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

let client: EdgeDBClient;
let experienceService: ExperienceService;
let skillService: SkillService;
let achievementService: AchievementService;
let tagService: TagService;
let projectService: ProjectService;
let certificationService: CertificationService;
let educationService: EducationService;
let languageService: LanguageService;
let hobbyService: HobbyService;

/**
 * List available tools
 */
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // Experience tools
      {
        name: 'add_experience',
        description: 'Create a new work experience entry',
        inputSchema: {
          type: 'object',
          properties: {
            title: { type: 'string', description: 'Job title' },
            organization: { type: 'string', description: 'Organization/company name' },
            start_date: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
            end_date: { type: 'string', description: 'End date (YYYY-MM-DD), optional' },
            description: { type: 'string', description: 'Experience description' },
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }, 
              description: 'Associated tags with name and category' 
            },
            language: { type: 'string', enum: ['en', 'et'], description: 'Language of description' }
          },
          required: ['title', 'organization', 'start_date', 'tags', 'language']
        }
      },
      {
        name: 'get_experience',
        description: 'Retrieve experience by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string', description: 'Experience ID' }
          },
          required: ['id']
        }
      },
      {
        name: 'update_experience',
        description: 'Update an experience entry',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string', description: 'Experience ID' },
            title: { type: 'string' },
            organization: { type: 'string' },
            start_date: { type: 'string' },
            end_date: { type: 'string' },
            description: { type: 'string' }
          },
          required: ['id']
        }
      },
      // Skill tools
      {
        name: 'add_skill',
        description: 'Create a new skill entry',
        inputSchema: {
          type: 'object',
          properties: {
            name: { type: 'string', description: 'Skill name (must be unique)' },
            level: { type: 'number', description: 'Skill level 1-10' },
            description: { type: 'string' },
            evidence_refs: { type: 'array', items: { type: 'string' }, description: 'Evidence references' },
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }
            }
          },
          required: ['name', 'level', 'tags']
        }
      },
      {
        name: 'get_skill',
        description: 'Retrieve skill by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' }
          },
          required: ['id']
        }
      },
      {
        name: 'update_skill',
        description: 'Update a skill entry',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            name: { type: 'string' },
            level: { type: 'number' },
            description: { type: 'string' },
            evidence_refs: { type: 'array', items: { type: 'string' } }
          },
          required: ['id']
        }
      },
      // Achievement tools
      {
        name: 'add_achievement',
        description: 'Create a new achievement entry',
        inputSchema: {
          type: 'object',
          properties: {
            title: { type: 'string', description: 'Achievement title' },
            date: { type: 'string', description: 'Achievement date (YYYY-MM-DD)' },
            description: { type: 'string', description: 'Achievement description' },
            tags: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }
            }
          },
          required: ['title', 'date', 'tags']
        }
      },
      {
        name: 'get_achievement',
        description: 'Retrieve achievement by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' }
          },
          required: ['id']
        }
      },
      // Project tools
      {
        name: 'add_project',
        description: 'Create a new project entry',
        inputSchema: {
          type: 'object',
          properties: {
            external_id: { type: 'string', description: 'Unique external identifier (e.g., filename stem)' },
            name: { 
              type: 'object',
              properties: {
                et: { type: 'string', description: 'Estonian name' },
                en: { type: 'string', description: 'English name' }
              },
              description: 'Project name (at least one language required)'
            },
            url: { type: 'string', description: 'Project URL (optional)' },
            repository: { type: 'string', description: 'Git repository URL (optional)' },
            status: { 
              type: 'string', 
              enum: ['active', 'archived', 'planned', 'maintenance'],
              description: 'Project status (default: active)'
            },
            dates: {
              type: 'object',
              properties: {
                start: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
                end: { type: 'string', description: 'End date (YYYY-MM-DD), optional' }
              },
              required: ['start']
            },
            technologies: {
              type: 'array',
              items: { type: 'string' },
              description: 'Technologies used in project'
            },
            article: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              },
              description: 'Project description (at least one language required)'
            },
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }, 
              description: 'Associated tags with name and category' 
            },
            skills_demonstrated: {
              type: 'array',
              items: { type: 'string' },
              description: 'Array of skill external_ids'
            }
          },
          required: ['external_id', 'name', 'last_verified', 'tags']
        }
      },
      {
        name: 'get_project',
        description: 'Retrieve project by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' }
          },
          required: ['id']
        }
      },
      {
        name: 'update_project',
        description: 'Update a project entry',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string', description: 'Project ID' },
            name: { 
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            url: { type: 'string' },
            repository: { type: 'string' },
            status: { type: 'string', enum: ['active', 'archived', 'planned', 'maintenance'] },
            dates: {
              type: 'object',
              properties: {
                start: { type: 'string', description: 'Start date (YYYY-MM-DD)' },
                end: { type: 'string', description: 'End date (YYYY-MM-DD), optional' }
              }
            },
            technologies: { type: 'array', items: { type: 'string' } },
            article: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            }
          },
          required: ['id']
        }
      },
      {
        name: 'search_projects',
        description: 'Search projects by tags, status, or technologies',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }, 
              description: 'Filter by tags (AND logic)' 
            },
            status: { 
              type: 'string', 
              enum: ['active', 'archived', 'planned', 'maintenance'],
              description: 'Filter by project status' 
            },
            technologies: {
              type: 'array',
              items: { type: 'string' },
              description: 'Filter by technologies used'
            }
          }
        }
      },
      // Tag tools
      {
        name: 'list_tags',
        description: 'List all available tags, optionally by category',
        inputSchema: {
          type: 'object',
          properties: {
            category: { type: 'string', description: 'Filter by category (optional)' }
          }
        }
      },
      {
        name: 'add_tag',
        description: 'Create a new tag/classifier',
        inputSchema: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            category: { type: 'string', description: 'Tag category (e.g., languages, skills, domains)' }
          },
          required: ['name', 'category']
        }
      },
      {
        name: 'get_tag_usage',
        description: 'Get usage statistics for a tag',
        inputSchema: {
          type: 'object',
          properties: {
            tag: { type: 'string', description: 'Tag name' }
          },
          required: ['tag']
        }
      },
      {
        name: 'find_similar_tags',
        description: 'Find tags similar to input string using fuzzy matching (Levenshtein distance)',
        inputSchema: {
          type: 'object',
          properties: {
            input: { type: 'string', description: 'String to match against tag names' },
            max_distance: { type: 'number', description: 'Maximum edit distance (default: 3)' },
            category: { type: 'string', description: 'Filter by category (optional)' }
          },
          required: ['input']
        }
      },
      // Search tools
      {
        name: 'search_experiences',
        description: 'Search experiences by tags, organization, or date range',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }, 
              description: 'Filter by tags (AND logic)' 
            },
            organization: { type: 'string', description: 'Filter by organization name' },
            date_range: {
              type: 'object',
              properties: {
                start: { type: 'string', description: 'Range start date (YYYY-MM-DD)' },
                end: { type: 'string', description: 'Range end date (YYYY-MM-DD)' }
              },
              description: 'Filter by date range (overlapping)'
            }
          }
        }
      },
      {
        name: 'search_skills',
        description: 'Search skills by tags and minimum level',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }, 
              description: 'Filter by tags (AND logic)' 
            },
            level_min: { type: 'number', description: 'Minimum skill level (1-10)' }
          }
        }
      },
      {
        name: 'search_achievements',
        description: 'Search achievements by tags and date range',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string', description: 'Tag name' },
                  category: { type: 'string', description: 'Tag category' }
                },
                required: ['name', 'category']
              }, 
              description: 'Filter by tags (AND logic)' 
            },
            date_range: {
              type: 'object',
              properties: {
                start: { type: 'string', description: 'Range start date (YYYY-MM-DD)' },
                end: { type: 'string', description: 'Range end date (YYYY-MM-DD)' }
              },
              description: 'Filter by date range'
            }
          }
        }
      },
      // Certification tools
      {
        name: 'add_certification',
        description: 'Create a new certification entry',
        inputSchema: {
          type: 'object',
          properties: {
            external_id: { type: 'string', description: 'Unique external identifier' },
            title: { 
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              },
              description: 'Certification title (at least one language required)'
            },
            issuer: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              },
              description: 'Issuing organization (at least one language required)'
            },
            date: { type: 'string', description: 'Issue date (YYYY-MM-DD)' },
            expiry_date: { type: 'string', description: 'Expiry date (YYYY-MM-DD), optional' },
            credential_id: { type: 'string', description: 'Credential ID, optional' },
            credential_url: { type: 'string', description: 'Credential URL, optional' },
            article: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              },
              description: 'Description (optional)'
            },
            verification_status: { type: 'string', enum: ['verified', 'draft', 'outdated'] },
            last_verified: { type: 'string', description: 'Last verification date (YYYY-MM-DD)' },
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            }
          },
          required: ['external_id', 'title', 'issuer', 'date', 'last_verified', 'tags']
        }
      },
      {
        name: 'get_certification',
        description: 'Retrieve certification by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' }
          },
          required: ['id']
        }
      },
      {
        name: 'update_certification',
        description: 'Update a certification entry',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            title: { 
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            issuer: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            date: { type: 'string' },
            expiry_date: { type: 'string' },
            credential_id: { type: 'string' },
            credential_url: { type: 'string' },
            article: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            }
          },
          required: ['id']
        }
      },
      {
        name: 'search_certifications',
        description: 'Search certifications by tags, issuer, or date range',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            },
            issuer: { type: 'string', description: 'Filter by issuer name' },
            date_range: {
              type: 'object',
              properties: {
                start: { type: 'string' },
                end: { type: 'string' }
              }
            }
          }
        }
      },
      // Education tools
      {
        name: 'add_education',
        description: 'Create a new education entry',
        inputSchema: {
          type: 'object',
          properties: {
            external_id: { type: 'string' },
            institutions: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  et: { type: 'string' },
                  en: { type: 'string' }
                }
              },
              description: 'Array of institutions'
            },
            fields: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  et: { type: 'string' },
                  en: { type: 'string' }
                }
              },
              description: 'Fields of study'
            },
            dates: {
              type: 'object',
              properties: {
                start: { type: 'string' },
                end: { type: 'string' }
              },
              required: ['start']
            },
            degree: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            article: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            verification_status: { type: 'string', enum: ['verified', 'draft', 'outdated'] },
            last_verified: { type: 'string' },
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            }
          },
          required: ['external_id', 'institutions', 'fields', 'dates', 'last_verified', 'tags']
        }
      },
      {
        name: 'get_education',
        description: 'Retrieve education by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' }
          },
          required: ['id']
        }
      },
      {
        name: 'update_education',
        description: 'Update an education entry',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            institutions: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  et: { type: 'string' },
                  en: { type: 'string' }
                }
              }
            },
            fields: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  et: { type: 'string' },
                  en: { type: 'string' }
                }
              }
            },
            dates: {
              type: 'object',
              properties: {
                start: { type: 'string' },
                end: { type: 'string' }
              }
            },
            degree: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            }
          },
          required: ['id']
        }
      },
      {
        name: 'search_education',
        description: 'Search education entries by tags, institution, or date range',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            },
            institution: { type: 'string' },
            date_range: {
              type: 'object',
              properties: {
                start: { type: 'string' },
                end: { type: 'string' }
              }
            }
          }
        }
      },
      // Language tools
      {
        name: 'add_language',
        description: 'Create a new language entry',
        inputSchema: {
          type: 'object',
          properties: {
            external_id: { type: 'string' },
            name: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            proficiency: {
              type: 'object',
              description: 'Language proficiency levels (JSON object)'
            },
            article: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            verification_status: { type: 'string', enum: ['verified', 'draft', 'outdated'] },
            last_verified: { type: 'string' },
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            },
            evidence: {
              type: 'array',
              items: { type: 'string' },
              description: 'Experience IDs where language was used'
            }
          },
          required: ['external_id', 'name', 'proficiency', 'last_verified', 'tags']
        }
      },
      {
        name: 'get_language',
        description: 'Retrieve language by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' }
          },
          required: ['id']
        }
      },
      {
        name: 'update_language',
        description: 'Update a language entry',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            name: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            proficiency: { type: 'object' }
          },
          required: ['id']
        }
      },
      {
        name: 'search_languages',
        description: 'Search languages by tags or proficiency',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            },
            min_proficiency: { type: 'string' }
          }
        }
      },
      // Hobby tools
      {
        name: 'add_hobby',
        description: 'Create a new hobby entry',
        inputSchema: {
          type: 'object',
          properties: {
            external_id: { type: 'string' },
            name: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            tools: {
              type: 'array',
              items: { type: 'string' },
              description: 'Tools/technologies used'
            },
            article: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            verification_status: { type: 'string', enum: ['verified', 'draft', 'outdated'] },
            last_verified: { type: 'string' },
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            }
          },
          required: ['external_id', 'name', 'last_verified', 'tags']
        }
      },
      {
        name: 'get_hobby',
        description: 'Retrieve hobby by ID',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' }
          },
          required: ['id']
        }
      },
      {
        name: 'update_hobby',
        description: 'Update a hobby entry',
        inputSchema: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            name: {
              type: 'object',
              properties: {
                et: { type: 'string' },
                en: { type: 'string' }
              }
            },
            tools: {
              type: 'array',
              items: { type: 'string' }
            }
          },
          required: ['id']
        }
      },
      {
        name: 'search_hobbies',
        description: 'Search hobbies by tags or tools',
        inputSchema: {
          type: 'object',
          properties: {
            tags: { 
              type: 'array', 
              items: { 
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  category: { type: 'string' }
                },
                required: ['name', 'category']
              }
            },
            tool: { type: 'string' }
          }
        }
      }
    ]
  };
});

/**
 * Handle tool calls
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const params = (args ?? {}) as Record<string, unknown>;

  const queriedAtUtc = new Date().toISOString();

  const ok = (data: unknown) => {
    return {
      content: [
        {
          type: 'text' as const,
          text: JSON.stringify(
            {
              meta: {
                tool: name,
                queried_at_utc: queriedAtUtc
              },
              data
            },
            null,
            2
          )
        }
      ]
    };
  };

  try {
    switch (name) {
      case 'add_experience':
        {
          const title = String(params.title ?? '').trim();
          const organization = String(params.organization ?? '').trim();
          const startDate = String(params.start_date ?? '').trim();
          const endDate = String(params.end_date ?? '').trim();
          const description = (params.description !== undefined ? String(params.description) : '').trim();
          const language = params.language === 'et' ? 'et' : 'en';
          const lastVerified = new Date().toISOString().slice(0, 10);

          if (!title) throw new Error('title is required');
          if (!organization) throw new Error('organization is required');
          if (!startDate) throw new Error('start_date is required');
          if (!endDate) throw new Error('end_date is required');

          const titleT: any = { [language]: title };
          const companyT: any = { [language]: organization };
          const articleT: any = description ? { [language]: description } : undefined;
          const externalIdBase = slugifyExternalId(`${organization}-${title}` || 'experience');
          const external_id = `${externalIdBase}-${startDate}`;

          const created = await experienceService.addExperience({
            external_id,
            title: titleT,
            company: companyT,
            dates: { start: startDate, end: endDate },
            article: articleT,
            verification_status: VerificationStatus.Draft,
            last_verified: lastVerified,
            tags: (params.tags as TagReference[] | undefined) ?? [],
            skills_demonstrated: []
          } as any);

          // Trigger auto-compile (debounced)
          try {
            scheduleAutoCompile();
          } catch (err) {
            console.error('Failed to schedule auto-compile:', err);
          }

          return {
            content: [
              {
                type: 'text',
                text: JSON.stringify(
                  {
                    meta: {
                      tool: name,
                      queried_at_utc: queriedAtUtc
                    },
                    data: created
                  },
                  null,
                  2
                )
              }
            ]
          };
        }

      case 'get_experience':
        return ok(await experienceService.getExperience(params.id as string));

      case 'update_experience':
        {
          const id = String(params.id ?? '').trim();
          if (!id) throw new Error('id is required');

          const updates: Record<string, unknown> = {};

          if (params.title !== undefined) {
            const title = String(params.title).trim();
            if (!title) throw new Error('title cannot be empty');
            updates.title = { en: title };
          }

          // Tool schema uses `organization`; service field is `company` (Translation)
          if (params.organization !== undefined) {
            const organization = String(params.organization).trim();
            if (!organization) throw new Error('organization cannot be empty');
            updates.company = { en: organization };
          }

          if (params.start_date !== undefined || params.end_date !== undefined) {
            const startDate = String(params.start_date ?? '').trim();
            const endDate = String(params.end_date ?? '').trim();
            if (!startDate) throw new Error('start_date is required when updating dates');
            if (!endDate) throw new Error('end_date is required when updating dates');
            updates.dates = { start: startDate, end: endDate };
          }

          // Tool schema uses `description`; service field is `article` (Translation)
          if (params.description !== undefined) {
            const description = String(params.description).trim();
            if (!description) throw new Error('description cannot be empty');
            updates.article = { en: description };
          }

          const updated = await experienceService.updateExperience(id, updates as any);
          try {
            scheduleAutoCompile();
          } catch (err) {
            console.error('Failed to schedule auto-compile:', err);
          }

          return ok(updated);
        }

      case 'add_skill':
        {
          const name = String(params.name ?? '').trim();
          const level = Number(params.level);
          const description = (params.description !== undefined ? String(params.description) : '').trim();
          const lastVerified = new Date().toISOString().slice(0, 10);

          if (!name) throw new Error('name is required');
          if (!Number.isFinite(level)) throw new Error('level is required');

          const external_id = slugifyExternalId(name);

          const created = await skillService.addSkill({
            external_id,
            name: { en: name },
            category: SkillCategory.Other,
            level,
            article: description ? { en: description } : undefined,
            verification_status: VerificationStatus.Draft,
            last_verified: lastVerified,
            tags: (params.tags as TagReference[] | undefined) ?? []
          } as any);

          try {
            scheduleAutoCompile();
          } catch (err) {
            console.error('Failed to schedule auto-compile:', err);
          }

          return ok(created);
        }

      case 'get_skill':
        return ok(await skillService.getSkill(params.id as string));

      case 'update_skill':
        {
          const id = String(params.id ?? '').trim();
          if (!id) throw new Error('id is required');

          const updates: Record<string, unknown> = {};

          if (params.name !== undefined) {
            const name = String(params.name).trim();
            if (!name) throw new Error('name cannot be empty');
            updates.name = { en: name };
          }

          if (params.level !== undefined) {
            const level = Number(params.level);
            if (!Number.isFinite(level)) throw new Error('level must be a number');
            updates.level = level;
          }

          // Tool schema uses `description`; service field is `article` (Translation)
          if (params.description !== undefined) {
            const description = String(params.description).trim();
            if (!description) throw new Error('description cannot be empty');
            updates.article = { en: description };
          }

          // evidence_refs is not currently modeled in the EdgeDB Skill type; ignore safely
          const updated = await skillService.updateSkill(id, updates as any);
          try {
            scheduleAutoCompile();
          } catch (err) {
            console.error('Failed to schedule auto-compile:', err);
          }

          return ok(updated);
        }

      case 'add_achievement':
        {
          const title = String(params.title ?? '').trim();
          const date = String(params.date ?? '').trim();
          const description = (params.description !== undefined ? String(params.description) : '').trim();
          const lastVerified = new Date().toISOString().slice(0, 10);
          const externalIdBase = slugifyExternalId(title || 'achievement');
          const external_id = `${externalIdBase}-${date || lastVerified}`;

          const created = await achievementService.addAchievement({
            external_id,
            title: { en: title },
            date,
            article: description ? { en: description } : undefined,
            verification_status: VerificationStatus.Draft,
            last_verified: lastVerified,
            tags: (params.tags as TagReference[] | undefined) ?? []
          } as any);

          try {
            scheduleAutoCompile();
          } catch (err) {
            console.error('Failed to schedule auto-compile:', err);
          }

          return ok(created);
        }

      case 'get_achievement':
        return ok(await achievementService.getAchievement(params.id as string));

      case 'add_project':
        return ok(await projectService.addProject(params as any));

      case 'get_project':
        return ok(await projectService.getProject(params.id as string));

      case 'update_project':
        return ok(await projectService.updateProject(params.id as string, params as any));

      case 'search_projects':
        return ok(
          await projectService.searchProjects({
            tags: params.tags as TagReference[] | undefined,
            status: params.status as ProjectStatus | undefined,
            technologies: params.technologies as string[] | undefined
          })
        );

      case 'list_tags':
        return ok(await tagService.listTags(params.category as string | undefined));

      case 'add_tag':
        {
          const created = await tagService.addTag(params.name as string, params.category as string);
          try {
            scheduleAutoCompile();
          } catch (err) {
            console.error('Failed to schedule auto-compile:', err);
          }

          return ok(created);
        }

      case 'get_tag_usage':
        return ok(await tagService.getTagUsage(params.tag as string));

      case 'find_similar_tags':
        return ok(
          await tagService.findSimilarTags(
            params.input as string,
            params.max_distance as number | undefined,
            params.category as string | undefined
          )
        );

      case 'search_experiences':
        return ok(
          await experienceService.searchExperiences({
            tags: params.tags as TagReference[] | undefined,
            organization: params.organization as string | undefined,
            dateRange: params.date_range as { start?: string; end?: string } | undefined
          })
        );

      case 'search_skills':
        return ok(
          await skillService.searchSkills({
            tags: params.tags as TagReference[] | undefined,
            levelMin: params.level_min as number | undefined
          })
        );

      case 'search_achievements':
        return ok(
          await achievementService.searchAchievements({
            tags: params.tags as TagReference[] | undefined,
            dateRange: params.date_range as { start?: string; end?: string } | undefined
          })
        );

      // Certification handlers
      case 'add_certification':
        return ok(await certificationService.addCertification(params as any));

      case 'get_certification':
        return ok(await certificationService.getCertification(params.id as string));

      case 'update_certification':
        return ok(await certificationService.updateCertification(params.id as string, params as any));

      case 'search_certifications':
        return ok(
          await certificationService.searchCertifications({
            tags: params.tags as TagReference[] | undefined,
            issuer: params.issuer as string | undefined,
            dateRange: params.date_range as { start?: string; end?: string } | undefined
          })
        );

      // Education handlers
      case 'add_education':
        return ok(await educationService.addEducation(params as any));

      case 'get_education':
        return ok(await educationService.getEducation(params.id as string));

      case 'update_education':
        return ok(await educationService.updateEducation(params.id as string, params as any));

      case 'search_education':
        return ok(
          await educationService.searchEducation({
            tags: params.tags as TagReference[] | undefined,
            institution: params.institution as string | undefined,
            dateRange: params.date_range as { start?: string; end?: string } | undefined
          })
        );

      // Language handlers
      case 'add_language':
        return ok(await languageService.addLanguage(params as any));

      case 'get_language':
        return ok(await languageService.getLanguage(params.id as string));

      case 'update_language':
        return ok(await languageService.updateLanguage(params.id as string, params as any));

      case 'search_languages':
        return ok(
          await languageService.searchLanguages({
            tags: params.tags as TagReference[] | undefined,
            minProficiency: params.min_proficiency as string | undefined
          })
        );

      // Hobby handlers
      case 'add_hobby':
        return ok(await hobbyService.addHobby(params as any));

      case 'get_hobby':
        return ok(await hobbyService.getHobby(params.id as string));

      case 'update_hobby':
        return ok(await hobbyService.updateHobby(params.id as string, params as any));

      case 'search_hobbies':
        return ok(
          await hobbyService.searchHobbies({
            tags: params.tags as TagReference[] | undefined,
            tool: params.tool as string | undefined
          })
        );

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(
            {
              meta: {
                tool: name,
                queried_at_utc: queriedAtUtc,
                is_error: true
              },
              error: {
                message: error instanceof Error ? error.message : String(error)
              }
            },
            null,
            2
          )
        }
      ],
      isError: true
    };
  }
});

/**
 * Main entry point
 */
async function main() {
  // Initialize EdgeDB client
  client = new EdgeDBClient();
  await client.connect();

  // Initialize services
  experienceService = new ExperienceService(client);
  skillService = new SkillService(client);
  achievementService = new AchievementService(client);
  tagService = new TagService(client);
  projectService = new ProjectService(client);
  certificationService = new CertificationService(client);
  educationService = new EducationService(client);
  languageService = new LanguageService(client);
  hobbyService = new HobbyService(client);

  console.error('KnB MCP Server initialized');

  // Start server
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Server connected and listening');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
