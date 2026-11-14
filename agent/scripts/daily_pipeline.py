"""
Daily content pipeline — chạy bởi .github/workflows/daily-content-pipeline.yml.

Đọc chính các file SKILL.md trong .claude/skills/ làm nguồn hướng dẫn
(adn-tai-sinh-ruc-ro-story, self-critique-score-loop) để logic ở đây và
logic khi chạy trong Claude Code chat luôn khớp nhau.

TTS (ElevenLabs) và Facebook posting có implementation thật (best-effort
theo cấu trúc API đã biết, NÊN kiểm tra lại với docs hiện tại của từng
provider trước khi tin tưởng chạy không giám sát lâu dài). Video-gen
(Runway/Kling/Luma) và SEO/keyword-rank CHƯA implement thật — mỗi
provider có format request khác nhau và cần xác nhận cụ thể trước khi
viết, nên để stub rõ ràng thay vì đoán và báo sai là "đã xong".
"""
import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
DATA_DIR = REPO_ROOT / "agent" / "data"
TODAY = date.today().isoformat()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SCORE_THRESHOLD = int(os.environ.get("SCORE_THRESHOLD", "95"))
MAX_CRITIQUE_ROUNDS = 3
MIN_ARTICLES_PER_DAY = 5

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID")
RUNWAY_API_KEY = os.environ.get("RUNWAY_API_KEY")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
SEO_API_KEY = os.environ.get("SEO_API_KEY")


def log(msg):
    print(f"[{datetime.utcnow().isoformat()}Z] {msg}", flush=True)


def read_skill(name):
    path = SKILLS_DIR / name / "SKILL.md"
    if not path.exists():
        raise FileNotFoundError(f"Thiếu skill {name} tại {path}")
    return path.read_text(encoding="utf-8")


def call_claude(system, user, max_tokens=2000):
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("Thiếu ANTHROPIC_API_KEY — không thể gọi Claude API.")
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-sonnet-5",
            "max_tokens": max_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"Không tìm thấy JSON trong phản hồi: {text[:200]}")
    return json.loads(match.group(0))


def generate_ideas(story_skill, n):
    prompt = (
        f"Dựa trên hướng dẫn series sau:\n\n{story_skill}\n\n"
        f"Đề xuất {n} ý tưởng tập mới, mỗi ý tưởng 1 góc độ khác nhau, "
        "không trùng mô-típ. Trả về JSON: "
        '{"ideas": [{"title": "...", "premise": "..."}]}'
    )
    data = extract_json(call_claude("Bạn là biên kịch series ADN Tái Sinh Rực Rỡ.", prompt))
    return data["ideas"][:n]


def write_draft(story_skill, idea):
    prompt = (
        f"Hướng dẫn series:\n\n{story_skill}\n\n"
        f"Viết kịch bản đầy đủ cho ý tưởng: {idea['title']} — {idea['premise']}. "
        "Theo đúng cấu trúc 5 phần trong hướng dẫn, có mốc thời gian."
    )
    return call_claude("Bạn là biên kịch series ADN Tái Sinh Rực Rỡ.", prompt, max_tokens=3000)


def critique_and_score(critique_skill, draft):
    prompt = (
        f"Tiêu chí chấm điểm:\n\n{critique_skill}\n\n"
        f"Bản nháp:\n\n{draft}\n\n"
        "Đóng vai biên tập viên khó tính: liệt kê điểm yếu cụ thể theo "
        "5 tiêu chí, rồi chấm điểm. Trả về JSON: "
        '{"critique": "...", "score_breakdown": {"hook": 0, "structure": 0, '
        '"tone": 0, "message": 0, "distribution": 0}, "total": 0}'
    )
    return extract_json(call_claude("Bạn là biên tập viên khó tính.", prompt, max_tokens=1500))


def revise(draft, critique):
    prompt = (
        f"Bản nháp:\n\n{draft}\n\nPhản biện cần sửa:\n\n{critique}\n\n"
        "Viết lại bản hoàn chỉnh đã sửa theo đúng từng điểm phản biện."
    )
    return call_claude("Bạn là biên kịch đang sửa bài theo phản biện.", prompt, max_tokens=3000)


def run_self_critique_loop(story_skill, critique_skill, idea):
    draft = write_draft(story_skill, idea)
    rounds = []
    for round_num in range(1, MAX_CRITIQUE_ROUNDS + 1):
        result = critique_and_score(critique_skill, draft)
        rounds.append({"round": round_num, "score": result["total"], "breakdown": result["score_breakdown"]})
        if result["total"] >= SCORE_THRESHOLD:
            return {
                "title": idea["title"], "content": draft, "status": "approved_for_publish",
                "final_score": result["total"], "rounds": rounds,
            }
        draft = revise(draft, result["critique"])
    return {
        "title": idea["title"], "content": draft, "status": "needs_human_review",
        "final_score": rounds[-1]["score"] if rounds else None, "rounds": rounds,
        "reason": f"Hết {MAX_CRITIQUE_ROUNDS} vòng vẫn chưa đạt {SCORE_THRESHOLD}/100.",
    }


