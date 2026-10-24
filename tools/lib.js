/* shared toolkit for Dar Al Athari ads: everything is a pure function of t */
var K=3, $=function(i){return document.getElementById(i)};
function cl(x){return x<0?0:x>1?1:x} function sm(x){x=cl(x);return x*x*(3-2*x)} function oc(x){x=cl(x);return 1-Math.pow(1-x,3)}
function ic(x){x=cl(x);return x*x*x} function io(x){x=cl(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2} function lerp(a,b,p){return a+(b-a)*p}
function ob(x){x=cl(x);var c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}
function os(x){x=cl(x);var c=1.0;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}
function win(t,a,b,fi,fo){return sm((t-a)/(fi||.4))*(1-sm((t-b)/(fo||.4)))}
var _seed=7; function rnd(){_seed=(_seed*16807)%2147483647;return (_seed-1)/2147483646}
function el(cls,css,parent,html,tag){var d=document.createElement(tag||'div');if(cls)d.className=cls;d.style.cssText=css||'';if(html)d.innerHTML=html;parent.appendChild(d);return d}
function keyed(K_,t){var a=K_[0],b=K_[K_.length-1];if(t<=a[0])return a.slice(1);if(t>=b[0])return b.slice(1);
  for(var i=0;i<K_.length-1;i++)if(t>=K_[i][0]&&t<=K_[i+1][0]){a=K_[i];b=K_[i+1];break}
  var p=io((t-a[0])/(b[0]-a[0])),o=[];for(var j=1;j<a.length;j++)o.push(lerp(a[j],b[j],p));return o}

/* the books I have photos of */
var SPEC={
 tw:{W:200,H:288,D:40, front:'assets/k_tw_front.jpg', back:null, spine:null, col:'#1d4630', rtl:false,
     en:'Kitab at-Tawhid', ar:'كتاب التوحيد', by:'Shaykh Muhammad ibn Abd al-Wahhab', lang:'ENGLISH'},
 ken:{W:200,H:300,D:32, front:'assets/k_en_front.jpg', back:null, spine:'assets/k_en_spine.jpg', col:'#efe7da', rtl:false,
     en:'The Book of Knowledge', ar:'كتاب العلم', by:'Shaykh Ibn Uthaymeen', lang:'ENGLISH'},
 een:{W:200,H:300,D:58, front:'assets/e_front.jpg', back:'assets/e_back.jpg', spine:'assets/e_spine.jpg', col:'#1f4a47', rtl:false,
     en:'The Disease and the Cure', ar:'الداء والدواء', by:'Imam Ibn al-Qayyim', lang:'ENGLISH'},
 kar:{W:210,H:300,D:34, front:'assets/k_ar_front.jpg', back:'assets/k_ar_back.jpg', spine:'assets/k_ar_spine.jpg', col:'#9a4126', rtl:true,
     en:"Kitab al-'Ilm", ar:'كتاب العلم', by:'Shaykh Ibn Uthaymeen', lang:'ARABIC'},
 aar:{W:216,H:310,D:50, front:'assets/a_front.jpg', back:'assets/a_back.jpg', spine:'assets/a_spine.jpg', col:'#171717', rtl:true,
     en:"Ad-Da' wa ad-Dawa'", ar:'الداء والدواء', by:'Imam Ibn al-Qayyim', lang:'ARABIC'},
 sth:{W:210,H:294,D:15, front:'assets/sth_front.jpg', back:'assets/sth_back.jpg', spine:'assets/sth_spine.jpg', col:'#151a2a', rtl:true,
     en:'Sharh Thalathat al-Usul', ar:'شرح ثلاثة الأصول', by:'Shaykh Muhammad ibn Salih al-Uthaymeen', lang:'ARABIC'},
 ft:{W:210,H:300,D:43, front:'assets/ft_front.jpg', back:'assets/ft_back.jpg', spine:'assets/ft_spine.jpg', col:'#e8692a', rtl:false,
     en:'Five Foundational Treatises of Creed', ar:'التعليقات البهية على الرسائل العقدية', by:'Shaykh Ahmad bin Yahya al-Najmi', lang:'ENGLISH'},
 ts:{W:200,H:301,D:57, front:'assets/ts_front.jpg', back:'assets/ts_back.jpg', spine:'assets/ts_spine.jpg', col:'#1f4a3a', rtl:true,
     en:"Tafsir as-Sa'di", ar:'تيسير الكريم الرحمن في تفسير كلام المنان', by:"Shaykh Abd ar-Rahman ibn Nasir as-Sa'di", lang:'ARABIC'},
 fq1:{W:200,H:294,D:41, front:'assets/fq_v1_front.jpg', back:'assets/fq_v1_back.jpg', spine:'assets/fq_v1_spine.jpg', col:'#2a3fb0', rtl:false,
     en:"Fiqh According to the Qur'an & Sunnah, Vol. 1", ar:'اللباب في فقه السنة والكتاب', by:'Muhammad Subhi bin Hasan Hallaq', lang:'ENGLISH'},
 fq2:{W:200,H:294,D:41, front:'assets/fq_v2_front.jpg', back:'assets/fq_v2_back.jpg', spine:'assets/fq_v2_spine.jpg', col:'#2a3fb0', rtl:false,
     en:"Fiqh According to the Qur'an & Sunnah, Vol. 2", ar:'اللباب في فقه السنة والكتاب', by:'Muhammad Subhi bin Hasan Hallaq', lang:'ENGLISH'},
 bi:{W:195,H:300,D:21, front:'assets/bi_front.jpg', back:'assets/bi_back.jpg', spine:'assets/bi_spine.jpg', col:'#efece4', rtl:false,
     en:'The Beliefs of the Imams of the Sunnah', ar:'', by:'Shaykh, Dr. Khalid Al-Dhafiri', lang:'ENGLISH'},
 pi:{W:188,H:300,D:23, front:'assets/pi_front.jpg', back:'assets/pi_back.jpg', spine:'assets/pi_spine.jpg', col:'#174a44', rtl:false,
     en:'The Pillars of Islam & Iman', ar:'أركان الإسلام والإيمان', by:'Sheikh Muhammad bin Jamil Zeno', lang:'ENGLISH'},
 ks:{W:209,H:300,D:19, front:'assets/ks_front.jpg', back:'assets/ks_back.jpg', spine:'assets/ks_spine.jpg', col:'#161a2a', rtl:true,
     en:'Sharh Kashf ash-Shubuhat, followed by Sharh al-Usul as-Sittah', ar:'شرح كشف الشبهات ويليه شرح الأصول الستة', by:'Shaykh Muhammad ibn Salih al-Uthaymeen', lang:'ARABIC'},
 fw:{W:203,H:300,D:25, front:'assets/fw_front.jpg', back:'assets/fw_back.jpg', spine:'assets/fw_spine.jpg', col:'#1a1a1a', rtl:true,
     en:"Al-Fawa'id", ar:'الفوائد', by:'Imam Ibn Qayyim al-Jawziyyah', lang:'ARABIC'}};
var GREEN_SPINE='background:linear-gradient(to bottom,transparent 7%,#c9a24a 7%,#c9a24a 7.6%,transparent 7.6%,transparent 92.4%,#c9a24a 92.4%,#c9a24a 93%,transparent 93%),linear-gradient(to right,#143524,#1f4d35 45%,#173c29);';

/* a 3D book, faces laid out at K times size */
function makeBook(parent,key){
  var b=Object.assign({key:key},SPEC[key]);
  var W=b.W*K,H=b.H*K,D=b.D*K,dir=b.rtl?-1:1,root=el('', 'left:0;top:0;width:0;height:0',parent),f={},rect='left:'+(-W/2)+'px;top:'+(-H/2)+'px;width:'+W+'px;height:'+H+'px;';
  function img(u,c){return u?'background-image:url('+u+');':'background:'+c+';'}
  f.front=el('face',rect+img(b.front)+'transform:translateZ('+(D/2)+'px)',root);
  f.back=el('face',rect+img(b.back,b.col)+'transform:translateZ('+(-D/2)+'px) rotateY(180deg)',root);
  f.spine=el('face','left:'+(-dir*W/2-D/2)+'px;top:'+(-H/2)+'px;width:'+D+'px;height:'+H+'px;'+(b.spine?img(b.spine):GREEN_SPINE)+'transform:rotateY('+(-dir*90)+'deg)',root);
  f.fore=el('face paperx','left:'+(dir*(W/2-3)-D/2)+'px;top:'+(-H/2+3)+'px;width:'+D+'px;height:'+(H-6)+'px;transform:rotateY('+(dir*90)+'deg)',root);
  f.top=el('face papery','left:'+(-W/2+3)+'px;top:'+(-H/2+3-D/2)+'px;width:'+(W-6)+'px;height:'+D+'px;transform:rotateX(90deg)',root);
  f.bot=el('face papery','left:'+(-W/2+3)+'px;top:'+(H/2-3-D/2)+'px;width:'+(W-6)+'px;height:'+D+'px;transform:rotateX(-90deg)',root);
  for(var k in f){var o=document.createElement('i');o.style.cssText='position:absolute;left:0;top:0;width:100%;height:100%;display:block';f[k].appendChild(o);f[k]._o=o}
  b.root=root;b.f=f;b.dir=dir;return b;
}
function rot3(n,ry,rx,rz){var a=rz*Math.PI/180,x=n[0]*Math.cos(a)-n[1]*Math.sin(a),y=n[0]*Math.sin(a)+n[1]*Math.cos(a),z=n[2];
  a=rx*Math.PI/180;var y2=y*Math.cos(a)-z*Math.sin(a),z2=y*Math.sin(a)+z*Math.cos(a);
  a=ry*Math.PI/180;return [x*Math.cos(a)+z2*Math.sin(a),y2,-x*Math.sin(a)+z2*Math.cos(a)]}
var LIGHT=[-.25,-.45,.86], AMB=.3, DIFF=.85;
function setLight(v,amb,diff){var n=Math.hypot(v[0],v[1],v[2]);LIGHT=[v[0]/n,v[1]/n,v[2]/n];if(amb!=null)AMB=amb;if(diff!=null)DIFF=diff}
setLight(LIGHT);
function lit(n,p){var w=rot3(n,p.ry||0,p.rx||0,p.rz||0);return Math.min(1.15,AMB+DIFF*Math.max(0,w[0]*LIGHT[0]+w[1]*LIGHT[1]+w[2]*LIGHT[2]))}
/* p: x y z ry rx rz s, g (brightness multiplier), blur, op */
function pose(b,p){
  if(p.hide){b.root.style.display='none';return} b.root.style.display='block';
  var s=(p.s==null?1:p.s)/K;
  b.root.style.transform='translate3d('+(p.x||0)+'px,'+(p.y||0)+'px,'+(p.z||0)+'px) rotateY('+(p.ry||0)+'deg) rotateX('+(p.rx||0)+'deg) rotateZ('+(p.rz||0)+'deg) scale3d('+s+','+s+','+s+')';
  var f=b.f,d=b.dir,g=p.g==null?1:p.g,bl=p.blur>.05?' blur('+p.blur.toFixed(2)+'px)':'';
  function F(e,n){var v=lit(n,p)*g,o=e._o;
    if(v<1){o.style.background='#000';o.style.opacity=(1-v).toFixed(3)}else{o.style.background='#fff';o.style.opacity=Math.min(.35,(v-1)*.6).toFixed(3)}
    e.style.filter=bl?bl.trim():'none'}
  F(f.front,[0,0,1]);F(f.back,[0,0,-1]);F(f.spine,[-d,0,0]);F(f.fore,[d,0,0]);F(f.top,[0,-1,0]);F(f.bot,[0,1,0]);
  b.root.style.opacity=p.op==null?1:p.op;
}

/* text: elements with data-t="start,end" and data-fx */
var TEXTS=[];
function initText(){document.querySelectorAll('[data-t]').forEach(function(e){var p=e.dataset.t.split(',').map(Number);TEXTS.push({el:e,s:p[0],e:p[1],fx:e.dataset.fx||'rise'})})}
function drawText(t){
  for(var i=0;i<TEXTS.length;i++){var o=TEXTS[i],e=o.el,out=sm((t-o.e)/.35),p;
    if(t<o.s-.05||t>o.e+.4){e.style.opacity=0;continue}
    if(o.fx==='rise'){p=oc((t-o.s)/.6);e.style.opacity=p*(1-out);e.style.transform='translateY('+((1-p)*22-out*14)+'px)';e.style.filter='blur('+((1-p)*6+out*5)+'px)';}
    else if(o.fx==='slam'){p=oc((t-o.s)/.3);e.style.opacity=cl((t-o.s)/.1)*(1-out);e.style.transform='scale('+lerp(1.5,1,p)+')';e.style.filter='blur('+((1-p)*8+out*6)+'px)';}
    else if(o.fx==='fade'){e.style.opacity=sm((t-o.s)/.5)*(1-out);}
    else if(o.fx==='pop'){p=ob((t-o.s)/.5);e.style.opacity=cl((t-o.s)/.2);e.style.transform='scale('+Math.max(.4,p)+')';}
    else if(o.fx==='cut'){e.style.opacity=(t>=o.s&&t<o.e)?1:0;var q=oc((t-o.s)/.18);e.style.transform='scale('+lerp(1.12,1,q)+')';}
    else if(o.fx==='type'){var full=e.dataset.full||(e.dataset.full=e.textContent);var n=Math.floor(cl((t-o.s)/(full.length*.045))*full.length);e.textContent=full.slice(0,n)||'​';e.style.opacity=1-out;}
  }
}

/* end card: logo, line, pill, link in bio */
var END=null;
function initEnd(o){END=Object.assign({logoTop:150,lineTop:286,pillTop:640,dark:true},o);
  var st=$('stage');
  var lg=el('','top:'+END.logoTop+'px',st,null,'img');lg.id='logo';lg.src=END.dark?'assets/logo.png':'assets/logo_dark.png';lg.style.mixBlendMode=END.dark?'screen':'multiply';
  el('c h it','top:'+END.lineTop+'px;font-size:'+(END.size||42)+'px',st,END.line).dataset.t=(END.t0+.4)+',99';
  var pc=el('c','top:'+END.pillTop+'px',st,'<span class="pill" id="pill">Shop at daralathari.com</span>');pc.dataset.t=(END.t0+1.0)+',99';pc.dataset.fx='pop';
  el('','',st).id='ring';
  var lb=el('c','top:'+(END.pillTop+82)+'px;font-family:var(--ui);font-weight:600;font-size:16px;color:var(--dim)',st,'Link in bio');lb.dataset.t=(END.t0+1.5)+',99';lb.dataset.fx='fade';
}
function drawEnd(t){if(!END)return;var t0=END.t0,lg=oc((t-t0)/.8),L_=$('logo');L_.style.opacity=lg;L_.style.transform='scale('+lerp(1.2,1,lg)+')';
  var pu=t>t0+1.7?((t-t0-1.7)%1.6)/1.6:-1,ring=$('ring'),pill=$('pill');
  if(pu>=0){var pr=sm(pu/.25)*(1-sm((pu-.25)/.25));pill.style.transform='scale('+(1+.045*pr)+')';
    ring.style.top=(END.pillTop-6-pu*14)+'px';ring.style.width=(330+pu*60)+'px';ring.style.height=(72+pu*28)+'px';ring.style.opacity=(1-pu)*.8}
  else{pill.style.transform='none';ring.style.opacity=0}}

function overlays(){var st=$('stage');el('','',st).id='vig';el('','',st).id='grain';el('','',st).id='black'}
function drawCommon(t,T){drawText(t);drawEnd(t);$('black').style.opacity=Math.max(1-sm(t/.25),sm((t-(T-.35))/.35)*0)}
