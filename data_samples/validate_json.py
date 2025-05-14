"""
Script kiểm tra định dạng JSON
"""
import json
import os
import sys

def validate_json_file(file_path):
    """Kiểm tra xem file JSON có hợp lệ không"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"✅ File JSON hợp lệ, có {len(data)} mục")
            return True
    except json.JSONDecodeError as e:
        print(f"❌ File JSON không hợp lệ: {e}")
        return False
    except Exception as e:
        print(f"❌ Có lỗi khi đọc file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python validate_json.py <đường_dẫn_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    validate_json_file(file_path)
