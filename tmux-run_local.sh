unset PROMPT_COMMAND

sync=false

for arg in "$@"; do
  if [[ $arg == "--sync" || $arg == "-s" ]]; then
    sync=true
  fi
done

echo $sync >> sync.txt

tmux set -g pane-border-status top
tmux set -g mouse on
tmux set -g pane-border-format "#{pane_title}"

tmux split-window -fh "tmux select-pane -T \"Web Backend\"; ./start_web-run_local.sh || read"

if $sync; then
    tmux split-window -fh "tmux select-pane -T \"Discord Bot\"; ./bot.sh --sync || read"
else
    tmux split-window -fh "tmux select-pane -T \"Discord Bot\"; ./bot.sh || read"
fi

tmux split-window -fv -l "2"\
    "tmux select-pane -T \"Web URL\";\
    source .env;\
    echo \"http://\${HTTP_HOST}:\${HTTP_PORT}\" | less"
