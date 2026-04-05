#!/bin/bash
# Launch the widget in the background. Logs go to /tmp/claude-usage-widget.log
cd "$(dirname "$0")"
nohup python3 widget.py > /tmp/claude-usage-widget.log 2>&1 &
echo "Widget started (PID $!)"
echo "Logs:  /tmp/claude-usage-widget.log"
echo "Stop:  pkill -f 'python3 widget.py'"
