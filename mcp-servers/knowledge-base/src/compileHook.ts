import { exec } from 'child_process';
import * as path from 'path';

let timer: NodeJS.Timeout | null = null;
let debounceMs = Number(process.env.KNB_AUTO_COMPILE_DEBOUNCE_MS) || 250;

// Runner can be replaced in tests
let runner: (kbRoot?: string) => void = (kbRoot?: string) => {
  // Default: run the npm compile script in repo root
  exec('npm run compile', { cwd: path.join(__dirname, '..', '..', '..') }, (err, stdout, stderr) => {
    if (err) {
      console.error('Auto-compile failed:', err);
    } else {
      console.log('Auto-compile completed');
    }
  });
};

export function setAutoCompileRunner(r: (kbRoot?: string) => void) {
  runner = r;
}

export function scheduleAutoCompile(kbRoot?: string) {
  if (timer) {
    clearTimeout(timer);
  }

  timer = setTimeout(() => {
    try {
      runner(kbRoot);
    } catch (err) {
      console.error('Auto-compile runner error:', err);
    }
    timer = null;
  }, debounceMs);
}

export function resetAutoCompileDebounce() {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
}
