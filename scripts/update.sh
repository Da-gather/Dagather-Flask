pkill -9 python3
cd flask-app
git pull origin main
nohup python3 main.py  > log.log 2>&1  &
