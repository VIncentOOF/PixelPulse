import io
import hashlib
import sys
import os
import time

print("  ")
print("Python Hash-Cracker")
print("Version 4.0 Stable")


def info():
    print(" ")
    print("Information:")
    print("[*] Options:")
    print("[*] (-h) Hash")
    print("[*] (-t) Type [See supported hashes]")
    print("[*] (-w) Wordlist")
    print("[*] (-n) Numbers bruteforce")
    print("[*] (-v) Verbose [{WARNING}Slows cracking down!]\n")
    print("[*] Examples:")
    print("[>] ./Hash-Cracker.py -h <hash> -t md5 -w DICT.txt")
    print("[>] ./Hash-Cracker.py -h <hash> -t sha384 -n -v")
    print("[*] Supported Hashes:")
    print("[>] md5, sha1, sha224, sha256, sha384, sha512")
    print("[*] That's all folks!\n")


def checkOS():
    if os.name == "nt":
        operatingSystem = "Windows"
    elif os.name == "posix":
        operatingSystem = "posix"
    else:
        operatingSystem = "Unknown"
    return operatingSystem


class hashCracking:

    def hashCrackWordlist(self, userHash, hashType, wordlist, verbose, bruteForce=False):
        start = time.time()
        solved = False
        self.lineCount = 0
        if "md5" in hashType:
            h = hashlib.md5
        elif "sha1" in hashType:
            h = hashlib.sha1
        elif "sha224" in hashType:
            h = hashlib.sha224
        elif "sha256" in hashType:
            h = hashlib.sha256
        elif "sha384" in hashType:
            h = hashlib.sha384
        elif "sha512" in hashType:
            h = hashlib.sha512
        else:
            print("[-] Is \'%s\' a supported hash type?" % hashType)
            exit()
        if bruteForce is True:
            while True:
                line = "%s" % self.lineCount
                line.strip()
                numberHash = h(line.encode()).hexdigest().strip()
                if verbose is True:
                    sys.stdout.write('\r' + str(line) + ' ' * 20)
                    sys.stdout.flush()
                if numberHash.strip() == userHash.strip().lower():
                    end = time.time()
                    print("\n[+] Hash is: %s" % self.lineCount)
                    print("[*] Time: %s seconds" % round((end - start), 2))
                    savedHashFile = open('SavedHashes.txt', 'a+')
                    for solvedHash in savedHashFile:
                        if numberHash in solvedHash.split(":")[1].strip():
                            solved = True
                    if solved is False:
                        print("[*] Hash to SavedHashes.txt")
                        savedHashFile.write('%s:{}'.format(numberHash) % line)
                        savedHashFile.write('\n')
                    savedHashFile.close()
                    exit()
                else:
                    self.lineCount = self.lineCount + 1
        else:
            with open(wordlist, "r") as infile:
                for line in infile:
                    line = line.strip()
                    encodeline= str.encode(line)
                    lineHash = h(encodeline).hexdigest()
                    if verbose is True:
                        sys.stdout.write('\r' + str(line) + ' ' * 20)
                        sys.stdout.flush()

                    if str(lineHash) == str(userHash.lower()):
                        end = time.time()
                        print("\n[+] Hash is: %s" % line)
                        print("[*] Words tried: %s" % self.lineCount)
                        print("[*] Time: %s seconds" % round((end - start), 2))
                        savedHashFile = open('SavedHashes.txt', 'a+')
                        for solvedHash in savedHashFile:
                            if lineHash in solvedHash.split(":")[1].strip():
                                solved = True
                        if solved is False:
                            print("[*] Hash to SavedHashes.txt")
                            savedHashFile.write('%s:{}'.format(lineHash) % line)
                            savedHashFile.write('\n')
                        savedHashFile.close()
                        exit()
                    else:
                        self.lineCount = self.lineCount + 1

            end = time.time()
            print("\n[-] Cracking Failed")
            print("[*] Reached end of wordlist")
            print("[*] Words tried: %s" % self.lineCount)
            print("[*] Time: %s seconds" % round((end - start), 2))
            exit()


def main():
    hashType = None
    userHash = None
    wordlist = None
    verbose = None
    numbersBruteForce = False

    print("[Running on %s]\n" % checkOS())

    info_choice = input("Would you like to see the info? (y/n): ").strip().lower()
    if info_choice == 'y':
        info()
        sys.exit()

    hashType = input("Enter the hash type (md5, sha1, sha224, sha256, sha384, sha512): ").strip().lower()
    userHash = input("Enter the hash: ").strip().lower()
    wordlist = input("Enter the path to the wordlist: ").strip()
    verbose_choice = input("Enable verbose mode? (y/n): ").strip().lower()
    verbose = verbose_choice == 'y'
    brute_force_choice = input("Use numbers brute force? (y/n): ").strip().lower()
    numbersBruteForce = brute_force_choice == 'y'

    if not (hashType and userHash):
        print('[*] You must provide both the hash type and the hash')
        sys.exit()

    # looks through saved hash file instead of hashing all Wordlist entries
    with open('SavedHashes.txt', 'a+') as savedHashFile:
        for solvedHash in savedHashFile:
            solvedHash = solvedHash.split(":")
            if userHash.lower() == solvedHash[1].strip():
                print("[*] Saved Hash is: %s" % solvedHash[0])
                exit()
        else:
            print("[*] Hash: %s" % userHash)
            print("[*] Hash type: %s" % hashType)
            print("[*] Wordlist: %s" % wordlist)
            print("[+] Cracking...")
            try:
                h = hashCracking()
                h.hashCrackWordlist(userHash, hashType, wordlist, verbose, bruteForce=numbersBruteForce)

            except IndexError:
                print("\n[-] Hash not cracked:")
                print("[*] Reached end of wordlist")
                print("[*] Try another wordlist")
                print("[*] Words tried: %s" % h.lineCount)

            except KeyboardInterrupt:
                print("\n[Exiting...]")
                print("Words tried: %s" % h.lineCount)

            except IOError as e:
                print("\n[-] Couldn't find wordlist")
                print("[*] Is this right?")
                print("[>] %s" % wordlist)


if __name__ == "__main__":
    main()

