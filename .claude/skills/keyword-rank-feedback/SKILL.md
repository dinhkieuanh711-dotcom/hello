---
name: keyword-rank-feedback
description: >
  Quét thứ hạng từ khoá của các bài đã đăng (Google Search Console hoặc
  1 API rank-tracking), so sánh với mục tiêu, đề xuất tối ưu bài cũ +
  đề xuất chủ đề bài mới cho daily-article-writer. Cần kết nối 1 nguồn
  dữ liệu thứ hạng — chưa có thì bỏ qua bước này, ghi "chưa kết nối" vào
  báo cáo ngày.
---

# Keyword Rank Feedback

## Yêu cầu trước khi chạy được
Cần 1 trong 2, điền vào `agent/config/seo.json` (copy từ
`seo.json.example`):
- **Google Search Console API** (miễn phí, cần site đã verify + OAuth
  credentials) — chính xác nhất vì là dữ liệu thật từ Google.
- **1 API rank-tracking trả phí** (SerpApi, Ahrefs, SEMrush...) — nếu
  bài đăng ở nơi không verify được Search Console.

## Quy trình

1. Lấy danh sách `target_keyword` của các bài đã đăng
   (`agent/data/articles_<ngày>.json`, các bài `status: published`).
2. Gọi API, lấy thứ hạng hiện tại + lưu lượng ước tính cho từng từ khoá.
3. So sánh với lần quét trước (`agent/data/keyword_history.json`) —
   tăng/giảm hạng, từ khoá nào đang mất vị trí.
4. Đề xuất:
   - **Tối ưu bài cũ**: bài tụt hạng → gợi ý sửa tiêu đề/đoạn mở/từ khoá
     phụ.
   - **Bài mới**: từ khoá liên quan có nhu cầu tìm kiếm nhưng chưa có
     bài nào che phủ → đưa vào input cho `daily-article-writer` ngày
     tiếp theo.
5. Ghi lại vào `agent/data/keyword_history.json` (có timestamp, không
   ghi đè mất lịch sử) — đây là "trí nhớ" để agent cải thiện dần theo dữ
   liệu thật, giống cơ chế của `channel-analytics-feedback`.
6. Nếu chưa có `agent/config/seo.json` hợp lệ, báo rõ trong
   `daily-agent-report`: "Chưa kết nối nguồn dữ liệu từ khoá — bước tối
   ưu/đề xuất theo thứ hạng đang tạm dừng", không tự bịa số liệu.
