---
name: content-scorer
description: >
  Chấm điểm 0-100 cho các ý tưởng video trong ideas_<ngày>.json theo 5
  tiêu chí, xếp hạng, đánh dấu top ý tưởng nên sản xuất. Dùng làm bước 3,
  chạy sau daily-content-proposer và trước video-script-production.
---

# Content Scorer

## Tiêu chí (mỗi tiêu chí 0-20 điểm)

1. **Độ bám trend** — khớp với tin/xu hướng vừa quét mạnh tới đâu.
2. **Sức mạnh hook** — 3 giây đầu có giữ chân người xem không.
3. **Khả thi sản xuất** — có đủ ảnh/sản phẩm, không cần dựng cảnh phức tạp.
4. **Khác biệt** — có trùng góc quay với video đã đăng gần đây không
   (đọc lịch sử trong `agent/data/published.json` nếu có).
5. **Dự đoán tương tác** — dựa trên dữ liệu feedback loop từ
   `channel-analytics-feedback` nếu đã có (ví dụ: angle "so sánh giá"
   từng cho CTR cao hơn → cộng điểm cho ý tưởng cùng angle).

## Quy trình

1. Đọc `agent/data/ideas_<ngày>.json`.
2. Chấm từng ý tưởng, ghi `score` (tổng 0-100) + `score_breakdown`.
3. Sắp giảm dần theo `score`, đánh dấu top theo số lượng video người
   dùng muốn sản xuất mỗi ngày (mặc định: tất cả 10, ưu tiên sản xuất
   trước những ý tưởng điểm cao nhất nếu giới hạn ngân sách API).
4. Cập nhật lại `agent/data/ideas_<ngày>.json` với điểm số, giữ
   `status: "proposed"` cho tới khi người dùng hoặc bước tiếp theo duyệt
   sang `status: "approved"`.
5. KHÔNG tự động chuyển sang sản xuất nếu điểm dưới ngưỡng do người dùng
   đặt (mặc định ngưỡng 60/100) — những ý tưởng dưới ngưỡng giữ nguyên
   `status: "rejected"` kèm lý do.
