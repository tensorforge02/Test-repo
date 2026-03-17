import random
import string


def generate_password(length):
    # characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation

    # generate password
    password = ''.join(random.choice(characters) for i in range(length))

    return password


def main():
    print("🔐 Password Generator")

    try:
        length = int(input("Enter password length: "))
        password = generate_password(length)
        print("\nGenerated Password:", password)

    except ValueError:
        print("Please enter a valid number.")


if __name__ == "__main__":
    main()