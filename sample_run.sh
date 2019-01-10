config_file=$1
if [ $1 == ""]; then
    config_file="$(pwd)/config/config.py"
fi

export FLASK_APP=app
export FLASK_ENV=development
export SCHEDULR_SETTINGS=$config_file
flask run
