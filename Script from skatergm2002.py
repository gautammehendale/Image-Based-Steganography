#------ External Libraries ------#
import cv2
import struct
import bitstring
import numpy  as np
import zigzag as zz
import binascii
#================================#
#---------- Source Files --------#
import data_embedding as stego
import run_stego_algorithm as src
import image_preparation   as img
import re

# ============================================================================= #
# ============================================================================= #
# =========================== BEGIN CODE OPERATION ============================ #
# ============================================================================= #
# ============================================================================= #
# print('hii')
stego_image     = cv2.imread(src.STEGO_IMAGE_FILEPATH, flags=cv2.IMREAD_COLOR)
stego_image_f32 = np.float32(stego_image)
stego_image_YCC = img.YCC_Image(cv2.cvtColor(stego_image_f32, cv2.COLOR_BGR2YCrCb))

# FORWARD DCT STAGE
dct_blocks = [cv2.dct(block) for block in stego_image_YCC.channels[0]]  # Only care about Luminance layer

# QUANTIZATION STAGE
dct_quants = [np.around(np.divide(item, img.JPEG_STD_LUM_QUANT_TABLE)) for item in dct_blocks]

# Sort DCT coefficients by frequency
sorted_coefficients = [zz.zigzag(block) for block in dct_quants]
# print(sorted_coefficients)
# DATA EXTRACTION STAGE
recovered_data = stego.extract_encoded_data_from_DCT(sorted_coefficients)
# recovered_data=recovered_data[9:]
# print(recovered_data)
# Convert the recovered hexadecimal string to binary data
# Convert the recovered hexadecimal string to binary data
hex_string = str(recovered_data)  # Convert to a string if it's not already
if hex_string.startswith("0x"):
    hex_string = hex_string[2:]  # Remove the "0x" prefix

# print(hex_string)
# Sanitize the hex_string to remove non-hexadecimal characters

sanitized_hex_string = ''.join(filter(lambda x: x in '0123456789abcdef', hex_string))

binary_data = bytes.fromhex(sanitized_hex_string)
print(binary_data)
pattern = re.compile(b'(?P<text>[A-Za-z ]+)')

match = pattern.search(binary_data)
if match:
    extracted_text = match.group('text').decode('ascii')
    print(extracted_text)
else:
    print("Text not found in binary data")
# Decode the binary data as ASCII text

# decoded_text = binary_data.decode('ascii')
# print(decoded_text)
# extracted_message = decoded_text
# except UnicodeDecodeError:
#     print("Error: Failed to decode the data as ASCII text.")
# print(sanitized_hex_string)

# Check if the sanitized_hex_string is empty
# if not sanitized_hex_string:
#     print("Error: No valid hexadecimal data found.")
# else:
#     print(sanitized_hex_string)
#     binary_data = bytes.fromhex(sanitized_hex_string)

# # Decode the binary data as ASCII text
#     try:
#         decoded_text = binary_data.decode('ascii')
#         print(decoded_text)
#     except UnicodeDecodeError:
#         print("Error: Failed to decode the data as ASCII text.")
    # decoded_string = bytes.fromhex(sanitized_hex_string).decode('ascii', errors='ignore')

    # print(decoded_string)
    # binary_data = bytes.fromhex(sanitized_hex_string)

    # print(binary_data)

    # # Decode the binary data to text (assuming it's text data)
    # try:
    #     decoded_text = binary_data.decode('ascii')
    #     print("Extracted Message:")
    #     print(decoded_text)
    # except UnicodeDecodeError:

    #     print("Error: Failed to decode the extracted data as text.")
