import requests
from bs4 import BeautifulSoup
import json
import glob
import random
from collections import Counter
import pandas as pd
import csv



def read_json(file_path):
    """
    Đọc file JSON và hiển thị dữ liệu với format đẹp hơn
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    print(json.dumps(data, indent=4))  # Hiển thị dữ liệu với format đẹp hơn
    return data

def read_json_folder(folder_path):
    """
    Lấy danh sách tất cả các file JSON trong thư mục
    """
    json_files = glob.glob("result 2/*.json")
    print(json_files)

def random_json_files(folder_path, num_files=500):
    # Tìm tất cả file JSON trong thư mục
    json_files = glob.glob(folder_path)
    print(f"Số lượng file JSON: {len(json_files)}")
    # Kiểm tra nếu số lượng file ít hơn số lượng cần lấy
    if len(json_files) < num_files:
        raise ValueError(f"Chỉ có {len(json_files)} file JSON, không đủ để lấy {num_files} file mẫu.")
    # Lấy ngẫu nhiên `num_files` file
    random_files = random.sample(json_files, num_files)
    print("Các file được chọn ngẫu nhiên:", random_files)

    return random_files
"""
    try:
        random_file = random_json_files("/Users/hoang/projects/python_env/result 2*.json", num_files=500)
    except ValueError as e:
        print("Lỗi:", e)
"""

def get_sample_values(all_keys, random_files):
    sample_values = {key: None for key in all_keys}  # Tạo dictionary lưu giá trị mẫu
    for random_files in random_files:
        try:
            with open(random_files, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Kiểm tra và lưu giá trị mẫu cho từng key
            for key in all_keys:
                if sample_values[key] is None and key in data:  # Chỉ lấy giá trị đầu tiên gặp
                    sample_values[key] = data[key]
        except Exception as e:
            print(f"Error processing file {random_files}: {e}")

    return sample_values


def extract_keys(data, prefix=''):
    keys = set()
    for key, value in data.items():
        if isinstance(value, dict):
            keys |= extract_keys(value, prefix + key + ".")  # Lấy key trong object lồng nhau
        else:
            keys.add(prefix + key)
    return keys

def extract_nested_keys(data, parent_key=''):
    """
    Hàm đệ quy để trích xuất tất cả các keys, kể cả keys lồng nhau.
    """
    keys = []
    if isinstance(data, dict):  # Nếu là dictionary
        for key, value in data.items():
            full_key = f"{key}" if parent_key else key
            #full_key = f"{parent_key}.{key}" if parent_key else key  # Gộp key cha và key con
            keys.append(full_key)
            keys.extend(extract_nested_keys(value, full_key))  # Đệ quy
    elif isinstance(data, list):  # Nếu là danh sách
        for index, item in enumerate(data):
            full_key = f"{parent_key}[{index}]"
            keys.extend(extract_nested_keys(item, full_key))  # Đệ quy
    return keys

def list_all_keys_with_nesting(selected_files):
    #Liệt kê tất cả các keys (bao gồm lồng nhau) từ các file JSON đã chọn.
    all_keys = []
    for file in selected_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Lỗi khi đọc file {file}: {e}")

    # Đếm số lần xuất hiện của từng key
    key_counter = Counter(all_keys)
    sample_values = {key: None for key in all_keys}  # Tạo dictionary lưu giá trị mẫu

    # In danh sách keys với số lần xuất hiện
    print("\nDanh sách keys (bao gồm keys lồng nhau) và số lần xuất hiện:")
    for key, count in key_counter.items():
        print(f"{key}")

    # for key in all_keys:
    #     if sample_values[key] is None and key in data:  # Chỉ lấy giá trị đầu tiên gặp
    #         sample_values[key] = data[key]

    #     print(f"{sample_values}")
        # print(f"{type(key)}")
        # print(f"{key}: {count} lần")

    return all_keys

"""
    try:
        # Thay đường dẫn folder JSON vào đây
        selected_files = random_json_files("/path/to/json/files/*.json", num_files=500)
        all_nested_keys = list_all_keys_with_nesting(selected_files)
    except Exception as e:
        print(f"Lỗi: {e}")
