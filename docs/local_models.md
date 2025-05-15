# Sử dụng Local LLM Models trong I Ching Divination API

Tài liệu này hướng dẫn cách sử dụng và tối ưu hóa các mô hình ngôn ngữ (LLM) cục bộ thông qua thư viện Hugging Face Transformers thay vì sử dụng OpenAI API.

## Cài đặt

1. Cài đặt các gói phụ thuộc cơ bản:

```bash
pip install -r requirements.txt
```

2. Cài đặt các gói tối ưu hóa hiệu năng (khuyến nghị cho GPU):

```bash
pip install -U accelerate optimum bitsandbytes flash-attn xformers
```

3. Tạo file `.env` từ file `.env.example`:

```bash
cp .env.example .env
```

4. Cấu hình các tham số trong file `.env`

## Cấu hình

Trong file `.env`, bạn có thể chọn sử dụng OpenAI hoặc Hugging Face như sau:

### Sử dụng OpenAI

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL_NAME=gpt-4
```

### Sử dụng Hugging Face (Local LLM) với tối ưu hóa

```bash
LLM_PROVIDER=huggingface
LLM_OPTIMIZE=True
HF_MODEL_NAME=microsoft/phi-2
```

## Lựa chọn mô hình Hugging Face

Dưới đây là một số gợi ý về các mô hình phù hợp dựa trên tài nguyên phần cứng:

### Cho máy tính chỉ có CPU

| Mô hình | Kích thước | Chất lượng | Tốc độ | Thiết lập khuyến nghị |
|---------|-----------|------------|--------|------------------------|
| microsoft/phi-2 | 2.7B | Tốt | Trung bình | `HF_USE_8BIT=False`, `HF_DEVICE=cpu` |
| TinyLlama/TinyLlama-1.1B-Chat-v1.0 | 1.1B | Trung bình | Nhanh | `HF_USE_8BIT=False`, `HF_DEVICE=cpu` |

### Cho máy tính có GPU với VRAM thấp (4-8GB)

| Mô hình | Kích thước | Chất lượng | Tốc độ | Thiết lập khuyến nghị |
|---------|-----------|------------|--------|------------------------|
| microsoft/phi-2 | 2.7B | Tốt | Nhanh | `HF_USE_8BIT=True` |
| TheBloke/Mistral-7B-Instruct-v0.2-GPTQ | 7B (4-bit) | Tốt | Trung bình | `HF_USE_BETTER_TRANSFORMER=True` |

### Cho máy tính có GPU với VRAM trung bình (8-16GB)

| Mô hình | Kích thước | Chất lượng | Tốc độ | Thiết lập khuyến nghị |
|---------|-----------|------------|--------|------------------------|
| meta-llama/Meta-Llama-3-8B-Instruct | 8B | Rất tốt | Nhanh | `HF_USE_FLASH_ATTENTION=True` |
| TheBloke/WizardLM-13B-V1.2-GPTQ | 13B (4-bit) | Rất tốt | Trung bình | `HF_USE_BETTER_TRANSFORMER=True` |

### Cho máy tính có GPU mạnh (≥24GB VRAM)

| Mô hình | Kích thước | Chất lượng | Tốc độ | Thiết lập khuyến nghị |
|---------|-----------|------------|--------|------------------------|
| meta-llama/Meta-Llama-3-70B-Instruct | 70B (8-bit) | Xuất sắc | Trung bình | `HF_USE_8BIT=True` |
| mistralai/Mixtral-8x7B-Instruct-v0.1 | 48B (4-bit) | Xuất sắc | Trung bình | `HF_USE_4BIT=True` |

## Các Tham Số Tối Ưu Hóa Mới

Phiên bản mới hỗ trợ nhiều tham số tối ưu hóa hiệu năng:

| Tham số | Tác dụng | Khi nào nên bật |
|---------|----------|-----------------|
| LLM_OPTIMIZE | Bật/tắt tất cả tối ưu hóa | Luôn bật với GPU |
| HF_USE_BETTER_TRANSFORMER | Tối ưu hóa kiến trúc transformer | Khi dùng GPU |
| HF_USE_FLASH_ATTENTION | Tăng tốc các phép tính attention | Khi dùng GPU Tesla T4 trở lên |
| HF_USE_8BIT | Lượng tử hóa 8-bit giảm bộ nhớ | Khi VRAM/RAM hạn chế |
| HF_USE_4BIT | Lượng tử hóa 4-bit (chất lượng thấp hơn) | Khi cần chạy mô hình rất lớn |

## Tối ưu hóa hiệu năng

Để có hiệu năng tối đa khi chạy mô hình cục bộ:

### 1. Sử dụng các kỹ thuật lượng tử hóa

API hỗ trợ các phương pháp giảm kích thước mô hình:
- **8-bit Quantization**: Giảm 50% bộ nhớ (`HF_USE_8BIT=True`)
- **4-bit Quantization**: Giảm 75% bộ nhớ (`HF_USE_4BIT=True`)

### 2. Tận dụng các thư viện tăng tốc 

- **BetterTransformer**: Tối ưu hóa các phép toán transformer (`HF_USE_BETTER_TRANSFORMER=True`)
- **FlashAttention**: Tăng tốc phép toán attention (`HF_USE_FLASH_ATTENTION=True`)

### 3. Thiết lập theo phần cứng

- **GPU NVIDIA**: Bật tất cả các tùy chọn tối ưu
- **Apple Silicon**: Sử dụng `device="mps"` để tận dụng GPU của Apple
- **CPU**: Giảm kích thước mô hình và cân nhắc tắt các tối ưu hóa nặng

## Khắc phục sự cố

### Lỗi hết bộ nhớ (CUDA out of memory)

Nếu gặp lỗi hết bộ nhớ GPU:

1. Bật `HF_USE_8BIT=True` hoặc nặng hơn là `HF_USE_4BIT=True`
2. Giảm `HF_MAX_LENGTH` và `HF_MAX_NEW_TOKENS` xuống
3. Chọn mô hình nhỏ hơn hoặc phiên bản lượng tử hóa (GPTQ, GGML)
4. Thiết lập `device="cpu"` để chạy trên CPU nếu cần

### Tăng tốc độ sinh văn bản

Để tăng tốc độ xử lý:

1. Bật tất cả các tối ưu hóa (`HF_USE_BETTER_TRANSFORMER=True`, `HF_USE_FLASH_ATTENTION=True`)
2. Giảm `HF_MAX_NEW_TOKENS` xuống nếu chỉ cần câu trả lời ngắn
3. Giảm `HF_TEMPERATURE` xuống 0.6 hoặc 0.5 để ít phải tính toán xác suất hơn

### Cải thiện chất lượng kết quả

Nếu kết quả sinh ra không đạt chất lượng mong muốn:

1. Sử dụng mô hình lớn hơn (>7B tham số)
2. Dùng mô hình đã được huấn luyện đặc biệt cho instruction following
3. Đảm bảo prompt rõ ràng và đầy đủ ngữ cảnh
4. Tăng `HF_TEMPERATURE` (0.7-0.9) nếu kết quả quá máy móc

## Kiểm tra cấu hình phần cứng

Kiểm tra thông tin GPU của bạn:

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print(f"CUDA version: {torch.version.cuda}")
```
