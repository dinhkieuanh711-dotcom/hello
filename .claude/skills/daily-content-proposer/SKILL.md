---
name: daily-content-proposer
description: >
  Đọc kết quả fashion-news-scanner + ảnh sản phẩm có sẵn trong kho, đề
  xuất đúng 10 ý tưởng video/ngày cho kênh thời trang. Mỗi ý tưởng gồm
  tiêu đề, hook, sản phẩm dùng, góc quay, lý do chọn. Dùng làm bước 2,
  chạy sau fashion-news-scanner và trước content-scorer.
---

# Daily Content Proposer

1. Đọc `agent/data/news_<ngày>.json` (từ fashion-news-scanner) và danh
   sách ảnh sản phẩm hiện có (kho ảnh do người dùng cung cấp).
2. Ghép mỗi tin/xu hướng phù hợp với 1 sản phẩm cụ thể trong kho — không
   bịa sản phẩm không tồn tại.
3. Với mỗi ý tưởng, ghi đúng các trường:
   - `title`: tên ngắn gọi nội bộ
   - `hook`: câu mở đầu 3 giây đầu video
   - `product_ref`: ảnh/sản phẩm dùng
   - `angle`: góc nội dung (reveal, phối đồ, so sánh giá, storytelling...)
   - `why_now`: lý do liên quan tới tin/xu hướng vừa quét
4. Tạo đúng 10 ý tưởng/ngày, đa dạng góc quay (không lặp lại angle quá 3
   lần trong 10 ý tưởng).
5. Lưu vào `agent/data/ideas_<ngày>.json`, mỗi ý tưởng có `id` duy nhất,
   `status: "proposed"` để content-scorer và dashboard đọc tiếp.
