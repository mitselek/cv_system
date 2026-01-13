import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../../edgedb.js';
import { SkillService } from '../skill.js';
import { SkillCategory } from '../../types.js';

describe('Skill CRUD', () => {
  let client: EdgeDBClient;
  let service: SkillService;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new SkillService(client);
    await client.query('DELETE Skill');
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should create a skill with level validation', async () => {
    const result = await service.addSkill({
      external_id: 'test-skill-python',
      name: { en: 'Python' },
      category: SkillCategory.ProgrammingLanguage,
      level: 9,
      article: { en: 'Expert-level Python programming' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'languages', category: 'languages' },
        { name: 'backend', category: 'skills' }
      ]
    });

    expect(result).toHaveProperty('id');
    expect(result.name.en).toBe('Python');
    expect(result.level).toBe(9);
    expect(result.level).toBeGreaterThanOrEqual(1);
    expect(result.level).toBeLessThanOrEqual(10);
  });

  it('should reject invalid level values', async () => {
    await expect(
      service.addSkill({
        external_id: 'test-skill-invalid',
        name: { en: 'JavaScript' },
        category: SkillCategory.ProgrammingLanguage,
        level: 11, // Invalid
        last_verified: '2024-01-01',
        tags: []
      })
    ).rejects.toThrow();
  });

  it('should retrieve skill by ID', async () => {
    const created = await service.addSkill({
      external_id: 'test-skill-ts',
      name: { en: 'TypeScript' },
      category: SkillCategory.ProgrammingLanguage,
      level: 8,
      article: { en: 'Strong TypeScript skills' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'languages', category: 'languages' },
        { name: 'frontend', category: 'skills' }
      ]
    });

    const retrieved = await service.getSkill(created.id);
    expect(retrieved?.name.en).toBe('TypeScript');
    expect(retrieved?.level).toBe(8);
  });

  it('should update skill fields', async () => {
    const created = await service.addSkill({
      external_id: 'test-skill-docker',
      name: { en: 'Docker' },
      category: SkillCategory.DevOps,
      level: 7,
      article: { en: 'Working knowledge' },
      last_verified: '2024-01-01',
      tags: [{ name: 'devops', category: 'skills' }]
    });

    const updated = await service.updateSkill(created.id, {
      level: 8,
      article: { en: 'Advanced Docker experience' }
    });

    expect(updated.level).toBe(8);
    expect(updated.article?.en).toBe('Advanced Docker experience');
  });

  it('should enforce unique skill names', async () => {
    await service.addSkill({
      external_id: 'test-skill-k8s',
      name: { en: 'Kubernetes' },
      category: SkillCategory.DevOps,
      level: 5,
      article: { en: 'Basic knowledge' },
      last_verified: '2024-01-01',
      tags: [{ name: 'devops', category: 'skills' }]
    });

    // Attempt to create duplicate
    await expect(
      service.addSkill({
        external_id: 'test-skill-k8s-dup',
        name: { en: 'Kubernetes' },
        category: SkillCategory.DevOps,
        level: 6,
        article: { en: 'Different description' },
        last_verified: '2024-01-01',
        tags: [{ name: 'devops', category: 'skills' }]
      })
    ).rejects.toThrow();
  });
});

describe('Skill Search', () => {
  let client: EdgeDBClient;
  let service: SkillService;
  let skill1Id: string;
  let skill2Id: string;
  let skill3Id: string;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new SkillService(client);

    console.log('EdgeDB connected:', await client.query('SELECT 1'));

    // FULL cleanup - wipe everything for fresh test data
    await client.query('DELETE Skill');
    await client.query('DELETE Experience');
    await client.query('DELETE Achievement');
    await client.query('DELETE Tag');
    
    // Create test tags
    await client.query(`
      INSERT Tag { name := 'search-nodejs', category := 'languages' } UNLESS CONFLICT;
      INSERT Tag { name := 'search-python', category := 'languages' } UNLESS CONFLICT;
      INSERT Tag { name := 'search-backend', category := 'skills' } UNLESS CONFLICT;
      INSERT Tag { name := 'search-advanced', category := 'level' } UNLESS CONFLICT;
    `);

    // Create test skills
    const skill1 = await service.addSkill({
      external_id: 'test-skill-nodejs',
      name: { en: 'Node.js Backend' },
      category: SkillCategory.BackendDevelopment,
      level: 9,
      article: { en: 'Expert Node.js' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'search-nodejs', category: 'languages' },
        { name: 'search-backend', category: 'skills' }
      ]
    });
    skill1Id = skill1.id;

    const skill2 = await service.addSkill({
      external_id: 'test-skill-python',
      name: { en: 'Python Data Processing' },
      category: SkillCategory.BackendDevelopment,
      level: 7,
      article: { en: 'Data pipelines' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'search-python', category: 'languages' },
        { name: 'search-backend', category: 'skills' }
      ]
    });
    skill2Id = skill2.id;

    const skill3 = await service.addSkill({
      external_id: 'test-skill-fullstack',
      name: { en: 'Full Stack JS' },
      category: SkillCategory.Framework,
      level: 8,
      article: { en: 'Both frontend and backend' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'search-nodejs', category: 'languages' },
        { name: 'search-advanced', category: 'level' }
      ]
    });
    skill3Id = skill3.id;
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should search skills by single tag', async () => {
    const results = await service.searchSkills({ 
      tags: [{ name: 'search-nodejs', category: 'languages' }] 
    });

    expect(results).toHaveLength(2);
    expect(results.map(r => r.id)).toContain(skill1Id);
    expect(results.map(r => r.id)).toContain(skill3Id);
  });

  it('should search skills by multiple tags (AND logic)', async () => {
    const results = await service.searchSkills({
      tags: [
        { name: 'search-nodejs', category: 'languages' },
        { name: 'search-backend', category: 'skills' }
      ]
    });

    expect(results).toHaveLength(1);
    expect(results[0].id).toBe(skill1Id);
  });

  it('should search skills by minimum level', async () => {
    const results = await service.searchSkills({ levelMin: 8 });

    expect(results.length).toBeGreaterThanOrEqual(2);
    expect(results.every(s => s.level >= 8)).toBe(true);
    expect(results.map(r => r.id)).toContain(skill1Id); // level 9
    expect(results.map(r => r.id)).toContain(skill3Id); // level 8
  });

  it('should combine tag and level filters', async () => {
    const results = await service.searchSkills({
      tags: [{ name: 'search-backend', category: 'skills' }],
      levelMin: 8
    });

    expect(results).toHaveLength(1);
    expect(results[0].id).toBe(skill1Id); // Node.js Backend, level 9
  });

  it('should return empty array when no matches', async () => {
    const results = await service.searchSkills({
      tags: [{ name: 'nonexistent-tag', category: 'skills' }]
    });

    expect(results).toHaveLength(0);
  });
});
