import os
import argparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import pad, unpad
from PIL import Image


def encrypt_image(input_image, output_image, key_file):
    # Generate a random 256-bit (32 bytes) key using scrypt
    password = get_random_bytes(32)
    salt = get_random_bytes(16)
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)

    # Read input image
    image = Image.open(input_image)
    image_data = image.tobytes()

    # Encrypt image data
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(image_data, AES.block_size))

    # Write encrypted image
    with open(output_image, 'wb') as f:
        f.write(ct_bytes)

    # Save key to file
    with open(key_file, 'wb') as f:
        f.write(password + salt)


def decrypt_image(input_image, output_image, key_file):
    # Read key from file
    with open(key_file, 'rb') as f:
        key_data = f.read()
        password = key_data[:32]
        salt = key_data[32:]

    # Derive key from password and salt
    key = scrypt(password, salt, key_len=32, N=2**14, r=8, p=1)

    # Read encrypted image data
    with open(input_image, 'rb') as f:
        ct_bytes = f.read()

    # Decrypt image data
    cipher = AES.new(key, AES.MODE_CBC)
    pt_bytes = unpad(cipher.decrypt(ct_bytes), AES.block_size)

    # Write decrypted image data to output file
    with open(output_image, 'wb') as f:
        f.write(pt_bytes)

    print(f"Decrypted image saved to: {output_image}")


def main():
    parser = argparse.ArgumentParser(description='Image Encryption/Decryption')
    parser.add_argument('-e', '--encrypt', metavar='input_image', help='Encrypt an image')
    parser.add_argument('-d', '--decrypt', metavar='input_image', help='Decrypt an image')
    parser.add_argument('-o', '--output', metavar='output_image', help='Output filename for encrypted/decrypted image')
    parser.add_argument('-k', '--keyfile', metavar='key_file', help='File to save/load encryption key')

    args = parser.parse_args()

    if args.encrypt:
        if not args.output or not args.keyfile:
            print("Error: Please specify output image and key file")
            return
        encrypt_image(args.encrypt, args.output, args.keyfile)
        print(f"Image encrypted successfully. Encrypted image: {args.output}, Key file: {args.keyfile}")

    elif args.decrypt:
        if not args.output or not args.keyfile:
            print("Error: Please specify output image and key file")
            return
        decrypt_image(args.decrypt, args.output, args.keyfile)
        print(f"Image decrypted successfully. Decrypted image: {args.output}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
