"""
Video Repurposing Tool
- Download video from any URL (YouTube, TikTok, Instagram, etc.)
- Transcribe with faster-whisper (free, local)
- Split into short clips (~30-60s)
- Crop to vertical 9:16
- Burn subtitles
- Output ready-to-upload files

Usage:
    python scripts/repurpose.py <url> [--hashtags "tag1 tag2 tag3"] [--clip-duration 45]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yt_dlp


def download_video(url, output_dir):
    """Download video from any URL using yt-dlp."""
    print(f"[1/5] Downloading: {url}")
    ydl_opts = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = str(output_dir / f"{info['title']}.mp4")
        # Handle characters that might cause issues
        safe_title = "".join(c for c in info["title"] if c.isalnum() or c in " _-").strip()
        final_path = output_dir / f"{safe_title}.mp4"
        if not final_path.exists():
            # Find the actual downloaded file
            for f in output_dir.glob("*.mp4"):
                return str(f)
        return str(final_path)


def transcribe(video_path):
    """Transcribe video using faster-whisper."""
    print(f"[2/5] Transcribing (this may take a while)...")
    from faster_whisper import WhisperModel

    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, info = model.transcribe(video_path, language="en")
    result = []
    for seg in segments:
        result.append({
            "start": seg.start,
            "end": seg.end,
            "text": seg.text.strip(),
        })
    return result


def split_into_clips(video_path, segments, clip_duration=45, overlap=5):
    """Split video into clips based on transcription segments."""
    print(f"[3/5] Splitting into clips (~{clip_duration}s each)...")
    if not segments:
        # Fallback: split by duration
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", video_path],
            capture_output=True, text=True
        )
        info = json.loads(probe.stdout)
        duration = float(info["format"]["duration"])
        clips = []
        for start in range(0, int(duration), clip_duration - overlap):
            end = min(start + clip_duration, duration)
            clips.append((start, end))
        return clips

    clips = []
    clip_start = segments[0]["start"]
    last_end = segments[-1]["end"]

    for i, seg in enumerate(segments):
        if seg["end"] - clip_start >= clip_duration or (i == len(segments) - 1):
            end = min(seg["end"], clip_start + clip_duration + overlap)
            if end - clip_start >= 15:  # minimum 15s clip
                clips.append((clip_start, end))
            clip_start = max(0, end - overlap)

    # If no clips were created, make one from the whole video
    if not clips:
        clips.append((0, min(last_end, clip_duration)))
    return clips


def crop_to_vertical(input_path, output_path, start_time, end_time):
    """Crop video to vertical 9:16 and add subtitles."""
    print(f"    Cropping clip {start_time:.1f}s - {end_time:.1f}s...")

    # Get video dimensions
    probe = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", input_path],
        capture_output=True, text=True
    )
    info = json.loads(probe.stdout)
    stream = next(s for s in info["streams"] if s["codec_type"] == "video")
    width = int(stream["width"])
    height = int(stream["height"])

    # Calculate vertical crop (9:16 center crop)
    target_aspect = 9 / 16
    current_aspect = width / height

    if current_aspect > target_aspect:
        # Wider than 9:16 - crop sides
        new_width = int(height * target_aspect)
        x_offset = (width - new_width) // 2
        crop = f"{new_width}:{height}:{x_offset}:0"
        scale = f"scale=1080:1920"
    else:
        # Taller than 9:16 - crop top/bottom
        new_height = int(width / target_aspect)
        y_offset = (height - new_height) // 2
        crop = f"{width}:{new_height}:0:{y_offset}"
        scale = f"scale=1080:1920"

    # Cut and crop
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", input_path,
        "-t", str(end_time - start_time),
        "-vf", f"crop={crop},{scale}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        output_path,
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return True


def _format_srt_time(seconds):
    """Format seconds as SRT timestamp (HH:MM:SS,mmm)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _wrap_text(text, max_chars=35):
    """Wrap text to fit within subtitle width."""
    words = text.split()
    lines = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 > max_chars:
            lines.append(current)
            current = w
        else:
            current = (current + " " + w).strip()
    if current:
        lines.append(current)
    return "\n".join(lines)


def _generate_srt(segments, start_offset):
    """Generate SRT subtitle content from segments."""
    lines = []
    for i, seg in enumerate(segments, 1):
        rel_start = max(0, seg["start"] - start_offset)
        rel_end = seg["end"] - start_offset
        if rel_end - rel_start <= 0:
            continue
        text = _wrap_text(seg["text"])
        lines.append(str(i))
        lines.append(f"{_format_srt_time(rel_start)} --> {_format_srt_time(rel_end)}")
        lines.append(text)
        lines.append("")
    return "\n".join(lines)


