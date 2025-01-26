import sys
import os.path
import markdown

def file_converter(file):

    md = markdown.Markdown()
    file_name = os.path.splitext(file)[0]
    output_file = f"{file_name}.html"
    try:
        with open(file, mode="+r") as f:
            before_convert = f.read()
            result = md.convert(before_convert)
    except:
        return 1
    try:    
        with open(output_file, mode="+w") as f:
            f.write(result)
    except:
        return 1

    return 0

if __name__ == "__main__":
    
    args = sys.argv
    if len(args) < 2:
        print("ファイル名を入力してください")
    file = args[1]
    
    result = file_converter(file)
    
    if result > 0:
        print("変換失敗")
    else:
        print("変換成功")