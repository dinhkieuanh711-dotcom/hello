---
name: daily-agent-report
description: >
  Tổng hợp hoạt động trong ngày của agent (tin đã quét, ý tưởng đề xuất,
  điểm số, video đã sản xuất/đăng, thay đổi từ feedback loop) thành 1
  báo cáo ngắn. Chạy cuối mỗi chu kỳ ngày, sau tất cả các bước khác.
---

# Daily Agent Report

1. Đọc trong ngày: `news_<ngày>.json`, `ideas_<ngày>.json`,
   `published.json` (nếu có đăng), `scoring_weights_history.json` (nếu
   feedback loop vừa cập nhật).
2. Tóm tắt theo khối:
   - Số tin quét được, top 3 tin dùng được nhiều nhất.
   - 10 ý tưởng đề xuất + điểm số, bao nhiêu được duyệt/sản xuất/từ chối.
   - Video nào đã có kịch bản đầy đủ (`status: scripted`/`rendered`),
     cái nào đang chờ người dùng quyết định engine TTS/video-gen.
   - Nếu đã đăng: chỉ số thực tế + so sánh dự đoán + thay đổi trọng số.
   - Việc đang bị chặn (thiếu API key, thiếu token Facebook...).
3. Xuất báo cáo dạng Markdown ngắn (không quá 1 trang màn hình) vào
   `agent/data/reports/<ngày>.md`, và in tóm tắt 5-7 dòng ra chat cho
   người dùng.
