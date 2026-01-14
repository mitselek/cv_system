import { test, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { compileKnowledgeBase } from '../scripts/build_context';

function writeFile(filePath: string, content: string) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, content, 'utf8');
}

test('compileKnowledgeBase generates expected markdown structure for experiences', async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'kb-test-'));

  // Create experiences dir and a sample experience
  const expDir = path.join(tmp, 'experiences');
  fs.mkdirSync(expDir, { recursive: true });

  const sample = `---
id: test-exp-1
type: employment
company: Test Co
dates:\n  start: '2020-01'\n  end: '2020-12'
title:\n  en: Test Title\n  et: Test Pealkiri
status: verified
last_verified: '2025-01-01'
---

# Summary
Some description about the test experience.
`;

  writeFile(path.join(expDir, 'test-exp-1.md'), sample);

  await compileKnowledgeBase(tmp);

  const outFile = path.join(tmp, '_compiled_context.md');
  expect(fs.existsSync(outFile)).toBeTruthy();

  const out = fs.readFileSync(outFile, 'utf8');

  // Basic content checks
  expect(out).toContain('## Experiences');
  expect(out).toContain('### test-exp-1');
  expect(out).toContain('company: Test Co');
  expect(out).toContain('Some description about the test experience.');

  // Clean up
  fs.rmSync(tmp, { recursive: true, force: true });
});
