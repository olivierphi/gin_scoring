#!/bin/zsh

# A quick script, so that I can just run `source ~/_WORK/me/gin-scoring/dev-start.zsh` to get started :-) 

# @link https://stackoverflow.com/questions/2683279/how-to-detect-if-a-script-is-being-sourced
[[ ! $ZSH_EVAL_CONTEXT =~ :file$ ]] && echo "Script must be sourced" && exit 1

cd ${0:A:h}/ # Change to the directory of the current file

source .venv/bin/activate

export DJANGO_SETTINGS_MODULE=gin_scoring.project.settings.development
alias run_in_dotenv='dotenv -f .env.local run -- '

alias poetry='pipx run poetry==1.8.3'
alias djm='run_in_dotenv python manage.py'
alias test='DJANGO_SETTINGS_MODULE=gin_scoring.project.settings.test run_in_dotenv pytest -x --reuse-db'
alias test-no-reuse='DJANGO_SETTINGS_MODULE=gin_scoring.project.settings.test run_in_dotenv pytest -x'

# Show the aliases we just defined:
alias poetry && alias djm && alias test && alias test-no-reuse
