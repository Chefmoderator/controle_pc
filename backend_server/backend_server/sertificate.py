from OpenSSL import crypto

CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"

def createCertificate(ip: str):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.get_subject().CN = ip
    cert.set_serial_number(1001)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)

    san = f"IP:{ip},DNS:localhost"
    cert.add_extensions([
        crypto.X509Extension(b"subjectAltName", False, san.encode())
    ])

    cert.sign(key, "sha256")

    with open(CERT_FILE, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    with open(KEY_FILE, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    print("[OK] Certificate created for IP:", ip)