import os
import streamlit as st
from image_crypto import (
    encrypt_image,
    decrypt_image,
    sign_image,
    verify_image_signature,
    compare_images,
    generate_key_pair,
    load_image,
    save_image
)
from utils import save_pickle, load_pickle, save_public_key_pem, load_public_key_pem

os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="Image Encryptor", layout="centered")
st.title("🔐 Image Encryption & Signature App")

mode = st.sidebar.selectbox("Choose Mode", ["Encrypt", "Decrypt"])
key = st.text_input("Enter Encryption/Decryption Key", type="password")

if mode == "Encrypt":
    uploaded = st.file_uploader("Upload Image to Encrypt", type=["jpg", "jpeg", "png"])
    
    if uploaded and key:
        input_path = os.path.join("data", "input.png")
        with open(input_path, "wb") as f:
            f.write(uploaded.getbuffer())

        st.image(input_path, caption="Original Image")

        # Encrypt
        encrypted_image = encrypt_image(input_path, key)
        encrypted_path = os.path.join("data", "encrypted.png")
        save_image(encrypted_image, encrypted_path)
        st.image(encrypted_path, caption="Encrypted Image")

        # Sign
        private_key, public_key = generate_key_pair()
        signature = sign_image(input_path, private_key)

        save_pickle(signature, os.path.join("data", "signature.pkl"))
        save_public_key_pem(public_key, os.path.join("data", "public_key.pem"))

        st.success("✅ Image Encrypted and Signed!")

        with open(encrypted_path, "rb") as f:
            st.download_button("📥 Download Encrypted Image", f, file_name="encrypted.png")

        with open(os.path.join("data", "signature.pkl"), "rb") as f:
            st.download_button("📥 Download Signature", f, file_name="signature.pkl")

        with open(os.path.join("data", "public_key.pem"), "rb") as f:
            st.download_button("📥 Download Public Key", f, file_name="public_key.pem")

elif mode == "Decrypt":
    uploaded_encrypted = st.file_uploader("Upload Encrypted Image", type=["png", "jpg", "jpeg"])
    uploaded_public_key = st.file_uploader("Optionally Upload Public Key (.pem) to Verify (Optional)", type=["pem"])

    if uploaded_encrypted and key:
        encrypted_path = os.path.join("data", "encrypted_uploaded.png")
        with open(encrypted_path, "wb") as f:
            f.write(uploaded_encrypted.getbuffer())

        decrypted_image = decrypt_image(load_image(encrypted_path), key)
        decrypted_path = os.path.join("data", "decrypted.png")
        save_image(decrypted_image, decrypted_path)
        st.image(decrypted_path, caption="Decrypted Image")

        st.success("✅ Decryption Completed")

        # Only show public key info if uploaded
        if uploaded_public_key:
            pubkey_path = os.path.join("data", "public_key_uploaded.pem")
            with open(pubkey_path, "wb") as f:
                f.write(uploaded_public_key.getbuffer())
            st.info("📎 Public key uploaded, but no signature to verify.")

        with open(decrypted_path, "rb") as f:
            st.download_button("📥 Download Decrypted Image", f, file_name="decrypted.png")
