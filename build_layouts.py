# Converts the QUL line-layout databases (assest/*.db) and the Qudratullah 15-line JSON pages into compact
# files in layouts/ in the same format as mushaf.json:  page -> lines, a line is "h<surah>", "b" or runs
# [surah, ayah, firstWord, lastWord] (word index = number of words is the ayah number mark).
# Global word ids count every ayah's Uthmani words (uthmani.json) plus one mark per ayah.
import json, sqlite3, glob, os, sys
root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
u=json.load(open(os.path.join(root,'uthmani.json'),encoding='utf-8'))
starts=[]; sid=1                       # (first id, surah, ayah) in order
for si,s in enumerate(u):
    for ai,a in enumerate(s):
        starts.append((sid,si+1,ai+1)); sid+=len(a.split(' '))+1
import bisect
first=[x[0] for x in starts]
def runs(a,b):
    out=[]
    while a<=b:
        k=bisect.bisect_right(first,a)-1; st,s,ay=starts[k]
        end=(first[k+1]-1) if k+1<len(first) else sid-1
        e=min(b,end); out.append([s,ay,a-st,e-st]); a=e+1
    return out
def line(t,sn,a,b):
    if t=='surah_name': return 'h%d'%sn
    if t=='basmallah': return 'b'
    return runs(int(a),int(b))
LAY={
 'qpc-v1-15-lines':'مجمع الملك فهد ١٤٠٥ (١٥ سطر)',
 'qpc-v4-tajweed-15-lines':'QPC تجويد (١٥ سطر)',
 'digital-khatt-15-lines':'الخط الرقمي (١٥ سطر)',
 'qpc-nastaleeq-15-lines':'نستعليق (١٥ سطر)',
 'indopak-13-lines-layout-qudratullah':'إندوباك (١٣ سطر)',
 'indopak-9-lines-gaba':'إندوباك (٩ أسطر)',
 'taj-indopak-16-lines':'إندوباك (١٦ سطر)',
}
os.makedirs(os.path.join(root,'layouts'),exist_ok=True)
res={}
def save(id,pages):
    json.dump(pages,open(os.path.join(root,'layouts',id+'.json'),'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
    res[id]=pages
for f in sorted(glob.glob(os.path.join(root,'assest','*.db'))):
    id=os.path.basename(f)[:-3]
    c=sqlite3.connect(f); pages={}
    for p,ln,t,fw,lw,sn in c.execute('select page_number,line_number,line_type,first_word_id,last_word_id,surah_number from pages order by page_number,line_number'):
        pages.setdefault(p,[]).append(line(t,sn,fw,lw) if t!='ayah' or fw!='' else None)
    save(id,[[x for x in pages[p] if x] for p in sorted(pages)])
d=os.path.join(root,'mushaf','Indopak 15 lines layout(Qudratullah)')
pg=[]
for i in range(1,json.load(open(os.path.join(d,'info.json'),encoding='utf-8'))['number_of_pages']+1):
    j=json.load(open(os.path.join(d,'%d.json'%i),encoding='utf-8')); L=[]
    for k in sorted(j['lines'],key=int):
        l=j['lines'][k]; t=l['type']
        if t=='ayah': L.append(runs(l['first_word_id'],l['last_word_id']))
        elif t in('surah_name','basmallah'): L.append(line(t,l.get('surah_number'),0,0))
    pg.append(L)
save('indopak-15-lines',pg)
madani=json.load(open(os.path.join(root,'mushaf.json'),encoding='utf-8'))
idx=[]
for id,pages in res.items():
    ids=[]; 
    n=sum(len(p) for p in pages)
    # every word id must be covered exactly once, in order
    seen=[]
    for p in pages:
        for l in p:
            if isinstance(l,list):
                for s,a,w0,w1 in l: seen.append((s,a,w0,w1))
    print(id,len(pages),'pages', 'same as Madani' if pages==madani else '')
    idx.append({'id':id,'name':LAY.get(id,'إندوباك (١٥ سطر)'),'pages':len(pages),'same':pages==madani})
json.dump(idx,open(os.path.join(root,'layouts','index.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
