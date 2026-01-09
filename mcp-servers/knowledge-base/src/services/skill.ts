/**
 * Skill Service - CRUD operations for Skill entity
 */
import { EdgeDBClient } from '../edgedb.js';

export interface SkillInput {
  name: string;
  level: number; // 1-10
  description?: string;
  evidenceRefs?: string[];
  tags: string[];
}

export interface Skill extends SkillInput {
  id: string;
  created: string;
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
      INSERT Skill {
        name := <str>$name,
        level := <int16>$level,
        description := <str>$description,
        evidence_refs := <array<str>>$evidence_refs,
        tags := (
          FOR tag_name IN array_unpack(<array<str>>$tags)
          UNION (SELECT Tag FILTER .name = tag_name)
        )
      }
    `;

    const result = await this.client.querySingle<Skill>(query, {
      name: input.name,
      level: input.level,
      description: input.description || '',
      evidence_refs: input.evidenceRefs || [],
      tags: input.tags
    });

    if (!result) {
      throw new Error('Failed to create skill');
    }

    return result;
  }

  /**
   * Get skill by ID
   */
  async getSkill(id: string): Promise<Skill | null> {
    const query = `
      SELECT Skill {
        id,
        name,
        level,
        description,
        evidence_refs,
        tags: { name },
        created
      }
      FILTER .id = <uuid>$id
    `;

    return this.client.querySingle<Skill>(query, { id });
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
      UPDATE Skill
      SET {
        ${setClauses.join(',')}
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<Skill>(query, params);
    if (!result) {
      throw new Error('Failed to update skill');
    }

    return result;
  }
}
