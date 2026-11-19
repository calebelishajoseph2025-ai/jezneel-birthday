import { mkdirSync, copyFileSync, readFileSync } from 'node:fs';
const root = new URL('../', import.meta.url);
const index = new URL('index.html', root);
if (!readFileSync(index).equals(readFileSync(new URL('preview.html', root)))) throw new Error('index.html and preview.html differ');
mkdirSync(new URL('dist/', root), {recursive:true});
copyFileSync(index, new URL('dist/index.html', root));
console.log('Built dist/index.html — byte-identical to preview.html');
