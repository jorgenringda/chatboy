#!/bin/bash

cd chatboy

# Start tmux session
tmux new-session -d -s chatboy

# Split window horizontally
tmux split-window -h -t chatboy

# Run command in upper window
tmux send-keys -t chatboy:0.0 'cd api && source venv/bin/activate && printf "\033c" && uvicorn main:app --reload' C-m

# Run command in lower window
tmux send-keys -t chatboy:0.1 'cd gui && npm run dev' C-m

# Attach to the tmux session to see the windows
tmux attach-session -t chatboy