import hashlib

def GetPwd( _pwd: bytes, _salt: bytes ):
    for _ in range(3):
        _pwd = hashlib.pbkdf2_hmac(hash_name="sha512", password=_pwd, salt=_salt, iterations=100000 )
    return _pwd