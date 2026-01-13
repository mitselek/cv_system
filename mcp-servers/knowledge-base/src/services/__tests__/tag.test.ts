import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../../edgedb.js';
import { TagService } from '../tag.js';
import { SkillService } from '../skill.js';
import { ExperienceService } from '../experience.js';
import { SkillCategory } from '../../types.js';

describe('Tag/Classifier CRUD', () => {
  let client: EdgeDBClient;
  let service: TagService;
  const PREFIX = 'vitest-tag-crud';

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new TagService(client);

    // Scoped cleanup
    await client.query(
      `DELETE Tag FILTER .name LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );

    // Seed some tags (suite-scoped to avoid collisions)
    await service.addTag(`${PREFIX}-python`, 'languages');
    await service.addTag(`${PREFIX}-javascript`, 'languages');
    await service.addTag(`${PREFIX}-typescript`, 'languages');
    await service.addTag(`${PREFIX}-leadership`, 'soft-skills');
    await service.addTag(`${PREFIX}-communication`, 'soft-skills');
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should list all tags', async () => {
    const tags = await service.listTags();
    expect(tags.length).toBeGreaterThan(0);
    expect(tags.map(t => t.name)).toContain(`${PREFIX}-python`);
  });

  it('should list tags by category', async () => {
    const langTags = await service.listTags('languages');
    expect(langTags.length).toBeGreaterThanOrEqual(3);
    expect(langTags.map(t => t.name)).toContain(`${PREFIX}-python`);
    expect(langTags.map(t => t.name)).toContain(`${PREFIX}-javascript`);
  });

  it('should add new tag', async () => {
    const result = await service.addTag(`${PREFIX}-golang`, 'languages');
    expect(result.name).toBe(`${PREFIX}-golang`);
    expect(result.category).toBe('languages');
  });

  it('should enforce unique tag name per category', async () => {
    // UNLESS CONFLICT returns the existing tag instead of throwing
    const result = await service.addTag(`${PREFIX}-python`, 'languages');
    expect(result.name).toBe(`${PREFIX}-python`);
    expect(result.category).toBe('languages');
    // Should be same ID as the one created in beforeAll
  });

  it('should allow same tag name in different category', async () => {
    await service.addTag(`${PREFIX}-testing`, 'processes');
    const result = await service.addTag(`${PREFIX}-testing`, 'tools'); // Different category
    expect(result.name).toBe(`${PREFIX}-testing`);
    expect(result.category).toBe('tools');
  });
});

describe('Tag Usage Statistics', () => {
  let client: EdgeDBClient;
  let service: TagService;
  let skillService: SkillService;
  let experienceService: ExperienceService;
  const PREFIX = 'vitest-tag-usage';
  const tagInUse = `${PREFIX}-in-use`;
  const tagUnused = `${PREFIX}-unused`;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new TagService(client);

    skillService = new SkillService(client);
    experienceService = new ExperienceService(client);

    // Scoped cleanup
    await client.query(
      `DELETE Achievement FILTER .external_id LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );
    await client.query(
      `DELETE Experience FILTER .external_id LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );
    await client.query(
      `DELETE Skill FILTER .external_id LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );
    await client.query(
      `DELETE Tag FILTER .name LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );

    // Create tags
    await service.addTag(tagInUse, 'test');
    await service.addTag(tagUnused, 'test');

    // Create entities with the in-use tag
    await experienceService.addExperience({
      external_id: `${PREFIX}-exp-1`,
      title: { en: 'Test Experience' },
      company: { en: 'Test Org' },
      dates: { start: '2023-01-01', end: '2023-12-31' },
      article: { en: 'Test' },
      last_verified: '2024-01-01',
      tags: [{ name: tagInUse, category: 'test' }]
    });

    await skillService.addSkill({
      external_id: `${PREFIX}-skill-1`,
      name: { en: 'Test Skill 1' },
      category: SkillCategory.Other,
      level: 5,
      article: { en: 'Test' },
      last_verified: '2024-01-01',
      tags: [{ name: tagInUse, category: 'test' }]
    });

    await skillService.addSkill({
      external_id: `${PREFIX}-skill-2`,
      name: { en: 'Test Skill 2' },
      category: SkillCategory.Other,
      level: 7,
      article: { en: 'Test 2' },
      last_verified: '2024-01-01',
      tags: [{ name: tagInUse, category: 'test' }]
    });

  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should return usage counts for a tag', async () => {
    const usage = await service.getTagUsage(tagInUse);

    expect(usage.tag.name).toBe(tagInUse);
    expect(usage.experiences).toBe(1);
    expect(usage.skills).toBe(2);
    expect(usage.total).toBe(3);
  });

  it('should return zero counts for unused tag', async () => {
    const usage = await service.getTagUsage(tagUnused);

    expect(usage.tag.name).toBe(tagUnused);
    expect(usage.total).toBe(0);
  });

  it('should throw for non-existent tag', async () => {
    await expect(service.getTagUsage('nonexistent-tag')).rejects.toThrow('Tag not found');
  });
});

describe('Fuzzy Tag Matching', () => {
  let client: EdgeDBClient;
  let service: TagService;
  const PREFIX = 'vitest-tag-fuzzy';

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new TagService(client);

    // Scoped cleanup
    await client.query(
      `DELETE Tag FILTER .name LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );

    // Create test tags
    await service.addTag(`${PREFIX}-javascript`, 'languages');
    await service.addTag(`${PREFIX}-typescript`, 'languages');
    await service.addTag(`${PREFIX}-python`, 'languages');
    await service.addTag(`${PREFIX}-leadership`, 'soft-skills');
    await service.addTag(`${PREFIX}-communication`, 'soft-skills');
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should suggest correction for typo', async () => {
    const suggestions = await service.findSimilarTags(`${PREFIX}-javascrip`);
    
    expect(suggestions).toHaveLength(1);
    expect(suggestions[0].name).toBe(`${PREFIX}-javascript`);
    expect(suggestions[0].distance).toBeLessThanOrEqual(2);
  });

  it('should return multiple suggestions within threshold', async () => {
    const suggestions = await service.findSimilarTags(`${PREFIX}-typscript`, 2);
    
    expect(suggestions.length).toBeGreaterThan(0);
    expect(suggestions[0].name).toBe(`${PREFIX}-typescript`);
  });

  it('should return empty array when no similar tags', async () => {
    const suggestions = await service.findSimilarTags('golang', 2);
    
    expect(suggestions).toHaveLength(0);
  });

  it('should filter by category when provided', async () => {
    const suggestions = await service.findSimilarTags(`${PREFIX}-leadrship`, 2, 'soft-skills');
    
    expect(suggestions).toHaveLength(1);
    expect(suggestions[0].name).toBe(`${PREFIX}-leadership`);
    expect(suggestions[0].category).toBe('soft-skills');
  });

  it('should return suggestions sorted by distance', async () => {
    // 'typscript' is closer to 'typescript' than 'javascript'
    const suggestions = await service.findSimilarTags(`${PREFIX}-typscript`, 3);
    
    expect(suggestions.length).toBeGreaterThan(0);
    // First result should be closest match
    expect(suggestions[0].distance).toBeLessThanOrEqual(suggestions[suggestions.length - 1].distance);
  });
});
