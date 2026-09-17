export const $ = s => document.querySelector(s);
export const el = (tag,text,cls) => {const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
export function safeUrl(url){if(!url||!url.trim())return '';try{const u=new URL(url.startsWith('/') ? '.'+url : url,new URL('.',import.meta.url));return ['https:','http:'].includes(u.protocol)?u.href:'';}catch{return '';}}
export let profile;
const fallback={loadError:'Unable to load content. Please refresh and try again.'};
export const t = key => profile?.ui[key] || fallback[key] || key;
export async function loadJson(path){
 let r;try{r=await fetch(new URL(path,import.meta.url));}catch{throw Error(t('loadError'));}
 if(!r.ok)throw Error(t('loadError'));
 return r.json();
}
function saved(key,fallback){try{return localStorage.getItem(key)||fallback;}catch{return fallback;}}
const lang=new URLSearchParams(location.search).get('lang') || saved('language','en');
export const ready=(async()=>{
 profile=await loadJson('./data/'+(['en','zh'].includes(lang)?lang:'en')+'.json');
 document.documentElement.lang=profile.lang==='zh'?'zh-CN':'en';
 document.querySelectorAll('[data-i18n]').forEach(n=>n.textContent=t(n.dataset.i18n));
 document.querySelectorAll('[data-placeholder]').forEach(n=>n.placeholder=t(n.dataset.placeholder));
 document.querySelectorAll('[data-label]').forEach(n=>n.setAttribute('aria-label',t(n.dataset.label)));
 document.querySelectorAll('[data-title]').forEach(n=>n.title=t(n.dataset.title));
 document.querySelectorAll('[data-home]').forEach(n=>n.href='./?lang='+profile.lang);
 const language=$('#language');if(language){language.textContent=profile.lang==='en'?'中':'EN';language.setAttribute('aria-label',t('language'));language.onclick=()=>{const next=profile.lang==='en'?'zh':'en';try{localStorage.setItem('language',next);}catch{}const u=new URL(location.href);u.searchParams.set('lang',next);location.assign(u.href);};}
 const theme=$('#theme');function setTheme(sky){document.body.classList.toggle('sky',sky);if(theme){theme.textContent=sky?'☾':'☼';theme.setAttribute('aria-label',t(sky?'themeWarm':'themeSky'));}try{localStorage.setItem('theme',sky?'sky':'warm');}catch{}}
 setTheme(saved('theme','warm')==='sky');if(theme)theme.onclick=()=>setTheme(!document.body.classList.contains('sky'));
 return profile;
})();
