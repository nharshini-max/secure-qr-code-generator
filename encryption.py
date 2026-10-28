from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

KEY_FILE = "secret.key"


def generate_key():
    """Generate and save a 256-bit AES key."""
    key = AESGCM.generate_key(bit_length=256)

    with open(KEY_FILE, "wb") as file:
        file.write(key)

    return key


def load_key():
    """Load the AES key, or create one if it doesn't exist."""
    if not os.path.exists(KEY_FILE):
        return generate_key()
    
    with open(KEY_FILE, "rb") as file:
        return file.read()


def encrypt_message(message):
    """Encrypt a message using AES-256-GCM."""
    key = load_key()
    aes = AESGCM(key)

    nonce = os.urandom(12)
    encrypted_data = aes.encrypt(
        nonce,
        message.encode("utf-8"),
        None
    )

    # Store nonce + encrypted data together
    combined = nonce + encrypted_data

    return base64.urlsafe_b64encode(combined).decode("utf-8")


def decrypt_message(encrypted_message):
    """Decrypt AES-256-GCM encrypted data."""
    key = load_key()
    aes = AESGCM(key)

    combined = base64.urlsafe_b64decode(
        encrypted_message.encode("utf-8")
    )

    nonce = combined[:12]
    encrypted_data = combined[12:]

    decrypted_data = aes.decrypt(
        nonce,
        encrypted_data,
        None
    )

    return decrypted_data.decode("utf-8")


if __name__ == "__main__":
    print("====================================")
    print("   SECURE QR - AES-256 TEST")
    print("====================================")

    message = input("\nEnter confidential information: ")

    encrypted = encrypt_message(message)

    print("\nEncrypted data:")
    print(encrypted)

    decrypted = decrypt_message(encrypted)

    print("\nDecrypted information:")
    print(decrypted)

    print("\n✓ AES-256 encryption/decryption successful!")