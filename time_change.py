import csv
from datetime import datetime

# 更新日期时间格式以匹配实际的数据格式
date_format = "%d/%m/%Y - %H:%M:%S"  # 日/月/年 格式

# 打开原始CSV文件并读取内容
with open('transactions.csv', mode='r', newline='', encoding='utf-8') as infile, \
     open('data.csv', mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)  # 使用原始的字段名
    
    writer.writeheader()  # 写入表头
    
    for row in reader:
        try:
            # 尝试转换 'TimeStamp' 列为 Unix 时间戳
            dt_object = datetime.strptime(row['TimeStamp'], date_format)
            unix_timestamp = int(dt_object.timestamp())
            row['TimeStamp'] = str(unix_timestamp)
        except ValueError as e:
            print(f"无法解析时间戳 {row['TimeStamp']}，错误信息：{e}")
            # 如果转换失败，可以选择保留原始值或设置一个默认值
            row['TimeStamp'] = row['TimeStamp']  # 保持原样
            print(f"已保留原始值 {row['TimeStamp']}")
        
        # 写入整行数据到新的CSV文件
        writer.writerow(row)

print("转换完成，已保存至 'data.csv'")