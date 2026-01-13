import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../../edgedb.js';
import { ExperienceService } from '../experience.js';
import { TagService } from '../tag.js';

describe('Experience CRUD', () => {
  let client: EdgeDBClient;
  let service: ExperienceService;
  let tagService: TagService;
  const PREFIX = 'vitest-exp-crud';

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new ExperienceService(client);
    tagService = new TagService(client);

    // Scoped cleanup (never wipe shared DB state)
    await client.query(
      `DELETE Experience FILTER .external_id LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );
    await client.query(
      `DELETE Tag FILTER .name LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );

    // Create tags for testing
    await tagService.addTag(`${PREFIX}-nodejs`, 'languages');
    await tagService.addTag(`${PREFIX}-teamwork`, 'soft-skills');
    await tagService.addTag(`${PREFIX}-python`, 'languages');
    await tagService.addTag(`${PREFIX}-pm`, 'skills');
    await tagService.addTag(`${PREFIX}-junior`, 'skills');
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should create an experience and return typed result', async () => {
    const result = await service.addExperience({
      external_id: `${PREFIX}-1`,
      title: { en: 'Senior Software Engineer' },
      company: { en: 'TechCorp' },
      dates: { start: '2020-01-15', end: '2023-12-31' },
      article: { en: 'Led backend team' },
      last_verified: '2024-01-01',
      tags: [
        { name: `${PREFIX}-nodejs`, category: 'languages' },
        { name: `${PREFIX}-teamwork`, category: 'soft-skills' }
      ]
    });

    expect(result).toHaveProperty('id');
    expect(result.title.en).toBe('Senior Software Engineer');
    expect(result.company.en).toBe('TechCorp');
    expect(result.tags).toHaveLength(2);
    expect(result.tags).toContainEqual({ name: `${PREFIX}-nodejs`, category: 'languages' });
    expect(result.tags).toContainEqual({ name: `${PREFIX}-teamwork`, category: 'soft-skills' });
  });

  it('should retrieve experience by ID', async () => {
    const created = await service.addExperience({
      external_id: `${PREFIX}-2`,
      title: { en: 'Product Manager' },
      company: { en: 'StartupXYZ' },
      dates: { start: '2023-01-01', end: '2024-06-30' },
      article: { en: 'Managed product strategy' },
      last_verified: '2024-01-01',
      tags: [{ name: `${PREFIX}-pm`, category: 'skills' }]
    });

    const retrieved = await service.getExperience(created.id);
    expect(retrieved).toBeDefined();
    expect(retrieved?.title.en).toBe('Product Manager');
    expect(retrieved?.company.en).toBe('StartupXYZ');
  });

  it('should update experience fields', async () => {
    const created = await service.addExperience({
      external_id: `${PREFIX}-3`,
      title: { en: 'Junior Developer' },
      company: { en: 'OldCorp' },
      dates: { start: '2019-06-01', end: '2020-05-31' },
      article: { en: 'Learning role' },
      last_verified: '2024-01-01',
      tags: [{ name: `${PREFIX}-junior`, category: 'skills' }]
    });

    const updated = await service.updateExperience(created.id, {
      title: { en: 'Mid-level Developer' },
      article: { en: 'Grew into leadership' }
    });

    expect(updated.title.en).toBe('Mid-level Developer');
    expect(updated.article?.en).toContain('Grew into leadership');
    expect(updated.company.en).toBe('OldCorp'); // unchanged
  });

  it('should handle missing experience gracefully', async () => {
    const fakeUuid = '00000000-0000-0000-0000-000000000000';
    const result = await service.getExperience(fakeUuid);
    expect(result).toBeNull();
  });
});

describe('Experience Search', () => {
  let client: EdgeDBClient;
  let service: ExperienceService;
  let tagService: TagService;
  let exp1Id: string;
  let exp2Id: string;
  let exp3Id: string;
  const PREFIX = 'vitest-exp-search';

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new ExperienceService(client);
    tagService = new TagService(client);
    
    // Scoped cleanup
    await client.query(
      `DELETE Experience FILTER .external_id LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );
    await client.query(
      `DELETE Tag FILTER .name LIKE <str>$prefix`,
      { prefix: `${PREFIX}%` }
    );

    // Create test tags
    await tagService.addTag(`${PREFIX}-nodejs`, 'skills');
    await tagService.addTag(`${PREFIX}-python`, 'skills');
    await tagService.addTag(`${PREFIX}-teamwork`, 'skills');
    
    // Create test experiences
    const exp1 = await service.addExperience({
      external_id: `${PREFIX}-1`,
      title: { en: 'Node.js Developer' },
      company: { en: `${PREFIX}-TechCorp` },
      dates: { start: '2020-01-01', end: '2021-12-31' },
      article: { en: 'Backend development' },
      last_verified: '2024-01-01',
      tags: [
        { name: `${PREFIX}-nodejs`, category: 'skills' },
        { name: `${PREFIX}-teamwork`, category: 'skills' }
      ]
    });
    exp1Id = exp1.id;
    
    const exp2 = await service.addExperience({
      external_id: `${PREFIX}-2`,
      title: { en: 'Python Engineer' },
      company: { en: 'DataCorp' },
      dates: { start: '2022-01-01', end: '2023-06-30' },
      article: { en: 'Data pipelines' },
      last_verified: '2024-01-01',
      tags: [{ name: `${PREFIX}-python`, category: 'skills' }]
    });
    exp2Id = exp2.id;
    
    const exp3 = await service.addExperience({
      external_id: `${PREFIX}-3`,
      title: { en: 'Full Stack Developer' },
      company: { en: `${PREFIX}-TechCorp` },
      dates: { start: '2023-07-01', end: '2024-12-31' },
      article: { en: 'Both frontend and backend' },
      last_verified: '2024-01-01',
      tags: [
        { name: `${PREFIX}-nodejs`, category: 'skills' },
        { name: `${PREFIX}-python`, category: 'skills' }
      ]
    });
    exp3Id = exp3.id;
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should search experiences by single tag', async () => {
    const results = await service.searchExperiences({ 
      tags: [{ name: `${PREFIX}-nodejs`, category: 'skills' }] 
    });
    
    expect(results).toHaveLength(2);
    expect(results.map(r => r.id)).toContain(exp1Id);
    expect(results.map(r => r.id)).toContain(exp3Id);
  });

  it('should search experiences by multiple tags (AND logic)', async () => {
    const results = await service.searchExperiences({ 
      tags: [
        { name: `${PREFIX}-nodejs`, category: 'skills' },
        { name: `${PREFIX}-python`, category: 'skills' }
      ] 
    });
    
    expect(results).toHaveLength(1);
    expect(results[0].id).toBe(exp3Id);
  });

  it('should search experiences by organization', async () => {
    const results = await service.searchExperiences({ 
      organization: `${PREFIX}-TechCorp` 
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
      organization: `${PREFIX}-TechCorp`,
      tags: [{ name: `${PREFIX}-nodejs`, category: 'skills' }]
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
