import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../src/edgedb.js';
import { TagService } from '../src/services/tag.js';

describe('Tag/Classifier CRUD', () => {
  let client: EdgeDBClient;
  let service: TagService;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new TagService(client);
    await client.query('DELETE Tag');
    
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
    await expect(
      service.addTag('python', 'languages')
    ).rejects.toThrow();
  });

  it('should allow same tag name in different category', async () => {
    await service.addTag('testing', 'processes');
    const result = await service.addTag('testing', 'tools'); // Different category
    expect(result.name).toBe('testing');
    expect(result.category).toBe('tools');
  });
});
