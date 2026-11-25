c=bytes.fromhex("4a180cda8c0cdba0"); s=bytes.fromhex("6cb08b5b5565b0f2"); k=b"FRAMELIN"
p=bytes(a^b^kk for a,b,kk in zip(c,s,k))
print("computed",p.hex(),"expected 60fac6cc9c25221c", p.hex()=="60fac6cc9c25221c")
