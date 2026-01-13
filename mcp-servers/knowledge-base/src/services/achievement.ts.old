/**
 * Achievement Service - CRUD operations for Achievement entity
 */
import { EdgeDBClient } from '../edgedb.js';

export interface TagReference {
  name: string;
  category: string;
}

export interface AchievementInput {
  title: string;
  date: string;
  description?: string;
  tags: TagReference[];
}

export interface Achievement extends AchievementInput {
  id: string;
  created: string;
}

export interface AchievementSearchFilters {
  tags?: TagReference[];
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
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)
      SELECT (
        INSERT Achievement {
          title := <str>$title,
          date := <str>$date,
          description := <str>$description,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag 
              FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          )
        }
      ) {
        id,
        title,
        date,
        description,
        tags: { name, category },
        created
      }
    `;

    const data = await this.client.querySingle<any>(query, {
      title: input.title,
      date: input.date,
      description: input.description || '',
      tag_refs: input.tags.map(t => ({ name: t.name, category: t.category }))
    });

    if (!data) {
      throw new Error('Failed to create achievement');
    }

    return {
      ...data,
      created: data.created.toISOString(),
      tags: data.tags?.map((t: any) => ({ name: t.name, category: t.category })) || []
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
        tags: { name, category },
        created
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<any>(query, { id });
    if (!result) return null;

    return {
      ...result,
      tags: result.tags?.map((t: any) => ({ name: t.name, category: t.category })) || [],
      created: result.created.toISOString()
    };
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
      SELECT (
        UPDATE Achievement
        FILTER .id = <uuid>$id
        SET {
          ${setClauses.join(',')}
        }
      ) {
        id,
        title,
        date,
        description,
        tags: { name, category },
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, params);
    if (!result) {
      throw new Error('Failed to update achievement');
    }

    return {
      ...result,
      created: result.created.toISOString(),
      tags: result.tags?.map((t: any) => ({ name: t.name, category: t.category })) || []
    };
  }

  /**
   * Search achievements with optional filters
   */
  async searchAchievements(filters: AchievementSearchFilters = {}): Promise<Achievement[]> {
    const conditions: string[] = [];
    const params: Record<string, any> = {};

    // Filter by tags (AND logic - achievement must have ALL specified tags)
    if (filters.tags && filters.tags.length > 0) {
      params.tag_refs = filters.tags.map(t => ({ name: t.name, category: t.category }));
      conditions.push(`
        count((
          FOR tag_ref IN tag_refs 
          UNION (
            SELECT Tag 
            FILTER .name = tag_ref.name 
              AND .category = tag_ref.category 
              AND Tag IN Achievement.tags
          )
        )) = len(<array<tuple<name: str, category: str>>>$tag_refs)
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

    // Build WITH clause if we have tags
    const withClause = filters.tags && filters.tags.length > 0
      ? 'WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)'
      : '';

    const query = `
      ${withClause}
      SELECT Achievement {
        id,
        title,
        date,
        description,
        tags: { name, category } ORDER BY .name,
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
      tags: r.tags?.map((t: any) => ({ name: t.name, category: t.category })) || [],
      created: r.created.toISOString()
    }));
  }
}
