/**
 * MCP Server Entry Point for Knowledge Base
 */
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { EdgeDBClient } from './edgedb.js';
import { ExperienceService, type TagReference } from './services/experience.js';
import { SkillService } from './services/skill.js';
import { AchievementService } from './services/achievement.js';
import { TagService } from './services/tag.js';

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
