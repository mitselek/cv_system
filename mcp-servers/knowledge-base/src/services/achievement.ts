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

export class AchievementService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new achievement with date parsing
   */
  async addAchievement(input: AchievementInput): Promise<Achievement> {
    const query = `
      INSERT Achievement {
        title := <str>$title,
        date := <str>$date,
        description := <str>$description,
        tags := (
          FOR tag_name IN array_unpack(<array<str>>$tags)
          UNION (SELECT Tag FILTER .name = tag_name)
        )
      }
    `;

    const result = await this.client.querySingle<Achievement>(query, {
      title: input.title,
      date: input.date,
      description: input.description || '',
      tags: input.tags
    });

    if (!result) {
      throw new Error('Failed to create achievement');
    }

    return result;
  }

  /**
   * Get achievement by ID
   */
  async getAchievement(id: string): Promise<Achievement | null> {
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
}
