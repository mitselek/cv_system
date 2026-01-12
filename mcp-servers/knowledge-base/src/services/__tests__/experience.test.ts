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
    
    // Create tags for testing
    await client.query(`
      INSERT Tag { name := 'nodejs', category := 'languages' } UNLESS CONFLICT;
      INSERT Tag { name := 'teamwork', category := 'soft-skills' } UNLESS CONFLICT;
      INSERT Tag { name := 'python', category := 'languages' } UNLESS CONFLICT;
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
      tags: [
        { name: 'nodejs', category: 'languages' },
        { name: 'teamwork', category: 'soft-skills' }
      ],
      language: 'en'
    });

    expect(result).toHaveProperty('id');
    expect(result.title).toBe('Senior Software Engineer');
    expect(result.organization).toBe('TechCorp');
    expect(result.tags).toHaveLength(2);
    expect(result.tags).toContainEqual({ name: 'nodejs', category: 'languages' });
    expect(result.tags).toContainEqual({ name: 'teamwork', category: 'soft-skills' });
  });

  it('should retrieve experience by ID', async () => {
    const created = await service.addExperience({
      title: 'Product Manager',
      organization: 'StartupXYZ',
      startDate: '2023-01-01',
      endDate: '2024-06-30',
      description: 'Managed product strategy',
      tags: [{ name: 'pm', category: 'skills' }],
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
      tags: [{ name: 'junior', category: 'skills' }],
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

describe('Experience Search', () => {
  let client: EdgeDBClient;
  let service: ExperienceService;
  let exp1Id: string;
  let exp2Id: string;
  let exp3Id: string;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new ExperienceService(client);
    
    // Clean up
    await client.query('DELETE Experience');
    await client.query(`DELETE Tag FILTER .name IN {'search-nodejs', 'search-python', 'search-teamwork'}`);
    
    // Create test tags
    await client.query(`
      INSERT Tag { name := 'search-nodejs', category := 'skills' } UNLESS CONFLICT;
      INSERT Tag { name := 'search-python', category := 'skills' } UNLESS CONFLICT;
      INSERT Tag { name := 'search-teamwork', category := 'skills' } UNLESS CONFLICT;
    `);
    
    // Create test experiences
    const exp1 = await service.addExperience({
      title: 'Node.js Developer',
      organization: 'TechCorp',
      startDate: '2020-01-01',
      endDate: '2021-12-31',
      description: 'Backend development',
      tags: [
        { name: 'search-nodejs', category: 'skills' },
        { name: 'search-teamwork', category: 'skills' }
      ],
      language: 'en'
    });
    exp1Id = exp1.id;
    
    const exp2 = await service.addExperience({
      title: 'Python Engineer',
      organization: 'DataCorp',
      startDate: '2022-01-01',
      endDate: '2023-06-30',
      description: 'Data pipelines',
      tags: [{ name: 'search-python', category: 'skills' }],
      language: 'en'
    });
    exp2Id = exp2.id;
    
    const exp3 = await service.addExperience({
      title: 'Full Stack Developer',
      organization: 'TechCorp',
      startDate: '2023-07-01',
      description: 'Both frontend and backend',
      tags: [
        { name: 'search-nodejs', category: 'skills' },
        { name: 'search-python', category: 'skills' }
      ],
      language: 'en'
    });
    exp3Id = exp3.id;
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should search experiences by single tag', async () => {
    const results = await service.searchExperiences({ 
      tags: [{ name: 'search-nodejs', category: 'skills' }] 
    });
    
    expect(results).toHaveLength(2);
    expect(results.map(r => r.id)).toContain(exp1Id);
    expect(results.map(r => r.id)).toContain(exp3Id);
  });

  it('should search experiences by multiple tags (AND logic)', async () => {
    const results = await service.searchExperiences({ 
      tags: [
        { name: 'search-nodejs', category: 'skills' },
        { name: 'search-python', category: 'skills' }
      ] 
    });
    
    expect(results).toHaveLength(1);
    expect(results[0].id).toBe(exp3Id);
  });

  it('should search experiences by organization', async () => {
    const results = await service.searchExperiences({ 
      organization: 'TechCorp' 
    });
    
    expect(results).toHaveLength(2);
    expect(results.map(r => r.id)).toContain(exp1Id);
    expect(results.map(r => r.id)).toContain(exp3Id);
  });

  it('should search experiences by date range', async () => {
    const results = await service.searchExperiences({ 
      dateRange: { start: '2022-01-01', end: '2023-12-31' }
    });
    
    // Should include exp2 (started 2022-01-01) and exp3 (started 2023-07-01, no end date)
    expect(results.length).toBeGreaterThanOrEqual(2);
    expect(results.map(r => r.id)).toContain(exp2Id);
    expect(results.map(r => r.id)).toContain(exp3Id);
  });

  it('should combine multiple search filters', async () => {
    const results = await service.searchExperiences({ 
      organization: 'TechCorp',
      tags: [{ name: 'search-nodejs', category: 'skills' }]
    });
    
    expect(results).toHaveLength(2);
    expect(results.map(r => r.id)).toContain(exp1Id);
    expect(results.map(r => r.id)).toContain(exp3Id);
  });

  it('should return empty array when no matches', async () => {
    const results = await service.searchExperiences({ 
      organization: 'NonexistentCorp' 
    });
    
    expect(results).toHaveLength(0);
  });
});
