import base64
import base91
import argparse
import sys

def title():
    print("""  ______                   _     __             ____  ____    
.' ____ \                 (_)   /  |           |_   ||   _|   
| (___ \_|  _ .--..--.    __    `| |    .---.    | |__| |     
 _.____`.  [ `.-. .-. |  [  |    | |   / /__\\\\    |  __  |     
| \____) |  | | | | | |   | |   _| |_  | \__., _| |  | |_    
 \______.' [___||__||__] [___] |_____|  '.__.' |____||____| """)
    print("此脚本针对CTF中较大数据量的Base加密，支持单个解密、循环解密并自动将解码写入文件")

# 检查文件
def file_read(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"未找到文件：{filename}")
        return None
    except PermissionError:
        print("无法读取文件（无权限访问）")
        return None

# Base64解码函数
def base64_decode(encoded_text):
    try:
        decoded_text = base64.b64decode(encoded_text).decode()
        print(decoded_text)
        return decoded_text
    except base64.binascii.Error as e:
        print(f"Base解码错误：{e}")
# Base32解码函数
def base32_decode(encoded_text):
    try:
        decoded_text = base64.b32decode(encoded_text).decode()
        print(decoded_text)
        return decoded_text
    except base64.binascii.Error as e:
        print(f"Base解码错误：{e}")
# Base16解码函数
def base16_decode(encoded_text):
    try:
        decoded_text = base64.b16decode(encoded_text).decode()
        print(decoded_text)
        return decoded_text
    except base64.binascii.Error as e:
        print(f"Base解码错误：{e}")
# Base91解码函数
def base91_decode(encoded_text):
    try:
        decoded_text = base91.decode(encoded_text).decode()
        print(decoded_text)
        return decoded_text
    except base91.binascii.Error as e:
        print(f"Base解码错误：{e}")
# 循环解码函数
def base_repeat(decoded_text,num,times=0):
    decode_functions = {
        64: base64_decode,
        32: base32_decode,
        16: base16_decode,
        91: base91_decode
    }
    x = True
    while x :
        if num not in decode_functions.keys():
            print(int(input("工具中并没有此编码，请重新输入:")))
        else:
            x = False
    while True:
        try:
            decoded_text = base64.b64decode(decoded_text)
            times += 1
        except:
            print(f'Base{num}共decode了{times}次，最终解码结果如下:')
            print(str(decoded_text, 'utf-8'))
            return decoded_text

if __name__ == "__main__":
    title()
    parser = argparse.ArgumentParser(description="decode-Tools V1.0")
    parser.add_argument('-r', action='store', dest='repeat', help='读取对应文件，并对内容进行n次Base解码')
    parser.add_argument('-b16', action='store', dest='Base16decode', help='读取对应文件，并对内容进行Base16解码')
    parser.add_argument('-b32', action='store', dest='Base32decode', help='读取对应文件，并对内容进行Base32解码')
    parser.add_argument('-b64', action='store', dest='Base64decode', help='读取对应文件，并对内容进行Base64解码')
    parser.add_argument('-b91', action='store', dest='Base91decode', help='读取对应文件，并对内容进行Base91解码')
    args = parser.parse_args()

    # 处理重复解码参数
    if args.repeat:
        num = int(input("输入需要重复解码的Base类型,暂时支持64、32、16、91\nBase类型 >>>"))
        file_content = file_read(args.repeat)
        decoded_text = base_repeat(file_content,num)

    # 处理单个解码参数
    try:
        if args.Base64decode:
            file_content = file_read(args.Base64decode)
            decoded_text = base64_decode(file_content)
        if args.Base32decode:
            file_content = file_read(args.Base32decode)
            decoded_text = base32_decode(file_content)
        if args.Base16decode:
            file_content = file_read(args.Base16decode)
            decoded_text = base16_decode(file_content)
        if args.Base91decode:
            file_content = file_read(args.Base91decode)
            decoded_text = base91_decode(file_content)
    except KeyboardInterrupt:
        print("Ctrl + C 手动终止了进程")
        sys.exit()
    except BaseException as e:
        err = str(e)
        print('脚本详细报错：' + err)
        sys.exit(0)

    if decoded_text :
        try:
            if type(decoded_text) == bytes:
                with open("output.txt", 'wb') as file:
                    file.write(decoded_text)
            else:
                with open("output.txt", 'w') as file:
                    file.write(decoded_text)
        except Exception as e:
            print(f"文件并没有被写入，发生错误为：{e}")