def synthesize_voice(text, out_path):
    if not (ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID):
        log("Bỏ qua TTS — thiếu ELEVENLABS_API_KEY/ELEVENLABS_VOICE_ID.")
        return None
    try:
        resp = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
            headers={"xi-api-key": ELEVENLABS_API_KEY, "content-type": "application/json"},
            json={"text": text, "model_id": "eleven_multilingual_v2"},
            timeout=120,
        )
        resp.raise_for_status()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(resp.content)
        return str(out_path)
    except Exception as e:
        log(f"Lỗi TTS: {e} — bỏ qua, không chặn pipeline.")
        return None


def render_video_stub(article_id):
    if not RUNWAY_API_KEY:
        log("Bỏ qua render video — thiếu RUNWAY_API_KEY.")
        return None
    log(
        f"[{article_id}] RUNWAY_API_KEY đã có nhưng việc gọi API video-gen thật "
        "CHƯA được implement — cần xác nhận lại endpoint/payload hiện tại của "
        "Runway trước khi viết, tránh đoán sai và chạy im lặng thất bại."
    )
    return None


def post_to_facebook(message, video_path=None):
    if not (FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN):
        log("Bỏ qua đăng Facebook — thiếu FB_PAGE_ID/FB_PAGE_ACCESS_TOKEN.")
        return None
    try:
        if video_path:
            with open(video_path, "rb") as f:
                resp = requests.post(
                    f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/videos",
                    data={"access_token": FB_PAGE_ACCESS_TOKEN, "description": message},
                    files={"source": f},
                    timeout=300,
                )
        else:
            resp = requests.post(
                f"https://graph.facebook.com/v21.0/{FB_PAGE_ID}/feed",
                data={"access_token": FB_PAGE_ACCESS_TOKEN, "message": message},
                timeout=60,
            )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        log(f"Lỗi đăng Facebook: {e} — bỏ qua, không chặn pipeline.")
        return None


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "reports").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "audio").mkdir(parents=True, exist_ok=True)

    if not ANTHROPIC_API_KEY:
        log("THIẾU ANTHROPIC_API_KEY — dừng pipeline, không có gì chạy được hôm nay.")
        sys.exit(1)

    story_skill = read_skill("adn-tai-sinh-ruc-ro-story")
    critique_skill = read_skill("self-critique-score-loop")

    ideas = generate_ideas(story_skill, MIN_ARTICLES_PER_DAY)
    articles = []
    for idea in ideas:
        log(f"Viết + phản biện: {idea['title']}")
        try:
            result = run_self_critique_loop(story_skill, critique_skill, idea)
        except Exception as e:
            log(f"Lỗi khi xử lý '{idea['title']}': {e}")
            continue
        result["id"] = re.sub(r"[^a-z0-9]+", "-", idea["title"].lower()).strip("-")[:40]
        articles.append(result)

        if result["status"] == "approved_for_publish":
            synthesize_voice(result["content"][:2500], DATA_DIR / "audio" / f"{result['id']}.mp3")
            render_video_stub(result["id"])
            # Chỉ đăng khi có cả FB token — hiện chưa có video thật nên đây sẽ
            # tự bỏ qua (post_to_facebook) cho tới khi render_video_stub xong.
            post_to_facebook(result["title"], video_path=None)

    out_path = DATA_DIR / f"articles_{TODAY}.json"
    out_path.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")

    approved = [a for a in articles if a["status"] == "approved_for_publish"]
    needs_review = [a for a in articles if a["status"] == "needs_human_review"]

    report = [
        f"# Báo cáo pipeline ngày {TODAY}",
        "",
        f"- Bài viết hôm nay: {len(articles)} (mục tiêu tối thiểu {MIN_ARTICLES_PER_DAY})",
        f"- Đạt ngưỡng {SCORE_THRESHOLD}/100: {len(approved)}",
        f"- Cần người duyệt: {len(needs_review)}",
        "",
        "## Việc đang bị chặn" if not (ELEVENLABS_API_KEY and RUNWAY_API_KEY and FB_PAGE_ACCESS_TOKEN and SEO_API_KEY) else "",
    ]
    if not ELEVENLABS_API_KEY:
        report.append("- Chưa có ELEVENLABS_API_KEY — không tạo được giọng đọc thật.")
    if not RUNWAY_API_KEY:
        report.append("- Chưa có RUNWAY_API_KEY, và việc gọi API video-gen thật còn chưa code — không render được video thật.")
    if not (FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN):
        report.append("- Chưa có FB_PAGE_ID/FB_PAGE_ACCESS_TOKEN — không đăng được lên Facebook.")
    if not SEO_API_KEY:
        report.append("- Chưa có SEO_API_KEY/Search Console — không quét được thứ hạng từ khoá.")

    report_path = DATA_DIR / "reports" / f"{TODAY}.md"
    report_path.write_text("\n".join(report), encoding="utf-8")
    log("\n".join(report))

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
