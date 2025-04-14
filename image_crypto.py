import cv2
import numpy as np
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives import serialization
from skimage.metrics import structural_similarity as ssim

def load_image(image_path):
    return cv2.imread(image_path)

def save_image(image_array, output_path):
    cv2.imwrite(output_path, image_array)

def prng(seed, size):
    random.seed(seed)
    return [random.randint(0, 255) for _ in range(size)]

def encrypt_image(image_path, key):
    image = load_image(image_path)
    key = int(key)
    rows, cols, channels = image.shape
    flat_image = image.flatten()

    indices = np.arange(flat_image.size)
    prng_indices = prng(key, len(indices))
    shuffled_indices = np.argsort(prng_indices)
    shuffled_image = flat_image[shuffled_indices].reshape(image.shape)

    encrypted_image = np.zeros((rows, cols, channels), dtype=np.uint8)
    for row in range(rows):
        for col in range(cols):
            for channel in range(channels):
                dynamic_key = (row + col + channel + key) % 256
                encrypted_image[row, col, channel] = shuffled_image[row, col, channel] ^ dynamic_key

    encrypted_image = np.roll(encrypted_image, shift=key % cols, axis=1)
    encrypted_image = np.roll(encrypted_image, shift=key % rows, axis=0)

    return encrypted_image

def decrypt_image(encrypted_image, key):
    rows, cols, channels = encrypted_image.shape
    key = int(key)

    decrypted_image = np.roll(encrypted_image, shift=-(key % cols), axis=1)
    decrypted_image = np.roll(decrypted_image, shift=-(key % rows), axis=0)

    for row in range(rows):
        for col in range(cols):
            for channel in range(channels):
                dynamic_key = (row + col + channel + key) % 256
                decrypted_image[row, col, channel] ^= dynamic_key

    flat_image = decrypted_image.flatten()
    indices = np.arange(flat_image.size)
    prng_indices = prng(key, len(indices))
    shuffled_indices = np.argsort(prng_indices)
    reverse_shuffled_image = np.zeros_like(flat_image)
    reverse_shuffled_image[shuffled_indices] = flat_image

    return reverse_shuffled_image.reshape((rows, cols, channels))

def generate_key_pair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def sign_image(image_path, private_key):
    image = load_image(image_path)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(image.tobytes())
    image_hash = digest.finalize()
    signature = private_key.sign(
        image_hash,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        utils.Prehashed(hashes.SHA256())
    )
    return signature

def verify_image_signature(image_path, signature, public_key):
    image = load_image(image_path)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(image.tobytes())
    image_hash = digest.finalize()
    try:
        public_key.verify(
            signature,
            image_hash,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            utils.Prehashed(hashes.SHA256())
        )
        return True
    except Exception:
        return False

def compare_images(img1_path, img2_path):
    img1 = load_image(img1_path)
    img2 = load_image(img2_path)
    score = ssim(img1, img2, channel_axis=-1)
    return score
