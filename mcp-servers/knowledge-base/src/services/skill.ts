/**
 * Skill Service - CRUD operations for Skill entity
 */
import { EdgeDBClient } from '../edgedb.js';
import { Translation, TagReference, SkillCategory, VerificationStatus } from '../types.js';

export interface SkillInput {
  external_id: string;
  name: Translation;
  category: SkillCategory;
  level: number; // 1-10
  level_display?: string;
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate format
  tags: TagReference[];
}

export interface Skill extends Omit<SkillInput, 'tags'> {
  id: string;
  tags: TagReference[];
  created: string;
}

export interface SkillSearchFilters {
  tags?: TagReference[];
  levelMin?: number;
  category?: SkillCategory;
}

export class SkillService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new skill with level validation (1-10)
   */
  async addSkill(input: SkillInput): Promise<Skill> {
    if (input.level < 1 || input.level > 10) {
      throw new Error('Skill level must be between 1 and 10');
    }

    // Validate Translation has at least one language
    if (!input.name.et && !input.name.en) {
      throw new Error('Skill name must have at least one language (et or en)');
    }

    const articleClause = input.article ? 'article := <Translation><json>$article,' : '';
    const query = `
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)
      SELECT (
        INSERT Skill {
          external_id := <str>$external_id,
          name := <Translation><json>$name,
          category := <SkillCategory>$category,
          level := <int16>$level,
          level_display := <str>$level_display,
          ${articleClause}
          verification_status := <VerificationStatus>$verification_status,
          last_verified := <IsoDate>$last_verified,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag 
              FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          )
        }
      ) {
        id,
        external_id,
        name,
        category,
        level,
        level_display,
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, {
      external_id: input.external_id,
      name: JSON.stringify(input.name),
      category: input.category,
      level: input.level,
      level_display: input.level_display || `${input.level}/10`,
      ...(input.article && { article: JSON.stringify(input.article) }),
      verification_status: input.verification_status || VerificationStatus.Draft,
      last_verified: input.last_verified,
      tag_refs: input.tags.map(t => ({ name: t.name, category: t.category }))
    });

    return this.formatSkill(result);
  }

  /**
   * Get skill by ID
   */
  async getSkill(id: string): Promise<Skill | null> {
    const query = `
      SELECT Skill {
        id,
        external_id,
        name,
        category,
        level,
        level_display,
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        created
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<any>(query, { id });
    if (!result) return null;

    return this.formatSkill(result);
  }

  /**
   * Update skill fields
   */
  async updateSkill(
    id: string,
    updates: Partial<Omit<SkillInput, 'external_id' | 'tags'>>
  ): Promise<Skill> {
    if (updates.level !== undefined) {
      if (updates.level < 1 || updates.level > 10) {
        throw new Error('Skill level must be between 1 and 10');
      }
    }

    if (updates.name && !updates.name.et && !updates.name.en) {
      throw new Error('Skill name must have at least one language (et or en)');
    }

    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.name !== undefined) {
      setClauses.push('name := <Translation>to_json($name)');
      params.name = JSON.stringify(updates.name);
    }

    if (updates.category !== undefined) {
      setClauses.push('category := <SkillCategory>$category');
      params.category = updates.category;
    }

    if (updates.level !== undefined) {
      setClauses.push('level := <int16>$level');
      params.level = updates.level;
    }

    if (updates.level_display !== undefined) {
      setClauses.push('level_display := <str>$level_display');
      params.level_display = updates.level_display;
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
        UPDATE Skill
        FILTER .id = <uuid>$id
        SET {
          ${setClauses.join(',\n          ')}
        }
      ) {
        id,
        external_id,
        name,
        category,
        level,
        level_display,
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, params);
    return this.formatSkill(result);
  }

  /**
   * Search skills with optional filters
   */
  async searchSkills(filters: SkillSearchFilters = {}): Promise<Skill[]> {
    const conditions: string[] = [];
    const params: Record<string, any> = {};

    // Filter by tags (AND logic - skill must have ALL specified tags)
    if (filters.tags && filters.tags.length > 0) {
      params.tag_refs = filters.tags.map(t => ({ name: t.name, category: t.category }));
      conditions.push(`
        count((
          FOR tag_ref IN tag_refs 
          UNION (
            SELECT Tag 
            FILTER .name = tag_ref.name 
              AND .category = tag_ref.category 
              AND Tag IN Skill.tags
          )
        )) = len(<array<tuple<name: str, category: str>>>$tag_refs)
      `);
    }

    // Filter by minimum level
    if (filters.levelMin !== undefined) {
      params.level_min = filters.levelMin;
      conditions.push('.level >= <int16>$level_min');
    }

    // Filter by category
    if (filters.category !== undefined) {
      params.category = filters.category;
      conditions.push('.category = <SkillCategory>$category');
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
      SELECT Skill {
        id,
        external_id,
        name,
        category,
        level,
        level_display,
        article,
        verification_status,
        last_verified,
        tags: { name, category } ORDER BY .name,
        created
      }
      ${whereClause}
      ORDER BY .level DESC THEN .external_id ASC
    `;

    // Only pass params if we actually have any
    const results = Object.keys(params).length > 0
      ? await this.client.query<any>(query, params)
      : await this.client.query<any>(query);

    return results.map(r => this.formatSkill(r));
  }

  /**
   * Format skill result from EdgeDB
   */
  private formatSkill(result: any): Skill {
    return {
      id: result.id,
      external_id: result.external_id,
      name: result.name as Translation,
      category: result.category,
      level: result.level,
      level_display: result.level_display,
      article: result.article as Translation || {},
      verification_status: result.verification_status,
      last_verified: result.last_verified,
      tags: result.tags?.map((t: any) => ({ name: t.name, category: t.category })) || [],
      created: result.created.toISOString()
    };
  }
}
