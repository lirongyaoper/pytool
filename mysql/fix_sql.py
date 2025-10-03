#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MySQL 8.0 SQL文件兼容性修复工具

此脚本用于修复MySQL SQL导出文件中的兼容性问题：
1. 移除整数类型的显示宽度（如 int(11) -> int）
2. 移除decimal/float类型的UNSIGNED属性

作者: Assistant
日期: 2025
"""

import re
import sys
import os
from datetime import datetime

def fix_sql_file(input_file, output_file=None, backup=True):
    """
    修复SQL文件中的MySQL 8.0兼容性问题
    
    Args:
        input_file (str): 输入的SQL文件路径
        output_file (str): 输出的SQL文件路径，默认为输入文件名_fixed.sql
        backup (bool): 是否创建原文件备份
    
    Returns:
        dict: 修复统计信息
    """
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：文件 {input_file} 不存在！")
        return None
    
    # 确定输出文件名
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}_fixed.sql"
    
    print(f"正在修复 {input_file}...")
    print(f"输出文件: {output_file}")
    
    try:
        # 读取文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建备份（如果需要）
        if backup and input_file != output_file:
            backup_file = f"{input_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已创建备份文件: {backup_file}")
        
        # 统计修复次数
        stats = {
            'int_fixes': 0,
            'decimal_fixes': 0,
            'float_fixes': 0,
            'file_size_before': len(content),
            'file_size_after': 0
        }
        
        # 1. 修复整数类型的显示宽度问题
        # 匹配各种整数类型：tinyint(数字), smallint(数字), mediumint(数字), int(数字), bigint(数字)
        int_patterns = [
            (r'\btinyint\(\d+\)', 'tinyint'),
            (r'\bsmallint\(\d+\)', 'smallint'), 
            (r'\bmediumint\(\d+\)', 'mediumint'),
            (r'\bint\(\d+\)', 'int'),
            (r'\bbigint\(\d+\)', 'bigint')
        ]
        
        for pattern, replacement in int_patterns:
            matches = re.findall(pattern, content, flags=re.IGNORECASE)
            stats['int_fixes'] += len(matches)
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # 2. 修复decimal类型的UNSIGNED问题
        decimal_pattern = r'\b(decimal\(\d+,\d+\))\s+unsigned'
        decimal_matches = re.findall(decimal_pattern, content, flags=re.IGNORECASE)
        stats['decimal_fixes'] = len(decimal_matches)
        content = re.sub(decimal_pattern, r'\1', content, flags=re.IGNORECASE)
        
        # 3. 修复float类型的UNSIGNED问题
        float_pattern = r'\b(float(?:\(\d+,\d+\))?)\s+unsigned'
        float_matches = re.findall(float_pattern, content, flags=re.IGNORECASE)
        stats['float_fixes'] = len(float_matches)
        content = re.sub(float_pattern, r'\1', content, flags=re.IGNORECASE)
        
        # 记录修复后的文件大小
        stats['file_size_after'] = len(content)
        
        # 写入修复后的文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 输出修复统计
        print(f"\n修复完成！")
        print(f"=" * 50)
        print(f"修复统计:")
        print(f"- 整数显示宽度问题: {stats['int_fixes']} 处")
        print(f"- decimal UNSIGNED问题: {stats['decimal_fixes']} 处")
        print(f"- float UNSIGNED问题: {stats['float_fixes']} 处")
        print(f"- 总计修复: {stats['int_fixes'] + stats['decimal_fixes'] + stats['float_fixes']} 处")
        print(f"- 文件大小变化: {stats['file_size_before']} -> {stats['file_size_after']} 字节")
        print(f"=" * 50)
        print(f"修复后的文件保存为: {output_file}")
        
        return stats
        
    except Exception as e:
        print(f"错误：处理文件时出现异常：{e}")
        return None

def show_help():
    """显示帮助信息"""
    help_text = """
MySQL 8.0 SQL文件兼容性修复工具使用说明

基本用法：
    python3 fix_sql.py <输入文件> [输出文件]

参数说明：
    输入文件    必需，要修复的SQL文件路径
    输出文件    可选，修复后的文件路径（默认为输入文件名_fixed.sql）

示例：
    # 修复单个文件，输出为 backup.sql_fixed.sql
    python3 fix_sql.py backup.sql
    
    # 修复文件并指定输出文件名
    python3 fix_sql.py backup.sql backup_mysql8.sql
    
    # 显示帮助信息
    python3 fix_sql.py --help

修复内容：
    1. 移除整数类型显示宽度：int(11) -> int
    2. 移除decimal类型UNSIGNED：decimal(8,2) unsigned -> decimal(8,2)
    3. 移除float类型UNSIGNED：float unsigned -> float

注意事项：
    - 脚本会自动创建原文件备份（带时间戳）
    - 支持UTF-8编码的SQL文件
    - 修复后的文件兼容MySQL 8.0+版本
    """
    print(help_text)

def main():
    """主函数"""
    # 检查命令行参数
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        show_help()
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 执行修复
    result = fix_sql_file(input_file, output_file)
    
    if result is None:
        sys.exit(1)
    else:
        print(f"\n修复成功完成！现在可以使用修复后的SQL文件进行数据导入。")
        print(f"导入命令示例：")
        output_name = output_file if output_file else f"{os.path.splitext(input_file)[0]}_fixed.sql"
        print(f"mysql -u username -p database_name < {output_name}")

if __name__ == "__main__":
    main()
