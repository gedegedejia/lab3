import csv

def read_hashes_from_csv(file_path, column_name):
    """从CSV文件中读取特定列的所有哈希值"""
    hashes = set()
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if column_name in row:
                hashes.add(row[column_name])
    return hashes

def read_hashes_from_txt(file_path):
    """从文本文件中读取所有行作为哈希值"""
    with open(file_path, mode='r', encoding='utf-8') as txtfile:
        return {line.strip() for line in txtfile}

def write_missing_hashes_to_file(missing_hashes, output_file):
    """将缺失的哈希值写入文件"""
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        for hash_value in missing_hashes:
            outfile.write(f"{hash_value}\n")

def main():
    # 文件路径
    csv_file = 'updated_transactions.csv'
    txt_file = 'eth_hash.txt'
    add_file = 'add.txt'

    # 读取哈希值
    csv_hashes = read_hashes_from_csv(csv_file, 'Hash')
    print(len(csv_hashes))
    
    txt_hashes = read_hashes_from_txt(txt_file)
    print(len(txt_hashes))

    # 找出在txt中但在csv中缺失的哈希值
    missing_hashes = txt_hashes - csv_hashes

    # 如果有缺失的哈希值，则写入add.txt
    if missing_hashes:
        print(f"Found {len(missing_hashes)} missing hash(es). Writing to {add_file}.")
        write_missing_hashes_to_file(missing_hashes, add_file)
    else:
        print("No missing hashes found.")

if __name__ == "__main__":
    main()