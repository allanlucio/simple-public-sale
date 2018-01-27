sudo apt install git-core
sudo apt install python3-pip
sudo apt install python3-dev
sudo apt install redis-server
sudo pip3 install -r requirements.txt
python3 manage.py migrate
echo 'Crie um usuario para acessar o sistema'
python3 manage.py createsuperuser
python3 manage.py runserver
