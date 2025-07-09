#!/usr/bin/env python3
import json
import time
import hmac
import hashlib
import base64
import random
import segno

SECRET_KEY = "Dhruv was here!!"

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def generate_signature(product_id, timestamp, mask):
    message = f"{product_id}{timestamp}{mask}".encode()
    digest = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).digest()
    prefix = xor_bytes(product_id[:8].encode(), SECRET_KEY[:8].encode())
    return base64.urlsafe_b64encode(prefix + digest).decode()

def generate_checksum(product_id, timestamp):
    digest = hashlib.sha256(f"{product_id}{timestamp}".encode()).hexdigest()
    return digest[:3].upper()

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    resp = input(f"{prompt}{suffix}: ").strip()
    return resp or default

def main():
    print("=== Secure QR Code Generator ===")
    product_id = ask("Product ID")
    batch      = ask("Batch code")
    mask_in    = ask("Mask pattern (0–7) or leave blank for random", "")
    mask       = int(mask_in) if mask_in.isdigit() and 0 <= int(mask_in) <= 7 else random.randrange(8)
    ver_in     = ask("QR version (1–40) or leave blank for auto", "")
    version    = int(ver_in) if ver_in.isdigit() and 1 <= int(ver_in) <= 40 else None
    variant    = ask("Variant ('standard' or 'micro')", "standard").lower()
    output     = ask("Output filename", "qr.png")

    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    sig       = generate_signature(product_id, timestamp, mask)
    chk       = generate_checksum(product_id, timestamp)
    payload   = {
        "id":      product_id,
        "batch":   batch,
        "ts":      timestamp,
        "pattern": mask,
        "sig":     sig,
        "chk":     chk
    }

    print("\nPayload:")
    print(json.dumps(payload, indent=2))

    qr = segno.make(
        json.dumps(payload, separators=(',',':')),
        error='L',
        version=version,
        mask=mask,
        micro=(variant=='micro')
    )
    qr.save(output, scale=10, border=4)
    print(f"\n✅ QR code written to {output}")

if __name__ == "__main__":
    main()
