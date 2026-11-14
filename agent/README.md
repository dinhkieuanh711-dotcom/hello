# Fashion Content Agent — kiến trúc & trạng thái

Agent gồm 6 bước, map với yêu cầu gốc. Mỗi bước là 1 skill trong
`.claude/skills/`. Trạng thái triển khai thực tế (không tô hồng):

| # | Bước | Skill | Trạng thái |
|---|------|-------|------------|
| 1 | Quét tin thời trang | `fashion-news-scanner` | ✅ chạy được ngay (web search) |
| 2 | Đề xuất 10 ý tưởng/ngày | `daily-content-proposer` | ✅ chạy được ngay |
| 3 | Duyệt + chấm điểm | `content-scorer` | ✅ chạy được ngay |
| 3b| Tạo video (giọng+nhạc+hiệu ứng) | `video-script-production` | ⚠️ ra **kịch bản sản xuất đầy đủ** (lời thoại, nhạc, hiệu ứng, storyboard) — render ra file mp4 thật cần nối 1 API TTS + 1 API video-gen do bạn chọn (xem README phần "Việc cần bạn quyết định") |
| 4 | Upload Facebook | — | ❌ chưa làm được từ sandbox này — xem phần dưới |
| 5 | Quét chỉ số kênh + feedback loop | `channel-analytics-feedback` | ⚠️ cần Facebook Page access token (Graph API) từ bạn |
| 6 | Đề xuất repo/tool | README này | ✅ xem danh sách bên dưới |
| 7 | Giao diện quản lý | `agent/dashboard/` (Artifact) | ✅ đã có bản đầu |
| 8 | Báo cáo hàng ngày | `daily-agent-report` | ✅ chạy được ngay |

## Vì sao bước 4 (upload Facebook) và 5 (quét chỉ số) chưa tự động được

- Session này chạy trong sandbox cloud, không resolve được
  `web.facebook.com` (đã test), và không có trình duyệt thật đăng nhập
  Facebook của bạn — nên **không thể** tự bấm "đăng bài" qua trình duyệt
  từ đây, dù bạn có yêu cầu.
- Hai cách thay thế thật sự chạy được:
  1. **Facebook Graph API** (khuyến nghị): bạn tạo 1 Meta App + lấy Page
     Access Token cho kênh. Agent gọi API để đăng bài + đọc Insights
     (view, like, share, comment) — tự động 100%, không cần trình duyệt.
  2. **Bán tự động**: agent xuất sẵn file video + caption, bạn tự đăng
     bằng tay trên máy của chính bạn (không phải trong sandbox này).

## Repo / công cụ đề xuất cài thêm (bước 6)

| Nhu cầu | Lựa chọn | Ghi chú |
|---|---|---|
| Giọng nói AI | ElevenLabs API, hoặc OpenAI TTS | Cloud, trả theo usage, nhân bản giọng cần file giọng mẫu + sự đồng ý |
| Giọng nói AI (chạy local, miễn phí) | Coqui XTTS-v2 / F5-TTS (GitHub) | Cần GPU, tự host, không phí API |
| Video AI (có API thật) | Runway Gen-4, Kling API, Luma Dream Machine | Google Flow/Veo hiện chủ yếu thao tác tay qua UI, chưa có API công khai ổn định |
| Nhạc nền | Suno API, hoặc thư viện nhạc có bản quyền thương mại (Epidemic Sound/Artlist) | Tránh dùng nguyên bài hát có bản quyền của kênh khác |
| Dựng/ghép video cuối | `ffmpeg` (đã có sẵn trong môi trường này) | Dùng lại cách render của skill `video-edit-ai-keynote` |
| Đăng + đo chỉ số Facebook | Facebook Graph API (Meta for Developers) | Cần Page token, không dùng trình duyệt |
| Lưu trạng thái pipeline | SQLite file trong `agent/data/` hoặc DB của dashboard Artifact | Nhẹ, không cần server riêng |
| Lịch chạy hàng ngày | `CronCreate` (có sẵn trong Claude Code) | Khỏi cần cài n8n/Zapier nếu chạy trong Claude Code |

**Chưa tự cài** các repo trên vì đều là dịch vụ trả phí/cần API key hoặc
GPU riêng — cần bạn chọn trước (xem câu hỏi cuối hội thoại).

## Tính năng đề xuất thêm (ngoài 8 ý của bạn)

- Hàng đợi duyệt thủ công trước khi đăng (an toàn, tránh đăng nhầm)
- Theo dõi chi phí API theo ngày/tháng (TTS + video-gen tốn tiền thật)
- Kiểm tra bản quyền nhạc/hình trước khi đăng
- Lưu lịch sử prompt/kịch bản theo từng video để feedback loop có "trí nhớ"
- Lịch nội dung dạng calendar trong dashboard
- Cảnh báo khi không được dùng tên thương hiệu thật (Hermès, Saint Laurent...)
  làm như sản phẩm đang bán là hàng chính hãng nếu không phải
