from __future__ import annotations


def progress_bar(done: int, total: int, width: int = 16) -> str:
    total = max(1, total)
    ratio = max(0.0, min(1.0, done / total))
    filled = int(width * ratio)
    return "█" * filled + "░" * (width - filled)


def speed_line(bytes_per_sec: float) -> str:
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.0f} B/s"
    if bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec/1024:.1f} KB/s"
    return f"{bytes_per_sec/(1024*1024):.2f} MB/s"
