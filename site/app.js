'use strict';
const $ = selector => document.querySelector(selector);
const preference = matchMedia('(prefers-reduced-motion: reduce)');
let reduced = preference.matches;
const toggle = $('#motion-toggle');
function setMotion(value) { reduced = value; document.documentElement.classList.toggle('reduced-motion', reduced); document.documentElement.classList.toggle('motion-enabled', !reduced); toggle.textContent = reduced ? 'Enable motion' : 'Reduce motion'; toggle.setAttribute('aria-pressed', String(reduced)); }
setMotion(reduced); toggle.addEventListener('click', () => setMotion(!reduced)); preference.addEventListener('change', e => setMotion(e.matches));
$('#copyright-year').textContent = new Date().getFullYear();
const clamp = (value, min=0, max=1) => Math.min(max, Math.max(min, value));
const smooth = value => { value=clamp(value); return value*value*(3-2*value); };
const rand = seed => { const n = Math.sin(seed*127.1+311.7)*43758.5453; return n-Math.floor(n); };

class Surface {
  constructor(canvas) { this.canvas=canvas; this.ctx=canvas.getContext('2d'); this.width=0; this.height=0; this.visible=true; new ResizeObserver(()=>this.resize()).observe(canvas); this.resize(); }
  resize(){ const rect=this.canvas.getBoundingClientRect(), dpr=Math.min(devicePixelRatio||1,2); this.dpr=dpr; this.width=rect.width; this.height=rect.height; this.canvas.width=Math.round(rect.width*dpr); this.canvas.height=Math.round(rect.height*dpr); this.ctx.setTransform(dpr,0,0,dpr,0,0); this.ctx.imageSmoothingEnabled=false; }
  clear(){this.ctx.clearRect(0,0,this.width,this.height);}
}
const research=new Surface($('#research-satellite'));
const surfaces=[research];
if ('IntersectionObserver' in window) { const observer=new IntersectionObserver(entries=>entries.forEach(e=>{const s=surfaces.find(s=>s.canvas===e.target);if(s)s.visible=e.isIntersecting;}),{rootMargin:'100px'}); surfaces.forEach(s=>observer.observe(s.canvas)); }

// Use the same 3D blueprint line geometry as the animated GitHub profile exports.
function drawSatellite(surface,angle,zoom=1,tilt=.4){Satellite3D.render(surface.ctx,surface.width,surface.height,angle,zoom,tilt);}
let elapsed=0,previous=0;
document.addEventListener('visibilitychange',()=>{previous=0;});
function frame(now){const dt=previous?Math.min((now-previous)/1000,.04):0;previous=now;if(!document.hidden){if(!reduced)elapsed+=dt;if(research.visible)drawSatellite(research,reduced ? .6 : elapsed*.35+.6,.92,.4);}requestAnimationFrame(frame);}
requestAnimationFrame(frame);

function dayText(day){return new Date(day.date+'T12:00:00Z').toLocaleDateString(undefined,{year:'numeric',month:'long',day:'numeric',timeZone:'UTC'});}
function activityURL(date){return `https://github.com/shawkialaddin?tab=overview&from=${date}&to=${date}`;}
function renderCalendar(days,year){
 const grid=$('#days'),months=$('#months');grid.replaceChildren();months.replaceChildren();$('#day-detail').textContent='Select a day to inspect activity.';
 const byDate=new Map(days.map(d=>[d.date,d]));const first=new Date(Date.UTC(year,0,1));const offset=first.getUTCDay();const last=new Date(Date.UTC(year,11,31));const total=Math.round((last-first)/86400000)+1;const columns=Math.ceil((offset+total)/7);
 grid.style.gridTemplateColumns=`repeat(${columns},minmax(8px,1fr))`;months.style.gridTemplateColumns=`repeat(${columns},minmax(8px,1fr))`;
 for(let m=0;m<12;m++){const date=new Date(Date.UTC(year,m,1)),day=Math.round((date-first)/86400000);const label=document.createElement('span');label.textContent=date.toLocaleDateString('en',{month:'short',timeZone:'UTC'});label.style.gridColumn=String(Math.floor((offset+day)/7)+1);months.append(label);}
 const today=new Date().toISOString().slice(0,10);
 for(let n=0;n<columns*7;n++){
  const date=new Date(first);date.setUTCDate(1+n-offset);const dateString=date.toISOString().slice(0,10);
  if(date.getUTCFullYear()!==Number(year)){const blank=document.createElement('span');blank.className='empty';grid.append(blank);continue;}
  const day=byDate.get(dateString),button=document.createElement('button');button.type='button';button.className='day';button.dataset.level=String(day?.level??0);
  const future=dateString>today;button.disabled=future||!day;const label=future?`${dateString}: future date`:day?`${dayText(day)}: ${day.count} contribution${day.count===1?'':'s'}`:`${dateString}: data unavailable`;
  button.setAttribute('aria-label',label);button.setAttribute('aria-pressed','false');button.title=label;
  button.addEventListener('click',()=>{grid.querySelector('[aria-pressed="true"]')?.setAttribute('aria-pressed','false');button.setAttribute('aria-pressed','true');const details=$('#day-detail');details.replaceChildren(document.createTextNode(label+' '));const link=document.createElement('a');link.href=activityURL(day.date);link.target='_blank';link.rel='noopener noreferrer';link.textContent='View activity ↗';details.append(link);});grid.append(button);
 }
 // Arrow keys follow the contribution calendar's seven-row geometry.
 grid.onkeydown=e=>{const moves={ArrowUp:-1,ArrowDown:1,ArrowLeft:-7,ArrowRight:7};if(!(e.key in moves)||!e.target.classList.contains('day'))return;e.preventDefault();const cells=[...grid.children];let next=cells.indexOf(e.target)+moves[e.key];while(next>=0&&next<cells.length){const cell=cells[next];if(cell.tagName==='BUTTON'&&!cell.disabled){cell.focus();break;}next+=moves[e.key];}};
 const visible=days.filter(d=>d.date<=today),sum=visible.reduce((total,d)=>total+d.count,0);$('#activity-summary').textContent=`${sum.toLocaleString()} contribution${sum===1?'':'s'} in ${year} · Public GitHub calendar`;
}
async function loadActivity(){
 try{const response=await fetch('activity.json',{cache:'no-cache'});if(!response.ok)throw Error('Activity data unavailable');const payload=await response.json();if(payload.username!=='shawkialaddin'||!payload.years)throw Error('Invalid contribution payload');const years=Object.keys(payload.years).filter(y=>/^\d{4}$/.test(y)&&Array.isArray(payload.years[y])).sort((a,b)=>b-a);if(!years.length)throw Error('Empty contribution payload');const year=$('#year');year.replaceChildren();for(const y of years){const option=document.createElement('option');option.value=y;option.textContent=y;year.append(option);}year.disabled=false;renderCalendar(payload.years[years[0]],years[0]);year.addEventListener('change',()=>renderCalendar(payload.years[year.value],year.value));const updated=new Date(payload.updatedAt);$('#updated').textContent=`Snapshot updated ${updated.toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'})}. Contributions, not only commits.`;}
 catch(error){$('#activity-summary').textContent='Activity is unavailable here. View the current calendar on GitHub.';$('#year').replaceChildren(new Option('Unavailable'));$('#day-detail').textContent='';console.warn('Could not load public contribution snapshot:',error.message);}
}
loadActivity();
