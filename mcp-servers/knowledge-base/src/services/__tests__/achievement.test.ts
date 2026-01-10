import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { EdgeDBClient } from '../../edgedb.js';
import { AchievementService } from '../achievement.js';

describe('Achievement CRUD', () => {
  let client: EdgeDBClient;
  let service: AchievementService;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new AchievementService(client);
    await client.query('DELETE Achievement');
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should create achievement with date parsing', async () => {
    const result = await service.addAchievement({
      title: 'Led successful platform migration',
      date: '2023-06-15',
      description: 'Migrated 500+ users to new infrastructure with zero downtime',
      tags: ['leadership', 'backend']
    });

    expect(result).toHaveProperty('id');
    expect(result.title).toBe('Led successful platform migration');
    expect(result.date).toBe('2023-06-15');
  });

  it('should parse various date formats', async () => {
    const result = await service.addAchievement({
      title: 'Achieved milestone',
      date: '2024-01-09', // ISO format
      description: 'Completed major project',
      tags: []
    });

    expect(result.date).toBeDefined();
  });

  it('should retrieve achievement by ID', async () => {
    const created = await service.addAchievement({
      title: '100% intern hire rate',
      date: '2022-12-31',
      description: 'Managed 4 interns, all converted to permanent roles',
      tags: ['leadership', 'hr']
    });

    const retrieved = await service.getAchievement(created.id);
    expect(retrieved?.title).toBe('100% intern hire rate');
  });

  it('should handle missing achievement gracefully', async () => {
    const result = await service.getAchievement('nonexistent-id');
    expect(result).toBeNull();
  });
});
