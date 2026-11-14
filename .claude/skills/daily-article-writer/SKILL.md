---
name: daily-article-writer
description: >
  Tự viết tối thiểu 5 bài/ngày (bài viết hoặc kịch bản, tuỳ nội dung đang
  chạy — ADN Tái Sinh Rực Rỡ, hoặc chủ đề khác người dùng chọn), đẩy từng
  bài qua self-critique-score-loop, chỉ giữ bài đạt >= ngưỡng điểm
  (mặc định 95/100) để đưa vào hàng đợi đăng. Chạy đầu mỗi chu kỳ ngày,
  trước daily-agent-report.
---

# Daily Article Writer

## Quy trình hàng ngày

1. Đọc chủ đề/series đang chạy (mặc định: `adn-tai-sinh-ruc-ro-story`,
   hoặc chủ đề khác nếu người dùng đổi) + dữ liệu đề xuất từ
   `keyword-rank-feedback` (nếu đã có — bài nào nên viết tiếp, từ khoá
   nào đang thiếu nội dung).
2. Viết tối thiểu 5 bài nháp, mỗi bài 1 góc độ/chủ đề khác nhau (không
   trùng mô-típ 2 bài liền kề).
3. Đẩy từng bài qua `self-critique-score-loop` (tối đa 3 vòng/bài).
4. Phân loại kết quả:
   - `approved_for_publish` (>= ngưỡng điểm) → vào hàng đợi đăng thật.
   - `needs_human_review` (hết vòng vẫn chưa đạt) → giữ lại, liệt kê rõ
     lý do trong báo cáo ngày, KHÔNG tự đăng.
5. Nếu số bài `approved_for_publish` trong ngày < 5 (ví dụ 3/5 bài đạt
   95+), viết thêm bài mới để bù — không hạ ngưỡng để bài yếu lọt qua.
6. Ghi toàn bộ kết quả vào `agent/data/articles_<ngày>.json`:
   mỗi bài có `id`, `title`, `score`, `status`, `critique_rounds`,
   `target_keyword` (nếu là bài SEO).
7. Nếu đã kết nối kênh đăng thật (Facebook Graph API / CMS blog), đăng
   các bài `approved_for_publish`; nếu chưa, giữ trong hàng đợi chờ
   người dùng bật kết nối.

## Giới hạn
- Không tự ý đổi chủ đề/thương hiệu nội dung mà không có tín hiệu rõ
  ràng từ người dùng.
- Không viết về người thật có thể nhận diện được trừ khi người dùng xác
  nhận có quyền kể câu chuyện đó (xem giới hạn trong
  `adn-tai-sinh-ruc-ro-story`).