def add_subtitles(clip_path, segments, start_offset, output_path):
    """Burn subtitles into video (hard-burn) using ffmpeg subtitles filter."""
    print(f"    Adding captions...")

    clip_dir = Path(clip_path).parent
    srt_name = f"subs_{Path(clip_path).stem}.srt"
    srt_path = clip_dir / srt_name
    srt_path.write_text(_generate_srt(segments, start_offset), encoding="utf-8")

    # Hard-burn using relative filename (avoids Windows path escaping issues)
    vf = (
        f"subtitles={srt_name}"
        f":force_style='FontName=Arial,FontSize=18,PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,"
        f"Alignment=2,MarginV=40'"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", clip_path,
        "-vf", vf,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_path,
    ]

    # Run from clip directory so relative path resolves
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=clip_dir)
    srt_path.unlink(missing_ok=True)

    if result.returncode != 0:
        print(f"    Hard-burn failed, falling back to soft subs: {result.stderr[-200:]}")
        # Fallback: embed SRT as subtitle stream
        fallback_srt = clip_dir / f"fallback_{srt_name}"
        fallback_srt.write_text(_generate_srt(segments, start_offset), encoding="utf-8")
        cmd2 = [
            "ffmpeg", "-y",
            "-i", clip_path,
            "-i", str(fallback_srt),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "copy",
            "-c:s", "mov_text",
            "-metadata:s:s:0", "language=eng",
            "-movflags", "+faststart",
            output_path,
        ]
        r2 = subprocess.run(cmd2, capture_output=True, text=True)
        fallback_srt.unlink(missing_ok=True)
        if r2.returncode != 0:
            import shutil
            shutil.copy2(clip_path, output_path)
    return True


def main():
    parser = argparse.ArgumentParser(description="Repurpose videos for TikTok/Reels/Shorts")
    parser.add_argument("url", help="Video URL to download and repurpose")
    parser.add_argument("--hashtags", default="fyp viral video", help="Space-separated hashtags (default: 'fyp viral video')")
    parser.add_argument("--clip-duration", type=int, default=45, help="Target clip duration in seconds (default: 45)")
    parser.add_argument("--output", default="output", help="Output directory (default: ./output)")
    parser.add_argument("--no-download", action="store_true", help="Skip download (use local file path instead)")
    parser.add_argument("--fast", action="store_true", help="Skip AI transcription (uses ffmpeg only — near-zero CPU)")
    parser.add_argument("--no-captions", action="store_true", help="Skip burning captions into clips")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output).resolve() / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)
    tmp_dir = Path(tempfile.mkdtemp())

    try:
        # Step 1: Download
        if args.no_download or os.path.isfile(args.url):
            video_path = args.url
            print(f"[1/5] Using local file: {video_path}")
        else:
            video_path = download_video(args.url, tmp_dir)

        # Step 2: Transcribe (skip if --fast)
        if args.fast:
            print(f"[2/5] Skipping AI transcription (--fast mode)...")
            segments = []
        else:
            segments = transcribe(video_path)

        # Step 3: Split into clips
        clips = split_into_clips(video_path, segments, args.clip_duration)

        # Step 4-5: Process each clip
        print(f"[4/5] Cropping & rendering {len(clips)} clip(s)...")
        output_files = []
        for i, (start, end) in enumerate(clips, 1):
            raw_clip = tmp_dir / f"raw_clip_{i}.mp4"
            captioned_clip = output_dir / f"repurposed_{i:02d}.mp4"

            # Crop to vertical
            crop_to_vertical(video_path, raw_clip, start, end)

            # Add captions (skip if --no-captions or no segments)
            clip_segments = [
                s for s in segments
                if s["start"] >= start and s["end"] <= end
            ] if segments else []

            if clip_segments and not args.no_captions:
                add_subtitles(str(raw_clip), clip_segments, start, str(captioned_clip))
            else:
                import shutil
                shutil.copy2(raw_clip, captioned_clip)

            output_files.append(str(captioned_clip))
            print(f"    -> {captioned_clip}")

        # Step 5: Generate hashtags file
        hashtags_file = output_dir / "hashtags.txt"
        tags = [f"#{t.strip()}" for t in args.hashtags.split()]
        hashtags_file.write_text(" ".join(tags))
        print(f"[5/5] Hashtags saved to: {hashtags_file}")

        print(f"\nDone! {len(output_files)} clip(s) ready in: {output_dir.resolve()}")
        print(f"Hashtags: {hashtags_file.read_text()}")
        for f in output_files:
            size_mb = os.path.getsize(f) / (1024 * 1024)
            print(f"  {f} ({size_mb:.1f} MB)")

    finally:
        # Cleanup temp
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
