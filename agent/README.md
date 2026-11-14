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
| 9 | Tự viết ≥5 bài/ngày + tự phản biện + tự chấm điểm | `daily-article-writer` + `self-critique-score-loop` | ✅ chạy được ngay (ngưỡng đăng mặc định 95/100) |
| 10 | Quét thứ hạng từ khoá + tự đề xuất bài mới | `keyword-rank-feedback` | ⚠️ cần Google Search Console hoặc 1 API rank-tracking (xem `agent/config/seo.json.example`) |
| 11 | Chạy 100% tự động hàng ngày, không cần mở chat | — | ⚠️ xem mục "Tự động hoá thật" bên dưới — quan trọng, đọc trước khi cho rằng việc này đã xong |

## Tự động hoá thật — giới hạn của CronCreate trong phiên chat này

`CronCreate` (công cụ đặt lịch có sẵn trong Claude Code) **chỉ sống
trong phiên chat này**: không ghi ra đĩa, tự hết hạn sau 7 ngày, và chỉ
chạy khi phiên chat này còn đang mở. Môi trường chạy Claude Code cũng bị
thu hồi khi không hoạt động. Nói cách khác: nếu chỉ dùng `CronCreate`,
hệ thống **sẽ không** thực sự "tự chạy mãi mãi không cần bạn" — nó âm
thầm dừng sau vài ngày hoặc khi phiên đóng, và bạn sẽ không được báo.

Cách duy nhất để có lịch chạy hàng ngày thật sự độc lập với phiên chat
này: **GitHub Actions** (lịch cron thật trên GitHub, chạy trên server
của GitHub chứ không phải trong phiên Claude Code). Cần:
- 1 Anthropic API key riêng (khác tài khoản Claude Code đang dùng),
  thêm làm GitHub Actions secret (không dán vào chat).
- 1 workflow `.github/workflows/daily-pipeline.yml` chạy script gọi API
  đó để thực hiện từng bước (viết bài, phản biện, chấm điểm...) và ghi
  kết quả/báo cáo vào repo hoặc gửi thông báo.

Việc này cần bạn xác nhận trước khi làm (tốn API quota thật, chạy không
giám sát hàng ngày) — xem câu hỏi cuối cùng ở hội thoại.

### Đã dựng: `.github/workflows/daily-content-pipeline.yml`

Chạy thật trên GitHub, 09:00 giờ VN mỗi ngày (hoặc bấm chạy tay qua tab
Actions). Script: `agent/scripts/daily_pipeline.py`. Để chạy được, vào
**Settings → Secrets and variables → Actions** của repo, thêm các secret
sau (Claude không thể tự thêm secret thay bạn — đây là thao tác chỉ chủ
repo làm được):

| Secret | Bắt buộc? | Dùng để |
|---|---|---|
| `ANTHROPIC_API_KEY` | **Bắt buộc** | Viết bài + tự phản biện + chấm điểm. Không có thì pipeline dừng ngay, không chạy gì. |
| `ELEVENLABS_API_KEY` + `ELEVENLABS_VOICE_ID` | Tuỳ chọn | Tạo giọng đọc thật. Thiếu thì bỏ qua bước này, báo rõ trong report. |
| `RUNWAY_API_KEY` | Tuỳ chọn | Hiện mới dừng ở mức đọc được key — phần gọi API video-gen thật **chưa viết**, vì cần xác nhận lại format request hiện tại của Runway trước (xem ghi chú trong script). |
| `FB_PAGE_ID` + `FB_PAGE_ACCESS_TOKEN` | Tuỳ chọn | Đăng bài lên Facebook Page. Thiếu thì bỏ qua, báo rõ trong report. |
| `SEO_API_KEY` | Tuỳ chọn | Quét thứ hạng từ khoá — hiện mới đọc key, chưa gọi API thật (cần chọn provider cụ thể trước). |

Mỗi lần chạy, pipeline ghi kết quả vào `agent/data/articles_<ngày>.json`
và báo cáo vào `agent/data/reports/<ngày>.md`, rồi tự commit lại vào
repo — bạn xem trực tiếp trong repo hoặc tab Actions, không cần mở lại
chat này.

