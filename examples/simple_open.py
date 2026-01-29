"""Minimal demo of Python's open() for quick experimentation.

Run:
    python examples/simple_open.py

What it shows:
- Create/overwrite a file with 'w'
- Read the whole file with 'r'
- Append with 'a'
- Read lines as a list and print them with line numbers
- Simple FileNotFoundError handling
"""


import os
# Note: This example is tailored for Windows paths (C:/).
def main():
    # Define your base directory on C:
    # Note: Writing directly to C:\ often fails due to permissions. 
    # It's better to use a folder like C:\temp or your Documents.
    base_directory = "C:\\Users\\AALEKHYA"

    user_input = input("Enter filename: ").strip() or "demo.txt"
    
    # This combines "C:/" with the filename safely
    filename = os.path.join(base_directory, user_input)

    print(f"Target path: {filename}")

    # Now open() will always point to C:
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Sample text")
    print(f"Wrote to {filename}.")

    # Read and print whole contents
    with open(filename, "r", encoding="utf-8") as f:
        contents = f.read()
    print("--- file contents ---")
    print(contents.rstrip())
    print("---------------------")

    # Optionally append
    append = input("Text to append (leave blank to skip): ").strip()
    if append:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(append + "\n")
        print("Appended to file.")

    # Read lines and print with numbers
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File not found when trying to read lines (unexpected).")
        return

    print("--- lines with numbers ---")
    for i, line in enumerate(lines, start=1):
        print(f"{i}: {line.rstrip()}")
    print("--------------------------")

    # Demonstrate FileNotFoundError handling
    missing = "this_file_does_not_exist.txt"
    try:
        open(missing, "r").close()
        print(f"{missing} exists (unexpected).")
    except FileNotFoundError:
        print(f"Trying to open {missing}: FileNotFoundError caught (this is normal).")


if __name__ == "__main__":
    main()
