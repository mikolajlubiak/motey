unset PROMPT_COMMAND

tmux set -g pane-border-status top
tmux set -g mouse on
tmux set -g pane-border-format "#{pane_title}"

br="-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n"

tmux split-window -fh "tmux select-pane -T \"Web Backend\"; ./start_web-run_local.sh"

tmux split-window -fh "tmux select-pane -T \"Discord Bot\"; ./bot.sh"

tmux split-window -fv -l "2"\
    "tmux select-pane -T \"Web URL\";\
    source .env;\
    echo \"http://\${HTTP_HOST}:\${HTTP_PORT}\" | less"
