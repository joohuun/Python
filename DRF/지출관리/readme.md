## API 명세서 [https://documenter.getpostman.com/view/20867321/VUxNT8tp](https://documenter.getpostman.com/view/20867321/VUxNT8tp)

![API.png](/screenshot/지출관리API.png)

## ERD
![ERD.png](/screenshot/지출관리ERD.png)

## .env 파일 manage.py와 동일 위치
- 실행시 필요한 환경 변수 설정 파일
```
SECRET_KEY='payhere_secret_key'

MYSQL_ROOT_PASSWORD='root_password'
MYSQL_DATABASE='dbname'
MYSQL_USER='unsername'
MYSQL_PASSWORD='password'
```

## local, python==3.10
 ```
 git clone https://github.com/joohuun/payhere.git
 cd payhere
 ```
 ```
 pip install -r requirements.txt
  ```
  ```
 python manage.py makemigrations
 ```
  ```
 python manage.py migrate
 ```
 ```
 python manage.py runserver
 ```
 
 ## ubuntu 20.04 
 docker-compose 다운로드
 ```
 sudo apt install curl
 ```
 ```
 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
 ```
 ```
 sudo docker-compose up
 ```
