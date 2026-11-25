import requests, json
base="https://<host>/ooklakappa"
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json"})
tok=s.post(base+"/api/login",json={"username":"qa_probe_1","password":"Probe12345!"},timeout=20).json()["token"]
H={"Authorization":"Bearer "+tok}
def call(tag,m,p,**kw):
    r=s.request(m,base+p,headers=H if not kw.pop("anon",False) else {},timeout=20,**kw)
    print("===",tag,r.status_code,r.text[:400]); return r
call("PUT self password","PUT","/api/users/320",json={"password":"NewPass123!"})
call("login new pass","POST","/api/login",anon=True,json={"username":"qa_probe_1","password":"NewPass123!"})
call("login old pass","POST","/api/login",anon=True,json={"username":"qa_probe_1","password":"Probe12345!"})
call("login by email","POST","/api/login",anon=True,json={"username":"usuario@example.com","password":"NewPass123!"})
call("reg with role","POST","/api/register",anon=True,json={"username":"qa_probe_role","password":"Probe12345!","role":"admin"})
