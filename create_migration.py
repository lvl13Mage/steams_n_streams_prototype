import subprocess

def prompt_for_message():
    message = input("Enter the revision message: ")
    return message

def create_revision(message):
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", message])

def main():
    message = prompt_for_message()
    create_revision(message)

if __name__ == "__main__":
    main()