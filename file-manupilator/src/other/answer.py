import sys

food = sys.stdin.buffer.readline()
print(f"your favorite food is {food.decode()}\n")
sys.stdin.flush()