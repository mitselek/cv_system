/**
 * Experience Service - CRUD operations for Experience entity
 */
import { EdgeDBClient } from '../edgedb.js';

export interface ExperienceInput {
  title: string;
  organization: string;
  startDate: string;
  endDate?: string;
  description?: string;
  tags: string[];
  language: 'en' | 'et';
}

export interface Experience extends ExperienceInput {
  id: string;
  created: string;
}

export interface ExperienceSearchFilters {
  tags?: string[];
  organization?: string;
  dateRange?: {
    start: string;
    end: string;
  };
}

export class ExperienceService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new experience
   */
  async addExperience(input: ExperienceInput): Promise<Experience> {
    const query = `
      SELECT (
        INSERT Experience {
          title := <str>$title,
          organization := <str>$organization,
          start_date := <str>$start_date,
          end_date := <OPTIONAL str>$end_date,
          description_en := <OPTIONAL str>$description_en,
          description_et := <OPTIONAL str>$description_et,
          tags := (
            SELECT DISTINCT Tag FILTER .name IN array_unpack(<array<str>>$tags)
          )
        }
      ) {
        id,
        title,
        organization,
        start_date,
        end_date,
        description_en,
        description_et,
        tags: { name } ORDER BY .name,
        created
      }
    `;

    const data = await this.client.querySingle<any>(query, {
      title: input.title,
      organization: input.organization,
      start_date: input.startDate,
      end_date: input.endDate || null,
      description_en: input.language === 'en' ? input.description : null,
      description_et: input.language === 'et' ? input.description : null,
      tags: input.tags
    });

    if (!data) {
      throw new Error('Failed to create experience');
    }

    return {
      id: data.id,
      title: data.title,
      organization: data.organization,
      startDate: data.start_date,
      endDate: data.end_date,
      description: input.description || '',
      tags: data.tags?.map((t: any) => t.name) || [],
      language: input.language,
      created: data.created.toISOString()
    };
  }

  /**
   * Get experience by ID
   */
  async getExperience(id: string): Promise<Experience | null> {
    // Validate UUID format
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
      return null;
    }
    const query = `
      SELECT Experience {
        id,
        title,
        organization,
        start_date,
        end_date,
        description_en,
        description_et,
        tags: { name },
        created
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<any>(query, { id });
    if (!result) return null;

    return {
      id: result.id,
      title: result.title,
      organization: result.organization,
      startDate: result.start_date,
      endDate: result.end_date,
      description: result.description_en || result.description_et || '',
      tags: result.tags?.map((t: any) => t.name) || [],
      language: result.description_en ? 'en' : 'et',
      created: result.created.toISOString()
    };
  }

  /**
   * Update experience fields
   */
  async updateExperience(
    id: string,
    updates: Partial<Omit<ExperienceInput, 'tags' | 'language'>>
  ): Promise<Experience> {
    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.title !== undefined) {
      setClauses.push('title := <str>$title');
      params.title = updates.title;
    }

    if (updates.organization !== undefined) {
      setClauses.push('organization := <str>$organization');
      params.organization = updates.organization;
    }

    if (updates.startDate !== undefined) {
      setClauses.push('start_date := <str>$start_date');
      params.start_date = updates.startDate;
    }

    if (updates.endDate !== undefined) {
      setClauses.push('end_date := <str>$end_date');
      params.end_date = updates.endDate;
    }

    if (updates.description !== undefined) {
      setClauses.push('description_en := <str>$description');
      params.description = updates.description;
    }

    if (setClauses.length === 0) {
      // No updates, return current
      const current = await this.getExperience(id);
      if (!current) throw new Error('Experience not found');
      return current;
    }

    const query = `
      SELECT (
        UPDATE Experience
        FILTER .id = <uuid>$id
        SET {
          ${setClauses.join(',')}
        }
      ) {
        id,
        title,
        organization,
        start_date,
        end_date,
        description_en,
        description_et,
        tags: { name },
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, params);
    if (!result) {
      throw new Error('Failed to update experience');
    }

    // Transform DB response to Experience interface
    return {
      id: result.id,
      title: result.title,
      organization: result.organization,
      startDate: result.start_date,
      endDate: result.end_date,
      description: result.description_en || result.description_et || '',
      tags: result.tags?.map((t: any) => t.name) || [],
      language: result.description_en ? 'en' : 'et',
      created: result.created.toISOString()
    };
  }

  /**
   * Search experiences with optional filters
   */
  async searchExperiences(filters: ExperienceSearchFilters = {}): Promise<Experience[]> {
    const conditions: string[] = [];
    const params: Record<string, any> = {};

    // Filter by tags (AND logic - experience must have ALL specified tags)
    if (filters.tags && filters.tags.length > 0) {
      params.tags = filters.tags;
      // Count how many of the requested tags are in this experience's tags
      // Must equal the number of requested tags (AND logic)
      conditions.push(`
        count((FOR tag IN array_unpack(<array<str>>$tags) 
               UNION (SELECT Tag FILTER .name = tag AND Tag IN Experience.tags)))
        = len(<array<str>>$tags)
      `);
    }

    // Filter by organization
    if (filters.organization) {
      params.organization = filters.organization;
      conditions.push('.organization = <str>$organization');
    }

    // Filter by date range (overlap check)
    if (filters.dateRange) {
      params.range_start = filters.dateRange.start;
      params.range_end = filters.dateRange.end;
      // Use ?? to coalesce the OR result, defaulting to checking if end_date doesn't exist
      conditions.push(`
        .start_date <= <str>$range_end AND 
        ((.end_date >= <str>$range_start) ?? (NOT EXISTS .end_date))
      `);
    }

    const whereClause = conditions.length > 0 
      ? `FILTER ${conditions.join(' AND ')}`
      : '';

    const query = `
      SELECT Experience {
        id,
        title,
        organization,
        start_date,
        end_date,
        description_en,
        description_et,
        tags: { name } ORDER BY .name,
        created
      }
      ${whereClause}
      ORDER BY .start_date DESC
    `;

    // Only pass params if we actually have any
    const results = Object.keys(params).length > 0
      ? await this.client.query<any>(query, params)
      : await this.client.query<any>(query);

    return results.map((r: any) => ({
      id: r.id,
      title: r.title,
      organization: r.organization,
      startDate: r.start_date,
      endDate: r.end_date,
      description: r.description_en || r.description_et || '',
      tags: r.tags?.map((t: any) => t.name) || [],
      language: r.description_en ? 'en' as const : 'et' as const,
      created: r.created.toISOString()
    }));
  }
}
