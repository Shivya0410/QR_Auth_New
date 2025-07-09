#!/usr/bin/env python3
import json
import hmac
import hashlib
import base64
import cv2
import sys
from PIL import Image

SECRET_KEY = "Dhruv was here!!"

def xor_bytes(a,b):
    return bytes(x^y for x,y in zip(a,b))

def make_sig(pid,ts,mask):
    msg = f"{pid}{ts}{mask}".encode()
    h   = hmac.new(SECRET_KEY.encode(),msg,hashlib.sha256).digest()
    px  = xor_bytes(pid[:8].encode(),SECRET_KEY[:8].encode())
    return base64.urlsafe_b64encode(px+h).decode()

def make_chk(pid,ts):
    h = hashlib.sha256(f"{pid}{ts}".encode()).hexdigest()
    return h[:3].upper()

def validate(d):
    pid,ts,mask = d["id"],d["ts"],d["pattern"]
    sig,chk     = d["sig"],d["chk"]
    ok_sig = hmac.compare_digest(sig,make_sig(pid,ts,mask))
    ok_chk = (chk==make_chk(pid,ts))
    print(f"ID       : {pid}")
    print(f"Batch    : {d['batch']}")
    print(f"Timestamp: {ts}")
    print(f"Pattern  : {mask}")
    print(f"Checksum : {chk} {'✔️' if ok_chk else '❌'}")
    print(f"Signature: {sig[:10]}... {'✔️' if ok_sig else '❌'}")
    print("\n" + ("✅ genuine" if ok_sig and ok_chk else "❌ tampered"))

def scan(imgpath):
    img = cv2.imread(imgpath)
    data,_,_ = cv2.QRCodeDetector().detectAndDecode(img)
    if not data:
        print("❌ no QR found"); return
    try:
        js = json.loads(data)
    except:
        print("❌ invalid JSON"); return
    validate(js)

def main():
    if len(sys.argv)!=3 or sys.argv[1]!="--input":
        print("usage: validator.py --input <qr-image>")
        return
    scan(sys.argv[2])

if __name__=="__main__":
    main()
