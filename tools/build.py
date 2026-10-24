"""build.py PROJECT_DIR  ->  writes PROJECT_DIR/film.html from film_src.html
Fonts: first line of film_src.html:  <!--FONTS Family:fontsource-pkg:subset:w1,w2:style; ... -->
Placeholders: /*FONTS*/ (font-face css) and /*LIB*/ (tools/lib.js 3D book toolkit)."""
import base64, os, re, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d=os.path.abspath(sys.argv[1]); src=open(os.path.join(d,'film_src.html'),encoding='utf8').read()
css=''
m=re.search(r'<!--FONTS(.*?)-->',src,re.S)
for spec in (m.group(1).split(';') if m else []):
    spec=spec.strip()
    if not spec: continue
    fam,pkg,sub,ws,style=[x.strip() for x in spec.split(':')]
    for w in ws.split(','):
        p=os.path.join(ROOT,'node_modules/@fontsource/%s/files/%s-%s-%s-%s.woff2'%(pkg,pkg,sub,w,style))
        if not os.path.exists(p): os.system('cd %s && npm i --silent @fontsource/%s'%(ROOT,pkg))
        b=base64.b64encode(open(p,'rb').read()).decode()
        css+="@font-face{font-family:'%s';font-weight:%s;font-style:%s;src:url(data:font/woff2;base64,%s) format('woff2');}\n"%(fam,w,style,b)
h=src.replace('/*FONTS*/',css).replace('/*LIB*/',open(os.path.join(ROOT,'tools/lib.js'),encoding='utf8').read())
open(os.path.join(d,'film.html'),'w',encoding='utf8').write(h)
a=os.path.join(d,'assets')
if not os.path.exists(a): os.symlink(os.path.join(ROOT,'assets'),a)
print('built',d)
