import sys
from selenium.webdriver import Firefox

if __name__ == "__main__":
    # Access command-line arguments
    arg1 = sys.argv[1] if len(sys.argv) > 1 else None
    arg2 = sys.argv[2] if len(sys.argv) > 2 else None
    print("Argument 1:", arg1)
    print("Argument 2:", arg2)