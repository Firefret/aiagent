from functions.run_python_file import run_python_file
def test():
    print("should print the calculator's usage instructions")
    result = run_python_file("calculator", "main.py")
    print(result)

    print("should run the calculator... which gives a kinda nasty rendered result")
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)

    print("Should run the calculator tests... which should pass")
    result = run_python_file("calculator", "tests.py")
    print(result)

    print("this should return an error")
    result = run_python_file("calculator", "../main.py")
    print(result)

    print("this should return an error")
    result = run_python_file("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    test()
