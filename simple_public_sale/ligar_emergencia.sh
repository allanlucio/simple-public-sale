gnome-terminal -e "python3 manage.py runserver --noworker 0.0.0.0:8888"
gnome-terminal -e "python3 manage.py runworker"
firefox "0.0.0.0:8888"

echo "Minimize os terminais, caso os encerre pode pausar o sistema"
echo "Abra o link no ip_damaquina:8888"
