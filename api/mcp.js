import {VERSION,THEMES,SCENE_TYPES,designSpec,htmlTemplate,createScene,colorContrast,sanitizeTitle} from '../public/js/engine.mjs';

const TOOL_LIST=[
 {name:'forge_capabilities',description:'Report actual remote capabilities and limits. Works in ChatGPT on mobile and desktop when this HTTPS MCP endpoint is connected.',inputSchema:{type:'object',properties:{},additionalProperties:false}},
 {name:'forge_design_spec',description:'Generate an actionable, editable responsive UI design specification with tokens. Does not claim screenshot parity.',inputSchema:{type:'object',properties:{title:{type:'string',maxLength:100},theme:{type:'string',enum:Object.keys(THEMES)}},additionalProperties:false}},
 {name:'forge_ui_html',description:'Generate a standalone interactive responsive HTML dashboard (real working UI). Returns source text; not an Android APK.',inputSchema:{type:'object',properties:{title:{type:'string',maxLength:100},theme:{type:'string',enum:Object.keys(THEMES)}},additionalProperties:false}},
 {name:'forge_3d_scene_plan',description:'Create real deterministic geometry scene plan for an illustrative blockout, exportable to GLB via the PWA. NOT a photoreal model.',inputSchema:{type:'object',properties:{type:{type:'string',enum:SCENE_TYPES},seed:{type:'integer',minimum:0,maximum:1000000}},additionalProperties:false}},
 {name:'forge_contrast',description:'Compute WCAG relative luminance contrast between two hex colors.',inputSchema:{type:'object',properties:{foreground:{type:'string',pattern:'^#[0-9a-fA-F]{6}$'},background:{type:'string',pattern:'^#[0-9a-fA-F]{6}$'}},required:['foreground','background'],additionalProperties:false}}
];
const allowedOrigin=(origin,host)=>{if(!origin)return true;try{const u=new URL(origin);const h=host?.split(':')[0]?.toLowerCase();return u.protocol==='https:'&&((u.hostname.toLowerCase()===h)||u.hostname.toLowerCase()==='chatgpt.com'||u.hostname.toLowerCase().endsWith('.chatgpt.com'));}catch{return false}};
function rpcError(id,code,message){return {jsonrpc:'2.0',id,error:{code,message}}}
function doCall(name,a){
 if(a===null||typeof a!=='object'||Array.isArray(a))throw new Error('Tool arguments must be an object');
 if(Object.keys(a).length>12)throw new Error('Too many tool arguments');
 if(name==='forge_capabilities')return {version:VERSION,transport:'streamable-http/stateless',mobile:true,desktop:true,web_pwa:true,local_executor_optional:true,tools:TOOL_LIST.map(t=>t.name),continuous_background_jobs:false,subscription_or_cloud_ai:false,photorealism:false,hosting:'request-driven; availability depends on hosting provider',notes:'MCP tools are public, stateless and intentionally cannot modify user files or execute commands.'};
 if(name==='forge_design_spec'||name==='forge_ui_html'){
  const title=sanitizeTitle(a.title??'New Studio'),theme=a.theme??'obsidian';if(!Object.hasOwn(THEMES,theme))throw Error('Unsupported theme');
  return name==='forge_design_spec'?designSpec({title,theme}):{kind:'interactive_html',title,html:htmlTemplate({title,theme}),instruction:'Save the HTML to a file or use the cross-platform PWA Export HTML button.'};
 }
 if(name==='forge_3d_scene_plan'){
  const type=a.type??'city',seed=a.seed??42;if(!SCENE_TYPES.includes(type))throw Error('Unsupported scene type');if(!Number.isInteger(seed)||seed<0||seed>1e6)throw Error('Invalid seed');return createScene(type,seed);
 }
 if(name==='forge_contrast'){if(!/^#[0-9a-fA-F]{6}$/.test(a.foreground??'')||!/^#[0-9a-fA-F]{6}$/.test(a.background??''))throw Error('Provide two six-digit hex colors');const ratio=colorContrast(a.foreground,a.background);return {contrastRatio:ratio,wcagAA_normalText:ratio>=4.5,wcagAA_largeText:ratio>=3};}
 throw new Error('Unknown tool');
}
export function handleRpc(msg){
 if(!msg||typeof msg!=='object'||Array.isArray(msg)||msg.jsonrpc!=='2.0'||typeof msg.method!=='string')return rpcError(msg?.id??null,-32600,'Invalid Request');
 if(!Object.hasOwn(msg,'id'))return null;
 if(typeof msg.id!=='number'&&typeof msg.id!=='string')return rpcError(null,-32600,'Invalid id');
 const id=msg.id,params=msg.params??{};
 if(!params||typeof params!=='object'||Array.isArray(params))return rpcError(id,-32602,'Invalid params');
 if(msg.method==='initialize')return {jsonrpc:'2.0',id,result:{protocolVersion:'2025-11-25',capabilities:{tools:{listChanged:false}},serverInfo:{name:'vibe-visual-forge-cloud',version:VERSION}}};
 if(msg.method==='ping')return {jsonrpc:'2.0',id,result:{}};
 if(msg.method==='tools/list')return {jsonrpc:'2.0',id,result:{tools:TOOL_LIST}};
 if(msg.method==='tools/call'){
   if(typeof params.name!=='string')return rpcError(id,-32602,'Missing tool name');
   try{const output=doCall(params.name,params.arguments??{});return {jsonrpc:'2.0',id,result:{content:[{type:'text',text:JSON.stringify(output)}],structuredContent:output,isError:false}};}
   catch(e){return {jsonrpc:'2.0',id,result:{content:[{type:'text',text:e.message}],isError:true}};}
 }
 return rpcError(id,-32601,'Method not found');
}
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');res.setHeader('X-Content-Type-Options','nosniff');res.setHeader('Vary','Origin');
 if(!allowedOrigin(req.headers.origin,req.headers.host)){res.statusCode=403;return res.json({error:'Forbidden origin'});}
 if(req.method==='OPTIONS'){res.setHeader('Allow','POST, OPTIONS');res.statusCode=204;return res.end();}
 if(req.method!=='POST'){res.setHeader('Allow','POST, OPTIONS');res.statusCode=405;return res.json({error:'POST required for stateless MCP'});}
 const accept=req.headers.accept??'';if(!accept.includes('application/json')||!accept.includes('text/event-stream')){res.statusCode=406;return res.json({error:'MCP client must Accept application/json and text/event-stream'});}
 let data=req.body;if(typeof data==='string'){if(data.length>65_536){res.statusCode=413;return res.json({error:'Payload too large'});}try{data=JSON.parse(data)}catch{data=null;}}
 if(typeof data!=='object'||data===null){res.statusCode=400;return res.json(rpcError(null,-32700,'Parse error'));}
 if(Buffer.byteLength(JSON.stringify(data))>65_536){res.statusCode=413;return res.json({error:'Payload too large'});}
 if(Array.isArray(data)){res.statusCode=400;return res.json(rpcError(null,-32600,'Batch requests not supported'));}
 const result=handleRpc(data);if(result===null){res.statusCode=202;return res.end();}
 return res.status(200).json(result);
}
