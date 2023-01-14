echo " BUILD START"
Python3.10.9 -m install -r requirements.txt
Python3.10.9 manage.py collectstatic --noinput --clear
echo " BUILD END"