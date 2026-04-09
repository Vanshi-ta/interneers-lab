import os
import subprocess
import sys
import socket

def check_mongo():
    s = socket.socket()
    try:
        s.connect(("localhost", 27019))
        s.close()
        return True
    except:
        return False
    
def run_tests():
    print("Starting regression test check...")

    # Set test environment
    os.environ["ENV"] = "test"

    try:
        result = subprocess.run(
            [sys.executable, "manage.py", "test"],
            check=True
        )

        print("All tests passed! No regressions detected.")

    except subprocess.CalledProcessError:
        print("Tests failed! Regression detected.")
        sys.exit(1)

if __name__ == "__main__":
    if not check_mongo():
        print("MongoDB is not running on localhost:27017")
        print("Start MongoDB before running tests")
        sys.exit(1)
    run_tests()