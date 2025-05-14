"""
Script phân tích dữ liệu huấn luyện cho mô hình giải quẻ Kinh Dịch
"""
import json
import os
import argparse
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
import seaborn as sns

# Đường dẫn mặc định đến file dữ liệu
DEFAULT_DATA_PATH = os.path.join("sample_data.json")

def load_data(data_path):
    """Tải dữ liệu từ file JSON"""
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def analyze_topics(data):
    """Phân tích phân bố chủ đề trong dữ liệu"""
    topics = [item['topic'] for item in data]
    topic_counts = Counter(topics)
    
    # Tạo biểu đồ phân bố chủ đề
    plt.figure(figsize=(10, 6))
    bars = plt.bar(topic_counts.keys(), topic_counts.values())
    plt.title('Phân bố chủ đề trong dữ liệu')
    plt.xlabel('Chủ đề')
    plt.ylabel('Số lượng')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Thêm nhãn giá trị trên mỗi cột
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                 f'{height}',
                 ha='center', va='bottom')
    
    # Lưu biểu đồ
    output_path = os.path.join("topic_distribution.png")
    plt.savefig(output_path)
    print(f"Đã lưu biểu đồ phân bố chủ đề vào {output_path}")
    plt.close()
    
    return topic_counts

def analyze_hexagrams(data):
    """Phân tích phân bố các quẻ trong dữ liệu"""
    hexagrams = [item['hexagram']['number'] for item in data]
    hex_counts = Counter(hexagrams)
    
    # Tạo biểu đồ phân bố quẻ
    plt.figure(figsize=(12, 6))
    plt.bar(hex_counts.keys(), hex_counts.values())
    plt.title('Phân bố các quẻ trong dữ liệu')
    plt.xlabel('Số quẻ')
    plt.ylabel('Số lượng')
    plt.xticks(list(range(1, 65, 2)))  # Hiển thị số quẻ từ 1-64
    plt.tight_layout()
    
    # Lưu biểu đồ
    output_path = os.path.join("hexagram_distribution.png")
    plt.savefig(output_path)
    print(f"Đã lưu biểu đồ phân bố quẻ vào {output_path}")
    plt.close()
    
    return hex_counts

def create_wordcloud(data):
    """Tạo đồ thị từ khóa phổ biến trong câu hỏi và lời giải"""
    # Kết hợp tất cả câu hỏi
    all_questions = ' '.join([item['question'] for item in data])
    
    # Tạo wordcloud cho câu hỏi
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                          max_words=100, contour_width=3, contour_color='steelblue',
                          font_path='arial.ttf', collocations=False).generate(all_questions)
    
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Từ khóa phổ biến trong câu hỏi')
    plt.axis('off')
    
    # Lưu wordcloud
    output_path = os.path.join("question_wordcloud.png")
    plt.savefig(output_path)
    print(f"Đã lưu biểu đồ từ khóa câu hỏi vào {output_path}")
    plt.close()
    
    # Kết hợp tất cả lời giải
    all_interpretations = ' '.join([item['interpretation'] for item in data])
    
    # Tạo wordcloud cho lời giải
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                          max_words=100, contour_width=3, contour_color='steelblue',
                          font_path='arial.ttf', collocations=False).generate(all_interpretations)
    
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Từ khóa phổ biến trong lời giải quẻ')
    plt.axis('off')
    
    # Lưu wordcloud
    output_path = os.path.join("interpretation_wordcloud.png")
    plt.savefig(output_path)
    print(f"Đã lưu biểu đồ từ khóa lời giải vào {output_path}")
    plt.close()

def analyze_correlations(data):
    """Phân tích mối tương quan giữa quẻ và chủ đề"""
    # Chuẩn bị dữ liệu
    df_data = []
    for item in data:
        df_data.append({
            'hexagram': item['hexagram']['number'],
            'topic': item['topic'],
            'hexagram_name': item['hexagram']['name']
        })
    
    df = pd.DataFrame(df_data)
    
    # Tạo bảng tần suất
    pivot_table = pd.crosstab(df['hexagram_name'], df['topic'])
    
    # Tạo heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot_table, annot=True, cmap='YlGnBu', fmt='d')
    plt.title('Mối tương quan giữa quẻ và chủ đề')
    plt.tight_layout()
    
    # Lưu heatmap
    output_path = os.path.join("hexagram_topic_correlation.png")
    plt.savefig(output_path)
    print(f"Đã lưu biểu đồ tương quan vào {output_path}")
    plt.close()

def analyze_data(data_path):
    """Phân tích dữ liệu và tạo báo cáo"""
    print(f"Phân tích dữ liệu từ {data_path}...")
    
    try:
        # Tải dữ liệu
        data = load_data(data_path)
        print(f"Đã tải {len(data)} mẫu dữ liệu")
        
        # In thông tin dữ liệu để debug
        print("Ví dụ dữ liệu đầu tiên:")
        print(f"  ID: {data[0]['id']}")
        print(f"  Câu hỏi: {data[0]['question']}")
        print(f"  Quẻ: {data[0]['hexagram']['name']} (#{data[0]['hexagram']['number']})")
        print(f"  Chủ đề: {data[0]['topic']}")
        
        # Phân tích chủ đề
        topic_counts = analyze_topics(data)
        print("\nPhân bố chủ đề:")
        for topic, count in topic_counts.items():
            print(f"  {topic}: {count} mẫu")
        
        # Phân tích quẻ
        hex_counts = analyze_hexagrams(data)
        print("\nPhân bố quẻ (top 10):")
        for hex_num, count in hex_counts.most_common(10):
            # Tìm tên quẻ
            hex_name = next((item['hexagram']['name'] for item in data if item['hexagram']['number'] == hex_num), "")
            print(f"  Quẻ {hex_num} ({hex_name}): {count} mẫu")
        
        # Thống kê độ dài câu hỏi và lời giải
        q_lengths = [len(item['question']) for item in data]
        i_lengths = [len(item['interpretation']) for item in data]
        
        print("\nThống kê độ dài:")
        print(f"  Độ dài câu hỏi: Min={min(q_lengths)}, Max={max(q_lengths)}, Trung bình={sum(q_lengths)/len(q_lengths):.1f} ký tự")
        print(f"  Độ dài lời giải: Min={min(i_lengths)}, Max={max(i_lengths)}, Trung bình={sum(i_lengths)/len(i_lengths):.1f} ký tự")
        
        # Tạo wordcloud
        try:
            create_wordcloud(data)
        except Exception as e:
            print(f"Lỗi khi tạo wordcloud: {e}")
        
        # Phân tích tương quan
        try:
            analyze_correlations(data)
        except Exception as e:
            print(f"Lỗi khi phân tích tương quan: {e}")
        
        print("\nHoàn thành phân tích dữ liệu!")
        
    except Exception as e:
        print(f"Lỗi khi phân tích dữ liệu: {e}")

def main():
    parser = argparse.ArgumentParser(description="Phân tích dữ liệu huấn luyện cho mô hình giải quẻ Kinh Dịch")
    parser.add_argument("--data", type=str, default=DEFAULT_DATA_PATH, help="Đường dẫn đến file dữ liệu")
    
    args = parser.parse_args()
    
    analyze_data(args.data)

if __name__ == "__main__":
    main()
