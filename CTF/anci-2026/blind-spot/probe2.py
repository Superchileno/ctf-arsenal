import requests, time
for p in ["/blind-spot/"]:
    t=time.time()
    try:
        r = requests.get("https://<host>"+p, timeout=150, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=True)
        print(p, r.status_code, len(r.content), round(time.time()-t,1))
        print(r.text[:2000])
    except Exception as e:
        print(p, "ERR", type(e).__name__, round(time.time()-t,1), e)
