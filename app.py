import streamlit as st
import qrcode
import cv2
import numpy as np

from encryption import encrypt_message, decrypt_message


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Secure QR Code Generator",
    page_icon="🔐",
    layout="centered"
)


# ==========================================
# TITLE
# ==========================================

st.title("🔐 Secure QR Code Generator")

st.write(
    "A secure system that encrypts confidential information "
    "using AES-256-GCM before encoding it into a QR code."
)

st.divider()


# ==========================================
# SECTION 1 - GENERATE SECURE QR
# ==========================================

st.header("1. Generate Secure QR Code")

message = st.text_area(
    "Enter confidential information:",
    height=150,
    placeholder="Enter your confidential message here..."
)


if st.button(
    "🔒 Encrypt & Generate QR",
    use_container_width=True
):

    if not message.strip():

        st.warning(
            "Please enter confidential information."
        )

    else:

        try:

            # AES-256-GCM encryption
            encrypted_data = encrypt_message(message)

            # Create QR code
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4
            )

            qr.add_data(encrypted_data)
            qr.make(fit=True)

            qr_image = qr.make_image()

            # Save QR code
            qr_path = "secure_qr.png"

            qr_image.save(qr_path)

            st.success(
                "Secure QR code generated successfully!"
            )

            # Display QR code
            st.image(
                qr_path,
                caption="Encrypted Secure QR Code",
                width=300
            )

            # Download QR code
            with open(qr_path, "rb") as file:

                st.download_button(
                    label="⬇️ Download Secure QR",
                    data=file,
                    file_name="secure_qr.png",
                    mime="image/png",
                    use_container_width=True
                )

            # Display encrypted information
            with st.expander(
                "View Encrypted Data"
            ):

                st.code(encrypted_data)

        except Exception as error:

            st.error(
                f"An error occurred: {error}"
            )


st.divider()


# ==========================================
# SECTION 2 - SCAN / UPLOAD QR
# ==========================================

st.header("2. Scan / Upload Secure QR")

st.write(
    "Upload the generated QR code image. "
    "The system will automatically extract the "
    "encrypted information and decrypt it."
)


uploaded_file = st.file_uploader(
    "Upload QR Code Image",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file is not None:

    try:

        # Read uploaded image
        file_bytes = np.asarray(
            bytearray(uploaded_file.read()),
            dtype=np.uint8
        )

        image = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

        # OpenCV QR detector
        detector = cv2.QRCodeDetector()

        encrypted_data, points, _ = (
            detector.detectAndDecode(image)
        )


        # Check whether QR was detected
        if encrypted_data:

            st.success(
                "QR code successfully detected!"
            )

            # Show extracted encrypted data
            with st.expander(
                "View Extracted Encrypted Data"
            ):

                st.code(encrypted_data)


            # ==================================
            # DECRYPTION
            # ==================================

            try:

                decrypted_message = decrypt_message(
                    encrypted_data
                )

                st.success(
                    "Decryption successful!"
                )

                st.subheader(
                    "Original Confidential Information"
                )

                st.info(
                    decrypted_message
                )

            except Exception:

                st.error(
                    "Decryption failed. The QR data may "
                    "have been modified or the encryption "
                    "key may not match."
                )

        else:

            st.error(
                "Could not detect a QR code in the "
                "uploaded image."
            )

    except Exception as error:

        st.error(
            f"QR processing error: {error}"
        )


st.divider()


# ==========================================
# SECURITY INFORMATION
# ==========================================

st.subheader("🔐 Security Information")

st.write(
    "The system uses AES-256-GCM symmetric encryption. "
    "Confidential information is encrypted before being "
    "encoded into the QR code. Therefore, scanning the "
    "QR code alone does not reveal the original information."
)

st.write(
    "AES-GCM also provides integrity protection, allowing "
    "the system to detect modified or tampered encrypted data."
)


st.divider()


# ==========================================
# PROJECT FOOTER
# ==========================================

st.caption(
    "Secure QR Code Generator | AES-256-GCM Encryption"
)