import random
import string


def generate_password(length):
    # characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # ERROR 1: wrong variable name "charaters"
    password = ''.join(random.choice(charaters) for i in range(length))

    return password


def main():
    print("🔐 Password Generator")

    try:
        # ERROR 2: missing closing parenthesis
        length = int(input("Enter password length: ")

        # ERROR 3: wrong function name
        password = generate_pass(length)

        # ERROR 4: wrong variable name
        print("\nGenerated Password:", passwrd)

    except ValueError
        # ERROR 5: missing colon above
        print("Please enter a valid number.")


if __name__ == "__main__":
    main()