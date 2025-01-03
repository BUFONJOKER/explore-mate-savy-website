from cryptography.fernet import Fernet

key = b'kKXgzCaDaQ-8o2QnEp4b5tTmh34b95Pcj1W8ZO_HSXM='

# Encrypt the password
def encrypt_password(password: str) -> str:
    
    cipher = Fernet(key)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()

# Decrypt the password
def decrypt_password(encrypted_password: str) -> str:
    
    cipher = Fernet(key)
    decrypted_password = cipher.decrypt(encrypted_password.encode())
    return decrypted_password.decode()


