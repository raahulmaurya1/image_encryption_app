
# 🔒 Image Encryption & Decryption with Digital Signature Verification

> 🛡️ A Python-based tool to securely **encrypt**, **decrypt**, and **verify images** using a hybrid of dynamic key-based pixel shuffling and RSA digital signatures. Built for interactive use in Streamlit.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Streamlit-red)


---

## 🌟 Features

- 🔐 **Secure Encryption** with dynamic key-based XOR operations and pixel shuffling
- 🔓 **Decryption** to retrieve original images with high accuracy
- 🖋 **RSA Digital Signatures** to ensure image authenticity
- 🧠 **SSIM Comparison** to verify image similarity after decryption
- ⚡ **Colab Ready**: Easy file uploads, downloads, and visualization

---

## 📽️ Demo

> Run it directly in [Streamlit 🚀](https://imageencryptionapp-fey4sg4wuccsyzqtaf7egu.streamlit.app/)  
> No setup needed – upload an image, choose a key, and go!

---

## 📽️ Flow diagram

<img src="https://raw.githubusercontent.com/raahulmaurya1/image_encryption_app/c4427f6c7cf0c972e428af0d37f6e56064148800/diagram.png" alt="Encryption Diagram" width="1100">

## 🛠️ How It Works

1. **Encryption**
   - Flattens and shuffles image pixels using a pseudo-random key
   - Applies XOR operation with a dynamic key
   - Shifts image rows and columns for added security

2. **Decryption**
   - Reverses shifting and XOR operations
   - Unshuffles pixels using the same key

3. **Digital Signature**
   - Signs original image with RSA private key
   - Verifies the decrypted image hash using the public key

---

## 🚀 Installation

> You don’t need to install anything locally!  

However, if running locally:

```bash
pip install opencv-python cryptography scikit-image
```

---

## 📦 Usage

### 1. Run the Tool

```python
run_image_encryptor()
```

### 2. Choose an Option

- `1`: Encrypt and Sign an Image
- `2`: Decrypt and Verify an Image

---

## 🧪 Example Screenshots

| Encryption | Decryption | SSIM Score |
|------------|------------|------------|
| <img src="https://github.com/raahulmaurya1/image_encryption_app/blob/6cdd9e33bb1edde188116b7a14c8c53b2dd034c2/encrypted.png?raw=true" width="200"/> | <img src="https://github.com/raahulmaurya1/image_encryption_app/blob/6cdd9e33bb1edde188116b7a14c8c53b2dd034c2/normal_image.png?raw=true" width="200"/> | `🧠 SSIM: 1.000` |


---

## 🧪 Salt-and-Pepper Noise Test

📊 **Histogram:**  
<img src="https://github.com/raahulmaurya1/image_encryption_app/blob/ce3fa4629c6ffaa509c00f0891a8760cd9e1bf28/Histogram.png?raw=true" width="800" height="300"/>

SSIM between Original and Decrypted Image: `1.0000`

🖼️ **Noisy Image:**  
<img src="https://github.com/raahulmaurya1/image_encryption_app/blob/ce3fa4629c6ffaa509c00f0891a8760cd9e1bf28/salt_paper_test.png?raw=true" width="800"/>



---

## 📚 Technologies Used

- **Python 3.8+**
- **OpenCV**
- **Cryptography**
- **RSA (2048-bit)**
- **Google Colab**
- **SSIM from scikit-image**

---

## 🤝 Contributing

Pull requests are welcome!  
If you find bugs or have ideas for improvements, feel free to open an issue.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

Created with 💙 by [Rahul Maurya]  
📧 Email: raahulmaurya2@gmail.com  
🔗 GitHub: [@raahulmaurya1](https://github.com/yourgithub)
