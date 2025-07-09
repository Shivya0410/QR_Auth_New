# QRDetect: Cyber-grade Anti-Counterfeit QR Toolkit

## 🚀 Overview

**QRDetect** is a Python framework—crafted from a QR & cybersecurity expert’s POV—to generate and verify **tamper-sensitive**, **mask-pattern-bound**, **XOR+HMAC-signed** QR codes.  
A **normal scanner** (e.g. smartphone camera, ZXing) will decode the embedded JSON, but **even 5% tampering** (scratches, JSON edit, wrong mask) triggers a **fake** alert.

---

## ⚙️ Features

1. **Payload Binding**  
   - `id` (product)  
   - `batch` (lot)  
   - `ts` (UTC timestamp)

2. **Mask-Pattern Lock**  
   - You choose mask 0–7.  
   - Payload includes `pattern`.  
   - Re-encoding with wrong mask → mismatch.

3. **XOR + HMAC-SHA256 Signature**  
   - Covers *all* fields `(id‖ts‖pattern)`.  
   - 8-byte XOR prefix obfuscation + SHA256 HMAC.  
   - Base64 URL-safe.

4. **Human-Readable Checksum**  
   - First 3 hex digits of SHA256(id‖ts).  
   - Quick manual verify (e.g. `chk=7F9`).

5. **Low EC Level**  
   - Uses **L** (~7%).  
   - Minor physical damage still decodes but breaks sig/checksum.

6. **Micro-QR Support**  
   - Generate tiny Micro-QR symbols for ultra-compact needs.

---

## 📐 Advanced QR Patterns

A true QR expert knows:

- **Model 1 vs Model 2**: We use **Model 2** (ISO/IEC 18004) for versions 1–40.
- **Micro-QR**: Ultra-small codes (versions M1–M4).  
- **iQR & SQRC**: Not currently implemented, but segno supports iQR in future.
- **Mask Patterns** (0–7): Chosen to minimize “bad” modules (long runs, dark/light modules).
- **Function Patterns**:  
  - Finder, alignment, timing, format & version info.  
  - We NEVER overwrite these—only data modules change.
- **Error Correction Levels**:  
  - L (7%), M (15%), Q (25%), H (30%).  
  - We pick **L** to force integrity checks on even minor edits.

---

## 🔒 Security Model & Threats

- **Threat**: Attacker prints a look-alike QR, edits JSON or re-generates code.
- **Mitigation**:  
  - **HMAC** binds every bit of payload. Any JSON tweak fails.  
  - **Mask lock**: wrong mask → backend flags “pattern mismatch.”  
  - **Checksum**: human-readable tamper check.  
  - **Low EC**: ~5% physical tamper still decodes but breaks crypto.

> **Note**: Keep `SECRET_KEY` offline. If leaked, attacker can forge.

---

## 📦 Usage

### 1. Generate QR

```bash
python generator.py \
  --id    PROD202507 \
  --batch B202507 \
  --mask  3 \
  --version 5 \
  --variant standard \
  --output prod_qr.png
