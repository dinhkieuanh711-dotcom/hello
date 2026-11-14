---
name: video-script-production
description: >
  Từ 1 ý tưởng đã duyệt (status: approved), tạo gói sản xuất đầy đủ:
  storyboard (dùng lại product-ugc-video-prompt), lời thoại voiceover
  timed theo giây, mood nhạc + hiệu ứng âm thanh, phụ đề. Đây là kịch
  bản sản xuất — việc render ra file mp4 thật cần nối API TTS + API
  video-gen (xem agent/README.md phần "Việc cần bạn quyết định").
---

# Video Script Production

## Giới hạn
Skill này tạo **kịch bản sản xuất đầy đủ** (text), không tự render ra
file âm thanh/video thật trong sandbox này — vì chưa có API TTS/video-gen
nào được kết nối. Khi người dùng nối 1 API cụ thể, bước cuối (gọi API,
lưu file) sẽ được thêm vào, không cần viết lại toàn bộ skill.

## Quy trình

1. Dùng `product-ugc-video-prompt` để lấy storyboard 5 cảnh cho sản phẩm
   trong ý tưởng.
2. Viết **lời thoại voiceover** cho từng cảnh, mỗi câu ghi mốc thời gian
   (vd `0:00-0:03`), độ dài câu khớp với thời lượng cảnh (~2.5 từ/giây
   tiếng Việt để lipsync/nhịp đọc tự nhiên).
3. Chọn **mood nhạc** (thể loại, tempo, năng lượng) — không chỉ định bài
   hát có bản quyền cụ thể trừ khi người dùng xác nhận có giấy phép.
4. Liệt kê **hiệu ứng** cần dùng: chuyển cảnh, hiệu ứng chữ (phụ đề bôi
   vàng từ khoá theo giây), hiệu ứng âm thanh (swoosh, tiếng kéo khoá...).
5. Xuất gói hoàn chỉnh dạng 1 file `agent/data/scripts/<id>.json` gồm:
   `storyboard`, `voiceover_lines`, `music_brief`, `sfx_cues`,
   `captions`. Đánh dấu ý tưởng `status: "scripted"`.
6. Nếu người dùng đã nối API TTS/video-gen (ghi trong
   `agent/config/engines.json`), gọi API theo thứ tự: TTS trước (có
   voiceover_lines) → video-gen nhận ảnh sản phẩm + storyboard + audio
   → ghép bằng `ffmpeg` theo cách render của skill `video-edit-ai-keynote`
   → lưu file final vào `agent/data/output/<id>.mp4`, đánh dấu
   `status: "rendered"`.
