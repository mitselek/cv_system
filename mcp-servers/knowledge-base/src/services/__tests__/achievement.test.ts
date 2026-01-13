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
      external_id: 'test-ach-1',
      title: { en: 'Led successful platform migration' },
      date: '2023-06-15',
      article: { en: 'Migrated 500+ users to new infrastructure with zero downtime' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'leadership', category: 'soft-skills' },
        { name: 'backend', category: 'skills' }
      ]
    });

    expect(result).toHaveProperty('id');
    expect(result.title.en).toBe('Led successful platform migration');
    expect(result.date).toBe('2023-06-15');
  });

  it('should parse various date formats', async () => {
    const result = await service.addAchievement({
      external_id: 'test-ach-2',
      title: { en: 'Achieved milestone' },
      date: '2024-01-09', // ISO format
      article: { en: 'Completed major project' },
      last_verified: '2024-01-01',
      tags: []
    });

    expect(result.date).toBeDefined();
  });

  it('should retrieve achievement by ID', async () => {
    const created = await service.addAchievement({
      external_id: 'test-ach-3',
      title: { en: '100% intern hire rate' },
      date: '2022-12-31',
      article: { en: 'Managed 4 interns, all converted to permanent roles' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'leadership', category: 'soft-skills' },
        { name: 'hr', category: 'soft-skills' }
      ]
    });

    const retrieved = await service.getAchievement(created.id);
    expect(retrieved?.title.en).toBe('100% intern hire rate');
  });

  it('should handle missing achievement gracefully', async () => {
    const result = await service.getAchievement('nonexistent-id');
    expect(result).toBeNull();
  });
});

describe('Achievement Search', () => {
  let client: EdgeDBClient;
  let service: AchievementService;
  let ach1Id: string;
  let ach2Id: string;
  let ach3Id: string;

  beforeAll(async () => {
    client = new EdgeDBClient();
    await client.connect();
    service = new AchievementService(client);

    console.log('EdgeDB connected:', await client.query('SELECT 1'));

    // Full cleanup for fresh test data
    await client.query('DELETE Achievement');
    await client.query('DELETE Skill');
    await client.query('DELETE Experience');
    await client.query('DELETE Tag');

    // Create test tags
    await client.query(`
      INSERT Tag { name := 'search-leadership', category := 'soft-skills' } UNLESS CONFLICT;
      INSERT Tag { name := 'search-backend', category := 'skills' } UNLESS CONFLICT;
      INSERT Tag { name := 'search-migration', category := 'skills' } UNLESS CONFLICT;
    `);

    // Create test achievements
    const ach1 = await service.addAchievement({
      external_id: 'test-ach-search-1',
      title: { en: 'Platform Migration' },
      date: '2023-06-15',
      article: { en: 'Led successful platform migration' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'search-leadership', category: 'soft-skills' },
        { name: 'search-backend', category: 'skills' }
      ]
    });
    ach1Id = ach1.id;

    const ach2 = await service.addAchievement({
      external_id: 'test-ach-search-2',
      title: { en: 'Team Mentoring' },
      date: '2023-12-01',
      article: { en: '100% intern hire rate' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'search-leadership', category: 'soft-skills' },
        { name: 'search-migration', category: 'skills' }
      ]
    });
    ach2Id = ach2.id;

    const ach3 = await service.addAchievement({
      external_id: 'test-ach-search-3',
      title: { en: 'Database Optimization' },
      date: '2024-03-20',
      article: { en: 'Improved query performance 10x' },
      last_verified: '2024-01-01',
      tags: [
        { name: 'search-backend', category: 'skills' },
        { name: 'search-migration', category: 'skills' }
      ]
    });
    ach3Id = ach3.id;
  });

  afterAll(async () => {
    await client.disconnect();
  });

  it('should search achievements by single tag', async () => {
    const results = await service.searchAchievements({ 
      tags: [{ name: 'search-leadership', category: 'soft-skills' }] 
    });

    expect(results).toHaveLength(2);
    expect(results.map(r => r.id)).toContain(ach1Id);
    expect(results.map(r => r.id)).toContain(ach2Id);
  });

  it('should search achievements by multiple tags (AND logic)', async () => {
    const results = await service.searchAchievements({
      tags: [
        { name: 'search-leadership', category: 'soft-skills' },
        { name: 'search-backend', category: 'skills' }
      ]
    });

    expect(results).toHaveLength(1);
    expect(results[0].id).toBe(ach1Id);
  });

  it('should search achievements by date range', async () => {
    const results = await service.searchAchievements({
      dateRange: {
        start: '2023-10-01',
        end: '2024-01-31'
      }
    });

    expect(results).toHaveLength(1);
    expect(results[0].id).toBe(ach2Id); // 2023-12-01
  });

  it('should combine tag and date range filters', async () => {
    const results = await service.searchAchievements({
      tags: [{ name: 'search-backend', category: 'skills' }],
      dateRange: {
        start: '2024-01-01'
      }
    });

    expect(results).toHaveLength(1);
    expect(results[0].id).toBe(ach3Id); // Database Optimization, 2024-03-20
  });

  it('should return empty array when no matches', async () => {
    const results = await service.searchAchievements({
      tags: [{ name: 'nonexistent-tag', category: 'skills' }]
    });

    expect(results).toHaveLength(0);
  });
});
