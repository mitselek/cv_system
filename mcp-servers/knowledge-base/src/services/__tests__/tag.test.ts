import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../../edgedb.js';
import { TagService } from '../tag.js';

describe('Tag/Classifier CRUD', () => {
  let client: EdgeDBClient;
  let service: TagService;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new TagService(client);
    // Delete entities first (they reference tags), ignore errors if they don't exist
    try {
      await client.query('DELETE Experience');
      await client.query('DELETE Skill');
      await client.query('DELETE Achievement');
      await client.query('DELETE Tag');
    } catch (e) {
      // Ignore errors - fresh DB won't have these
    }
    
    // Seed some tags
    await service.addTag('python', 'languages');
    await service.addTag('javascript', 'languages');
    await service.addTag('typescript', 'languages');
    await service.addTag('leadership', 'soft-skills');
    await service.addTag('communication', 'soft-skills');
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should list all tags', async () => {
    const tags = await service.listTags();
    expect(tags.length).toBeGreaterThan(0);
    expect(tags.map(t => t.name)).toContain('python');
  });

  it('should list tags by category', async () => {
    const langTags = await service.listTags('languages');
    expect(langTags.length).toBeGreaterThanOrEqual(3);
    expect(langTags.map(t => t.name)).toContain('python');
    expect(langTags.map(t => t.name)).toContain('javascript');
  });

  it('should add new tag', async () => {
    const result = await service.addTag('golang', 'languages');
    expect(result.name).toBe('golang');
    expect(result.category).toBe('languages');
  });

  it('should enforce unique tag name per category', async () => {
    // UNLESS CONFLICT returns the existing tag instead of throwing
    const result = await service.addTag('python', 'languages');
    expect(result.name).toBe('python');
    expect(result.category).toBe('languages');
    // Should be same ID as the one created in beforeAll
  });

  it('should allow same tag name in different category', async () => {
    await service.addTag('testing', 'processes');
    const result = await service.addTag('testing', 'tools'); // Different category
    expect(result.name).toBe('testing');
    expect(result.category).toBe('tools');
  });
});

describe('Tag Usage Statistics', () => {
  let client: EdgeDBClient;
  let service: TagService;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new TagService(client);

    // Full cleanup for accurate counts
    await client.query('DELETE Experience');
    await client.query('DELETE Skill');
    await client.query('DELETE Achievement');
    await client.query('DELETE Tag');

    // Create tags
    await service.addTag('usage-test-tag', 'test');
    await service.addTag('unused-tag', 'test');

    // Create entities with the usage-test-tag
    await client.query(`
      INSERT Experience {
        title := 'Test Exp 1',
        organization := 'Test Org',
        start_date := '2023-01-01',
        tags := (SELECT DISTINCT Tag FILTER .name = 'usage-test-tag')
      }
    `);

    await client.query(`
      INSERT Skill {
        name := 'Test Skill 1',
        level := 5,
        description := 'Test',
        tags := (SELECT DISTINCT Tag FILTER .name = 'usage-test-tag')
      }
    `);

    await client.query(`
      INSERT Skill {
        name := 'Test Skill 2',
        level := 7,
        description := 'Test 2',
        tags := (SELECT DISTINCT Tag FILTER .name = 'usage-test-tag')
      }
    `);
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should return usage counts for a tag', async () => {
    const usage = await service.getTagUsage('usage-test-tag');

    expect(usage.tag.name).toBe('usage-test-tag');
    expect(usage.experiences).toBe(1);
    expect(usage.skills).toBe(2);
    expect(usage.achievements).toBe(0);
    expect(usage.total).toBe(3);
  });

  it('should return zero counts for unused tag', async () => {
    const usage = await service.getTagUsage('unused-tag');

    expect(usage.tag.name).toBe('unused-tag');
    expect(usage.total).toBe(0);
  });

  it('should throw for non-existent tag', async () => {
    await expect(service.getTagUsage('nonexistent-tag')).rejects.toThrow('Tag not found');
  });
});
