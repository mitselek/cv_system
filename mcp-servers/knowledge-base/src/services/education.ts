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
    if (!input.dates.end) {
      throw new Error('Education dates.end is required');
    }

    const query = `
      INSERT Education {
        external_id := <str>$external_id,
        institutions := <array<Translation>>$institutions,
        fields := <array<Translation>>$fields,
        dates := (\`start\` := <IsoDate>$date_start, \`end\` := <IsoDate>$date_end),
        degree := <optional Translation>$degree,
        article := <optional Translation>$article,
        verification_status := <optional VerificationStatus>$verification_status ?? <VerificationStatus>'draft',
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
      institutions: input.institutions,
      fields: input.fields,
      date_start: input.dates.start,
      date_end: input.dates.end,
      last_verified: input.last_verified,
      tag_names: input.tags.map(t => t.name),
      tag_categories: input.tags.map(t => t.category),
      degree: input.degree ?? null,
      article: input.article ?? null,
      verification_status: input.verification_status ?? null
    };

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
      setClauses.push('institutions := <array<Translation>>$institutions');
      params.institutions = updates.institutions;
    }
    if (updates.fields) {
      setClauses.push('fields := <array<Translation>>$fields');
      params.fields = updates.fields;
    }
    if (updates.dates) {
      const hasStart = updates.dates.start !== undefined;
      const hasEnd = updates.dates.end !== undefined;

      if (hasStart && hasEnd) {
        setClauses.push('dates := (`start` := <IsoDate>$date_start, `end` := <IsoDate>$date_end)');
        params.date_start = updates.dates.start;
        params.date_end = updates.dates.end;
      } else if (hasStart) {
        setClauses.push('dates := (`start` := <IsoDate>$date_start, `end` := .dates.`end`)');
        params.date_start = updates.dates.start;
      } else if (hasEnd) {
        setClauses.push('dates := (`start` := .dates.`start`, `end` := <IsoDate>$date_end)');
        params.date_end = updates.dates.end;
      }
    }
    if (updates.degree !== undefined) {
      setClauses.push('degree := <optional Translation>$degree');
      params.degree = updates.degree ?? null;
    }
    if (updates.article !== undefined) {
      setClauses.push('article := <optional Translation>$article');
      params.article = updates.article ?? null;
    }
    if (updates.verification_status) {
      setClauses.push('verification_status := <VerificationStatus>$verification_status');
      params.verification_status = updates.verification_status;
    }
    if (updates.last_verified) {
      setClauses.push('last_verified := <IsoDate>$last_verified');
      params.last_verified = updates.last_verified;
    }

    if (setClauses.length === 0) {
      const existing = await this.getEducation(id);
      if (!existing) throw new Error('Education not found');
      return existing;
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
        count((
          FOR tag_ref IN tag_refs
          UNION (
            SELECT Tag
            FILTER .name = tag_ref.name
              AND .category = tag_ref.category
              AND Tag IN .tags
          )
        )) = len(<array<tuple<name: str, category: str>>>$tag_refs)
      `);
      params.tag_refs = filters.tags.map(t => ({ name: t.name, category: t.category }));
    }

    if (filters.institution) {
      whereClauses.push(`
        EXISTS (
          FOR inst IN array_unpack(.institutions)
          UNION (
            contains(
              str_lower(<str>json_get(inst, 'et') ?? <str>json_get(inst, 'en')),
              str_lower(<str>$institution)
            )
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

    const withClause = filters.tags && filters.tags.length > 0
      ? 'WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)'
      : '';

    const query = `
      ${withClause}
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
