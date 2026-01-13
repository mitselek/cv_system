/**
 * Project Service - CRUD operations for Project entity
 */
import { EdgeDBClient } from '../edgedb.js';
import { Translation, TagReference, VerificationStatus, ProjectStatus } from '../types.js';

export interface ProjectInput {
  external_id: string;
  name: Translation;
  url?: string;
  repository?: string;
  status?: ProjectStatus;
  dates?: { start: string; end?: string }; // IsoDate format
  technologies?: string[];
  article?: Translation;
  verification_status?: VerificationStatus;
  last_verified: string; // IsoDate format
  tags: TagReference[];
  skills_demonstrated?: string[]; // Skill external_ids
}

export interface Project extends Omit<ProjectInput, 'tags' | 'skills_demonstrated'> {
  id: string;
  tags: TagReference[];
  skills_demonstrated: string[];
  created: string;
}

export interface ProjectSearchFilters {
  tags?: TagReference[];
  status?: ProjectStatus;
  technologies?: string[];
}

export class ProjectService {
  constructor(private client: EdgeDBClient) {}

  /**
   * Add new project
   */
  async addProject(input: ProjectInput): Promise<Project> {
    if (!input.name.et && !input.name.en) {
      throw new Error('Project name must have at least one language (et or en)');
    }

    const articleClause = input.article ? 'article := <Translation>$article,' : '';
    const datesClause = input.dates
      ? input.dates.end
        ? 'dates := (`start` := <IsoDate>$date_start, `end` := <IsoDate>$date_end),'
        : 'dates := (`start` := <IsoDate>$date_start, `end` := <IsoDate>$date_start),'
      : '';
    const technologiesClause = input.technologies ? 'technologies := <array<str>>$technologies,' : '';

    const query = `
      WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs),
           skill_ids := array_unpack(<array<str>>$skill_ids)
      SELECT (
        INSERT Project {
          external_id := <str>$external_id,
          name := <Translation>$name,
          url := <optional HttpUrl>$url,
          repository := <optional HttpUrl>$repository,
          status := <ProjectStatus>$status,
          ${datesClause}
          ${technologiesClause}
          ${articleClause}
          verification_status := <VerificationStatus>$verification_status,
          last_verified := <IsoDate>$last_verified,
          tags := DISTINCT (
            FOR tag_ref IN tag_refs UNION (
              SELECT Tag 
              FILTER .name = tag_ref.name AND .category = tag_ref.category
            )
          ),
          skills_demonstrated := DISTINCT (
            FOR skill_id IN skill_ids UNION (
              SELECT Skill FILTER .external_id = skill_id
            )
          )
        }
      ) {
        id,
        external_id,
        name,
        url,
        repository,
        status,
        dates,
        technologies,
        article,
        verification_status,
        last_verified,
        created,
        tags: { name, category },
        skills_demonstrated: { external_id, name }
      }
    `;

    const tagRefs = input.tags.map((tag) => ({ name: tag.name, category: tag.category }));
    const skillIds = input.skills_demonstrated || [];

    const params: Record<string, unknown> = {
      external_id: input.external_id,
      name: input.name,
      url: input.url || null,
      repository: input.repository || null,
      status: input.status || ProjectStatus.Active,
      verification_status: input.verification_status || VerificationStatus.Draft,
      last_verified: input.last_verified,
      tag_refs: tagRefs,
      skill_ids: skillIds
    };

    if (input.dates) {
      params.date_start = input.dates.start;
      if (input.dates.end) {
        params.date_end = input.dates.end;
      }
    }

    if (input.technologies) {
      params.technologies = input.technologies;
    }

    if (input.article) {
      params.article = input.article;
    }

    const result = await this.client.querySingle<Project>(query, params);

    if (!result) {
      throw new Error('Failed to create project');
    }

    return result;
  }

