/* Shared 3D satellite renderer for live canvases and profile GIF exports. */
(function(root){
'use strict';
const dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),sub=(a,b)=>a.map((v,i)=>v-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],unit=a=>{const n=Math.hypot(...a)||1;return a.map(v=>v/n);};
function render(ctx,w,h,angle,zoom=1,tilt=.4){
 const faces=[],scale=Math.min(w/4.7,h/3.1)*zoom;
 const transform=([x,y,z])=>{const a=x*Math.cos(angle)-z*Math.sin(angle),b=x*Math.sin(angle)+z*Math.cos(angle);return[a,y*Math.cos(tilt)-b*Math.sin(tilt),y*Math.sin(tilt)+b*Math.cos(tilt)];};
 const project=p=>{const f=7/(7+p[2]);return[w/2+p[0]*scale*f,h*.53+p[1]*scale*f];};
 function face(points,color,edge='#9aa9aa',width=.65){const v=points.map(transform);faces.push({v,color,edge,width,z:v.reduce((s,p)=>s+p[2],0)/v.length});}
 function box(cx,cy,cz,sx,sy,sz,color,open=false){const v=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]].map(p=>[cx+p[0]*sx/2,cy+p[1]*sy/2,cz+p[2]*sz/2]);for(const f of [[0,3,2,1],[4,5,6,7],[0,1,5,4],[3,7,6,2],[1,2,6,5],[0,4,7,3]]){if(open&&(f.join()==="0,3,2,1"||f.join()==="4,5,6,7"))continue;face(f.map(i=>v[i]),color);}}
 // Extruded solar arrays, with individual cells on both sides.
 for(const side of [-1,1]){
 box(side*.52,0,0,.42,.075,.09,[126,139,143]);
 box(side*1.25,0,0,1.18,.79,.06,[55,67,73],true);
 for(const z of [-.034,.034])for(let x=0;x<6;x++)for(let y=0;y<4;y++){
  const cx=side*(.69+x*.19),cy=-.355+y*.19;
  const p=[[cx-.085,cy,z],[cx+.085,cy,z],[cx+.085,cy+.164,z],[cx-.085,cy+.164,z]];
  face(z<0?p.reverse():p,[35,72,89],'#7c969c',.35);
 }
 }
 // Layered metallic bus, chamfer-like corner rails and instrument package.
 box(0,0,0,.7,.83,.64,[159,165,160]);box(0,-.43,0,.76,.055,.7,[201,207,199]);box(0,.43,0,.76,.055,.7,[101,115,114]);
 for(const x of [-.35,.35])for(const z of [-.32,.32])box(x,0,z,.035,.85,.035,[207,214,206]);
 box(0,.04,-.36,.38,.43,.1,[87,98,102]);box(0,-.08,-.43,.15,.15,.06,[20,36,44]);
 // A shallow parabolic dish with actual curved 3D geometry.
 box(0,-.58,0,.045,.27,.045,[182,193,192]);
 const n=24,rings=5;
 for(let j=0;j<rings;j++)for(let i=0;i<n;i++){
  const vertex=(r,a)=>[Math.cos(a)*r,-.82+.32*r*r,Math.sin(a)*r];
  const r0=j/rings*.36,r1=(j+1)/rings*.36,a=i/n*Math.PI*2,b=(i+1)/n*Math.PI*2;
  face([vertex(r0,a),vertex(r1,a),vertex(r1,b),vertex(r0,b)],[177,192,193],j===rings-1?'#d0dcda':'#829496',.3);
 }
 box(0,-.91,0,.018,.26,.018,[204,218,215]);
 ctx.clearRect(0,0,w,h);
 // Understated orbital guide behind the shaded model.
 ctx.save();ctx.strokeStyle='#34413c';ctx.lineWidth=.65;ctx.setLineDash([2,7]);ctx.beginPath();ctx.ellipse(w/2,h*.56,scale*1.95,scale*.52,-.2,0,Math.PI*2);ctx.stroke();ctx.restore();
 const light=unit([-.6,-.8,-1]);
 faces.sort((a,b)=>b.z-a.z);
 for(const f of faces){const normal=unit(cross(sub(f.v[1],f.v[0]),sub(f.v[2],f.v[0]))),lambert=Math.max(0,dot(normal,light)),shade=.34+.66*lambert;const center=f.v.reduce((a,p)=>a.map((v,i)=>v+p[i]/f.v.length),[0,0,7]);if(dot(normal,center)>=0)continue;ctx.beginPath();f.v.forEach((p,i)=>{const q=project(p);i?ctx.lineTo(...q):ctx.moveTo(...q);});ctx.closePath();ctx.fillStyle=`rgb(${f.color.map(c=>Math.round(c*shade)).join(',')})`;ctx.fill();ctx.strokeStyle=f.edge;ctx.lineWidth=f.width;ctx.stroke();}
}
if(typeof module!=='undefined')module.exports={render};else root.Satellite3D={render};
})(typeof globalThis!=='undefined'?globalThis:this);
