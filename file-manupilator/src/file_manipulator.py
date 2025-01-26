import sys
    
def reverse(inputfile, outputfile):
    try:
        with open(inputfile, mode="+r") as f:
            str = f.read()
            reverse_str = str[::-1]
            with open(outputfile, mode="+w") as outf:
                outf.write(reverse_str)
    except:
        print("file open error")
        return -1
    return 0

def copy(inputfile, outputfile):
    try:
        with open(inputfile, mode="+r") as f:
            str = f.read()
            with open(outputfile, mode="+w") as outf:
                outf.write(str)
    except:
        print("file open error")
        return -1
    return 0


def duplicate(inputfile, n):
    try:
        with open(inputfile, "+r") as f:
            str = f.read()
        with open(inputfile, "+a") as f:
            for _ in range(int(n)):
                f.write(str)
    except:
        print("file open error")
        return -1
    return 0

def replace(inputfile, needle, newstring):
    try:
        with open(inputfile, mode="+r") as f:
            str = f.read()
            new_str = str.replace(needle, newstring)
        with open(inputfile, mode="+w") as f:
            f.write(new_str)
    except:
        print("file open error")
        return -1
    return 0

if __name__ == "__main__":
    args = sys.argv


    command = args[1]
    result = 0

    if command == "reverse":
        if(len(args) != 4):
            exit()
        result = reverse(args[2], args[3])
    elif command == "copy":
        if(len(args) != 4):
            exit()
        result = copy(args[2], args[3])
    elif command == "duplicate-contents":
        if(len(args) != 4):
            exit()
        result = duplicate(args[2], args[3])
    elif command == "replace-string":
        if(len(args) != 5):
            exit()
        result = replace(args[2], args[3], args[4])
    else:
        print("input correct command\n"
              "---------------------\n"
              "reverse\n"
              "copy\n"
              "duplicate-contents\n"
              "replace-string\n")
        exit()

    if result < 0:
        print("failed\n")
    else:
        print("success\n")