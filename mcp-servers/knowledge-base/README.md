# Knowledge Base MCP Server

TypeScript + EdgeDB implementation of the Knowledge Base MCP server for the CV System.

## Features

- **Type-Safe CRUD Operations:** Full type safety from database to MCP tools
- **Test-Driven Development:** All operations tested before implementation
- **EdgeDB Integration:** Leverages graph-relational database for complex queries
- **MCP Protocol:** Compliant Model Context Protocol server for VS Code integration

## Architecture

```
src/
  edgedb.ts              # EdgeDB client wrapper
  server.ts              # MCP server entry point + tool handlers
  services/
    experience.ts        # Experience CRUD
    skill.ts             # Skill CRUD
    achievement.ts       # Achievement CRUD
    tag.ts               # Tag/classifier management
    __tests__/
      *.test.ts          # Test suite (TDD-first)
```

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Generate EdgeDB Types

```bash
npm run edgedb:generate
```

### 3. Run Tests

```bash
npm test
```

### 4. Build

```bash
npm run build
```

### 5. Run Server

```bash
npm start
```

## Testing

Tests are written first (TDD), then implementation follows.

### Run All Tests
```bash
npm test
```

### Watch Mode
```bash
npm test -- --watch
```

### Coverage
```bash
npm run test:coverage
```

### UI Dashboard
```bash
npm run test:ui
```

## Services

### ExperienceService
- `addExperience(input)` - Create work experience
- `getExperience(id)` - Retrieve by ID
- `updateExperience(id, updates)` - Update fields

### SkillService
- `addSkill(input)` - Create skill with level validation (1-10)
- `getSkill(id)` - Retrieve by ID
- `updateSkill(id, updates)` - Update fields

### AchievementService
- `addAchievement(input)` - Create achievement with date parsing
- `getAchievement(id)` - Retrieve by ID
- `updateAchievement(id, updates)` - Update fields

### TagService
- `listTags(category?)` - List all or filtered tags
- `addTag(name, category)` - Create classifier
- `getTagUsage(tag)` - Usage statistics

## MCP Tools

All services are exposed as MCP tools:

- `add_experience` - Create experience
- `get_experience` - Retrieve experience
- `update_experience` - Update experience
- `add_skill` - Create skill
- `get_skill` - Retrieve skill
- `update_skill` - Update skill
- `add_achievement` - Create achievement
- `get_achievement` - Retrieve achievement
- `list_tags` - List tags
- `add_tag` - Create tag
- `get_tag_usage` - Get tag statistics

## Type Safety

TypeScript with strict mode + EdgeDB types provide end-to-end type safety:

1. **Database Level:** Schema constraints in EdgeDB SDL
2. **Query Level:** EdgeDB query builder with generated types
3. **Service Level:** Service methods with strict input/output types
4. **Tool Level:** MCP tool input schemas match TypeScript interfaces
5. **Static Checking:** TypeScript compiler catches all type mismatches

## Configuration

Environment variables:

- `EDGEDB_DSN` - Connection string (default: `edgedb://edgedb@localhost:5656/edgedb`)
- `EDGEDB_TLS_SECURITY` - TLS mode (default: `insecure` for dev)

## Development Workflow

1. Write test cases in `src/services/__tests__/`
2. Run tests (will fail initially)
3. Implement service methods
4. Run tests until passing
5. Add MCP tool handlers in `src/server.ts`
6. Verify type safety: `npm run type-check`

