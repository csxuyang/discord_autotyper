ps -ef|grep auto_typer.py |grep -v grep|cut -c 9-16|`xargs kill -9`
nohup python3 -u auto_typer.py >> typer.log 2>&1 &
