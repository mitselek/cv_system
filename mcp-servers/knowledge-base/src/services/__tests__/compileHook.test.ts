import { test, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import { scheduleAutoCompile, setAutoCompileRunner, resetAutoCompileDebounce } from '../../compileHook';

test('scheduleAutoCompile calls runner once when debounced', async () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'knb-auto-'));
  let calls = 0;

  setAutoCompileRunner((kbRoot?: string) => {
    calls += 1;
    // create marker file
    fs.writeFileSync(path.join(tmp, 'AUTO_COMPILED'), 'ok');
  });

  // Trigger multiple times in quick succession
  scheduleAutoCompile(tmp);
  scheduleAutoCompile(tmp);
  scheduleAutoCompile(tmp);

  // Wait long enough for debounce to trigger
  await new Promise(resolve => setTimeout(resolve, 500));

  expect(calls).toBe(1);
  expect(fs.existsSync(path.join(tmp, 'AUTO_COMPILED'))).toBeTruthy();

  // Cleanup
  resetAutoCompileDebounce();
  fs.rmSync(tmp, { recursive: true, force: true });
});
