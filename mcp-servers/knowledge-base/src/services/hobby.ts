/**
 * Hobby Service - CRUD operations for hobbies
 */
import { EdgeDBClient } from '../edgedb.js';
import type { TagReference, Translation, VerificationStatus } from '../types.js';

export interface HobbyInput {
  external_id: string;
  name: Translation;
  tools?: string[];
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate
  tags: TagReference[];
}

export interface HobbySearchFilters {
  tags?: TagReference[];
  tool?: string;
}

export interface Hobby {
  id: string;
  external_id: string;
  name: Translation;
  tools?: string[];
  article?: Translation;
  verification_status: VerificationStatus;
  last_verified: string;
  created: string;
  tags: Array<{ id: string; name: string; category: string }>;
}

export class HobbyService {
  constructor(private client: EdgeDBClient) {}

  async addHobby(input: HobbyInput): Promise<Hobby> {
    const query = `
      INSERT Hobby {
        external_id := <str>$external_id,
        name := <json>$name,
        tools := <array<str>>$tools IF EXISTS $tools ELSE {},
        article := <json>$article IF EXISTS $article ELSE {},
        verification_status := <VerificationStatus>$verification_status ?? <VerificationStatus>'draft',
        last_verified := <IsoDate>$last_verified,
        tags := (
          SELECT Tag FILTER
            .name IN array_unpack(<array<str>>$tag_names) AND
            .category IN array_unpack(<array<str>>$tag_categories)
        )
      }
    `;

    const params: Record<string, any> = {
      external_id: input.external_id,
      name: JSON.stringify(input.name),
      last_verified: input.last_verified,
      tag_names: input.tags.map(t => t.name),
      tag_categories: input.tags.map(t => t.category)
    };

    // Add optional params
    if (input.tools && input.tools.length > 0) params['tools'] = input.tools;
    if (input.article) params['article'] = JSON.stringify(input.article);
    if (input.verification_status) params['verification_status'] = input.verification_status;

    const result = await this.client.querySingle<Hobby>(query, params);
    if (!result) throw new Error('Failed to create hobby');
    const created = await this.getHobby(result.id);
    if (!created) throw new Error('Hobby not found after creation');
    return created;
  }

  async getHobby(id: string): Promise<Hobby | null> {
    const query = `
      SELECT Hobby {
        id,
        external_id,
        name,
        tools,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category }
      }
      FILTER .id = <uuid>$id
    `;

    return this.client.querySingle<Hobby>(query, { id });
  }

  async updateHobby(id: string, updates: Partial<HobbyInput>): Promise<Hobby> {
    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.name) {
      setClauses.push('name := <json>$name');
      params.name = JSON.stringify(updates.name);
    }
    if (updates.tools !== undefined) {
      setClauses.push('tools := <array<str>>$tools');
      params.tools = updates.tools;
    }
    if (updates.article !== undefined) {
      setClauses.push('article := <json>$article');
      params.article = JSON.stringify(updates.article);
    }
    if (updates.verification_status) {
      setClauses.push('verification_status := <VerificationStatus>$verification_status');
      params.verification_status = updates.verification_status;
    }
    if (updates.last_verified) {
      setClauses.push('last_verified := <IsoDate>$last_verified');
      params.last_verified = updates.last_verified;
    }

    const query = `
      UPDATE Hobby
      FILTER .id = <uuid>$id
      SET { ${setClauses.join(', ')} }
    `;

    await this.client.query(query, params);
    const updated = await this.getHobby(id);
    if (!updated) throw new Error('Hobby not found after update');
    return updated;
  }

  async searchHobbies(filters: HobbySearchFilters = {}): Promise<Hobby[]> {
    const whereClauses: string[] = [];
    const params: Record<string, any> = {};

    if (filters.tags && filters.tags.length > 0) {
      whereClauses.push(`
        ALL (
          SELECT (tag_name, tag_category) IN enumerate(array_unpack(<array<tuple<str, str>>>$tag_pairs))
          FOR tag_name IN array_unpack(.tags.name)
          FOR tag_category IN array_unpack(.tags.category)
        )
      `);
      params.tag_pairs = filters.tags.map(t => [t.name, t.category]);
    }

    if (filters.tool) {
      whereClauses.push(`<str>$tool IN array_unpack(.tools)`);
      params.tool = filters.tool;
    }

    const whereClause = whereClauses.length > 0 ? `FILTER ${whereClauses.join(' AND ')}` : '';

    const query = `
      SELECT Hobby {
        id,
        external_id,
        name,
        tools,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category }
      }
      ${whereClause}
      ORDER BY .name
    `;

    return this.client.query<Hobby>(query, params);
  }
}
