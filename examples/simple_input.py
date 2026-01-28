"""Minimal demonstration of Python's input() function.

Run:
    python examples/simple_input.py

What it shows:
- Prompt for a name
- Read one line and echo it back
- Exit on `/quit` or EOF
"""


def main():
    name = input("Name: ").strip() or "Guest"
    print("line no 15 executed") 
    print(f"Hello, {name}!")

    



if __name__ == "__main__":
    main()
