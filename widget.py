#!/usr/bin/env python3
"""Claude Code Max plan usage widget. Always-on-top, draggable.

Shows current utilization % for the rolling 5-hour and 7-day windows,
pulled from the same internal endpoint Claude Code's /usage uses.

Controls:
  - Left-click + drag: move
  - Double-click / right-click: close
"""
import json
import tkinter as tk
import urllib.request
import urllib.error
from pathlib import Path

CREDS_PATH = Path.home() / ".claude" / ".credentials.json"
USAGE_URL = "https://api.anthropic.com/api/oauth/usage"
POLL_MS = 120_000  # 2 min


def get_token():
    with open(CREDS_PATH) as f:
        data = json.load(f)
    return data["claudeAiOauth"]["accessToken"]


def fetch_usage():
    token = get_token()
    req = urllib.request.Request(
        USAGE_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "anthropic-beta": "oauth-2025-04-20",
            "User-Agent": "claude-usage-widget/1.0",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def color_for(pct):
    if pct < 60:
        return "#4ade80"  # green
    if pct < 85:
        return "#facc15"  # yellow
    return "#ef4444"  # red


class Widget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("claude-usage")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.88)
        self.root.configure(bg="#111827")

        screen_w = self.root.winfo_screenwidth()
        self.root.geometry(f"150x58+{screen_w - 170}+20")

        frame = tk.Frame(self.root, bg="#111827", padx=10, pady=6,
                         highlightbackground="#374151", highlightthickness=1)
        frame.pack(fill="both", expand=True)

        self.label_5h = tk.Label(
            frame, text="5h:  --", fg="#e5e7eb", bg="#111827",
            font=("DejaVu Sans Mono", 11, "bold"), anchor="w",
        )
        self.label_5h.pack(fill="x")

        self.label_week = tk.Label(
            frame, text="Wk:  --", fg="#e5e7eb", bg="#111827",
            font=("DejaVu Sans Mono", 11, "bold"), anchor="w",
        )
        self.label_week.pack(fill="x")

        for w in (self.root, frame, self.label_5h, self.label_week):
            w.bind("<Button-1>", self._start_drag)
            w.bind("<B1-Motion>", self._do_drag)
            w.bind("<Button-3>", lambda e: self.root.destroy())
            w.bind("<Double-Button-1>", lambda e: self.root.destroy())

        self._offset = (0, 0)
        self.update_usage()
        self.root.mainloop()

    def _start_drag(self, event):
        self._offset = (event.x_root - self.root.winfo_x(),
                        event.y_root - self.root.winfo_y())

    def _do_drag(self, event):
        x = event.x_root - self._offset[0]
        y = event.y_root - self._offset[1]
        self.root.geometry(f"+{x}+{y}")

    def update_usage(self):
        try:
            data = fetch_usage()
            h5 = float(data.get("five_hour", {}).get("utilization", 0) or 0)
            wk = float(data.get("seven_day", {}).get("utilization", 0) or 0)
            self.label_5h.config(text=f"5h:  {h5:5.1f}%", fg=color_for(h5))
            self.label_week.config(text=f"Wk:  {wk:5.1f}%", fg=color_for(wk))
        except urllib.error.HTTPError as e:
            self.label_5h.config(text=f"5h:  err{e.code}", fg="#ef4444")
            self.label_week.config(text="Wk:  --", fg="#ef4444")
        except Exception:
            self.label_5h.config(text="5h:  offline", fg="#9ca3af")
            self.label_week.config(text="Wk:  --", fg="#9ca3af")
        self.root.after(POLL_MS, self.update_usage)


if __name__ == "__main__":
    Widget()