"""

def compare_json_keys_random(selected_files):
    """
    So sánh keys giữa các file JSON đã chọn ngẫu nhiên.
    """
    all_keys = set()  # Tập hợp chứa tất cả keys duy nhất
    file_key_map = {}  # Lưu keys của từng file

    # Đọc keys từ mỗi file JSON
    for file in selected_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):  # File JSON dạng object
                    keys = set(data.keys())
                    file_key_map[file] = keys
                    all_keys.update(keys)
                else:
                    print(f"File {file} không phải là JSON dạng object.")
        except Exception as e:
            print(f"Lỗi khi đọc file {file}: {e}")

    # So sánh keys
    print("\nSo sánh keys giữa các file:")
    for file, keys in file_key_map.items():
        missing_keys = all_keys - keys  # Keys mà file này không có
        extra_keys = keys - all_keys  # Keys không nằm trong tập hợp chung
        print(f"\nFile: {file}")
        print(f" - Keys thiếu: {missing_keys if missing_keys else 'Không có'}")
        print(f" - Keys dư: {extra_keys if extra_keys else 'Không có'}")

    # In tất cả các keys duy nhất
    print("\nTất cả các keys duy nhất trong các file JSON đã chọn:")
    print(all_keys)
"""
    try:
        # Bước 1: Chọn ngẫu nhiên 10 file JSON
        selected_files = random_json_files("/Users/hoang/projects/python_env/result 2/*.json", num_files=500)
        print("Các file được chọn ngẫu nhiên:", selected_files)

        # Bước 2: So sánh keys giữa các file đã chọn
        compare_json_keys_random(selected_files)

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
"""

def list_all_keys_with_duplicates(selected_files):
    """
    Liệt kê tất cả các keys (bao gồm keys trùng) từ các file JSON đã chọn.
    """
    all_keys = []  # Danh sách chứa tất cả keys (bao gồm bị trùng)

    for file in selected_files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):  # Nếu JSON là object
                    keys = data.keys()
                    all_keys.extend(keys)  # Thêm keys vào danh sách
                else:
                    print(f"File {file} không phải JSON dạng object.")
        except Exception as e:
            print(f"Lỗi khi đọc file {file}: {e}")

    # Đếm số lần xuất hiện của từng key
    key_counter = Counter(all_keys)

    # In danh sách keys với số lần xuất hiện
    print("\nDanh sách keys và số lần xuất hiện:")
    for key, count in key_counter.items():
        print(f"{key}: {count} lần")

    return all_keys

 # Ví dụ sử dụng
"""
try:
    # Thay đường dẫn folder JSON vào đây
    selected_files = random_json_files("/path/to/json/files/*.json", num_files=500)
    all_keys = list_all_keys_with_duplicates(selected_files)
except Exception as e:
    print(f"Lỗi: {e}")
"""


def extract_specific_key(json_folder, key_to_extract):
    """
    Hàm xuất ra giá trị của key cụ thể từ các file JSON.

    Args:
        json_folder (str): Đường dẫn thư mục chứa các file JSON.
        key_to_extract (str): Tên key cần lấy.

    Returns:
        list: Danh sách các giá trị của key từ tất cả file JSON.
    """
    extracted_values = []  # Danh sách lưu trữ giá trị của key
    json_files = glob.glob(f"{json_folder}/*.json")  # Lấy danh sách file JSON

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)  # Đọc nội dung file JSON
                # Kiểm tra key và thêm vào danh sách nếu tồn tại
                if key_to_extract in data:
                    extracted_values.append(data[key_to_extract])
                else:
                    print(f"Key '{key_to_extract}' không tồn tại trong file: {file_path}")
        except json.JSONDecodeError:
            print(f"File không hợp lệ hoặc không thể đọc: {file_path}")

    return extracted_values

# Sử dụng hàm
"""
json_folder = "path/to/json/folder"  # Thay bằng đường dẫn thực tế
key_to_extract = "key_cụ_thể"  # Thay bằng tên key bạn muốn lấy
result = extract_specific_key(json_folder, key_to_extract)

print("Danh sách giá trị của key:")
print(result)

"""

#products_df = pd.DataFrame(products)


def extract_repurchase_values(folder_path, key):
    values = []  # Danh sách lưu trữ các giá trị của key
    json_files = glob.glob(f"{folder_path}/*.json")  # Lấy tất cả file JSON trong folder
    all_keys = []  # Danh sách chứa tất cả keys (bao gồm bị lồng)


    for file in json_files:
        try:
            # Mở và đọc nội dung file JSON
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                keys = extract_nested_keys(data)  # Lấy tất cả các keys từ file
                all_keys.extend(keys)
            # Kiểm tra xem key có trong file không
            if key in data:
                values.append(data[key])  # Lưu giá trị của key vào danh sách
            else:
                values.append(None)  # Nếu không tìm thấy key, thêm giá trị None
        except json.JSONDecodeError:
            print(f"Không thể đọc file JSON: {file}")
        except Exception as e:
            print(f"Lỗi không xác định khi xử lý file {file}: {e}")

    return values


if __name__ == "__main__":

    random_files = random_json_files("/Users/hoang/projects/python_env/result 2/*.json", num_files=500)
    all_keys = list_all_keys_with_nesting(random_files)
