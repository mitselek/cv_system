/**
 * Certification Service - CRUD operations for certifications
 */
import { EdgeDBClient } from '../edgedb.js';
import type { TagReference, Translation, VerificationStatus } from '../types.js';

export interface CertificationInput {
  external_id: string;
  title: Translation;
  issuer: Translation;
  date: string; // IsoDate
  expiry_date?: string; // IsoDate
  credential_id?: string;
  credential_url?: string;
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate
  tags: TagReference[];
}

export interface CertificationSearchFilters {
  tags?: TagReference[];
  issuer?: string;
  dateRange?: { start?: string; end?: string };
}

export interface Certification {
  id: string;
  external_id: string;
  title: Translation;
  issuer: Translation;
  date: string;
  expiry_date?: string;
  credential_id?: string;
  credential_url?: string;
  article?: Translation;
  verification_status: VerificationStatus;
  last_verified: string;
  created: string;
  tags: Array<{ id: string; name: string; category: string }>;
}

export class CertificationService {
  constructor(private client: EdgeDBClient) {}

  async addCertification(input: CertificationInput): Promise<Certification> {
    const query = `
      INSERT Certification {
        external_id := <str>$external_id,
        title := <json>$title,
        issuer := <json>$issuer,
        date := <IsoDate>$date,
        expiry_date := <IsoDate>$expiry_date IF EXISTS $expiry_date ELSE {},
        credential_id := <str>$credential_id IF EXISTS $credential_id ELSE {},
        credential_url := <HttpUrl>$credential_url IF EXISTS $credential_url ELSE {},
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
      title: JSON.stringify(input.title),
      issuer: JSON.stringify(input.issuer),
      date: input.date,
      last_verified: input.last_verified,
      tag_names: input.tags.map(t => t.name),
      tag_categories: input.tags.map(t => t.category)
    };

    // Add optional params
    if (input.expiry_date) params['expiry_date'] = input.expiry_date;
    if (input.credential_id) params['credential_id'] = input.credential_id;
    if (input.credential_url) params['credential_url'] = input.credential_url;
    if (input.article) params['article'] = JSON.stringify(input.article);
    if (input.verification_status) params['verification_status'] = input.verification_status;

    const result = await this.client.querySingle<Certification>(query, params);
    if (!result) throw new Error('Failed to create certification');
    const created = await this.getCertification(result.id);
    if (!created) throw new Error('Certification not found after creation');
    return created;
  }

  async getCertification(id: string): Promise<Certification | null> {
    const query = `
      SELECT Certification {
        id,
        external_id,
        title,
        issuer,
        date,
        expiry_date,
        credential_id,
        credential_url,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category }
      }
      FILTER .id = <uuid>$id
    `;

    return this.client.querySingle<Certification>(query, { id });
  }

  async updateCertification(id: string, updates: Partial<CertificationInput>): Promise<Certification> {
    const setClauses: string[] = [];
    const params: Record<string, any> = { id };

    if (updates.title) {
      setClauses.push('title := <json>$title');
      params.title = JSON.stringify(updates.title);
    }
    if (updates.issuer) {
      setClauses.push('issuer := <json>$issuer');
      params.issuer = JSON.stringify(updates.issuer);
    }
    if (updates.date) {
      setClauses.push('date := <IsoDate>$date');
      params.date = updates.date;
    }
    if (updates.expiry_date !== undefined) {
      setClauses.push('expiry_date := <IsoDate>$expiry_date');
      params.expiry_date = updates.expiry_date;
    }
    if (updates.credential_id !== undefined) {
      setClauses.push('credential_id := <str>$credential_id');
      params.credential_id = updates.credential_id;
    }
    if (updates.credential_url !== undefined) {
      setClauses.push('credential_url := <HttpUrl>$credential_url');
      params.credential_url = updates.credential_url;
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
      UPDATE Certification
      FILTER .id = <uuid>$id
      SET { ${setClauses.join(', ')} }
    `;

    await this.client.query(query, params);
    const updated = await this.getCertification(id);
    if (!updated) throw new Error('Certification not found after update');
    return updated;
  }

  async searchCertifications(filters: CertificationSearchFilters = {}): Promise<Certification[]> {
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

    if (filters.issuer) {
      whereClauses.push(`contains(str_lower(<str>.issuer['et'] ?? <str>.issuer['en']), str_lower(<str>$issuer))`);
      params.issuer = filters.issuer;
    }

    if (filters.dateRange?.start) {
      whereClauses.push(`.date >= <IsoDate>$date_start`);
      params.date_start = filters.dateRange.start;
    }

    if (filters.dateRange?.end) {
      whereClauses.push(`.date <= <IsoDate>$date_end`);
      params.date_end = filters.dateRange.end;
    }

    const whereClause = whereClauses.length > 0 ? `FILTER ${whereClauses.join(' AND ')}` : '';

    const query = `
      SELECT Certification {
        id,
        external_id,
        title,
        issuer,
        date,
        expiry_date,
        credential_id,
        credential_url,
        article,
        verification_status,
        last_verified,
        created,
        tags: { id, name, category }
      }
      ${whereClause}
      ORDER BY .date DESC
    `;

    return this.client.query<Certification>(query, params);
  }
}
