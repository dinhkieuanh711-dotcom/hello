---
name: self-critique-score-loop
description: >
  Vòng lặp tự viết - tự phản biện - tự sửa - tự chấm điểm cho bất kỳ nội
  dung dạng bài viết/kịch bản nào (dùng bởi daily-article-writer,
  adn-tai-sinh-ruc-ro-story, daily-content-proposer...). Chỉ đánh dấu
  "approved_for_publish" khi đạt ngưỡng điểm do người dùng đặt (mặc định
  95/100). Không tự hạ tiêu chí để đạt điểm — hết số vòng mà chưa đạt thì
  chuyển trạng thái "needs_human_review", không tự đăng.
---

# Self-Critique Score Loop

## Tiêu chí chấm điểm (mặc định — agent có thể tinh chỉnh dần qua feedback loop thật, không tự ý hạ chuẩn)

5 tiêu chí, mỗi tiêu chí tối đa 20 điểm:

1. **Hook/mở đầu** — 3 dòng/3 giây đầu có giữ được người đọc/xem không.
2. **Cấu trúc & mạch logic** — các đoạn nối nhau hợp lý, không lủng củng.
3. **Văn phong & cảm xúc** — đúng giọng thương hiệu (vd: redemption cho
   series ADN, UGC tự nhiên cho video sản phẩm).
4. **Giá trị/thông điệp** — có rút ra được điều gì đó, không sáo rỗng.
5. **Tối ưu kênh phân phối** — từ khoá/SEO nếu là bài viết web, hoặc
   hook/caption nếu là mạng xã hội.

Ghi `score_breakdown` theo từng tiêu chí, không chỉ ghi tổng điểm — để
sau này feedback loop biết chính xác điểm nào cần cải thiện.

## Quy trình (tối đa 3 vòng lặp)

1. **Viết nháp** (dùng skill nội dung tương ứng: `daily-article-writer`,
   `adn-tai-sinh-ruc-ro-story`...).
2. **Tự phản biện** — đóng vai 1 biên tập viên khó tính, liệt kê CỤ THỂ
   từng điểm yếu theo 5 tiêu chí trên (không viết chung chung "cần hay
   hơn" — phải chỉ rõ câu/đoạn nào yếu và vì sao).
3. **Tự sửa** theo đúng từng điểm phản biện vừa nêu.
4. **Chấm lại điểm** theo 5 tiêu chí, ghi `score_breakdown` + tổng.
5. Nếu tổng `>= threshold` (mặc định 95) → `status: "approved_for_publish"`,
   dừng vòng lặp.
   Nếu `< threshold` và chưa đủ 3 vòng → quay lại bước 2 với bản đã sửa.
   Nếu hết 3 vòng vẫn `< threshold` → `status: "needs_human_review"`,
   kèm lý do cụ thể (tiêu chí nào thấp nhất, vì sao không sửa được thêm)
   — **không** tự đăng, không tự nới lỏng tiêu chí để "đạt điểm giả".
6. Lưu toàn bộ lịch sử các vòng (draft, critique, score từng vòng) vào
   `agent/data/critique_log/<id>.json` — đây là dữ liệu để
   `keyword-rank-feedback`/feedback loop sau này học dần tiêu chí nào
   thực sự tương quan với hiệu quả thật, từ đó tinh chỉnh trọng số theo
   dữ liệu thật, không phải đoán.
