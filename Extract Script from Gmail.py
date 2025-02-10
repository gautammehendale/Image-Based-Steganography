import cv2
import numpy as np

def text_to_bits(text):
    """Convert a text message into a bitstream."""
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def embed_message(cover_image, secret_message):
    if cover_image is None:
        raise ValueError("Failed to load the cover image.")

    # Convert the secret message to a bitstream
    secret_bits = text_to_bits(secret_message)

    # Get the dimensions of the cover image
    height, width, channels = cover_image.shape

    # Ensure that the secret message can fit in the cover image
    max_capacity = height * width * channels
    if len(secret_bits) > max_capacity:
        raise ValueError("The secret message is too large to be embedded in the cover image.")

    # Create a copy of the cover image
    stego_image = cover_image.copy()

    # Embed the secret message into the cover image using LSB
    secret_index = 0
    for row in range(height):
        for col in range(width):
            for channel in range(channels):
                if secret_index < len(secret_bits):
                    pixel_value = stego_image[row, col, channel]
                    new_pixel_value = pixel_value & 0xFE | int(secret_bits[secret_index])
                    stego_image[row, col, channel] = new_pixel_value
                    secret_index += 1

    return stego_image

def extract_message(stego_image):
    if stego_image is None:
        raise ValueError("Failed to load the steganographic image.")

    # Get the dimensions of the stego image
    height, width, channels = stego_image.shape

    # Initialize an empty bitstream for the extracted message
    extracted_bits = ""

    for row in range(height):
        for col in range(width):
            for channel in range(channels):
                pixel_value = stego_image[row, col, channel]
                # Extract the LSB of the pixel value
                extracted_bits += str(pixel_value & 1)

    return extracted_bits

def bits_to_text(bits):
    """Convert a bitstream into bytes."""
    # Ensure the bitstream has a length that is a multiple of 8
    padding = len(bits) % 8
    if padding > 0:
        bits = bits[:-padding]

    # Convert the bitstream to bytes and return
    byte_data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
    return byte_data


# Load the cover image
cover_image = cv2.imread("car_3.jpg")

if cover_image is not None:
    # Define the secret message
    secret_message = "Hello, this is a secret message!"

    # Embed the secret message into the cover image
    stego_image = embed_message(cover_image, secret_message)

    # Save the steganographic image
    cv2.imwrite("stego_image.png", stego_image)

    # Load the steganographic image
    stego_image = cv2.imread("stego_image.png")

    # Extract the hidden message
    extracted_bits = extract_message(stego_image)

    # Convert the extracted bits back to text
    extracted_message = bits_to_text(extracted_bits)

    print("Extracted Message:", extracted_message)
else:
    print("Failed to load the cover image.")
