import { createServer } from 'node:http';
import { readFileSync } from 'node:fs';
const args=process.argv.slice(2); const at=args.indexOf('--port');
const port=Number(at>=0?args[at+1]:process.env.PORT||5173);
const html=()=>readFileSync(new URL(args.includes('--dist')?'../dist/index.html':'../index.html',import.meta.url));
createServer((req,res)=>{const p=new URL(req.url,'http://localhost').pathname;if(p!=='/'&&p!=='/index.html'&&p!=='/preview.html'){res.writeHead(404);res.end('Not found');return;}try{res.writeHead(200,{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'});res.end(html());}catch(e){res.writeHead(500);res.end('Run npm run build first for the production preview.');}}).listen(port,'0.0.0.0',()=>console.log(`Birthday site: http://localhost:${port}`));
