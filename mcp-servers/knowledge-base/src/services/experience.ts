/**
 * Experience Service - CRUD operations for Experience entity
 */
import { EdgeDBClient } from '../edgedb.js';
import { Translation, TagReference, VerificationStatus } from '../types.js';

export interface ExperienceInput {
  external_id: string;
  title: Translation;
  company: Translation;
  url?: string;
  dates: { start: string; end: string }; // IsoDate format
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate format
  tags: TagReference[];
  skills_demonstrated?: string[]; // Skill external_ids
}

export interface Experience extends Omit<ExperienceInput, 'tags' | 'skills_demonstrated'> {
  id: string;
  tags: TagReference[];
  skills_demonstrated: string[];
  created: string;
}

export interface ExperienceSearchFilters {
  tags?: TagReference[];
  company?: string;
  organization?: string; // Alias for company
  dateRange?: { start?: string; end?: string };
}

export class ExperienceService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new experience
   */
  async addExperience(input: ExperienceInput): Promise<Experience> {
    if (!input.title.et && !input.title.en) {
      throw new Error('Experience title must have at least one language (et or en)');
    }

    if (!input.company.et && !input.company.en) {
      throw new Error('Experience company must have at least one language (et or en)');
    }

    const query = `
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs),
           skill_ids := array_unpack(<array<str>>$skill_ids)
      SELECT (
        INSERT Experience {
          external_id := <str>$external_id,
          title := <Translation>to_json($title),
          company := <Translation>to_json($company),
          url := <optional HttpUrl>$url,
          dates := (start := <IsoDate>$date_start, end := <IsoDate>$date_end),
          article := <Translation>to_json($article),
          verification_status := <VerificationStatus>$verification_status,
          last_verified := <IsoDate>$last_verified,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag 
              FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          ),
          skills_demonstrated := (
            FOR skill_id IN skill_ids UNION (
              SELECT Skill FILTER .external_id = skill_id
            )
          )
        }
      ) {
        id,
        external_id,
        title,
        company,
        url,
        dates: { start, end },
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        skills_demonstrated: { external_id } ORDER BY .external_id,
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, {
      external_id: input.external_id,
      title: JSON.stringify(input.title),
      company: JSON.stringify(input.company),
      url: input.url || null,
      date_start: input.dates.start,
      date_end: input.dates.end,
      article: input.article ? JSON.stringify(input.article) : JSON.stringify({}),
      verification_status: input.verification_status || VerificationStatus.Draft,
      last_verified: input.last_verified,
      tag_refs: input.tags.map(t => ({ name: t.name, category: t.category })),
      skill_ids: input.skills_demonstrated || []
    });

    return this.formatExperience(result);
  }

  /**
   * Get experience by ID
   */
  async getExperience(id: string): Promise<Experience | null> {
    const query = `
      SELECT Experience {
        id,
        external_id,
        title,
        company,
        url,
        dates: { start, end },
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        skills_demonstrated: { external_id } ORDER BY .external_id,
        created
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<any>(query, { id });
    if (!result) return null;

    return this.formatExperience(result);
  }

  /**
   * Update experience fields
   */
  async updateExperience(
    id: string,
    updates: Partial<Omit<ExperienceInput, 'external_id' | 'tags' | 'skills_demonstrated'>>
  ): Promise<Experience> {
    if (updates.title && !updates.title.et && !updates.title.en) {
      throw new Error('Experience title must have at least one language (et or en)');
    }

    if (updates.company && !updates.company.et && !updates.company.en) {
      throw new Error('Experience company must have at least one language (et or en)');
    }

    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.title !== undefined) {
      setClauses.push('title := <Translation>to_json($title)');
      params.title = JSON.stringify(updates.title);
    }

    if (updates.company !== undefined) {
      setClauses.push('company := <Translation>to_json($company)');
      params.company = JSON.stringify(updates.company);
    }

    if (updates.url !== undefined) {
      setClauses.push('url := <optional HttpUrl>$url');
      params.url = updates.url || null;
    }

    if (updates.dates !== undefined) {
      setClauses.push('dates := (start := <IsoDate>$date_start, end := <IsoDate>$date_end)');
      params.date_start = updates.dates.start;
      params.date_end = updates.dates.end;
    }

    if (updates.article !== undefined) {
      setClauses.push('article := <Translation>to_json($article)');
      params.article = JSON.stringify(updates.article);
    }

    if (updates.verification_status !== undefined) {
      setClauses.push('verification_status := <VerificationStatus>$verification_status');
      params.verification_status = updates.verification_status;
    }

    if (updates.last_verified !== undefined) {
      setClauses.push('last_verified := <IsoDate>$last_verified');
      params.last_verified = updates.last_verified;
    }

    if (setClauses.length === 0) {
      throw new Error('No fields to update');
    }

    const query = `
      SELECT (
        UPDATE Experience
        FILTER .id = <uuid>$id
        SET {
          ${setClauses.join(',\n          ')}
        }
      ) {
        id,
        external_id,
        title,
        company,
        url,
        dates: { start, end },
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        skills_demonstrated: { external_id } ORDER BY .external_id,
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, params);
    return this.formatExperience(result);
  }

  /**
   * Search experiences with optional filters
   */
  async searchExperiences(filters: ExperienceSearchFilters = {}): Promise<Experience[]> {
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
              AND Tag IN Experience.tags
          )
        )) = len(<array<tuple<name: str, category: str>>>$tag_refs)
      `);
    }

    // Filter by company (fuzzy match on English or Estonian)
    const companySearch = filters.company || filters.organization;
    if (companySearch !== undefined) {
      params.company_search = companySearch.toLowerCase();
      conditions.push(`(
        str_lower(<str>json_get(.company, 'en') ?? '') LIKE '%' ++ <str>$company_search ++ '%'
        OR str_lower(<str>json_get(.company, 'et') ?? '') LIKE '%' ++ <str>$company_search ++ '%'
      )`);
    }

    // Filter by date range (overlapping)
    if (filters.dateRange) {
      if (filters.dateRange.start) {
        params.range_start = filters.dateRange.start;
        conditions.push('.dates.end >= <IsoDate>$range_start');
      }
      if (filters.dateRange.end) {
        params.range_end = filters.dateRange.end;
        conditions.push('.dates.start <= <IsoDate>$range_end');
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
      SELECT Experience {
        id,
        external_id,
        title,
        company,
        url,
        dates: { start, end },
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        skills_demonstrated: { external_id } ORDER BY .external_id,
        created
      }
      ${whereClause}
      ORDER BY .dates.start DESC THEN .external_id ASC
    `;

    const results = Object.keys(params).length > 0
      ? await this.client.query<any>(query, params)
      : await this.client.query<any>(query);

    return results.map(r => this.formatExperience(r));
  }

  /**
   * Format experience result from EdgeDB
   */
  private formatExperience(result: any): Experience {
    return {
      id: result.id,
      external_id: result.external_id,
      title: result.title as Translation,
      company: result.company as Translation,
      url: result.url,
      dates: {
        start: result.dates.start,
        end: result.dates.end
      },
      article: result.article as Translation || {},
      verification_status: result.verification_status,
      last_verified: result.last_verified,
      tags: result.tags?.map((t: any) => ({ name: t.name, category: t.category })) || [],
      skills_demonstrated: result.skills_demonstrated?.map((s: any) => s.external_id) || [],
      created: result.created.toISOString()
    };
  }
}
