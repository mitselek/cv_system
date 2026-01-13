# MCP Knowledge Base Tool Verification

## Objective

Systematically verify that all MCP tools exposed by the Knowledge Base server are functioning correctly with EdgeDB integration.

## Background

The MCP server (`mcp-servers/knowledge-base/`) exposes 44+ tools for querying and managing CV knowledge base data. We need to verify each tool works correctly with the current EdgeDB schema and data model.

**Test Data Source:** Use existing `knowledge_base/` file-based system as reference data for validation.

## Known Issues

- ❌ **`search_experiences`** - EdgeDB query error: `Unexpected keyword 'START'` (reserved keyword conflict in dates field)

## Testing Checklist

### Experience Tools

- [x] `list_tags` - ✅ Working (retrieved 182 tags)
- [ ] `add_experience`
- [x] `get_experience` - Needs testing
- [ ] `update_experience`
- [ ] ❌ `search_experiences` - **BROKEN** (keyword conflict)

### Skill Tools

- [ ] `add_skill`
- [x] `get_skill` - ✅ Working (Python skill retrieved successfully)
- [ ] `update_skill`
- [x] `search_skills` - ✅ Working (found 13 skills with level ≥8)

### Achievement Tools

- [ ] `add_achievement`
- [ ] `get_achievement`
- [ ] `search_achievements`

### Project Tools

- [ ] `add_project`
- [ ] `get_project`
- [ ] `update_project`
- [x] `search_projects` - ✅ Working (found 16 active projects)

### Certification Tools

- [ ] `add_certification`
- [ ] `get_certification`
- [ ] `update_certification`
- [ ] `search_certifications`

### Education Tools

- [ ] `add_education`
- [ ] `get_education`
- [ ] `update_education`
- [ ] `search_education`

### Language Tools

- [ ] `add_language`
- [ ] `get_language`
- [ ] `update_language`
- [ ] `search_languages`

### Hobby Tools

- [ ] `add_hobby`
- [ ] `get_hobby`
- [ ] `update_hobby`
- [ ] `search_hobbies`

### Tag Tools

- [x] `list_tags` - ✅ Working (all tags retrieved)
- [ ] `add_tag`
- [ ] `get_tag_usage`
- [ ] `find_similar_tags`

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

1. **Critical:** Fix `search_experiences` EdgeDB query

   - Issue: Reserved keyword `start` in `dates: { start, end }`
   - Solution: Use backticks `\`start\`` or rename field
   - File: `mcp-servers/knowledge-base/src/services/experience.ts`

2. **High:** Test all CRUD operations for each entity type

3. **Medium:** Verify search filters work correctly (tags, date_range, level_min, etc.)

4. **Low:** Performance testing with large result sets

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
