import os
import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie
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

# --- UTILS ---
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# --- SETUP ---
os.makedirs("data", exist_ok=True)
st.set_page_config(page_title="Image Encryptor", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #f5f5f5;
    }
    .stButton>button {
        background-color: #154799;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        margin-top: 0.5rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
lottie_lock = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_h4th9ofg.json")

with st.container():
    col1, col2 = st.columns([1, 3])
    with col1:
        if lottie_lock:
            st_lottie(lottie_lock, height=140, speed=1)
        else:
            st.markdown("🔐")
    with col2:
        st.markdown("## 🔐 **SecurePixelChain**")
        st.markdown("A Cryptography algorithm ensures image confidentiality with encryption and guarantees integrity through signature verification. 🧠✨")

st.markdown("---")

# --- MODE SELECTION ---
mode = st.selectbox("🔁 Choose Mode", ["Encrypt", "Decrypt"])
key = st.text_input("🔑 Enter Encryption/Decryption Key", type="password")

# --- ENCRYPT MODE ---
if mode == "Encrypt":
    uploaded = st.file_uploader("📤 Upload Image to Encrypt", type=["jpg", "jpeg", "png"])

    if uploaded and key:
        run = st.button("🚀 Run Encryption")
        if run:
            with st.spinner("🔐 Encrypting & Signing... please wait..."):
                input_path = os.path.join("data", "input.png")
                with open(input_path, "wb") as f:
                    f.write(uploaded.getbuffer())

                st.image(input_path, caption="📷 Original Image", use_column_width=True)

                encrypted_image = encrypt_image(input_path, key)
                encrypted_path = os.path.join("data", "encrypted.png")
                save_image(encrypted_image, encrypted_path)
                st.image(encrypted_path, caption="🛡️ Encrypted Image", use_column_width=True)

                private_key, public_key = generate_key_pair()
                signature = sign_image(input_path, private_key)

                save_pickle(signature, os.path.join("data", "signature.pkl"))
                save_public_key_pem(public_key, os.path.join("data", "public_key.pem"))

                st.success("✅ Encrypted and Signed Successfully!")

                with open(encrypted_path, "rb") as f:
                    st.download_button("📥 Download Encrypted Image", f, file_name="encrypted.png")

                with open("data/signature.pkl", "rb") as f:
                    st.download_button("📥 Download Signature", f, file_name="signature.pkl")

                with open("data/public_key.pem", "rb") as f:
                    st.download_button("📥 Download Public Key", f, file_name="public_key.pem")

# --- DECRYPT MODE ---
elif mode == "Decrypt":
    uploaded_encrypted = st.file_uploader("📥 Upload Encrypted Image", type=["png", "jpg", "jpeg"])
    uploaded_public_key = st.file_uploader("🔐 Optionally Upload Public Key (.pem)", type=["pem"])

    if uploaded_encrypted and key:
        run = st.button("🔓 Run Decryption")
        if run:
            with st.spinner("🔍 Decrypting... please wait..."):
                encrypted_path = os.path.join("data", "encrypted_uploaded.png")
                with open(encrypted_path, "wb") as f:
                    f.write(uploaded_encrypted.getbuffer())

                decrypted_image = decrypt_image(load_image(encrypted_path), key)
                decrypted_path = os.path.join("data", "decrypted.png")
                save_image(decrypted_image, decrypted_path)
                st.image(decrypted_path, caption="📷 Decrypted Image", use_column_width=True)

                st.success("✅ Decryption Completed!")

                if uploaded_public_key:
                    pubkey_path = os.path.join("data", "public_key_uploaded.pem")
                    with open(pubkey_path, "wb") as f:
                        f.write(uploaded_public_key.getbuffer())
                    st.info("🗝️ Public key uploaded. Signature verification not implemented yet.")

                with open(decrypted_path, "rb") as f:
                    st.download_button("📥 Download Decrypted Image", f, file_name="decrypted.png")
