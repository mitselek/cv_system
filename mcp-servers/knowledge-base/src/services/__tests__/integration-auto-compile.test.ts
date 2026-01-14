import { test, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { EdgeDBClient } from '../../edgedb';
import { ExperienceService } from '../../services/experience';
import { setAutoCompileRunner, resetAutoCompileDebounce } from '../../compileHook';
import { scheduleAutoCompile } from '../../compileHook';

test('adding experience in EdgeDB triggers compile via auto-runner (integration)', async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'knb-int-'));

  // Dynamic import of compiler to avoid loader issues
  const buildModule = await import('../../../../../scripts/build_context');
  const compileKnowledgeBase = buildModule.compileKnowledgeBase as (kb?: string, s?: 'filesystem'|'edgedb') => Promise<void>;

  // Prepare EdgeDB client and service
  const client = new EdgeDBClient();
  await client.connect();
  const expService = new ExperienceService(client);

  const external_id = `int-test-exp-${Date.now()}`;

  // Replace the runner to call compileKnowledgeBase against our tmp dir
  setAutoCompileRunner(async (kbRoot?: string) => {
    await compileKnowledgeBase(tmp, 'edgedb');
  });

  // Add experience to EdgeDB
  const created = await expService.addExperience({
    external_id,
    title: { en: 'Integration Test Experience' },
    company: { en: 'Integration Co' },
    dates: { start: '2025-01', end: '2025-12' },
    article: { en: 'Integration test body' },
    verification_status: 'verified',
    last_verified: '2025-12-01',
    tags: [],
    skills_demonstrated: []
  });

  // Schedule auto-compile (simulating server's behavior)
  scheduleAutoCompile();

  // Wait for debounce + compile
  await new Promise(resolve => setTimeout(resolve, 600));

  const outFile = path.join(tmp, '_compiled_context.md');
  expect(fs.existsSync(outFile)).toBeTruthy();

  const out = fs.readFileSync(outFile, 'utf8');
  expect(out).toContain(`### ${external_id}`);
  expect(out).toContain('Integration Test Experience');

  // Cleanup
  resetAutoCompileDebounce();
  await client.disconnect();
});