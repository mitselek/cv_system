/**
 * Language Service - CRUD operations for languages
 */
import { EdgeDBClient } from '../edgedb.js';
import type { TagReference, Translation, VerificationStatus } from '../types.js';

export interface LanguageInput {
  external_id: string;
  name: Translation;
  proficiency: Record<string, string>; // LanguageProficiency JSON
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate
  tags: TagReference[];
  evidence?: string[]; // Experience IDs
}

export interface LanguageSearchFilters {
  tags?: TagReference[];
  minProficiency?: string;
}

export interface Language {
  id: string;
  external_id: string;
  name: Translation;
  proficiency: Record<string, string>;
  article?: Translation;
  verification_status: VerificationStatus;
  last_verified: string;
  created: string;
  tags: Array<{ id: string; name: string; category: string }>;
  evidence: Array<{ id: string; external_id: string }>;
}

export class LanguageService {
  constructor(private client: EdgeDBClient) {}

  async addLanguage(input: LanguageInput): Promise<Language> {
    const query = `
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs),
           evidence_ids := array_unpack(<array<uuid>>$evidence_ids)
      SELECT (
        INSERT KnowledgeBaseLanguage {
          external_id := <str>$external_id,
          name := <Translation>$name,
          proficiency := <LanguageProficiency>$proficiency,
          article := <optional Translation>$article,
          verification_status := <optional VerificationStatus>$verification_status ?? <VerificationStatus>'draft',
          last_verified := <IsoDate>$last_verified,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          ),
          evidence := DISTINCT (
            FOR evidence_id IN evidence_ids UNION (
              SELECT Experience FILTER .id = evidence_id
            )
          )
        }
      ) { id };
    `;

    const result = await this.client.querySingle<{ id: string }>(query, {
      external_id: input.external_id,
      name: input.name,
      proficiency: input.proficiency,
      article: input.article ?? null,
      verification_status: input.verification_status ?? null,
      last_verified: input.last_verified,
      tag_refs: input.tags.map(t => ({ name: t.name, category: t.category })),
      evidence_ids: input.evidence ?? []
    });

    if (!result) throw new Error('Failed to create language');

    const created = await this.getLanguage(result.id);
    if (!created) throw new Error('Language not found after creation');
    return created;
  }

  async getLanguage(id: string): Promise<Language | null> {
    const query = `
      SELECT KnowledgeBaseLanguage {
        id,
        external_id,
        name,
        proficiency,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category },
        evidence: { id, external_id }
      }
      FILTER .id = <uuid>$id
    `;

    return this.client.querySingle<Language>(query, { id });
  }

  async updateLanguage(id: string, updates: Partial<LanguageInput>): Promise<Language> {
    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.name) {
      setClauses.push('name := <Translation>$name');
      params.name = updates.name;
    }
    if (updates.proficiency) {
      setClauses.push('proficiency := <LanguageProficiency>$proficiency');
      params.proficiency = updates.proficiency;
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
      UPDATE KnowledgeBaseLanguage
      FILTER .id = <uuid>$id
      SET { ${setClauses.join(', ')} }
    `;

    await this.client.query(query, params);
    const updated = await this.getLanguage(id);
    if (!updated) throw new Error('Language not found after update');
    return updated;
  }

  async searchLanguages(filters: LanguageSearchFilters = {}): Promise<Language[]> {
    const whereClauses: string[] = [];
    const params: Record<string, any> = {};

    if (filters.tags && filters.tags.length > 0) {
      params.tag_refs = filters.tags.map(t => ({ name: t.name, category: t.category }));
      whereClauses.push(`
        count((
          FOR tag_ref IN tag_refs
          UNION (
            SELECT .tags
            FILTER .name = tag_ref.name
              AND .category = tag_ref.category
          )
        )) = len(<array<tuple<name: str, category: str>>>$tag_refs)
      `);
    }

    if (filters.minProficiency) {
      // This is a simplified check - you might want more sophisticated proficiency filtering
      whereClauses.push(`EXISTS .proficiency`);
    }

    const whereClause = whereClauses.length > 0 ? `FILTER ${whereClauses.join(' AND ')}` : '';

    const withClause = filters.tags && filters.tags.length > 0
      ? 'WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)'
      : '';

    const query = `
      ${withClause}
      SELECT KnowledgeBaseLanguage {
        id,
        external_id,
        name,
        proficiency,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category },
        evidence: { id, external_id }
      }
      ${whereClause}
      ORDER BY .external_id
    `;

    return this.client.query<Language>(query, params);
  }
}
