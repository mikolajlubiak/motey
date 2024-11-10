if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo -e "This script must be sourced, run it with \033[1msource run_local.sh\033[0m"
    exit
fi

sync=false

for arg in "$@"; do
  if [[ $arg == "--sync" || $arg == "-s" ]]; then
    sync=true
  fi
done

./alembic.sh >> logs/alembic.out 2>> logs/alembic.err

source .venv/bin/activate

if $sync; then
    tmux new "source tmux-run_local.sh --sync"
else
    tmux new "source tmux-run_local.sh"
fi
