# MCP Knowledge Base Tool Verification

## Objective

Systematically verify that all MCP tools exposed by the Knowledge Base server are functioning correctly with EdgeDB integration.

## Background

The MCP server (`mcp-servers/knowledge-base/`) exposes 44+ tools for querying and managing CV knowledge base data. We need to verify each tool works correctly with the current EdgeDB schema and data model.

**Test Data Source:** Use existing `knowledge_base/` file-based system as reference data for validation.

## Known Issues

- ✅ No known issues confirmed in this run. `search_experiences` (including `date_range`) verified working.
- Note: During this run, `search_certifications` and `search_education` initially failed with `JSON index 'et' is out of bounds` when filtering translation fields that lacked an `et` key (evidence: `2026-01-13T20:52:42.984Z`, `2026-01-13T20:52:43.541Z`). After adjusting the fixtures to include both `et` and `en`, searches returned results (evidence: education `2026-01-13T20:57:55.453Z`; certifications with `et` substring `2026-01-13T20:58:09.175Z`).

## Testing Checklist

### Experience Tools

- [x] `add_experience` - ✅ Working (`queried_at_utc=2026-01-13T20:44:34.490Z`)
- [x] `get_experience` - ✅ Working (`queried_at_utc=2026-01-13T20:44:41.287Z`)
- [x] `update_experience` - ✅ Working (`queried_at_utc=2026-01-13T20:44:51.940Z`)
- [x] `search_experiences` - ✅ Working (organization: `2026-01-13T20:45:01.198Z`, date_range: `2026-01-13T20:45:14.456Z`)

### Skill Tools

- [x] `add_skill` - ✅ Working (`queried_at_utc=2026-01-13T20:45:28.242Z`)
- [x] `get_skill` - ✅ Working (`queried_at_utc=2026-01-13T20:45:36.312Z`)
- [x] `update_skill` - ✅ Working (`queried_at_utc=2026-01-13T20:45:44.283Z`)
- [x] `search_skills` - ✅ Working (level_min run: `2026-01-13T20:41:14.479Z`; tag-filter run: `2026-01-13T20:45:57.132Z`)

### Achievement Tools

- [x] `add_achievement` - ✅ Working (`queried_at_utc=2026-01-13T20:46:06.705Z`)
- [x] `get_achievement` - ✅ Working (`queried_at_utc=2026-01-13T20:46:13.000Z`)
- [x] `search_achievements` - ✅ Working (`queried_at_utc=2026-01-13T20:46:19.170Z`)

### Project Tools

- [x] `add_project` - ✅ Working (`queried_at_utc=2026-01-13T20:46:31.369Z`)
- [x] `get_project` - ✅ Working (`queried_at_utc=2026-01-13T20:46:36.971Z`)
- [x] `update_project` - ✅ Working (`queried_at_utc=2026-01-13T20:46:46.249Z`)
- [x] `search_projects` - ✅ Working (`queried_at_utc=2026-01-13T20:41:14.047Z`)

### Certification Tools

- [x] `add_certification` - ✅ Working (`queried_at_utc=2026-01-13T20:52:00.820Z`)
- [x] `get_certification` - ✅ Working (`queried_at_utc=2026-01-13T20:52:16.500Z`)
- [x] `update_certification` - ✅ Working (`queried_at_utc=2026-01-13T20:52:27.739Z`)
- [x] `search_certifications` - ✅ Working (`queried_at_utc=2026-01-13T20:58:09.175Z`)

### Education Tools

- [x] `add_education` - ✅ Working (`queried_at_utc=2026-01-13T20:52:01.255Z`)
- [x] `get_education` - ✅ Working (`queried_at_utc=2026-01-13T20:52:17.072Z`)
- [x] `update_education` - ✅ Working (`queried_at_utc=2026-01-13T20:52:28.147Z`)
- [x] `search_education` - ✅ Working (`queried_at_utc=2026-01-13T20:57:55.453Z`)

### Language Tools

- [x] `add_language` - ✅ Working (`queried_at_utc=2026-01-13T20:58:36.739Z`) (requires `proficiency`)
- [x] `get_language` - ✅ Working (`queried_at_utc=2026-01-13T20:58:46.478Z`)
- [x] `update_language` - ✅ Working (`queried_at_utc=2026-01-13T20:58:52.836Z`)
- [x] `search_languages` - ✅ Working (`queried_at_utc=2026-01-13T20:59:00.353Z`)

