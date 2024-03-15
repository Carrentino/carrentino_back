if [ -f .env ]; then
    echo "Загрузка переменных из файла .env..."
    source .env
fi

echo "Запуск MinIO..."
MINIO_ROOT_USER=$AWS_ACCESS_KEY_ID MINIO_ROOT_PASSWORD=$AWS_SECRET_ACCESS_KEY minio server ~/mnt/data --console-address ":9001" &

echo "Запуск сервера..."
python car_rent/manage.py runserver
wait
