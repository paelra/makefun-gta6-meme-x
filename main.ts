// Copy POST.json to /output, where the gate reads it; the entry itself is the X post.
import { copyFile, mkdir } from 'node:fs/promises';
import { join } from 'node:path';

async function main(): Promise<void> {
  const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

  try {
    await mkdir(outputDir, { recursive: true });
    await copyFile(join(botDir, 'POST.json'), join(outputDir, 'POST.json'));
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
}

void main();
