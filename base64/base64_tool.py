import base64
import argparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES
import sys
import os
# 命令行编码：python base64_tool.py -e "hello world"

# 命令行解码：python base64_tool.py -d "aGVsbG8gd29ybGQ="

# 启动GUI：python base64_tool.py --gui
class Base64Tool:
    def __init__(self):
        self.setup_cli()
        
    def setup_cli(self):
        """设置命令行参数解析"""
        parser = argparse.ArgumentParser(description="Base64 编码/解码工具")
        parser.add_argument('--encode', '-e', help="编码字符串")
        parser.add_argument('--decode', '-d', help="解码字符串")
        parser.add_argument('--file-encode', '-fe', help="编码文件")
        parser.add_argument('--file-decode', '-fd', help="解码 Base64 并保存为文件")
        parser.add_argument('--output', '-o', help="输出文件路径（用于文件解码）")
        parser.add_argument('--gui', action='store_true', help="启动图形界面")

        args = parser.parse_args()
        
        if args.gui or len(sys.argv) == 1:
            self.launch_gui()
        else:
            self.handle_cli(args)
    
    def handle_cli(self, args):
        """处理命令行操作"""
        if args.encode:
            print("Base64 编码结果:", self.base64_encode(args.encode))
        elif args.decode:
            print("Base64 解码结果:", self.base64_decode(args.decode))
        elif args.file_encode:
            print("文件 Base64 编码结果:", self.file_to_base64(args.file_encode))
        elif args.file_decode and args.output:
            self.base64_to_file(args.file_decode, args.output)
            print(f"解码成功，已保存到: {args.output}")
        else:
            print("请提供正确的参数，使用 -h 查看帮助")
    
    def base64_encode(self, text: str) -> str:
        """Base64 编码字符串"""
        encoded_bytes = base64.b64encode(text.encode('utf-8'))
        return encoded_bytes.decode('utf-8')
    
    def base64_decode(self, encoded_text: str) -> str:
        """Base64 解码字符串"""
        try:
            decoded_bytes = base64.b64decode(encoded_text.encode('utf-8'))
            return decoded_bytes.decode('utf-8')
        except Exception:
            return "错误: 无效的Base64字符串"
    
    def file_to_base64(self, file_path: str) -> str:
        """将文件内容转为 Base64"""
        try:
            with open(file_path, 'rb') as file:
                file_bytes = file.read()
            return base64.b64encode(file_bytes).decode('utf-8')
        except Exception as e:
            return f"错误: {str(e)}"
    
    def base64_to_file(self, encoded_str: str, output_file: str):
        """将 Base64 字符串写入文件"""
        try:
            decoded_bytes = base64.b64decode(encoded_str.encode('utf-8'))
            with open(output_file, 'wb') as file:
                file.write(decoded_bytes)
            return True
        except Exception as e:
            return False
    
    def launch_gui(self):
        """启动图形用户界面"""
        self.root = TkinterDnD.Tk()
        self.root.title("Base64 编码/解码工具")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # 输入标签
        ttk.Label(main_frame, text="输入:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # 输入文本框
        self.input_text = scrolledtext.ScrolledText(main_frame, width=80, height=10)
        self.input_text.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.input_text.drop_target_register(DND_FILES)
        self.input_text.dnd_bind('<<Drop>>', self.on_file_drop)
        
        # 模式选择
        ttk.Label(main_frame, text="模式:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.mode = tk.StringVar(value="encode")
        ttk.Radiobutton(main_frame, text="编码", variable=self.mode, value="encode").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(main_frame, text="解码", variable=self.mode, value="decode").grid(row=2, column=2, sticky=tk.W)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="执行转换", command=self.perform_conversion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="从文件加载", command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存到文件", command=self.save_to_file).pack(side=tk.LEFT, padx=5)
        
        # 输出标签
        ttk.Label(main_frame, text="输出:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        
        # 输出文本框
        self.output_text = scrolledtext.ScrolledText(main_frame, width=80, height=10)
        self.output_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.root.mainloop()
    
    def on_file_drop(self, event):
        """处理文件拖放事件"""
        file_path = event.data.strip('{}')
        if os.path.isfile(file_path):
            self.load_file_content(file_path)
    
    def load_file_content(self, file_path):
        """加载文件内容到输入框"""
        try:
            if self.mode.get() == "encode":
                # 对于编码模式，直接读取二进制内容并编码
                with open(file_path, 'rb') as f:
                    content = f.read()
                base64_content = base64.b64encode(content).decode('utf-8')
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, base64_content)
                self.mode.set("decode")  # 自动切换到解码模式
                self.status_var.set(f"已加载并编码文件: {os.path.basename(file_path)}")
            else:
                # 对于解码模式，尝试解码文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, content)
                self.status_var.set(f"已加载文件: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件: {str(e)}")
    
    def perform_conversion(self):
        """执行编码或解码操作"""
        input_content = self.input_text.get(1.0, tk.END).strip()
        
        if not input_content:
            messagebox.showwarning("警告", "请输入要处理的内容")
            return
        
        try:
            if self.mode.get() == "encode":
                result = self.base64_encode(input_content)
            else:
                result = self.base64_decode(input_content)
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)
            self.status_var.set("转换完成")
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")
    
    def clear_text(self):
        """清空输入和输出文本框"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("已清空")
    
    def load_from_file(self):
        """从文件加载内容"""
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[("所有文件", "*.*"), ("文本文件", "*.txt")]
        )
        
        if file_path:
            self.load_file_content(file_path)
    
    def save_to_file(self):
        """保存输出内容到文件"""
        output_content = self.output_text.get(1.0, tk.END).strip()
        
        if not output_content:
            messagebox.showwarning("警告", "没有内容可保存")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                self.status_var.set(f"已保存到: {file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件时发生错误: {str(e)}")

if __name__ == "__main__":
    Base64Tool()