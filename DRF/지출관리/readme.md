## API 명세서 [https://documenter.getpostman.com/view/20867321/VUxNT8tp](https://documenter.getpostman.com/view/20867321/VUxNT8tp)

![API.png](/screenshot/지출관리API.png)

## ERD
![ERD.png](/screenshot/지출관리ERD.png)
```
Table "user_user" {
  "id" bigint(20) [pk, not null, increment]
  "last_login" datetime(6) [default: NULL]
  "email" varchar(100) [not null]
  "username" varchar(20) [not null]
  "password" varchar(128) [not null]
  "is_active" tinyint(1) [not null]
  "is_admin" tinyint(1) [not null]
  "is_superuser" tinyint(1) [not null]
}

Table "expenditure" {
  "id" bigint(20) [pk, not null, increment]
  "dec" longtext [not null]
  "amount" int(11) [not null]
  "date" date [not null]
  "is_active" tinyint(1) [not null]
  "category_id" bigint(20) [ref: > category.id, not null]
  "user_id" bigint(20) [ref: > user_user.id, not null]
}

Table "category" {
  "id" bigint(20) [pk, not null, increment]
  "name" varchar(50) [not null]
}

Table "comment" {
  "id" bigint(20) [pk, not null, increment]
  "comment" longtext [not null]
  "expenditure_id" bigint(20) [ref: > expenditure.id, default: NULL]
  "user_id" bigint(20) [ref: > user_user.id, default: NULL] 
}
```
## .env 파일 manage.py와 동일 위치
- 실행시 필요한 환경 변수 설정 파일
```
SECRET_KEY='payhere_secret_key'

DB_ROOT_PASSWORD=payhere
DB_DATABASE=payhere
DB_USER=payhere
DB_PASSWORD=payhere
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

## 요구사항 3-d. 삭제한 내역은 언제든지 다시 복구 할 수 있어야 한다.
> - 지출기록은 사용자의 소비 습관을 파악 할 수 있는 데이터로 삭제하지 않고 수집한다.  

> - 사용자는 실제 데이터를 삭제 할 수 없고 Put 메소드를 사용하여 비활성화 처리하고 사용자가 조회 할 수 없도록 숨검처리 하도록 작성 [코드참조](https://github.com/joohuun/payhere/blob/b4ac24e86fe7623b2bca9b8212fd9a38554789b2/accountbook/views.py#L51)
> - 개발자가 DB를 삭제해야할 경우 백업하여 관리 [블로그참조](https://1q2w3ee.tistory.com/54)

## 구현
> - 언어에 상관없이 Docker를 기반으로 서버를 실행 할 수 있도록 작성해주세요. [코드참조](https://github.com/joohuun/payhere/blob/main/docker-compose.yml)   
> - DB 관련 테이블에 대한 DDL 파일을 소스 디렉토리 안에 넣어주세요. [코드참조](https://github.com/joohuun/payhere/blob/main/payhere_ddl.sql)   
> - 가능하다면 테스트 케이스를 작성해주세요. [test_user](https://github.com/joohuun/payhere/tree/main/user/tests), [test_accountbook](https://github.com/joohuun/payhere/tree/main/accountbook/tests)
> - 토큰을 발행해서 인증을 제어하는 방식으로 구현해주세요 [코드참조](https://github.com/joohuun/payhere/blob/8a610acb1f8003b84e0a23eac96201cc7b417ab7/user/serializers.py#L28)
