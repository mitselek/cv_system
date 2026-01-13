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
      INSERT KnowledgeBaseLanguage {
        external_id := <str>$external_id,
        name := <json>$name,
        proficiency := <json>$proficiency,
        article := <json>$article IF EXISTS $article ELSE {},
        verification_status := <VerificationStatus>$verification_status ?? <VerificationStatus>'draft',
        last_verified := <IsoDate>$last_verified,
        tags := (
          SELECT Tag FILTER
            .name IN array_unpack(<array<str>>$tag_names) AND
            .category IN array_unpack(<array<str>>$tag_categories)
        ),
        evidence := (
          SELECT Experience FILTER .id IN array_unpack(<array<uuid>>$evidence_ids)
        ) IF EXISTS $evidence_ids ELSE {}
      }
    `;

    const params: Record<string, any> = {
      external_id: input.external_id,
      name: JSON.stringify(input.name),
      proficiency: JSON.stringify(input.proficiency),
      last_verified: input.last_verified,
      tag_names: input.tags.map(t => t.name),
      tag_categories: input.tags.map(t => t.category)
    };

    // Add optional params
    if (input.article) params['article'] = JSON.stringify(input.article);
    if (input.verification_status) params['verification_status'] = input.verification_status;
    if (input.evidence && input.evidence.length > 0) params['evidence_ids'] = input.evidence;

    const result = await this.client.querySingle<Language>(query, params);
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
      setClauses.push('name := <json>$name');
      params.name = JSON.stringify(updates.name);
    }
    if (updates.proficiency) {
      setClauses.push('proficiency := <json>$proficiency');
      params.proficiency = JSON.stringify(updates.proficiency);
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
      whereClauses.push(`
        ALL (
          SELECT (tag_name, tag_category) IN enumerate(array_unpack(<array<tuple<str, str>>>$tag_pairs))
          FOR tag_name IN array_unpack(.tags.name)
          FOR tag_category IN array_unpack(.tags.category)
        )
      `);
      params.tag_pairs = filters.tags.map(t => [t.name, t.category]);
    }

    if (filters.minProficiency) {
      // This is a simplified check - you might want more sophisticated proficiency filtering
      whereClauses.push(`EXISTS .proficiency`);
    }

    const whereClause = whereClauses.length > 0 ? `FILTER ${whereClauses.join(' AND ')}` : '';

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
      ${whereClause}
      ORDER BY .name
    `;

    return this.client.query<Language>(query, params);
  }
}
