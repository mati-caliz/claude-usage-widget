# claude-usage-widget

Tiny always-on-top Tkinter widget that shows your Claude Code Max plan
utilization for the rolling **5-hour** and **7-day** windows.

It reads the OAuth token from `~/.claude/.credentials.json` (the same file
Claude Code writes) and polls the internal usage endpoint used by
`/usage`, refreshing every 2 minutes.

## Screenshot

```
┌──────────────┐
│ 5h:   42.3%  │
│ Wk:   18.7%  │
└──────────────┘
```

Colors: green `< 60%`, yellow `< 85%`, red otherwise.

## Requirements

- Python 3 with Tkinter (`sudo apt install python3-tk` on Debian/Ubuntu)
- An active Claude Code session (so `~/.claude/.credentials.json` exists)

## Usage

```bash
# run in the foreground
python3 widget.py

# or run detached, logs to /tmp/claude-usage-widget.log
./run.sh
```

### Controls

- **Left-click + drag** — move the widget
- **Double-click** or **right-click** — close it
- **Stop background instance** — `pkill -f 'python3 widget.py'`

## Notes

The widget calls `https://api.anthropic.com/api/oauth/usage` with the
`oauth-2025-04-20` beta header — the same request Claude Code makes for
`/usage`. If the endpoint changes upstream, the widget will show `err<code>`
or `offline` until updated.
