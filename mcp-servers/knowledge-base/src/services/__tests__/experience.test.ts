import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../src/edgedb.js';
import { ExperienceService } from '../src/services/experience.js';

describe('Experience CRUD', () => {
  let client: EdgeDBClient;
  let service: ExperienceService;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new ExperienceService(client);
    // Clean up before tests
    await client.query('DELETE Experience');
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
      tags: ['backend', 'leadership'],
      language: 'en'
    });

    expect(result).toHaveProperty('id');
    expect(result.title).toBe('Senior Software Engineer');
    expect(result.organization).toBe('TechCorp');
    expect(result.tags).toEqual(['backend', 'leadership']);
  });

  it('should retrieve experience by ID', async () => {
    const created = await service.addExperience({
      title: 'Product Manager',
      organization: 'StartupXYZ',
      startDate: '2023-01-01',
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
