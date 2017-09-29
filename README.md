# Extra Vinegar

Extra Vinegar is a Vigenère Cipher decryptor. Extra Vinegar utilizes the index of coincidence to decrypt. This program will not work with short ciphertexts as it doesn't have enough statistical data to accurately calculate the index of coincidence. 

If the program doesn't get the correct key you can play with the tested key size (-s) or you can overwrite the determined key size with (-k).

## Usage

```
usage: ExtraVinegar.py [-h] [-o OUTPUT] [-s SIZE] [-k KEYSIZE] InputFile

Extra Vinegar decrypts Vigenere ciphers with statistical analysis.

positional arguments:
  InputFile             Input file location containing ciphertext

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file location for plaintext
  -s SIZE, --size SIZE  Allows the maximum tested key size to be overridden
                        (default 10)
  -k KEYSIZE, --keysize KEYSIZE
                        Allows the calculated key size to be overridden
```

## Examples 

Decrypt:

`./ExtraVinegar.py TestInput.txt`

Decrypt and send plaintext to an output file:

`./ExtraVinegar.py TestInput.txt -o plaintext.txt`
