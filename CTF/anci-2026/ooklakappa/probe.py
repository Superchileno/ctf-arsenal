import requests, time
base="https://<host>/ooklakappa"
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"})
for p in ["/","/api","/api/","/login","/robots.txt","/admin"]:
    t=time.time()
    try:
        r=s.get(base+p,timeout=15,allow_redirects=False)
        print(p, r.status_code, len(r.content), round(time.time()-t,1), r.headers.get("Content-Type"), r.headers.get("Location"))
        if p=="/" and r.status_code==200:
            open("ANCI/ooklakappa/index.html","w",encoding="utf-8").write(r.text)
    except Exception as e:
        print(p,"ERR",type(e).__name__,round(time.time()-t,1))
