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
      return this.client.query<Tag>(query, { category });
    }

    return this.client.query<Tag>(query);
  }

  /**
   * Add new tag (with unique constraint per category)
   */
  async addTag(name: string, category: string): Promise<Tag> {
    const query = `
      SELECT (
        INSERT Tag {
          name := <str>$name,
          category := <str>$category
        } UNLESS CONFLICT ON (.name, .category) ELSE (
          SELECT Tag FILTER .name = <str>$name AND .category = <str>$category
        )
      ) {
        id,
        name,
        category,
        created
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
    // Use LIMIT 1 since same name can exist in different categories
    const tagQuery = `
      SELECT Tag {
        id,
        name,
        category,
        created
      }
      FILTER .name = <str>$name
      LIMIT 1
    `;

    const tag = await this.client.querySingle<Tag>(tagQuery, { name: tagName });

    if (!tag) {
      throw new Error(`Tag not found: ${tagName}`);
    }

    // Query uses subselect to filter by tag name
    const expCount = await this.client.querySingle<number>(
      `SELECT count((
        SELECT Experience 
        FILTER (SELECT Tag FILTER .name = <str>$name) IN .tags
      ))`,
      { name: tagName }
    );

    const skillCount = await this.client.querySingle<number>(
      `SELECT count((
        SELECT Skill 
        FILTER (SELECT Tag FILTER .name = <str>$name) IN .tags
      ))`,
      { name: tagName }
    );

    const achieveCount = await this.client.querySingle<number>(
      `SELECT count((
        SELECT Achievement 
        FILTER (SELECT Tag FILTER .name = <str>$name) IN .tags
      ))`,
      { name: tagName }
    );

    const experiences = expCount || 0;
    const skills = skillCount || 0;
    const achievements = achieveCount || 0;

    return {
      tag,
      experiences,
      skills,
      achievements,
      total: experiences + skills + achievements
    };
  }
}
