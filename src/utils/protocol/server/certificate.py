from OpenSSL import crypto
import pathlib

def create_certificate():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
        
    cert = crypto.X509()
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    if not pathlib.Path("./cert").exists():
        pathlib.Path("./cert").mkdir()
        
    with open("./cert/cert.pem", "wt") as file:
        file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open("./cert/key.pem", "wt") as file:
        file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))