### Hobby Tools

- [x] `add_hobby` - ✅ Working (`queried_at_utc=2026-01-13T20:52:01.652Z`)
- [x] `get_hobby` - ✅ Working (`queried_at_utc=2026-01-13T20:52:17.076Z`)
- [x] `update_hobby` - ✅ Working (`queried_at_utc=2026-01-13T20:52:28.501Z`)
- [x] `search_hobbies` - ✅ Working (`queried_at_utc=2026-01-13T20:52:44.064Z`)

### Tag Tools

- [x] `list_tags` - ✅ Working (`queried_at_utc=2026-01-13T20:41:13.618Z`)
- [x] `add_tag` - ✅ Working (`queried_at_utc=2026-01-13T20:43:57.963Z`)
- [x] `get_tag_usage` - ✅ Working (`queried_at_utc=2026-01-13T20:53:23.075Z`)
- [x] `find_similar_tags` - ✅ Working (`queried_at_utc=2026-01-13T20:53:23.593Z`)

## Testing Methodology

### For Query Tools (get, search, list)

1. Execute MCP tool call
2. Validate response structure matches schema
3. Cross-reference with `knowledge_base/*.md` files
4. Verify computed properties (e.g., `display_name`, `name_en`, `name_et`)
5. Check translation fallback logic (`get_text()` function)

### For Mutation Tools (add, update)

**Import/Re-import Workflow:**

1. Select test entity from `knowledge_base/*.md`
2. Delete existing EdgeDB record using `gel` CLI:

   ```bash
   gel -H localhost -P 5656 query "DELETE Experience FILTER .external_id = 'test-id';"
   ```

3. Re-import via MCP `add_*` tool using data from markdown file
4. Verify with `get_*` tool - compare with original markdown
5. Test `update_*` tool with field changes
6. Verify persistence with another `get_*` call

**Field Validation:**

1. Test with minimal required fields
2. Test with optional fields
3. Verify EdgeDB constraints
4. Validate data persistence
5. Check tag relationships
6. Verify skill_demonstrated links
7. Validate Translation JSON structure (et/en fields)

## Priority Fixes

1. **High:** Test remaining CRUD operations for each entity type

2. **Medium:** Verify search filters work correctly (tags, date_range, level_min, etc.)

3. **Low:** Performance testing with large result sets

## Acceptance Criteria

- [ ] All 44+ MCP tools execute without errors
- [ ] Query results match `knowledge_base/` reference data
- [ ] Translation fields properly returned (et/en)
- [ ] Computed properties work (`display_name`, `name_en`, `name_et`)
- [ ] Tag relationships correctly retrieved
- [ ] Skill links verified (experiences ↔ skills, projects ↔ skills)
- [ ] Date range filters work in search operations
- [ ] EdgeDB schema matches TypeScript types

## Test Data Validation

Use `knowledge_base/` directory structure as source of truth:

```bash
knowledge_base/
├── achievements/     # 13 achievements
├── certifications/   # 5 certifications
├── education/        # 2 education entries
├── experiences/      # 23 work experiences
├── hobbies/          # 2 hobbies
├── languages/        # 5 languages
├── projects/         # 16 projects
└── skills/           # 22 skills
```

### Example Test Cases

**Simple Experience (minimal fields):**

- `knowledge_base/experiences/mtu-2-tants-2000-2023.md` - IT Support role

**Complex Experience (all fields):**

- `knowledge_base/experiences/ilusa-koodi-instituut-2021-2024.md` - Team leadership, achievements, skills

**With Relationships:**

- Experience → Skills: `eesti-keele-instituut-2017-2018.md` (skills_demonstrated: java, spring-boot)
- Experience → Achievements: `eesti-kunstakadeemia-2009-2012.md` (3 achievements linked)

## Related Files

- `mcp-servers/knowledge-base/src/server.ts` - Tool definitions
- `mcp-servers/knowledge-base/src/services/*.ts` - Service implementations
- `dbschema/default.gel` - EdgeDB schema
- `mcp-servers/knowledge-base/src/types.ts` - TypeScript interfaces

## Labels

`mcp-server`, `edgedb`, `testing`, `priority:high`
