/**
 * Skill Service - CRUD operations for Skill entity
 */
import { EdgeDBClient } from '../edgedb.js';

export interface TagReference {
  name: string;
  category: string;
}

export interface SkillInput {
  name: string;
  level: number; // 1-10
  description?: string;
  evidenceRefs?: string[];
  tags: TagReference[];
}

export interface Skill extends SkillInput {
  id: string;
  created: string;
}

export interface SkillSearchFilters {
  tags?: TagReference[];
  levelMin?: number;
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

    const query = `
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)
      SELECT (
        INSERT Skill {
          name := <str>$name,
          level := <int16>$level,
          description := <str>$description,
          evidence_refs := <array<str>>$evidence_refs,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag 
              FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          )
        }
      ) {
        id,
        name,
        level,
        description,
        evidence_refs,
        tags: { name, category },
        created
      }
    `;

    const data = await this.client.querySingle<any>(query, {
      name: input.name,
      level: input.level,
      description: input.description || '',
      evidence_refs: input.evidenceRefs || [],
      tag_refs: input.tags.map(t => ({ name: t.name, category: t.category }))
    });

    if (!data) {
      throw new Error('Failed to create skill');
    }

    return {
      ...data,
      created: data.created.toISOString(),
      tags: data.tags?.map((t: any) => ({ name: t.name, category: t.category })) || []
    };
  }

  /**
   * Get skill by ID
   */
  async getSkill(id: string): Promise<Skill | null> {
    // Validate UUID format
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
      return null;
    }
    const query = `
      SELECT Skill {
        id,
        name,
        level,
        description,
        evidence_refs,
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
   * Update skill fields
   */
  async updateSkill(
    id: string,
    updates: Partial<Omit<SkillInput, 'tags'>>
  ): Promise<Skill> {
    if (updates.level !== undefined) {
      if (updates.level < 1 || updates.level > 10) {
        throw new Error('Skill level must be between 1 and 10');
      }
    }

    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.name !== undefined) {
      setClauses.push('name := <str>$name');
      params.name = updates.name;
    }

    if (updates.level !== undefined) {
      setClauses.push('level := <int16>$level');
      params.level = updates.level;
    }

    if (updates.description !== undefined) {
      setClauses.push('description := <str>$description');
      params.description = updates.description;
    }

    if (updates.evidenceRefs !== undefined) {
      setClauses.push('evidence_refs := <array<str>>$evidence_refs');
      params.evidence_refs = updates.evidenceRefs;
    }

    if (setClauses.length === 0) {
      const current = await this.getSkill(id);
      if (!current) throw new Error('Skill not found');
      return current;
    }

    const query = `
      SELECT (
        UPDATE Skill
        FILTER .id = <uuid>$id
        SET {
          ${setClauses.join(',')}
        }
      ) {
        id,
        name,
        level,
        description,
        evidence_refs,
        tags: { name, category },
        created
      }
    `;

    const result = await this.client.querySingle<any>(query, params);
    if (!result) {
      throw new Error('Failed to update skill');
    }

    return {
      ...result,
      created: result.created.toISOString(),
      tags: result.tags?.map((t: any) => ({ name: t.name, category: t.category })) || []
    };
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
        name,
        level,
        description,
        evidence_refs,
        tags: { name, category } ORDER BY .name,
        created
      }
      ${whereClause}
      ORDER BY .level DESC THEN .name ASC
    `;

    // Only pass params if we actually have any
    const results = Object.keys(params).length > 0
      ? await this.client.query<any>(query, params)
      : await this.client.query<any>(query);

    return results.map((r: any) => ({
      id: r.id,
      name: r.name,
      level: r.level,
      description: r.description || '',
      evidenceRefs: r.evidence_refs || [],
      tags: r.tags?.map((t: any) => ({ name: t.name, category: t.category })) || [],
      created: r.created.toISOString()
    }));
  }
}
