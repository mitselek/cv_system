/**
 * Achievement Service - CRUD operations for Achievement entity
 */
import { EdgeDBClient } from '../edgedb.js';
import { Translation, TagReference, VerificationStatus } from '../types.js';

export interface AchievementInput {
  external_id: string;
  title: Translation;
  date: string; // IsoDate format
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate format
  tags: TagReference[];
  parent_experience?: string; // Experience external_id
}

export interface Achievement extends Omit<AchievementInput, 'tags' | 'parent_experience'> {
  id: string;
  tags: TagReference[];
  parent_experience?: string;
  created: string;
}

export interface AchievementSearchFilters {
  tags?: TagReference[];
  dateRange?: { start?: string; end?: string };
}

export class AchievementService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new achievement
   */
  async addAchievement(input: AchievementInput): Promise<Achievement> {
    if (!input.title.et && !input.title.en) {
      throw new Error('Achievement title must have at least one language (et or en)');
    }

    const articleClause = input.article ? 'article := <Translation>$article,' : '';
    const query = `
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)
      SELECT (
        INSERT Achievement {
          external_id := <str>$external_id,
          title := <Translation>$title,
          date := <IsoDate>$date,
          ${articleClause}
          verification_status := <VerificationStatus>$verification_status,
          last_verified := <IsoDate>$last_verified,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag 
              FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          ),
          parent_experience := (
            SELECT Experience FILTER .external_id = <optional str>$parent_experience_id LIMIT 1
          )
        }
      ) {
        id,
        external_id,
        title,
        date,
        article := (SELECT .article IF EXISTS .article ELSE <json>{}),
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        parent_experience: { external_id },
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, {
      external_id: input.external_id,
      title: input.title,
      date: input.date,
      ...(input.article && { article: input.article }),
      verification_status: input.verification_status || VerificationStatus.Draft,
      last_verified: input.last_verified,
      tag_refs: input.tags.map(t => ({ name: t.name, category: t.category })),
      parent_experience_id: input.parent_experience || null
    });

    return this.formatAchievement(result);
  }

  /**
   * Get achievement by ID
   */
  async getAchievement(id: string): Promise<Achievement | null> {
    const query = `
      SELECT Achievement {
        id,
        external_id,
        title,
        date,
        article := (SELECT .article IF EXISTS .article ELSE <json>{}),
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        parent_experience: { external_id },
        created
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<any>(query, { id });
    if (!result) return null;

    return this.formatAchievement(result);
  }

  /**
   * Search achievements with optional filters
   */
  async searchAchievements(filters: AchievementSearchFilters = {}): Promise<Achievement[]> {
    const conditions: string[] = [];
    const params: Record<string, any> = {};

    // Filter by tags
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
        conditions.push('.date >= <IsoDate>$range_start');
      }
      if (filters.dateRange.end) {
        params.range_end = filters.dateRange.end;
        conditions.push('.date <= <IsoDate>$range_end');
      }
    }

    const whereClause = conditions.length > 0
      ? `FILTER ${conditions.join(' AND ')}`
      : '';

    const withClause = filters.tags && filters.tags.length > 0
      ? 'WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)'
      : '';

    const query = `
      ${withClause}
      SELECT Achievement {
        id,
        external_id,
        title,
        date,
        article := (SELECT .article IF EXISTS .article ELSE <json>{}),
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        parent_experience: { external_id },
        created
      }
      ${whereClause}
      ORDER BY .date DESC THEN .external_id ASC
    `;

    const results = Object.keys(params).length > 0
      ? await this.client.query<any>(query, params)
      : await this.client.query<any>(query);

    return results.map(r => this.formatAchievement(r));
  }

  /**
   * Format achievement result from EdgeDB
   */
  private formatAchievement(result: any): Achievement {
    return {
      id: result.id,
      external_id: result.external_id,
      title: result.title as Translation,
      date: result.date,
      article: result.article as Translation || {},
      verification_status: result.verification_status,
      last_verified: result.last_verified,
      tags: result.tags?.map((t: any) => ({ name: t.name, category: t.category })) || [],
      parent_experience: result.parent_experience?.external_id,
      created: result.created.toISOString()
    };
  }
}
