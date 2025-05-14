"""
Script tạo dữ liệu huấn luyện tự động cho mô hình giải quẻ Kinh Dịch
"""
import json
import random
import os
import time
from typing import List, Dict, Any
import argparse
from dotenv import load_dotenv
import openai
from tqdm import tqdm

# Tải biến môi trường từ file .env
load_dotenv()

# Cấu hình API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Đường dẫn đến file dữ liệu mẫu
SAMPLE_DATA_PATH = os.path.join("data_samples", "sample_data.json")
OUTPUT_DATA_PATH = os.path.join("data_samples", "generated_data.json")

# Danh sách các chủ đề
TOPICS = [
    "Sự nghiệp/Kinh doanh", 
    "Tình yêu/Mối quan hệ", 
    "Sức khỏe", 
    "Phát triển bản thân", 
    "Gia đình", 
    "Giáo dục", 
    "Tài chính", 
    "Du lịch", 
    "Tâm linh", 
    "Định hướng cuộc sống"
]

def load_hexagrams() -> List[Dict[str, Any]]:
    """Tải dữ liệu về các quẻ Kinh Dịch"""
    try:
        from app.data.hexagrams import HEXAGRAMS
        return HEXAGRAMS
    except ImportError:
        print("Không thể tải dữ liệu quẻ từ module app.data.hexagrams")
        # Tải từ file mẫu
        with open(SAMPLE_DATA_PATH, 'r', encoding='utf-8') as f:
            sample_data = json.load(f)
        
        # Trích xuất các quẻ duy nhất
        hexagrams = []
        unique_numbers = set()
        for item in sample_data:
            if item['hexagram']['number'] not in unique_numbers:
                hexagrams.append(item['hexagram'])
                unique_numbers.add(item['hexagram']['number'])
        
        return hexagrams

def generate_question(topic: str) -> str:
    """Tạo câu hỏi ngẫu nhiên cho một chủ đề cụ thể"""
    prompt = f"""Tạo một câu hỏi tự nhiên và cụ thể mà người dùng có thể hỏi khi xin lời giải quẻ Kinh Dịch. 
    Câu hỏi phải thuộc chủ đề "{topic}" và phải là câu hỏi mở (không phải câu hỏi có/không).
    Ví dụ: "Làm thế nào để tôi cải thiện mối quan hệ với đồng nghiệp hiện tại?"
    Trả về duy nhất câu hỏi, không cần giải thích hay chú thích."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=100
        )
        return response.choices[0].message.content.strip().strip('"\'')
    except Exception as e:
        print(f"Lỗi khi tạo câu hỏi: {e}")
        return f"Câu hỏi liên quan đến {topic}?"

def generate_interpretation(question: str, hexagram: Dict[str, Any], topic: str) -> str:
    """Tạo lời giải quẻ cá nhân hóa dựa trên câu hỏi và quẻ"""
    hex_info = (
        f"Số quẻ: {hexagram['number']}\n"
        f"Tên quẻ: {hexagram['name']}\n"
        f"Biểu tượng: {hexagram['symbol']}\n"
        f"Quái trên: {hexagram.get('upper_trigram', '')}\n"
        f"Quái dưới: {hexagram.get('lower_trigram', '')}\n"
        f"Ý nghĩa tổng quát: {hexagram.get('general_meaning', '')}\n"
    )
    
    prompt = f"""Với tư cách là chuyên gia Kinh Dịch, hãy tạo ra lời giải quẻ cá nhân hóa cho câu hỏi của người dùng dựa trên thông tin được cung cấp.
    
    Câu hỏi: {question}
    Chủ đề: {topic}
    Thông tin quẻ:
    {hex_info}
    
    Lời giải của bạn nên:
    1. Tôn trọng truyền thống Kinh Dịch
    2. Kết nối ý nghĩa của quẻ với câu hỏi cụ thể
    3. Đưa ra lời khuyên thực tiễn và hữu ích
    4. Dài khoảng 3-4 đoạn văn
    5. Sử dụng giọng điệu khôn ngoan và thấu hiểu
    
    Trả lời hoàn toàn bằng tiếng Việt."""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Lỗi khi tạo lời giải: {e}")
        return f"Lỗi khi tạo lời giải quẻ: {e}"

def generate_dataset(num_samples: int, output_path: str) -> None:
    """Tạo bộ dữ liệu với số lượng mẫu xác định"""
    hexagrams = load_hexagrams()
    
    # Tải dữ liệu mẫu để tham khảo định dạng
    sample_data = []
    if os.path.exists(SAMPLE_DATA_PATH):
        with open(SAMPLE_DATA_PATH, 'r', encoding='utf-8') as f:
            sample_data = json.load(f)
    
    # Nếu không có file mẫu, tạo một mảng trống
    if not sample_data:
        sample_data = []
    
    # Tạo dữ liệu mới
    generated_data = []
    next_id = max([item['id'] for item in sample_data], default=0) + 1
    
    print(f"Bắt đầu tạo {num_samples} mẫu dữ liệu...")
    
    for _ in tqdm(range(num_samples)):
        # Chọn ngẫu nhiên một chủ đề và một quẻ
        topic = random.choice(TOPICS)
        hexagram = random.choice(hexagrams)
        
        # Tạo câu hỏi
        question = generate_question(topic)
        
        # Tạo lời giải quẻ
        interpretation = generate_interpretation(question, hexagram, topic)
        
        # Tạo mẫu dữ liệu mới
        new_sample = {
            "id": next_id,
            "question": question,
            "hexagram": hexagram,
            "topic": topic,
            "interpretation": interpretation
        }
        
        generated_data.append(new_sample)
        next_id += 1
        
        # Đợi một chút để tránh vượt quá rate limit của API
        time.sleep(1)
    
    # Kết hợp dữ liệu mới với dữ liệu mẫu
    combined_data = sample_data + generated_data
    
    # Lưu dữ liệu mới vào file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, ensure_ascii=False, indent=2)
    
    print(f"Đã tạo xong {num_samples} mẫu dữ liệu và lưu vào {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Tạo dữ liệu huấn luyện cho mô hình giải quẻ Kinh Dịch")
    parser.add_argument("--samples", type=int, default=10, help="Số lượng mẫu cần tạo")
    parser.add_argument("--output", type=str, default=OUTPUT_DATA_PATH, help="Đường dẫn file đầu ra")
    
    args = parser.parse_args()
    
    generate_dataset(args.samples, args.output)

if __name__ == "__main__":
    main()
