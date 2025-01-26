import sys
import random

while True:

    sys.stdout.buffer.write(b"please input number n\n")
    sys.stdout.flush()

    n = int(sys.stdin.buffer.readline().decode().strip())
    sys.stdout.flush()

    sys.stdout.buffer.write(b"please input number m\n")
    sys.stdout.flush()

    m = int(sys.stdin.buffer.readline().decode().strip())
    sys.stdout.flush()
    
    if n < m:
        break
    else:
        continue

ans = random.randint(int(n), int(m))
sys.stdout.buffer.write(b"guess the number\n")
sys.stdout.flush()

while ans != int(sys.stdin.buffer.readline().decode().strip()):
    sys.stdout.buffer.write(b"your ans is failed\n")
    sys.stdout.buffer.write(b"guess the number\n")
    sys.stdout.flush()
    