import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// --- Interfaces for Knowledge Base Entities ---

interface MultilingualText {
  et?: string;
  en?: string;
}

interface DateRange {
  start: string;
  end: string;
}

interface BaseEntity {
  id: string;
  type: string;
  status: string;
  last_verified: string;
  tags?: string[];
}

interface Experience extends BaseEntity {
  company: string;
  url?: string;
  context?: string;
  dates: DateRange;
  title: MultilingualText;
  location: string;
  description?: MultilingualText;
  achievements?: string[]; // IDs of achievement modules
  skills_demonstrated?: string[]; // IDs of skill modules
}

interface Skill extends BaseEntity {
  skill_name: MultilingualText;
  category: string;
  proficiency_level?: string; // e.g., "9/10", "advanced"
  evidence?: string[]; // IDs of experience/achievement modules
}

interface Achievement extends BaseEntity {
  parent_experience: string; // ID of the parent experience
  title: MultilingualText;
  description?: MultilingualText;
}

interface Education extends BaseEntity {
  dates: DateRange | string; // Can be a range or single year string
  institutions?: string[];
  studies?: Array<{ field: MultilingualText; institution: string }>;
  degree: MultilingualText;
}

interface Certification extends BaseEntity {
  title: string;
  issuer: string;
  date: string;
  credential_id?: string;
  url?: string;
}

// --- Compiler Logic ---

const CV_SYSTEM_ROOT = path.join(__dirname, '..', '..');

export async function compileKnowledgeBase(knowledgeBaseRoot?: string, source: 'filesystem' | 'edgedb' = 'filesystem') {
  const KNOWLEDGE_BASE_ROOT = knowledgeBaseRoot ?? path.join(CV_SYSTEM_ROOT, 'knowledge_base');
  const OUTPUT_FILE = path.join(KNOWLEDGE_BASE_ROOT, '_compiled_context.md');

  if (source === 'edgedb') {
    // Query EdgeDB for canonical data
    const { EdgeDBClient } = await import('../mcp-servers/knowledge-base/src/edgedb.js');
    const client = new EdgeDBClient();
    await client.connect();

    let compiledContent = `# Compiled Professional Background\n\n`;
    compiledContent += `This document is automatically generated from the modular knowledge base (EdgeDB).\n`;
    compiledContent += `It serves as a consolidated context for LLM interactions.\n\n---\n\n`;

    // Experiences
    const exps: any[] = await client.query(`
      SELECT Experience {
        external_id,
        title,
        company,
        dates,
        article := (SELECT .article IF EXISTS .article ELSE <json>{}),
        tags: { name, category } ORDER BY .name
      }
      ORDER BY .dates.` + "`start` DESC"
    );

    if (exps.length > 0) {
      compiledContent += `## Experiences\n\n`;
      for (const e of exps) {
        const yamlBlock = yaml.dump({
          id: e.external_id,
          type: 'employment',
          company: e.company,
          dates: e.dates,
          title: e.title,
          status: e.verification_status ?? 'verified',
          last_verified: e.last_verified ?? new Date().toISOString().slice(0,10),
          tags: (e.tags || []).map((t: any) => `${t.name}/${t.category}`)
        });
        compiledContent += `### ${e.external_id}\n\n`;
        compiledContent += "```yaml\n" + yamlBlock + "\n```\n\n";
        if (e.article && Object.keys(e.article).length > 0) {
          // Keep markdown body if present under 'article.en' or 'article.et'
          const body = e.article.en ?? e.article.et ?? '';
          if (body) {
            compiledContent += `${body}\n\n`;
          }
        }
        compiledContent += `---\n\n`;
      }
    }

    // TODO: add Skills, Achievements, Projects, etc. from EdgeDB as needed

    compiledContent = compiledContent.replace(/\n{3,}/g, '\n\n');
    compiledContent = compiledContent.trimEnd() + '\n';

    fs.writeFileSync(OUTPUT_FILE, compiledContent, 'utf8');
    console.log(`Knowledge base compiled (EdgeDB) to ${OUTPUT_FILE}`);

    await client.disconnect();
    return;
  }

  // Default: filesystem-based compilation (existing behavior)
  let compiledContent = `# Compiled Professional Background\n\n`;
  compiledContent += `This document is automatically generated from the modular knowledge base.\n`;
  compiledContent += `It serves as a consolidated context for LLM interactions.\n\n---\n\n`;

  const entityTypes = ['experiences', 'skills', 'achievements', 'education', 'certifications', 'languages', 'hobbies'];

  for (const type of entityTypes) {
    const dirPath = path.join(KNOWLEDGE_BASE_ROOT, type);
    if (!fs.existsSync(dirPath)) {
      console.warn(`Directory not found: ${dirPath}. Skipping.`);
      continue;
    }

    const files = fs.readdirSync(dirPath).filter(file => file.endsWith('.md'));

    if (files.length > 0) {
      compiledContent += `## ${type.charAt(0).toUpperCase() + type.slice(1)}\n\n`;

      for (const file of files) {
        const filePath = path.join(dirPath, file);
        const fileContent = fs.readFileSync(filePath, 'utf8');

        // Extract YAML frontmatter and Markdown body
        const frontmatterMatch = fileContent.match(/(?:^|\n)---\s*\n([\s\S]*?)\n---\s*(?:\n|$)([\s\S]*)/);

        if (frontmatterMatch) {
          const frontmatter = frontmatterMatch[1];
          let markdownBody = frontmatterMatch[2].trim();

          const data = yaml.load(frontmatter) as BaseEntity; // Type assertion

          compiledContent += `### ${data.id}\n\n`;
          compiledContent += "```yaml\n" + frontmatter + "\n```\n\n";
          if (markdownBody) {
            // Increase heading levels by 2 to nest under h3 entity heading
            // Source convention: h2 for main sections, h3 for subsections
            // Compiled output: h4 for main sections, h5 for subsections (under h3 entity)
            // Process in reverse order (deepest first) to avoid double-replacement
            markdownBody = markdownBody.replace(/^##### /gm, '####### ');
            markdownBody = markdownBody.replace(/^#### /gm, '###### ');
            markdownBody = markdownBody.replace(/^### /gm, '##### ');
            markdownBody = markdownBody.replace(/^## /gm, '#### ');
            markdownBody = markdownBody.replace(/^# /gm, '### ');
            // Ensure blank line before headings (MD022)
            markdownBody = markdownBody.replace(/([^\n])\n(#{1,6} )/g, '$1\n\n$2');
            // Ensure blank line after headings (MD022)
            markdownBody = markdownBody.replace(/(#{1,6} .+)\n([^\n#])/g, '$1\n\n$2');
            compiledContent += `${markdownBody}\n\n`;
          }
          compiledContent += `---\n\n`;
        } else {
          console.warn(`No frontmatter found in ${file}. Appending raw content.`);
          compiledContent += `### ${file}\n\n`;
          compiledContent += `${fileContent.trim()}\n\n---\n\n`;
        }
      }
    }
  }

  // Remove any instances of 3+ consecutive newlines
  compiledContent = compiledContent.replace(/\n{3,}/g, '\n\n');
  
  // Remove trailing whitespace/newlines at the end of file
  compiledContent = compiledContent.trimEnd() + '\n';

  fs.writeFileSync(OUTPUT_FILE, compiledContent, 'utf8');
  console.log(`Knowledge base compiled to ${OUTPUT_FILE}`);
}

if (require.main === module) {
  compileKnowledgeBase().catch(console.error);
}