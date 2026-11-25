import urllib.request, urllib.error, socket, re, sys
base='https://<host>/unauth/'
paths='''login logout register signup admin dashboard home index index.html flag flags api api/v1 api/flag api/login api/register user users profile account me auth authenticate secret config .env .git/HEAD robots.txt sitemap.xml static/ console debug source app.py main.py requirements.txt Dockerfile README readme health status ping test upload files download notes note search contact about'''.split()
for p in paths:
    url=base+p
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        r=urllib.request.urlopen(req, timeout=8)
        body=r.read()
        code=r.status
        hdr=r.headers
    except urllib.error.HTTPError as e:
        body=e.read(); code=e.code; hdr=e.headers
    except Exception as e:
        print('ERR', p, e); continue
    title=''
    m=re.search(rb'<title>([^<]*)', body)
    if m: title=m.group(1).decode('latin1','replace')
    extra=''
    if hdr.get('Location'): extra+=' Loc='+hdr.get('Location')
    if hdr.get('Set-Cookie'): extra+=' Cookie='+hdr.get('Set-Cookie')
    print('%3d %5d /%s %s%s' % (code, len(body), p, title, extra))
