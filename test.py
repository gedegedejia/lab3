import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
from tqdm import tqdm
import os

CHECKPOINT_FILE = 'checkpoint.txt'

def load_checkpoint():
    """Load the list of processed hashes from checkpoint file."""
    if not os.path.exists(CHECKPOINT_FILE):
        return set()
    with open(CHECKPOINT_FILE, 'r') as f:
        return set(line.strip() for line in f)

def save_checkpoint(hash_value):
    """Save the hash to the checkpoint file."""
    with open(CHECKPOINT_FILE, 'a') as f:
        f.write(f"{hash_value}\n")

if __name__ == '__main__':
    try:
        # Load already processed hashes
        processed_hashes = load_checkpoint()

        driver = uc.Chrome()
        
        # 读取哈希列表
        with open('eth_hash.txt', 'r') as file:
            hash_list = [line.strip() for line in file if line.strip()]

        # 过滤掉已经处理过的哈希值
        hash_list = [h for h in hash_list if h not in processed_hashes]

        with open('transactions.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            # 如果文件为空，则写入表头
            if os.stat('transactions.csv').st_size == 0:
                writer.writerow(['Hash', 'From', 'To', 'Transaction Amount', 'TimeStamp', 'Fee'])

            for hash_value in tqdm(hash_list, desc='Processing transactions', unit='tx'):
                try:
                    driver.get(f'https://blockexplorer.one/ethereum/mainnet/tx/{hash_value}')
                    
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//td[@class="fromContent"]/div/a')))
                    hash_elem = driver.find_element(By.XPATH, './/td/a')
                    from_address = driver.find_element(By.XPATH, './/td[@class="fromContent"]/div/a').get_attribute('href')
                    to_address = driver.find_element(By.XPATH, './/td[@class="toContent"]/div/a').get_attribute('href')
                    amount = driver.find_element(By.XPATH, './/td[@class="amountTransacted"]/b').text
                    date = driver.find_element(By.XPATH, './/td[@class="dateTime tooltip"]/span').text
                    fee = driver.find_element(By.XPATH, './/td[@class="fee"]/div').text

                    writer.writerow([hash_elem.get_attribute('title'), from_address[-42:], to_address[-42:], amount, date, fee])
                    save_checkpoint(hash_value)  # 记录已处理的哈希值

                except Exception as e:
                    print(f"Error processing {hash_value}: {e}")
                    writer.writerow([hash_value, "N/A", "N/A", "N/A", "N/A", "N/A"])
                    save_checkpoint(hash_value)  # 即使出错也记录已处理的哈希值
                    continue

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # 确保无论是否发生异常都会关闭浏览器
        if 'driver' in locals():
            driver.quit()