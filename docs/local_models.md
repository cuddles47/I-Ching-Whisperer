# Sử dụng Local LLM Models trong I Ching Divination API

Tài liệu này hướng dẫn cách sử dụng các mô hình ngôn ngữ (LLM) cục bộ thông qua thư viện Hugging Face Transformers thay vì sử dụng OpenAI API.

## Cài đặt

1. Cài đặt các gói phụ thuộc cần thiết:

```bash
pip install -r requirements.txt
```

2. Tạo file `.env` từ file `.env.example`:

```bash
cp .env.example .env
```

3. Cấu hình các tham số trong file `.env`:

## Cấu hình

Trong file `.env`, bạn có thể chọn sử dụng OpenAI hoặc Hugging Face như sau:

### Sử dụng OpenAI

```
LLM_PROVIDER=openai
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL_NAME=gpt-4
```

### Sử dụng Hugging Face (Local LLM)

```
LLM_PROVIDER=huggingface
HF_MODEL_NAME=microsoft/phi-2
```

## Lựa chọn mô hình Hugging Face

Dưới đây là một số gợi ý về các mô hình phù hợp dựa trên tài nguyên phần cứng:

### Cho máy tính có GPU VRAM thấp hoặc chỉ có CPU

- `microsoft/phi-2`: Mô hình nhỏ (2.7B parameters), hiệu quả trên CPU hoặc GPU có ít RAM
- `TinyLlama/TinyLlama-1.1B-Chat-v1.0`: Mô hình siêu nhỏ, chạy được trên đa dạng thiết bị

### Cho máy tính có GPU với VRAM trung bình (>= 8GB)

- `mistralai/Mistral-7B-Instruct-v0.2`: Mô hình 7B hiệu năng cao
- `TheBloke/Llama-2-7B-Chat-GGML`: Phiên bản GGML tối ưu hóa của Llama 2

### Cho máy tính có GPU mạnh (>= 16GB VRAM)

- `meta-llama/Meta-Llama-3-8B-Instruct`: Mô hình 8B từ Meta AI
- `google/gemma-7b-it`: Google Gemma model đã được fine-tuned cho instruction following

## Tối ưu hóa hiệu năng

Để cải thiện hiệu năng:

1. Đảm bảo bạn có GPU và đã cài đặt drivers CUDA (NVIDIA) hoặc sử dụng MPS (Apple Silicon)

2. Sử dụng các mô hình quantized để giảm bộ nhớ:
   - Tìm các phiên bản GGML, GPTQ, hoặc AWQ của các mô hình

3. Điều chỉnh các tham số sinh văn bản:
   - Giảm `HF_MAX_LENGTH` nếu cần thiết
   - Thay đổi `HF_TEMPERATURE` và `HF_TOP_P` để cân bằng giữa sáng tạo và nhất quán

## Lưu ý về chất lượng

Các mô hình cục bộ nhỏ hơn có thể không mang lại chất lượng tốt như GPT-4. Tùy thuộc vào nhu cầu của bạn, hãy cân nhắc giữa:

- Mô hình nhỏ: Nhanh hơn, tiết kiệm tài nguyên, nhưng kết quả có thể kém chính xác
- Mô hình lớn: Kết quả tốt hơn, nhưng đòi hỏi phần cứng mạnh hơn và chậm hơn

## Điều chỉnh prompts

Nếu bạn thấy rằng các mô hình cục bộ không hoạt động tốt với prompts hiện tại, bạn có thể cần điều chỉnh:

1. Đơn giản hóa prompts
2. Sử dụng ít token hơn
3. Thêm ví dụ cụ thể
4. Sử dụng định dạng prompt cụ thể cho mô hình mà bạn đang sử dụng
