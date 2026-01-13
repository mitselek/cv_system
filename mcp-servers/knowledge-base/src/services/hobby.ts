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
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)
      SELECT (
        INSERT Hobby {
          external_id := <str>$external_id,
          name := <Translation>$name,
          tools := <optional array<str>>$tools,
          article := <optional Translation>$article,
          verification_status := <optional VerificationStatus>$verification_status ?? <VerificationStatus>'draft',
          last_verified := <IsoDate>$last_verified,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          )
        }
      ) { id };
    `;

    const result = await this.client.querySingle<{ id: string }>(query, {
      external_id: input.external_id,
      name: input.name,
      tools: input.tools ?? null,
      article: input.article ?? null,
      verification_status: input.verification_status ?? null,
      last_verified: input.last_verified,
      tag_refs: input.tags.map(t => ({ name: t.name, category: t.category }))
    });

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
      setClauses.push('name := <Translation>$name');
      params.name = updates.name;
    }
    if (updates.tools !== undefined) {
      setClauses.push('tools := <array<str>>$tools');
      params.tools = updates.tools;
    }
    if (updates.article !== undefined) {
      setClauses.push('article := <Translation>$article');
      params.article = updates.article;
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
    const conditions: string[] = [];
    const params: Record<string, any> = {};
    let withClause = '';

    if (filters.tags && filters.tags.length > 0) {
      withClause = 'WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)';
      params.tag_refs = filters.tags.map(t => ({ name: t.name, category: t.category }));
      conditions.push(`
        count((
          FOR tag_ref IN tag_refs 
          UNION (
            SELECT Tag 
            FILTER .name = tag_ref.name 
              AND .category = tag_ref.category 
              AND Tag IN Hobby.tags
          )
        )) = len(<array<tuple<name: str, category: str>>>$tag_refs)
      `);
    }

    if (filters.tool) {
      conditions.push(`<str>$tool IN array_unpack(.tools)`);
      params.tool = filters.tool;
    }

    const whereClause = conditions.length > 0 ? `FILTER ${conditions.join(' AND ')}` : '';

    const query = `
      ${withClause}
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
