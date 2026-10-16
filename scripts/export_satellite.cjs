// npm install @napi-rs/canvas, then run from the repository root.
const fs=require('fs'),os=require('os'),path=require('path');
const {createCanvas,loadImage,GlobalFonts}=require('@napi-rs/canvas');
const {render}=require('../site/satellite.js');
GlobalFonts.registerFromPath('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','Arial');
const output=path.join(os.tmpdir(),'satellite-profile-frames');fs.mkdirSync(output,{recursive:true});
(async()=>{
 for(const [name,w,h,x,y,sw,sh] of [['research',1200,358,762,67,418,257],['experiments',1200,342,641,83,510,202]]){
  let svg=fs.readFileSync(`assets/profile-${name}.svg`,'utf8');
  // Remove the existing nested wireframe group, retaining section typography.
  const start=svg.indexOf('<g transform="translate(');let depth=0,end=start;
  if(start>=0){const tags=/<g\b[^>]*>|<\/g>/g;tags.lastIndex=start;for(let m;(m=tags.exec(svg));){depth+=m[0].startsWith('</')?-1:1;if(depth===0){end=tags.lastIndex;break;}}svg=svg.slice(0,start)+svg.slice(end);}
  svg=svg.replace(/<text /g,'<text font-family="Arial" ');
  const base=await loadImage(Buffer.from(svg));const c=createCanvas(w,h),ctx=c.getContext('2d'),model=createCanvas(sw,sh),mc=model.getContext('2d');
  for(let f=0;f<96;f++){ctx.clearRect(0,0,w,h);ctx.drawImage(base,0,0);render(mc,sw,sh,f/96*Math.PI*2+.6,1,.4);ctx.drawImage(model,x,y);fs.writeFileSync(path.join(output,`${name}-${String(f).padStart(3,'0')}.png`),c.toBuffer('image/png'));}
 }
 console.log(output);
})();
