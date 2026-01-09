/**
 * Tag Service - Classifier/Tag management
 */
import { EdgeDBClient } from '../edgedb.js';

export interface Tag {
  id: string;
  name: string;
  category: string;
  created: string;
}

export class TagService {
  constructor(private client: EdgeDBClient) {}

  /**
   * List all tags, optionally filtered by category
   */
  async listTags(category?: string): Promise<Tag[]> {
    let query = 'SELECT Tag { id, name, category, created }';

    if (category) {
      query += ' FILTER .category = <str>$category';
      return this.client.query<Tag[]>(query, { category });
    }

    return this.client.query<Tag[]>(query);
  }

  /**
   * Add new tag (with unique constraint per category)
   */
  async addTag(name: string, category: string): Promise<Tag> {
    const query = `
      INSERT Tag {
        name := <str>$name,
        category := <str>$category
      }
    `;

    const result = await this.client.querySingle<Tag>(query, { name, category });

    if (!result) {
      throw new Error('Failed to create tag');
    }

    return result;
  }

  /**
   * Get tag usage - count how many entities use this tag
   */
  async getTagUsage(tagName: string): Promise<{
    tag: Tag;
    experiences: number;
    skills: number;
    achievements: number;
    total: number;
  }> {
    const tagQuery = `
      SELECT Tag {
        id,
        name,
        category,
        created
      }
      FILTER .name = <str>$name
    `;

    const tag = await this.client.querySingle<Tag>(tagQuery, { name: tagName });

    if (!tag) {
      throw new Error(`Tag not found: ${tagName}`);
    }

    const expCount = await this.client.querySingle<{ count: number }>(
      'SELECT count((SELECT Experience FILTER $tag IN .tags))',
      { tag }
    );

    const skillCount = await this.client.querySingle<{ count: number }>(
      'SELECT count((SELECT Skill FILTER $tag IN .tags))',
      { tag }
    );

    const achieveCount = await this.client.querySingle<{ count: number }>(
      'SELECT count((SELECT Achievement FILTER $tag IN .tags))',
      { tag }
    );

    return {
      tag,
      experiences: expCount?.count || 0,
      skills: skillCount?.count || 0,
      achievements: achieveCount?.count || 0,
      total: (expCount?.count || 0) + (skillCount?.count || 0) + (achieveCount?.count || 0)
    };
  }
}
