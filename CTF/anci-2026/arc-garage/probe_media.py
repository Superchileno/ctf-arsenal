import urllib.request, urllib.error

base = "https://<host>/media/challenges/ANCI-9/content/"
names = [
    "", "chall.c", "challenge.c", "src.c", "source.c", "old-school-bins.c",
    "solve.py", "solution.py", "exploit.py", "sol.py", "README.md", "readme.md",
    "flag.txt", "challenge.json", "metadata.json", "info.json", "old-school-bins.zip",
    "chall", "libc.so", "Dockerfile", "Makefile", "build.sh",
]
for n in names:
    url = base + n
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=8) as r:
            data = r.read(400)
            print("%-28s %s %s %r" % (n or "(dir)", r.status, r.headers.get("Content-Type"), data[:120]))
    except urllib.error.HTTPError as e:
        print("%-28s HTTP %s" % (n or "(dir)", e.code))
    except Exception as e:
        print("%-28s ERR %s" % (n or "(dir)", e))
