import base64
import argparse

def base64_encode(text: str) -> str:
    """Base64 编码字符串"""
    encoded_bytes = base64.b64encode(text.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def base64_decode(encoded_text: str) -> str:
    """Base64 解码字符串"""
    decoded_bytes = base64.b64decode(encoded_text.encode('utf-8'))
    return decoded_bytes.decode('utf-8')

def file_to_base64(file_path: str) -> str:
    """将文件内容转为 Base64"""
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    return base64.b64encode(file_bytes).decode('utf-8')

def base64_to_file(encoded_str: str, output_file: str):
    """将 Base64 字符串写入文件"""
    decoded_bytes = base64.b64decode(encoded_str.encode('utf-8'))
    with open(output_file, 'wb') as file:
        file.write(decoded_bytes)

def main():
    parser = argparse.ArgumentParser(description="Base64 编码/解码工具")
    parser.add_argument('--encode', '-e', help="编码字符串")
    parser.add_argument('--decode', '-d', help="解码字符串")
    parser.add_argument('--file-encode', '-fe', help="编码文件")
    parser.add_argument('--file-decode', '-fd', help="解码 Base64 并保存为文件")
    parser.add_argument('--output', '-o', help="输出文件路径（用于文件解码）")

    args = parser.parse_args()

    if args.encode:
        print("Base64 编码结果:", base64_encode(args.encode))
    elif args.decode:
        print("Base64 解码结果:", base64_decode(args.decode))
    elif args.file_encode:
        print("文件 Base64 编码结果:", file_to_base64(args.file_encode))
    elif args.file_decode and args.output:
        base64_to_file(args.file_decode, args.output)
        print(f"解码成功，已保存到: {args.output}")
    else:
        print("请提供正确的参数，使用 -h 查看帮助")

if __name__ == "__main__":
    main()