import requests, json
base="https://<host>/ooklakappa"
TOK="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzMjg0MTMwLCJpYXQiOjE3OTMyNzUyMTcsImp0aSI6IjExNmM1NGEwZmRmZTQ0Nzc4YzVkNDljMGZkNDVmMTYyIiwidXNlcl9pZCI6NzI1ODB9.dHumV2sRmb7zCcvoAwrNwB5SRODcMHiPrfZ6-7noPKE"
H={"User-Agent":"Mozilla/5.0","Authorization":"Bearer "+TOK,"Accept":"application/json"}
s=requests.Session()
def show(tag,r):
    print("=== ",tag, r.status_code, r.headers.get("Content-Type"))
    print(r.text[:1200])
    print()
for p in ["/api/health","/api/members","/api/users/72580","/api/admin/database"]:
    try:
        r=s.get(base+p,headers=H,timeout=20); show(p,r)
    except Exception as e: print(p,"ERR",e)