**Vẫn thiếu để "100% không cần bạn"**: TTS và Facebook posting đã viết
code thật (best-effort theo cấu trúc API đã biết — nên kiểm tra lần chạy
đầu để chắc chắn đúng), còn Runway/Kling/Luma (render video) và quét
thứ hạng từ khoá (SEO) mới dừng ở khung sườn, chưa có lệnh gọi API thật
— sẽ hoàn thiện ngay khi bạn chọn xong provider cụ thể và xác nhận
format request hiện tại của provider đó.

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

## Lựa chọn đã chốt: full automation

Bạn đã chọn: **giọng AI chung (ElevenLabs/OpenAI TTS)** + **video API trả
phí (Runway/Kling/Luma)** + **Facebook Graph API**. Cả 3 đều cần bạn tự
đăng ký/tạo credential — Claude không thể tạo tài khoản, thanh toán, hay
xin quyền ứng dụng thay bạn. Sau khi bạn điền vào các file dưới, nói với
agent để nối phần gọi API thật (hiện là template rỗng, không auto-chạy
cho tới khi có key thật).

### 1. ElevenLabs/OpenAI TTS
- Đăng ký tài khoản, lấy API key trong phần cài đặt nhà cung cấp.
- Chọn 1 giọng tiếng Việt có sẵn trên dashboard, copy `voice_id`.
- Điền vào `agent/config/engines.json` (copy từ `engines.json.example`).

### 2. Runway / Kling / Luma (video-gen)
- Đăng ký tài khoản nhà cung cấp bạn chọn, mua credit, lấy API key.
- Điền vào cùng file `agent/config/engines.json`, mục `video`.
- Đặt `budget.daily_cap_usd` theo mức bạn chấp nhận chi mỗi ngày — pipeline
  sẽ dừng render tự động nếu vượt mức, tránh chi phí ngoài kiểm soát khi
  chạy 10 video/ngày không giám sát.

### 3. Facebook Graph API
- Tạo 1 Meta App tại Meta for Developers (loại "Business").
- Thêm sản phẩm "Facebook Login" + xin quyền `pages_manage_posts`,
  `pages_read_engagement`, `pages_show_list`.
- Lấy Page Access Token, sau đó đổi sang **long-lived token** (không phải
  loại hết hạn sau 1-2 giờ) — nếu không chắc cách đổi, nói với agent, sẽ
  hướng dẫn cụ thể khi bạn có token ngắn hạn trong tay.
- Điền `page_id`, `page_access_token`, `app_id`, `app_secret` vào
  `agent/config/facebook.json` (copy từ `facebook.json.example`).
- Hai file config thật (`engines.json`, `facebook.json`) đã được
  `.gitignore` — sẽ không bị đẩy lên GitHub cùng mã nguồn.

### An toàn khi chạy full automation
Vì bạn chọn tự động hoàn toàn (không duyệt tay trước khi đăng), đề xuất
giữ lại 1 lớp an toàn tối thiểu: ngưỡng điểm từ `content-scorer` (mặc
định 60/100) vẫn chặn ý tưởng điểm thấp trước khi tới bước render/đăng,
và `budget.daily_cap_usd` chặn chi phí vượt mức — cả hai đều có thể tắt
nếu bạn muốn 100% không có lớp chặn nào.

## Tính năng đề xuất thêm (ngoài 8 ý của bạn)

- Hàng đợi duyệt thủ công trước khi đăng (an toàn, tránh đăng nhầm)
- Theo dõi chi phí API theo ngày/tháng (TTS + video-gen tốn tiền thật)
- Kiểm tra bản quyền nhạc/hình trước khi đăng
- Lưu lịch sử prompt/kịch bản theo từng video để feedback loop có "trí nhớ"
- Lịch nội dung dạng calendar trong dashboard
- Cảnh báo khi không được dùng tên thương hiệu thật (Hermès, Saint Laurent...)
  làm như sản phẩm đang bán là hàng chính hãng nếu không phải
