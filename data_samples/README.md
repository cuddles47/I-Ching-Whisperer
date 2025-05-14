# Hướng dẫn sử dụng dữ liệu mẫu

Tệp `sample_data.json` chứa các mẫu dữ liệu có thể được sử dụng để huấn luyện mô hình AI cho hệ thống giải quẻ Kinh Dịch.

## Cấu trúc dữ liệu

Mỗi mẫu bao gồm các trường sau:

1. `id`: ID duy nhất của mẫu dữ liệu
2. `question`: Câu hỏi của người dùng
3. `hexagram`: Thông tin về quẻ Kinh Dịch, bao gồm:
   - `number`: Số thứ tự của quẻ (1-64)
   - `name`: Tên quẻ (tiếng Việt)
   - `symbol`: Biểu tượng của quẻ
   - `upper_trigram`: Quái trên
   - `lower_trigram`: Quái dưới
   - `general_meaning`: Ý nghĩa tổng quát của quẻ
4. `topic`: Chủ đề/lĩnh vực của câu hỏi
5. `interpretation`: Lời giải quẻ chi tiết được cá nhân hóa theo câu hỏi

## Cách sử dụng dữ liệu

### 1. Huấn luyện mô hình phân loại chủ đề

Sử dụng cặp `question` và `topic` để huấn luyện mô hình phân loại chủ đề từ câu hỏi người dùng.

### 2. Huấn luyện mô hình tạo lời giải quẻ

Sử dụng các trường `question`, `topic`, `hexagram` làm đầu vào và `interpretation` làm đầu ra để huấn luyện mô hình tạo lời giải quẻ cá nhân hóa.

### 3. Mở rộng tập dữ liệu

Để có kết quả tốt hơn, bạn nên mở rộng tập dữ liệu này với:
- Nhiều câu hỏi đa dạng hơn cho từng chủ đề
- Các quẻ khác nhau (hiện tập dữ liệu mẫu chỉ có một số quẻ trong tổng số 64 quẻ)
- Các phong cách diễn giải khác nhau (formal, informal, chi tiết, tóm tắt, v.v.)

## Lưu ý

- Dữ liệu mẫu này chỉ nhằm mục đích minh họa và không đủ để huấn luyện một mô hình hoạt động tốt trong thực tế.
- Bạn nên thu thập ít nhất vài trăm mẫu cho mỗi loại quẻ/chủ đề để đảm bảo mô hình có đủ dữ liệu học.
- Cân nhắc việc tạo dữ liệu tăng cường (data augmentation) bằng cách biến đổi câu hỏi mà vẫn giữ nguyên ý nghĩa.
