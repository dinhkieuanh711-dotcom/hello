---
name: product-ugc-video-prompt
description: >
  Từ một ảnh sản phẩm (túi, áo, trang sức...) chụp kiểu flatlay sang trọng
  (nền tối, hộp/túi thương hiệu, phụ kiện bên cạnh), tạo ra bộ storyboard +
  prompt video sẵn dùng cho công cụ AI video (Google Flow, Veo, Runway...)
  theo phong cách "luxury reveal / UGC thử đồ" phổ biến trên các kênh
  reseller thời trang. Dùng khi người dùng đưa ảnh sản phẩm và muốn ra
  video có người mẫu mặc/dùng sản phẩm đó, theo tông tối + chữ vàng nhấn,
  nhạc nền sang trọng, phụ đề ngắn theo nhịp nói.
---

# Product UGC Video Prompt

## Giới hạn quan trọng
Skill này tạo phong cách chung của thể loại (dark luxury flatlay → reveal →
try-on → CTA), KHÔNG sao chép giọng nói/khuôn mặt thật của một người cụ thể
từ một kênh khác. Nếu người dùng muốn dùng giọng của chính họ, dùng audio
họ tự thu. Không tự ý tải/giả lập video từ một trang Facebook/TikTok khác.

## Quy trình

1. **Đọc ảnh sản phẩm đầu vào.** Ghi nhận: loại sản phẩm, màu sắc, chất
   liệu, phụ kiện đi kèm trong khung hình (túi, giày, kính, hộp thương
   hiệu), chữ/logo overlay đã có sẵn trên ảnh (tên shop, mã sản phẩm).

2. **Dựng storyboard 5 cảnh chuẩn thể loại** (mỗi cảnh 2-4 giây, tổng
   video 10-15 giây dọc 9:16):
   - **Cảnh 1 - Hook/Flatlay:** y nguyên bố cục ảnh gốc (treo trên móc,
     nền tối, phụ kiện xung quanh), camera lia nhẹ/push-in chậm.
   - **Cảnh 2 - Reveal chi tiết:** cận cảnh chất liệu, đường may, nút áo,
     khoá kéo — ánh sáng vàng ấm quét qua bề mặt.
   - **Cảnh 3 - Try-on:** người mẫu mặc/cầm sản phẩm, xoay người 360°
     chậm, biểu cảm tự tin.
   - **Cảnh 4 - Phối đồ:** toàn thân với phụ kiện đi kèm trong ảnh gốc.
   - **Cảnh 5 - CTA:** đứng yên nhìn thẳng camera, text giá/mã sản phẩm
     hiện lên.

3. **Sinh prompt cho từng cảnh** theo khung: [chủ thể] + [hành động] +
   [ống kính/chuyển động camera] + [ánh sáng] + [màu nền]. Ghi rõ nền đen
   ấm, viền vignette, điểm nhấn ánh vàng — khớp màu với ảnh gốc.

4. **Đề xuất nhạc theo mood, không theo track cụ thể**: ví dụ "nhạc
   piano/strings tối giản, tempo chậm, sang trọng" thay vì chỉ định một
   bài hát có bản quyền.

5. **Phụ đề:** 1 dòng ngắn/giây, bôi vàng từ khoá (tên sản phẩm, chất
   liệu, mã hàng), style giống `video-edit-ai-keynote` nếu skill đó có
   sẵn trong session.

6. **Xuất kết quả** dưới dạng danh sách cảnh có thể dán thẳng vào Google
   Flow / Veo / Runway, cộng gợi ý nhạc + caption.
