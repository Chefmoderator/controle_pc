from OpenSSL import crypto

cert_file = "cert.pem"
key_file = "key.pem"

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

cert = crypto.X509()
cert.get_subject().CN = "localhost"
cert.set_serial_number(1000)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365*24*60*60)  # 1 год
cert.set_issuer(cert.get_subject())
cert.set_pubkey(key)
cert.sign(key, "sha256")

with open(cert_file, "wb") as f:
    f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

with open(key_file, "wb") as f:
    f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
