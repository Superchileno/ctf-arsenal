import urllib.request, urllib.error, json
BASE='https://<host>/fireburned-2'
def post(path, obj, headers=None):
    data=json.dumps(obj).encode()
    h={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'}
    if headers: h.update(headers)
    r=urllib.request.Request(BASE+path, data=data, headers=h, method='POST')
    try:
        resp=urllib.request.urlopen(r, timeout=15); body=resp.read(); code=resp.status; hd=resp.headers
    except urllib.error.HTTPError as e:
        body=e.read(); code=e.code; hd=e.headers
    except Exception as e:
        return ('ERR',str(e))
    return (code, hd.get('Content-Type'), body[:2000])

cases=[
 ('/api/fetch', {}),
 ('/api/fetch', {'url':'http://example.com'}),
 ('/api/fetch', {'url':'https://example.com'}),
 ('/api/fetch', {'url':'http://fireburned--db:8080'}),
 ('/api/fetch', {'url':'http://fireburned--db:8080/'}),
 ('/api/preview', {'url':'http://fireburned--db:8080/'}),
 ('/api/preview', {'url':'http://example.com'}),
 ('/api/fetch', {'url':'file:///etc/passwd'}),
 ('/api/fetch', {'url':'http://127.0.0.1:8080/'}),
 ('/api/fetch', {'url':'http://localhost:8080/'}),
]
for p,o in cases:
    print('===',p,o)
    r=post(p,o)
    if r[0]=='ERR': print('ERR',r[1]); continue
    print(r[0],r[1]); print(r[2][:800])
