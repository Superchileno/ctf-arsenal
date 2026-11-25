import requests, time
base="https://<host>/blind-spot"
paths=["/","/health","/api","/api/preview","/preview","/docs","/openapi.json","/static/","/favicon.ico"]
for p in paths:
    t=time.time()
    try:
        r=requests.get(base+p,timeout=12,headers={"User-Agent":"Mozilla/5.0"},allow_redirects=False)
        print("GET",p,r.status_code,len(r.content),round(time.time()-t,1),r.headers.get("Content-Type"))
    except Exception as e:
        print("GET",p,"ERR",type(e).__name__,round(time.time()-t,1))
