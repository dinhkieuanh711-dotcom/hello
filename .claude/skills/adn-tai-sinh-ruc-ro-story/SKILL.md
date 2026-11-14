---
name: adn-tai-sinh-ruc-ro-story
description: >
  Viết kịch bản video kể chuyện series "ADN Tái Sinh Rực Rỡ" — chủ đề hôn
  nhân/gia đình, có twist xét nghiệm ADN, kết thúc theo hướng nhân vật
  chính vượt qua biến cố và "tái sinh rực rỡ". Xuất kịch bản giọng đọc
  timed theo giây, gợi ý hình ảnh/B-roll minh hoạ, mood nhạc, phụ đề —
  dùng cho video dạng AI voice kể chuyện trên nền ảnh/clip tư liệu.
  Dùng khi người dùng muốn video kể chuyện ADN/hôn nhân, không phải video
  UGC thời trang (đó là skill product-ugc-video-prompt).
---

# ADN Tái Sinh Rực Rỡ — Story Script

## Nguyên tắc bắt buộc
- **Nhân vật hư cấu**: trừ khi người dùng đưa 1 câu chuyện có thật và xác
  nhận có quyền kể (chính họ, hoặc người trong cuộc đồng ý), mọi câu
  chuyện viết ra đều là hư cấu/dàn dựng từ mô-típ phổ biến — không gán
  tên, hình ảnh, chi tiết nhận diện được của người có thật ngoài đời.
  Luôn ghi rõ trong caption video: "Nội dung mang tính chất hư cấu/giải
  trí" khi câu chuyện không có nguồn thật.
- **Không dùng hình ảnh/video người thật không đồng ý** để minh hoạ nhân
  vật — gợi ý dùng ảnh/clip stock chung chung (bàn tay, phong bì kết quả,
  khung cảnh phòng khách...) thay vì ảnh một người cụ thể.
- **Giữ tông redemption**: mọi kịch bản đều có hồi kết nhân vật chính
  mạnh mẽ hơn/ổn định hơn sau biến cố — không khai thác bi kịch đơn thuần
  không lối thoát.

## Cấu trúc kịch bản (chuẩn series, ~60-90 giây)

1. **Hook (0-5s)** — câu mở gây tò mò ngay, thường là 1 câu thoại/nghi
   vấn gây sốc nhẹ (vd: "Tờ giấy xét nghiệm ấy đã thay đổi cả cuộc đời
   tôi — nhưng không theo cách tôi nghĩ.").
2. **Bối cảnh (5-20s)** — giới thiệu nhân vật, hoàn cảnh hôn nhân/gia
   đình, mâu thuẫn tiềm ẩn.
3. **Biến cố — xét nghiệm ADN (20-40s)** — tình huống dẫn tới xét
   nghiệm, khoảnh khắc chờ kết quả, cú twist.
4. **Giằng co cảm xúc (40-60s)** — phản ứng, lựa chọn của nhân vật chính.
5. **Tái sinh rực rỡ (60-90s)** — nhân vật chính đứng dậy, kết thúc có
   hậu/mạnh mẽ, câu chốt mang tính thông điệp (không thuyết giáo dài).

## Output cho mỗi tập

- `voiceover_script`: lời dẫn chuyện, chia theo mốc giây như trên, tốc độ
  ~2.3-2.5 từ/giây tiếng Việt cho giọng đọc tự nhiên.
- `visual_cues`: gợi ý hình ảnh/B-roll cho từng đoạn (stock, không phải
  người thật) + kiểu chuyển cảnh.
- `music_brief`: mood nhạc theo từng đoạn (căng thẳng → lắng xuống →
  nhẹ nhõm/hy vọng ở đoạn tái sinh), không chỉ định bài hát có bản quyền.
- `captions`: phụ đề 1 dòng/giây, bôi vàng từ khoá cảm xúc/twist.
- `title_card`: "ADN TÁI SINH RỰC RỠ" + số tập, style chữ theo thương
  hiệu series (có thể dùng tông màu/kiểu chữ riêng nếu người dùng cung
  cấp bộ nhận diện).
- Lưu vào `agent/data/scripts_adn/<id>.json`, đánh dấu
  `status: "scripted"` để `video-script-production`/pipeline render
  dùng chung logic TTS + video-gen đã có.