  /**
   * Get project by ID
   */
  async getProject(id: string): Promise<Project | null> {
    const query = `
      SELECT Project {
        id,
        external_id,
        name,
        url,
        repository,
        status,
        dates,
        technologies,
        article,
        verification_status,
        last_verified,
        created,
        tags: { name, category },
        skills_demonstrated: { external_id, name }
      }
      FILTER .id = <uuid>$id
    `;

    return await this.client.querySingle<Project>(query, { id });
  }

  /**
   * Update project
   */
  async updateProject(id: string, updates: Partial<ProjectInput>): Promise<Project> {
    const setClauses: string[] = [];
    const params: Record<string, unknown> = { id };

    if (updates.name !== undefined) {
      setClauses.push('name := <Translation>$name');
      params.name = updates.name;
    }

    if (updates.url !== undefined) {
      setClauses.push('url := <optional HttpUrl>$url');
      params.url = updates.url || null;
    }

    if (updates.repository !== undefined) {
      setClauses.push('repository := <optional HttpUrl>$repository');
      params.repository = updates.repository || null;
    }

    if (updates.status !== undefined) {
      setClauses.push('status := <ProjectStatus>$status');
      params.status = updates.status;
    }

    if (updates.dates !== undefined) {
      setClauses.push('dates := (`start` := <IsoDate>$date_start, `end` := <IsoDate>$date_end)');
      params.date_start = updates.dates.start;
      params.date_end = updates.dates.end;
    }

    if (updates.technologies !== undefined) {
      setClauses.push('technologies := <array<str>>$technologies');
      params.technologies = updates.technologies;
    }

    if (updates.article !== undefined) {
      setClauses.push('article := <Translation>$article');
      params.article = updates.article;
    }

    if (setClauses.length === 0) {
      throw new Error('No update fields provided');
    }

    const query = `
      SELECT (
        UPDATE Project
        FILTER .id = <uuid>$id
        SET {
          ${setClauses.join(',\n          ')}
        }
      ) {
        id,
        external_id,
        name,
        url,
        repository,
        status,
        dates,
        technologies,
        article,
        verification_status,
        last_verified,
        created,
        tags: { name, category },
        skills_demonstrated: { external_id, name }
      }
    `;

    const result = await this.client.querySingle<Project>(query, params);

    if (!result) {
      throw new Error(`Project with id ${id} not found`);
    }

    return result;
  }

  /**
   * Search projects with filters
   */
  async searchProjects(filters?: ProjectSearchFilters): Promise<Project[]> {
    const conditions: string[] = [];
    const params: Record<string, unknown> = {};

    if (filters?.tags && filters.tags.length > 0) {
      const tagRefs = filters.tags.map((tag) => ({ name: tag.name, category: tag.category }));
      params.tag_refs = tagRefs;
      conditions.push(`
        WITH tag_refs := array_unpack(<array<tuple<name: str, category: str>>>$tag_refs)
        FOR tag_ref IN tag_refs UNION (
          SELECT Tag FILTER .name = tag_ref.name AND .category = tag_ref.category
        ) IN .tags
      `);
    }

    if (filters?.status) {
      params.status = filters.status;
      conditions.push('.status = <ProjectStatus>$status');
    }

    if (filters?.technologies && filters.technologies.length > 0) {
      params.technologies = filters.technologies;
      // Check if any technology in the filter list is in the project's technologies array
      conditions.push('EXISTS (SELECT .technologies FILTER .technologies IN <array<str>>$technologies)');
    }

    const filterClause = conditions.length > 0 ? `FILTER ${conditions.join(' AND ')}` : '';

    const query = `
      SELECT Project {
        id,
        external_id,
        name,
        url,
        repository,
        status,
        dates,
        technologies,
        article,
        verification_status,
        last_verified,
        created,
        tags: { name, category },
        skills_demonstrated: { external_id, name }
      }
      ${filterClause}
      ORDER BY .created DESC
    `;

    return await this.client.query<Project>(query, params);
  }
}
