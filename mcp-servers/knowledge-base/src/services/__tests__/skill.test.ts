import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../src/edgedb.js';
import { SkillService } from '../src/services/skill.js';

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
      name: 'Python',
      level: 9,
      description: 'Expert-level Python programming',
      evidenceRefs: ['EKI backend systems'],
      tags: ['languages', 'backend']
    });

    expect(result).toHaveProperty('id');
    expect(result.name).toBe('Python');
    expect(result.level).toBe(9);
    expect(result.level).toBeGreaterThanOrEqual(1);
    expect(result.level).toBeLessThanOrEqual(10);
  });

  it('should reject invalid level values', async () => {
    await expect(
      service.addSkill({
        name: 'JavaScript',
        level: 11, // Invalid
        description: '',
        evidenceRefs: [],
        tags: []
      })
    ).rejects.toThrow();
  });

  it('should retrieve skill by ID', async () => {
    const created = await service.addSkill({
      name: 'TypeScript',
      level: 8,
      description: 'Strong TypeScript skills',
      evidenceRefs: ['PÖFF system'],
      tags: ['languages', 'frontend']
    });

    const retrieved = await service.getSkill(created.id);
    expect(retrieved?.name).toBe('TypeScript');
    expect(retrieved?.level).toBe(8);
  });

  it('should update skill fields', async () => {
    const created = await service.addSkill({
      name: 'Docker',
      level: 7,
      description: 'Working knowledge',
      evidenceRefs: [],
      tags: ['devops']
    });

    const updated = await service.updateSkill(created.id, {
      level: 8,
      description: 'Advanced Docker experience'
    });

    expect(updated.level).toBe(8);
    expect(updated.description).toBe('Advanced Docker experience');
  });

  it('should enforce unique skill names', async () => {
    await service.addSkill({
      name: 'Kubernetes',
      level: 5,
      description: 'Basic knowledge',
      evidenceRefs: [],
      tags: ['devops']
    });

    // Attempt to create duplicate
    await expect(
      service.addSkill({
        name: 'Kubernetes',
        level: 6,
        description: 'Different description',
        evidenceRefs: [],
        tags: ['devops']
      })
    ).rejects.toThrow();
  });
});
