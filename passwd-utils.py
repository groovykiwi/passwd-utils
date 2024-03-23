import argparse
import requests
import hashlib
import random


# Colors
class c:
    red = "\033[91m"
    green = "\033[92m"
    gray = "\033[90m"
    bold = "\033[1m"
    end = "\033[0m"


# Arguments handling
parser = argparse.ArgumentParser()
parser.add_argument(
    "-b",
    "--breach",
    help="check if the password is in a breached database",
    metavar="password",
)
parser.add_argument(
    "-g",
    "--generate",
    help="converts the given password into a complex version",
    metavar="password",
)
args = parser.parse_args()


# Return content of api request, exit program on error
def getApiData(passwd):
    url = "https://api.pwnedpasswords.com/range/"
    res = requests.get(url + passwd)
    if res.status_code == 200:
        return res.text
    else:
        print("Error: Have I Been Pwnd sent an invalid response")
        exit()


def obfuscatePasswd(passwd):
    # Define a mapping of letters to similar-looking symbols
    symbolsMapping = {
        "a": ["@"],
        "b": ["8", "6", "ß"],
        "c": ["(", "{", "["],
        "d": [],
        "e": ["3", "€"],
        "f": ["ph"],
        "g": ["9"],
        "h": [],
        "i": ["1", "!", "|"],
        "j": [],
        "k": [],
        "l": ["1", "|", "£"],
        "m": [],
        "n": [],
        "o": ["0", "*"],
        "p": [],
        "q": ["9"],
        "r": [],
        "s": ["5", "$"],
        "t": ["7"],
        "u": [],
        "v": [],
        "w": ["uu", "2u"],
        "x": [],
        "y": [],
        "z": ["2"],
    }

    obfuscatedPasswd = ""
    for char in passwd.lower():  # Convert input to lowercase for easier mapping
        if char.isalpha():
            # Randomly choose one of the similar-looking symbols for the letter
            choices = symbolsMapping.get(char, [char])
            choices.append(char.upper())
            choices.append(char.lower())

            obfuscatedPasswd += random.choice(choices)
        elif char.isdigit():
            obfuscatedPasswd += str(
                random.randint(0, 9)
            )  # Replace digits with random digits
        else:
            obfuscatedPasswd += char  # Keep non-alphanumeric characters unchanged
    return obfuscatedPasswd


def main():
    # Breach Check
    if args.breach:
        # SHA-1 Password Hashing
        hashedPasswd = hashlib.sha1(args.breach.encode("utf-8")).hexdigest().upper()
        # Send first 5 bytes to the API (k-Anonymity)
        data = getApiData(hashedPasswd[:5])
        # Compare the tail of given password with all API returned hashes and print result
        for line in data.splitlines():
            if hashedPasswd[5:] == line.split(":")[0]:
                print(
                    f"\n{c.red}{args.breach}{c.end} was found in {c.red}{c.bold}{int(line.split(":")[1]):,}{c.end} data breaches"
                )
                return
        print(f"\n{c.green}{args.breach}{c.end} was not found in any data breaches")

    # Complex Password Generator
    elif args.generate:
        newPasswd = obfuscatePasswd(args.generate)
        print(
            "\nNew complex password:\n" + "-" * 21 + f"\n{c.green}\n{newPasswd}{c.end}"
        )
        if len(args.generate) < 14:
            print(
                f"\n{c.gray}[!] Try to make your password {c.red}14 characters{c.gray} or more. \nPassword length was found to be a primary factor in password strength by the NSIT.\n\
It takes {c.green}centuries{c.gray} to crack a 14 character password and only {c.red}days{c.gray} for a 10 character one."
            )


main()
