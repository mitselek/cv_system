import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../../edgedb.js';
import { ExperienceService } from '../experience.js';

describe('Experience CRUD', () => {
  let client: EdgeDBClient;
  let service: ExperienceService;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new ExperienceService(client);
    // Clean up before tests - delete entities first (they reference tags)
    try {
      await client.query('DELETE Experience');
      await client.query('DELETE Skill');
      await client.query('DELETE Achievement');
      await client.query('DELETE Tag');
    } catch (e) {
      // Some tags may be referenced by other test suites - that's OK
      // Just clean up what we can
      await client.query('DELETE Experience');
    }
    
    // KNOWN LIMITATION: Tags are matched by name only, not (name, category)
    // This means if "leadership" exists in multiple categories, it will match all.
    // Delete any conflicting tags from other test suites to ensure clean state.
    await client.query(`DELETE Tag FILTER .name = 'leadership' AND .category != 'skills'`);
    
    // Create tags for testing - use unique names to avoid collisions with other test suites
    await client.query(`
      INSERT Tag { name := 'nodejs', category := 'skills' } UNLESS CONFLICT;
      INSERT Tag { name := 'teamwork', category := 'skills' } UNLESS CONFLICT;
    `);
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should create an experience and return typed result', async () => {
    const result = await service.addExperience({
      title: 'Senior Software Engineer',
      organization: 'TechCorp',
      startDate: '2020-01-15',
      endDate: '2023-12-31',
      description: 'Led backend team',
      tags: ['nodejs', 'teamwork'],
      language: 'en'
    });

    expect(result).toHaveProperty('id');
    expect(result.title).toBe('Senior Software Engineer');
    expect(result.organization).toBe('TechCorp');
    expect(result.tags).toHaveLength(2);
    expect(result.tags).toContain('nodejs');
    expect(result.tags).toContain('teamwork');
  });

  it('should retrieve experience by ID', async () => {
    const created = await service.addExperience({
      title: 'Product Manager',
      organization: 'StartupXYZ',
      startDate: '2023-01-01',
      endDate: '2024-06-30',
      description: 'Managed product strategy',
      tags: ['pm'],
      language: 'en'
    });

    const retrieved = await service.getExperience(created.id);
    expect(retrieved).toBeDefined();
    expect(retrieved?.title).toBe('Product Manager');
    expect(retrieved?.organization).toBe('StartupXYZ');
  });

  it('should update experience fields', async () => {
    const created = await service.addExperience({
      title: 'Junior Developer',
      organization: 'OldCorp',
      startDate: '2019-06-01',
      description: 'Learning role',
      tags: ['junior'],
      language: 'en'
    });

    const updated = await service.updateExperience(created.id, {
      title: 'Mid-level Developer',
      description: 'Grew into leadership'
    });

    expect(updated.title).toBe('Mid-level Developer');
    expect(updated.description).toBe('Grew into leadership');
    expect(updated.organization).toBe('OldCorp'); // unchanged
  });

  it('should handle missing experience gracefully', async () => {
    const result = await service.getExperience('nonexistent-id');
    expect(result).toBeNull();
  });
});
