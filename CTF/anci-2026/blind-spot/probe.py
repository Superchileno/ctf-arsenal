import requests, time
paths = ["/", "/blind-spot", "/blind-spot/", "/blind-spot/index.html", "/login", "/robots.txt", "/api"]
for p in paths:
    t=time.time()
    try:
        r = requests.get("https://<host>"+p, timeout=8, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=False)
        print(p, r.status_code, len(r.content), round(time.time()-t,1), dict(list(r.headers.items())[:6]))
    except Exception as e:
        print(p, "ERR", type(e).__name__, round(time.time()-t,1))
