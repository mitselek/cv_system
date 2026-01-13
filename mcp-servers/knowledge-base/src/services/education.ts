/**
 * Education Service - CRUD operations for education entries
 */
import { EdgeDBClient } from '../edgedb.js';
import type { TagReference, Translation, VerificationStatus } from '../types.js';

export interface EducationInput {
  external_id: string;
  institutions: Translation[];
  fields: Translation[];
  dates: { start: string; end?: string }; // IsoDate
  degree?: Translation;
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate
  tags: TagReference[];
}

export interface EducationSearchFilters {
  tags?: TagReference[];
  institution?: string;
  dateRange?: { start?: string; end?: string };
}

export interface Education {
  id: string;
  external_id: string;
  institutions: Translation[];
  fields: Translation[];
  dates: { start: string; end?: string };
  degree?: Translation;
  article?: Translation;
  verification_status: VerificationStatus;
  last_verified: string;
  created: string;
  tags: Array<{ id: string; name: string; category: string }>;
}

export class EducationService {
  constructor(private client: EdgeDBClient) {}

  async addEducation(input: EducationInput): Promise<Education> {
    const query = `
      INSERT Education {
        external_id := <str>$external_id,
        institutions := <array<json>>$institutions,
        fields := <array<json>>$fields,
        dates := (
          \`start\` := <IsoDate>$date_start,
          \`end\` := <IsoDate>$date_end IF EXISTS $date_end ELSE <IsoDate>{}
        ),
        degree := <json>$degree IF EXISTS $degree ELSE {},
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
      institutions: input.institutions.map(i => JSON.stringify(i)),
      fields: input.fields.map(f => JSON.stringify(f)),
      date_start: input.dates.start,
      last_verified: input.last_verified,
      tag_names: input.tags.map(t => t.name),
      tag_categories: input.tags.map(t => t.category)
    };

    // Add optional params
    if (input.dates.end) params['date_end'] = input.dates.end;
    if (input.degree) params['degree'] = JSON.stringify(input.degree);
    if (input.article) params['article'] = JSON.stringify(input.article);
    if (input.verification_status) params['verification_status'] = input.verification_status;

    const result = await this.client.querySingle<Education>(query, params);
    if (!result) throw new Error('Failed to create education');
    const created = await this.getEducation(result.id);
    if (!created) throw new Error('Education not found after creation');
    return created;
  }

  async getEducation(id: string): Promise<Education | null> {
    const query = `
      SELECT Education {
        id,
        external_id,
        institutions,
        fields,
        dates,
        degree,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category }
      }
      FILTER .id = <uuid>$id
    `;

    return this.client.querySingle<Education>(query, { id });
  }

  async updateEducation(id: string, updates: Partial<EducationInput>): Promise<Education> {
    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.institutions) {
      setClauses.push('institutions := <array<json>>$institutions');
      params.institutions = updates.institutions.map(i => JSON.stringify(i));
    }
    if (updates.fields) {
      setClauses.push('fields := <array<json>>$fields');
      params.fields = updates.fields.map(f => JSON.stringify(f));
    }
    if (updates.dates) {
      if (updates.dates.end !== undefined) {
        setClauses.push('dates := (`start` := <IsoDate>$date_start, `end` := <IsoDate>$date_end)');
        params.date_start = updates.dates.start;
        params.date_end = updates.dates.end;
      } else {
        setClauses.push('dates.`start` := <IsoDate>$date_start');
        params.date_start = updates.dates.start;
      }
    }
    if (updates.degree !== undefined) {
      setClauses.push('degree := <json>$degree');
      params.degree = JSON.stringify(updates.degree);
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
      UPDATE Education
      FILTER .id = <uuid>$id
      SET { ${setClauses.join(', ')} }
    `;

    await this.client.query(query, params);
    const updated = await this.getEducation(id);
    if (!updated) throw new Error('Education not found after update');
    return updated;
  }

  async searchEducation(filters: EducationSearchFilters = {}): Promise<Education[]> {
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

    if (filters.institution) {
      whereClauses.push(`
        EXISTS (
          FOR inst IN array_unpack(.institutions)
          UNION (
            contains(str_lower(<str>inst['et'] ?? <str>inst['en']), str_lower(<str>$institution))
          )
        )
      `);
      params.institution = filters.institution;
    }

    if (filters.dateRange?.start) {
      whereClauses.push(`.dates.\`end\` >= <IsoDate>$date_start`);
      params.date_start = filters.dateRange.start;
    }

    if (filters.dateRange?.end) {
      whereClauses.push(`.dates.\`start\` <= <IsoDate>$date_end`);
      params.date_end = filters.dateRange.end;
    }

    const whereClause = whereClauses.length > 0 ? `FILTER ${whereClauses.join(' AND ')}` : '';

    const query = `
      SELECT Education {
        id,
        external_id,
        institutions,
        fields,
        dates,
        degree,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category }
      }
      ${whereClause}
      ORDER BY .dates.\`start\` DESC
    `;

    return this.client.query<Education>(query, params);
  }
}
