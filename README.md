
EN:Install 

1. Create auth and values dirs
1.1 mkdir auth
1.2 mkdir values
2. Run auth.py
2.1 ./auth.py
3. Run readphotos.py to get last photo id 
4. setup mysql params (see src readphoto.py) and sql to create records
5. Add to cron readphotos.py if need

RU: Установка
1. Создать директории auth и values
2. запустите auth.py он скажет какие файлы создать
3. Запустите readphotos.py 
4. Настройте параметры для mysql (см. readphotos.py)
5. добавьте в крон если надо

Зависимости/Dependency
request-oauth
mysqldb
