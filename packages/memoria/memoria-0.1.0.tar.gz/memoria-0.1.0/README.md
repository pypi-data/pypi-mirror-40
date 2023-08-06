# Memoria

Memoria is a Python library for saving and loading objects on the hard drive, caching, encryption, and password management.

## Crypto

Crypto is a class that can encrypt and decrypt an object.

```python
from memoria import Crypto

crypto = Crypto(key=1234)
random_obj = {'asdf':range(10)}

encrypted = crypto.encrypt(random_obj)
print(crypto.decrypt(encrypted))
```

## Pickler

## Box

## Vault

## PasswordManager

## HardMemory

## Cache
