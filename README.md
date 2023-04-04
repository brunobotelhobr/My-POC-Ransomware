# My-Python-Ransonware
POC of a Ransonware.
Wrning, this can encrypt for real your files, be careful.
## Setup
Install the requirements (Python 3)
```
pip3 install -r requirements.txt
```

## cc\service.py 
Is a simple FastAPI server that generates and returns a random encryption key for a given hostname. 
It has the following endpoints:

`/`: Returns an HTML homepage.
`/keys`: Returns a dictionary with the keys generated for each hostname.
`/keys`: (POST): Generates and returns an encryption key for the given hostname.
The server can be started by running main() function in the script.

To access the documentation access: `http://localhsot:8000/docs`

## ransonware.py
Is a command-line tool for encrypting or decrypting all files in a directory. 
It supports two actions: encrypt and decrypt. 
It uses the PyCryptodome library for AES encryption and decryption. 
It also has the option of obtaining the encryption key from a URL parameter.

To use the script, run python ransonware.py [directory] [action] [--url URL] [--key KEY], where:

[directory] is the directory containing the files to be processed.
[action] is the action to perform on the files (encrypt or decrypt).
[--url URL] is an optional URL parameter containing the encryption key.
[--key KEY] is an optional encryption or decryption key.
If the --url parameter is present, the script will obtain the key from the URL using a POST request to the specified endpoint.

Note that the encryption or decryption key must have exactly 16 characters.

## Examples
### Encrypt and Decrypt with password:
````
python ransonware.py example decrypt --key abcdef0123456789   
python ransonware.py example decrypt --key abcdef0123456789          
````

### Using the CC
Start the server:
```
python cc\service.py
```

Run the Ransonware 
```
python ransonware.py ./example encrypt --url "http://localhost:8000/"
```

Get the password on http://localhsot:8000/docs
```
python ransonware.py example decrypt --key abcdef0123456789   
```