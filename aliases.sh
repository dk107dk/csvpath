alias pytest='poetry run pytest'
alias flake8='poetry run flake8 --max-complexity=20'
alias run='poetry run python '
alias black='poetry run black .'
alias coverage='poetry run coverage run -m pytest'
alias report='poetry run coverage report -m'
alias html='poetry run coverage html '
alias run-pre-commit='poetry run pre-commit run --all-files'
alias as='source ./aliases.sh'
alias pylint='poetry run pylint csvpath '
echo ''
echo '==========================='
echo '   pytest '
echo '   flake8 '
echo '   pylint '
echo '   run-pre-commit '
echo '   black '
echo '   run '
echo '   coverage '
echo '   report '
echo '   html '
echo '   as '
echo '==========================='
echo ''

