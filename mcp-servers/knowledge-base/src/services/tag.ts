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

export interface TagSuggestion {
  name: string;
  category: string;
  distance: number;
}

/**
 * Calculate Levenshtein distance between two strings
 * Returns the minimum number of single-character edits needed to change one word into another
 */
function levenshteinDistance(str1: string, str2: string): number {
  const len1 = str1.length;
  const len2 = str2.length;

  // Create a 2D array for dynamic programming
  const matrix: number[][] = Array(len1 + 1)
    .fill(null)
    .map(() => Array(len2 + 1).fill(0));

  // Initialize first row and column
  for (let i = 0; i <= len1; i++) matrix[i][0] = i;
  for (let j = 0; j <= len2; j++) matrix[0][j] = j;

  // Fill the matrix
  for (let i = 1; i <= len1; i++) {
    for (let j = 1; j <= len2; j++) {
      const cost = str1[i - 1] === str2[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(
        matrix[i - 1][j] + 1, // deletion
        matrix[i][j - 1] + 1, // insertion
        matrix[i - 1][j - 1] + cost // substitution
      );
    }
  }

  return matrix[len1][len2];
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

  /**
   * Find tags similar to the input string using Levenshtein distance
   * @param input - The string to match against
   * @param maxDistance - Maximum edit distance to consider (default: 3)
   * @param category - Optional category filter
   * @returns Array of suggestions sorted by distance (closest first)
   */
  async findSimilarTags(
    input: string,
    maxDistance: number = 3,
    category?: string
  ): Promise<TagSuggestion[]> {
    // Get all tags (filtered by category if provided)
    const tags = await this.listTags(category);

    // Calculate distance for each tag
    const suggestions: TagSuggestion[] = tags
      .map(tag => ({
        name: tag.name,
        category: tag.category,
        distance: levenshteinDistance(input.toLowerCase(), tag.name.toLowerCase())
      }))
      .filter(s => s.distance <= maxDistance && s.distance > 0) // Exclude exact matches
      .sort((a, b) => a.distance - b.distance); // Sort by distance (closest first)

    return suggestions;
  }
}
