import requests, json, time, base64
base="https://<host>/ooklakappa"
TOK="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzkzMjg0MTMwLCJpYXQiOjE3OTMyNzUyMTcsImp0aSI6IjExNmM1NGEwZmRmZTQ0Nzc4YzVkNDljMGZkNDVmMTYyIiwidXNlcl9pZCI6NzI1ODB9.dHumV2sRmb7zCcvoAwrNwB5SRODcMHiPrfZ6-7noPKE"
def b64(s): return base64.urlsafe_b64decode(s+"="*(-len(s)%4))
print("now", int(time.time()), time.ctime())
print(json.loads(b64(TOK.split(".")[1])))
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json"})
for body in [{"username":"qa_probe_1","password":"Probe12345!"},{"username":"qa_probe_1","password":"Probe12345!","email":"usuario@example.com"}]:
    r=s.post(base+"/api/register",json=body,timeout=20)
    print("REGISTER",body, r.status_code, r.text[:400])
r=s.post(base+"/api/login",json={"username":"qa_probe_1","password":"Probe12345!"},timeout=20)
print("LOGIN", r.status_code, r.text[:600])
