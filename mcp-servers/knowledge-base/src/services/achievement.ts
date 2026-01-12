/**
 * Achievement Service - CRUD operations for Achievement entity
 */
import { EdgeDBClient } from '../edgedb.js';

export interface AchievementInput {
  title: string;
  date: string;
  description?: string;
  tags: string[];
}

export interface Achievement extends AchievementInput {
  id: string;
  created: string;
}

export interface AchievementSearchFilters {
  tags?: string[];
  dateRange?: {
    start?: string;  // ISO date
    end?: string;    // ISO date
  };
}

export class AchievementService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new achievement with date parsing
   */
  async addAchievement(input: AchievementInput): Promise<Achievement> {
    const query = `
      SELECT (
        INSERT Achievement {
          title := <str>$title,
          date := <str>$date,
          description := <str>$description,
          tags := (
            SELECT DISTINCT Tag FILTER .name IN array_unpack(<array<str>>$tags)
          )
        }
      ) {
        id,
        title,
        date,
        description,
        tags: { name },
        created
      }
    `;

    const data = await this.client.querySingle<any>(query, {
      title: input.title,
      date: input.date,
      description: input.description || '',
      tags: input.tags
    });

    if (!data) {
      throw new Error('Failed to create achievement');
    }

    return {
      ...data,
      created: data.created.toISOString(),
      tags: data.tags?.map((t: any) => t.name) || []
    };
  }

  /**
   * Get achievement by ID
   */
  async getAchievement(id: string): Promise<Achievement | null> {
    // Validate UUID format
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
      return null;
    }
    const query = `
      SELECT Achievement {
        id,
        title,
        date,
        description,
        tags: { name },
        created
      }
      FILTER .id = <uuid>$id
    `;

    return this.client.querySingle<Achievement>(query, { id });
  }

  /**
   * Update achievement fields
   */
  async updateAchievement(
    id: string,
    updates: Partial<Omit<AchievementInput, 'tags'>>
  ): Promise<Achievement> {
    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.title !== undefined) {
      setClauses.push('title := <str>$title');
      params.title = updates.title;
    }

    if (updates.date !== undefined) {
      setClauses.push('date := <str>$date');
      params.date = updates.date;
    }

    if (updates.description !== undefined) {
      setClauses.push('description := <str>$description');
      params.description = updates.description;
    }

    if (setClauses.length === 0) {
      const current = await this.getAchievement(id);
      if (!current) throw new Error('Achievement not found');
      return current;
    }

    const query = `
      UPDATE Achievement
      SET {
        ${setClauses.join(',')}
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<Achievement>(query, params);
    if (!result) {
      throw new Error('Failed to update achievement');
    }

    return result;
  }

  /**
   * Search achievements with optional filters
   */
  async searchAchievements(filters: AchievementSearchFilters = {}): Promise<Achievement[]> {
    const conditions: string[] = [];
    const params: Record<string, any> = {};

    // Filter by tags (AND logic - achievement must have ALL specified tags)
    if (filters.tags && filters.tags.length > 0) {
      params.tags = filters.tags;
      conditions.push(`
        count((FOR tag IN array_unpack(<array<str>>$tags) 
               UNION (SELECT Tag FILTER .name = tag AND Tag IN Achievement.tags)))
        = len(<array<str>>$tags)
      `);
    }

    // Filter by date range
    if (filters.dateRange) {
      if (filters.dateRange.start) {
        params.range_start = filters.dateRange.start;
        conditions.push('.date >= <str>$range_start');
      }
      if (filters.dateRange.end) {
        params.range_end = filters.dateRange.end;
        conditions.push('.date <= <str>$range_end');
      }
    }

    const whereClause = conditions.length > 0
      ? `FILTER ${conditions.join(' AND ')}`
      : '';

    const query = `
      SELECT Achievement {
        id,
        title,
        date,
        description,
        tags: { name } ORDER BY .name,
        created
      }
      ${whereClause}
      ORDER BY .date DESC THEN .title ASC
    `;

    // Only pass params if we actually have any
    const results = Object.keys(params).length > 0
      ? await this.client.query<any>(query, params)
      : await this.client.query<any>(query);

    return results.map((r: any) => ({
      id: r.id,
      title: r.title,
      date: r.date,
      description: r.description || '',
      tags: r.tags?.map((t: any) => t.name) || [],
      created: r.created.toISOString()
    }));
  }
}
