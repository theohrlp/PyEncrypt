import os
import gnupg
import io

#TODO   check if Skey is already decrypted
#TODO   delete Skey at the end
#TODO   

gpg = gnupg.GPG(gnupghome = '/home/theo/Desktop/2encreptPytemp')        # home dir for the gpg (any folder will do)

choice = input("Press 1 to encrypt or 2 to decrypt: ")

if choice=='1':

    symmetricOrAsymmetricEncrypt = input("Press 1 for symmetric encryption or 2 for asymmetric encryption: ")

    if symmetricOrAsymmetricEncrypt=='1':
        
        file2SymmeEncrLoc = input("Place here the full path to the location of the file you want to encrypt: ")     # path to the file you want to encrypt

        outFile = input("Place here the full path to the location you want the encrypted file to be: ")             # path to the file you encrypted

        passPhrase = input("Enter your password: ")

        with open(file2SymmeEncrLoc, 'rb') as f:
            data = gpg.encrypt_file(file=f, symmetric='AES256', passphrase=passPhrase, armor=False, recipients=None, output=outFile)

        print(data.ok)                          # If encryption succeeded, the returned object’s ok attribute is set to True
    
        print(data.status)                      # the status attribute provides more information as to the reason of failure (if there is one)
    
        print(data.stderr)                      # outputs to the standard stream

    
    elif symmetricOrAsymmetricEncrypt=='2':

        pubKeyLocation = input("Place here the full path to the location of the public key: ")                      # path to the public key

        keyData2 = open(pubKeyLocation).read()                                                                      # read the public key
    
        importPubKey = gpg.import_keys(keyData2)                                                                    # import that sucker
    
        print(importPubKey.counts)                                                                                  # if importPubKey.counts > 0 you imported that number of keys
    
        print(importPubKey.fingerprints)
    
        file2EncryptLocation = input("Place here the full path to the location of the file you want to encrypt: ")  # path to the file you want to encrypt
    
        outFile = input("Place here the full path to the location you want the encrypted file to be: ")              # path to the file you encrypted
    
        with open(file2EncryptLocation, 'rb') as f:
            encrypted_ascii_data = gpg.encrypt_file(f, importPubKey.fingerprints, always_trust = True, output=outFile)
    
        f.close()
    
        print(encrypted_ascii_data.ok)        # If encryption succeeded, the returned object’s ok attribute is set to True
    
        print(encrypted_ascii_data.status)    # the status attribute provides more information as to the reason of failure (if there is one)
    
        print(encrypted_ascii_data.stderr)    # outputs to the standard stream

    else:
        print("Please select either 1 or 2. ")

elif choice=='2':

    print("The program will first decrypt the secret key (which is encrypted symmetrically), then it will import that key and decrypt the given file (which is encrypted asymmetrically)")

    encryptedSecrKeyLocation = input("Place here the full path to the location of the encrypted secret key: ")           # path to the (encrypted) secret key

    decryptedSecrKeyLocation = input("Place here the full path to the location you want the decrypted key to be: ")      # path to the (decrypted) secret key

    passPhraseForSymmetric = input("Enter the password for the decryption of the secret key: ")                          # pass for the decryption

    with open(encryptedSecrKeyLocation, 'rb') as f:
        decrypted_data = gpg.decrypt_file(file=f, passphrase=passPhraseForSymmetric, always_trust = True, output=decryptedSecrKeyLocation)
    f.close()

    keyData = open(decryptedSecrKeyLocation).read()                                                                      # reads the decrypted secret key 

    print(keyData)

    import_result = gpg.import_keys(keyData)                                                                             # imports the secret key

    print(import_result.count)                                                                                           # if import_result.count > 0 you imported that number of keys

    print(import_result.fingerprints)                                                                                    # fingerprints of said keys

    encryptedFileLocation = input("Place here the full path to the location of the file you want to decrypt: ")          # path to the file you want to decrypt

    decryptedFileLocation = input("Place here the full path to the location you want the decrypted file to be: ")        # path to the output file (thats the file the program will put the decrypted data)

    passPhraseForAsymmetric = input("Enter the password for the decryption of the file: ")                               # pass for the decryption

    # rb stands for read binary
    with open(encryptedFileLocation, 'rb') as f:
        decrypted_data = gpg.decrypt_file(file=f, passphrase=passPhraseForAsymmetric, always_trust = True, output=decryptedFileLocation) # always_trust === Skip key validation and assume that used keys are always fully trusted
    f.close()

    print(decrypted_data.ok)        # If decryption succeeded, the returned object’s ok attribute is set to True

    print(decrypted_data.status)    # the status attribute provides more information as to the reason of failure (if there is one)

    print(decrypted_data.stderr)    # outputs to the standard stream

else:
    print("Please select either 1 or 2. ")


