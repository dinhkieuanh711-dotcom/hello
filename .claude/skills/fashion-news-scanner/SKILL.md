---
name: fashion-news-scanner
description: >
  Quét tin tức/xu hướng thời trang mới nhất trong ngày (web search), lọc
  theo độ liên quan tới kênh bán lẻ/resale thời trang, xuất danh sách tin
  có nguồn, ngày, tóm tắt 1 câu và lý do liên quan. Dùng làm bước 1 của
  pipeline content hàng ngày, chạy trước daily-content-proposer.
---

# Fashion News Scanner

1. Dùng WebSearch/WebFetch tìm tin trong 24-48h gần nhất theo các chủ đề:
   xu hướng chất liệu/màu sắc mùa, item đang viral trên TikTok/Instagram,
   phối đồ theo thời tiết/sự kiện, hàng mới ra mắt của các local brand
   lớn tại VN (nếu người dùng nhắm thị trường VN).
2. Loại bỏ tin không liên quan tới phân khúc sản phẩm của kênh (ví dụ:
   không lấy tin haute couture nếu kênh bán áo khoác da giá phổ thông).
3. Với mỗi tin giữ lại, ghi: tiêu đề, nguồn + link, ngày đăng, tóm tắt 1
   câu, "góc độ dùng được cho video" (ví dụ: "áo da nâu đang trend mùa
   đông → làm video phối áo da với kính mát + túi tối màu").
4. Xuất tối đa 15-20 tin/ngày, sắp theo độ liên quan giảm dần.
5. Lưu kết quả vào `agent/data/news_YYYY-MM-DD.json` để
   `daily-content-proposer` đọc lại — không cần người dùng tự chép tay.
