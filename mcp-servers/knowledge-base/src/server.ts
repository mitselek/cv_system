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
import { CertificationService } from './services/certification.js';
import { EducationService } from './services/education.js';
import { LanguageService } from './services/language.js';
import { HobbyService } from './services/hobby.js';
import { type TagReference, SkillCategory, VerificationStatus, ProjectStatus } from './types.js';

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
            title: { type: 'string' },
            date: { type: 'string', description: 'Achievement date (YYYY-MM-DD)' },
            description: { type: 'string' },
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

  try {
    switch (name) {
      case 'add_experience':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await experienceService.addExperience(params as any),
                null,
                2
              )
            }
          ]
        };

      case 'get_experience':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await experienceService.getExperience(params.id as string),
                null,
                2
              )
            }
          ]
        };

      case 'update_experience':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await experienceService.updateExperience(params.id as string, params as any),
                null,
                2
              )
            }
          ]
        };

      case 'add_skill':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await skillService.addSkill(params as any), null, 2)
            }
          ]
        };

      case 'get_skill':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await skillService.getSkill(params.id as string), null, 2)
            }
          ]
        };

      case 'update_skill':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await skillService.updateSkill(params.id as string, params as any),
                null,
                2
              )
            }
          ]
        };

      case 'add_achievement':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await achievementService.addAchievement(params as any),
                null,
                2
              )
            }
          ]
        };

      case 'get_achievement':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await achievementService.getAchievement(params.id as string),
                null,
                2
              )
            }
          ]
        };

      case 'add_project':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await projectService.addProject(params as any),
                null,
                2
              )
            }
          ]
        };

      case 'get_project':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await projectService.getProject(params.id as string),
                null,
                2
              )
            }
          ]
        };

      case 'update_project':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await projectService.updateProject(params.id as string, params as any),
                null,
                2
              )
            }
          ]
        };

      case 'search_projects':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await projectService.searchProjects({
                  tags: params.tags as TagReference[] | undefined,
                  status: params.status as ProjectStatus | undefined,
                  technologies: params.technologies as string[] | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      case 'list_tags':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await tagService.listTags(params.category as string | undefined), null, 2)
            }
          ]
        };

      case 'add_tag':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await tagService.addTag(params.name as string, params.category as string), null, 2)
            }
          ]
        };

      case 'get_tag_usage':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await tagService.getTagUsage(params.tag as string), null, 2)
            }
          ]
        };

      case 'find_similar_tags':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await tagService.findSimilarTags(
                  params.input as string,
                  params.max_distance as number | undefined,
                  params.category as string | undefined
                ),
                null,
                2
              )
            }
          ]
        };

      case 'search_experiences':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await experienceService.searchExperiences({
                  tags: params.tags as TagReference[] | undefined,
                  organization: params.organization as string | undefined,
                  dateRange: params.date_range as { start?: string; end?: string } | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      case 'search_skills':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await skillService.searchSkills({
                  tags: params.tags as TagReference[] | undefined,
                  levelMin: params.level_min as number | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      case 'search_achievements':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await achievementService.searchAchievements({
                  tags: params.tags as TagReference[] | undefined,
                  dateRange: params.date_range as { start?: string; end?: string } | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      // Certification handlers
      case 'add_certification':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await certificationService.addCertification(params as any),
                null,
                2
              )
            }
          ]
        };

      case 'get_certification':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await certificationService.getCertification(params.id as string),
                null,
                2
              )
            }
          ]
        };

      case 'update_certification':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await certificationService.updateCertification(params.id as string, params as any),
                null,
                2
              )
            }
          ]
        };

      case 'search_certifications':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await certificationService.searchCertifications({
                  tags: params.tags as TagReference[] | undefined,
                  issuer: params.issuer as string | undefined,
                  dateRange: params.date_range as { start?: string; end?: string } | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      // Education handlers
      case 'add_education':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await educationService.addEducation(params as any),
                null,
                2
              )
            }
          ]
        };

      case 'get_education':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await educationService.getEducation(params.id as string),
                null,
                2
              )
            }
          ]
        };

      case 'update_education':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await educationService.updateEducation(params.id as string, params as any),
                null,
                2
              )
            }
          ]
        };

      case 'search_education':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await educationService.searchEducation({
                  tags: params.tags as TagReference[] | undefined,
                  institution: params.institution as string | undefined,
                  dateRange: params.date_range as { start?: string; end?: string } | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      // Language handlers
      case 'add_language':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await languageService.addLanguage(params as any),
                null,
                2
              )
            }
          ]
        };

      case 'get_language':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await languageService.getLanguage(params.id as string),
                null,
                2
              )
            }
          ]
        };

      case 'update_language':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await languageService.updateLanguage(params.id as string, params as any),
                null,
                2
              )
            }
          ]
        };

      case 'search_languages':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await languageService.searchLanguages({
                  tags: params.tags as TagReference[] | undefined,
                  minProficiency: params.min_proficiency as string | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      // Hobby handlers
      case 'add_hobby':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await hobbyService.addHobby(params as any),
                null,
                2
              )
            }
          ]
        };

      case 'get_hobby':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await hobbyService.getHobby(params.id as string),
                null,
                2
              )
            }
          ]
        };

      case 'update_hobby':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await hobbyService.updateHobby(params.id as string, params as any),
                null,
                2
              )
            }
          ]
        };

      case 'search_hobbies':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await hobbyService.searchHobbies({
                  tags: params.tags as TagReference[] | undefined,
                  tool: params.tool as string | undefined
                }),
                null,
                2
              )
            }
          ]
        };

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error instanceof Error ? error.message : String(error)}`
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
