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

export class ExperienceService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new experience
   */
  async addExperience(input: ExperienceInput): Promise<Experience> {
    const query = `
      INSERT Experience {
        title := <str>$title,
        organization := <str>$organization,
        start_date := <str>$start_date,
        end_date := <str>$end_date,
        description_en := <str>$description_en,
        description_et := <str>$description_et,
        tags := (
          FOR tag_name IN array_unpack(<array<str>>$tags)
          UNION (SELECT Tag FILTER .name = tag_name)
        )
      }
    `;

    const result = await this.client.querySingle<Experience>(query, {
      title: input.title,
      organization: input.organization,
      start_date: input.startDate,
      end_date: input.endDate || null,
      description_en: input.language === 'en' ? input.description : null,
      description_et: input.language === 'et' ? input.description : null,
      tags: input.tags
    });

    if (!result) {
      throw new Error('Failed to create experience');
    }

    return result;
  }

  /**
   * Get experience by ID
   */
  async getExperience(id: string): Promise<Experience | null> {
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

    return this.client.querySingle<Experience>(query, { id });
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
      UPDATE Experience
      SET {
        ${setClauses.join(',')}
      }
      FILTER .id = <uuid>$id
    `;

    const result = await this.client.querySingle<Experience>(query, params);
    if (!result) {
      throw new Error('Failed to update experience');
    }

    return result;
  }
}
