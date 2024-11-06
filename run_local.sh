if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo -e "This script must be sourced, run it with \033[1msource run_local.sh\033[0m"
    exit
fi

./alembic.sh

source .venv/bin/activate

tmux new "source tmux-run_local.sh"
