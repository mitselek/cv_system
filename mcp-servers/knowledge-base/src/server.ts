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

const server = new Server({
  name: 'cv-system-knb-mcp',
  version: '0.1.0'
});

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
            tags: { type: 'array', items: { type: 'string' }, description: 'Associated tags' },
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
            tags: { type: 'array', items: { type: 'string' } }
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
            tags: { type: 'array', items: { type: 'string' } }
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
      }
    ]
  };
});

/**
 * Handle tool calls
 */
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'add_experience':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await experienceService.addExperience(args as any),
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
                await experienceService.getExperience(args.id),
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
                await experienceService.updateExperience(args.id, args as any),
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
              text: JSON.stringify(await skillService.addSkill(args as any), null, 2)
            }
          ]
        };

      case 'get_skill':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await skillService.getSkill(args.id), null, 2)
            }
          ]
        };

      case 'update_skill':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(
                await skillService.updateSkill(args.id, args as any),
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
                await achievementService.addAchievement(args as any),
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
                await achievementService.getAchievement(args.id),
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
              text: JSON.stringify(await tagService.listTags(args.category), null, 2)
            }
          ]
        };

      case 'add_tag':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await tagService.addTag(args.name, args.category), null, 2)
            }
          ]
        };

      case 'get_tag_usage':
        return {
          content: [
            {
              type: 'text',
              text: JSON.stringify(await tagService.getTagUsage(args.tag), null, 2)
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
