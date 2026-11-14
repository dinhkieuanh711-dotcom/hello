---
name: channel-analytics-feedback
description: >
  Đọc chỉ số (view, like, share, comment) của các video đã đăng qua
  Facebook Graph API Insights, so sánh với điểm dự đoán của
  content-scorer, cập nhật trọng số chấm điểm và gợi ý điều chỉnh
  prompt/kịch bản cho chu kỳ sau. Cần Facebook Page Access Token.
---

# Channel Analytics Feedback Loop

## Yêu cầu trước khi chạy được
Cần trong `agent/config/facebook.json`: `page_id`, `page_access_token`
(lấy từ Meta for Developers, do người dùng tự tạo app + cấp quyền
`pages_read_engagement`, `pages_manage_posts`). Chưa có thì bỏ qua bước
này, chỉ ghi "chưa kết nối" vào báo cáo hàng ngày.

## Quy trình

1. Gọi Graph API Insights cho từng video đã đăng (trong
   `agent/data/published.json`): `impressions`, `video_views`, `likes`,
   `shares`, `comments`.
2. So khớp với `score` dự đoán ban đầu của `content-scorer` cho cùng
   `id` — tính độ lệch (thực tế vs dự đoán).
3. Tìm pattern: angle/hook/mood nhạc nào có tương tác thực tế cao hơn dự
   đoán nhất quán → tăng trọng số tiêu chí tương ứng trong
   `content-scorer`; angle nào thấp hơn dự đoán nhất quán → giảm trọng số
   hoặc loại khỏi danh sách angle đề xuất của `daily-content-proposer`.
4. Ghi lại thay đổi trọng số + lý do vào
   `agent/data/scoring_weights_history.json` (có timestamp) — đây là
   "trí nhớ" để agent cải thiện dần, không ghi đè mất lịch sử cũ.
5. Xuất tóm tắt feedback loop vào báo cáo hàng ngày
   (`daily-agent-report`): video nào vượt kỳ vọng, video nào dưới kỳ
   vọng, thay đổi gì sẽ áp dụng cho chu kỳ tiếp theo.
