/* Rotating 3D blueprint: projected line geometry, without surface fills. */
(function(root){
'use strict';
function render(ctx,w,h,angle,zoom=1,tilt=.4){
 const scale=Math.min(w/4.7,h/3.1)*zoom,lines=[];
 const transform=([x,y,z])=>{const a=x*Math.cos(angle)-z*Math.sin(angle),b=x*Math.sin(angle)+z*Math.cos(angle);return[a,y*Math.cos(tilt)-b*Math.sin(tilt),y*Math.sin(tilt)+b*Math.cos(tilt)];};
 const project=p=>{const f=7/(7+p[2]);return[w/2+p[0]*scale*f,h*.53+p[1]*scale*f];};
 function line(points,weight=1,dashed=false){const v=points.map(transform);lines.push({v,weight,dashed,z:v.reduce((s,p)=>s+p[2],0)/v.length});}
 function box(cx,cy,cz,sx,sy,sz,weight=1){
  const v=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]].map(p=>[cx+p[0]*sx/2,cy+p[1]*sy/2,cz+p[2]*sz/2]);
  for(const [a,b] of [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]])line([v[a],v[b]],weight);
 }
 // Centre lines and orbital construction circles remain in the rotating 3D space.
 line([[-2.03,0,0],[2.03,0,0]],.27,true);line([[0,-1.2,0],[0,.98,0]],.27,true);line([[0,0,-1.1],[0,0,1.1]],.27,true);
 const orbit=Array.from({length:97},(_,i)=>{const t=i/96*Math.PI*2;return[Math.cos(t)*1.98,.12,Math.sin(t)*1.1];});line(orbit,.2,true);
 box(0,0,0,.7,.83,.64,1.15);
 box(0,-.43,0,.74,.035,.68,.65);box(0,.43,0,.74,.035,.68,.65);
 box(0,.04,-.34,.34,.4,.04,.65);
 for(const side of [-1,1]){
  line([[side*.35,0,0],[side*.66,0,0]],1);
  box(side*1.25,0,0,1.18,.79,.035,.95);
  for(let i=1;i<6;i++){const x=side*(.66+i*1.18/6);line([[x,-.395,-.02],[x,.395,-.02]],.52);}
  for(let j=1;j<4;j++){const y=-.395+j*.79/4;line([[side*.66,y,-.02],[side*1.84,y,-.02]],.52);}
  // Offset dimension guide and extension marks, without invented measurements.
  line([[side*.66,.52,0],[side*1.84,.52,0]],.32);
  for(const x of [side*.66,side*1.84]){line([[x,.42,0],[x,.59,0]],.32);line([[x-.035,.55,0],[x+.035,.49,0]],.5);}
 }
 line([[0,-.445,0],[0,-.82,0]],.9);
 // Sparse parabolic dish rings and spokes preserve the technical drawing style.
 const dish=(r,t)=>[Math.cos(t)*r,-.82+.55*r*r,Math.sin(t)*r];
 for(const r of [.18,.36])line(Array.from({length:49},(_,i)=>dish(r,i/48*Math.PI*2)),r===.36?.9:.4);
 for(let i=0;i<8;i++)line([dish(0,0),dish(.18,i/8*Math.PI*2),dish(.36,i/8*Math.PI*2)],.4);
 line([[0,-.82,0],[0,-1.055,0]],.8);
 ctx.clearRect(0,0,w,h);ctx.save();ctx.lineJoin='round';ctx.lineCap='round';
 lines.sort((a,b)=>b.z-a.z);
 for(const l of lines){const depth=Math.max(.32,Math.min(1,.75-l.z*.22));ctx.strokeStyle=`rgba(210,219,216,${depth*l.weight})`;ctx.lineWidth=l.weight>.8?.85:.55;ctx.setLineDash(l.dashed?[1.5,5]:[]);ctx.beginPath();l.v.forEach((p,i)=>{const q=project(p);i?ctx.lineTo(...q):ctx.moveTo(...q);});ctx.stroke();}
 ctx.restore();
}
if(typeof module!=='undefined')module.exports={render};else root.Satellite3D={render};
})(typeof globalThis!=='undefined'?globalThis:this);
