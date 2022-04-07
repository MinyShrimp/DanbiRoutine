# 단비교육 백엔드 개발 과제

## 기술스택
* Python - Django, DRF
* MySQL
* Docker
* AWS

## 기간
2022-04-07 (목) ~ 2022-04-14 (목) 1주일

## URLs
* [api]()
* [github]()
* [notion]()

## 기능
* 유저 로그인 / 로그아웃 (JWT 사용) + 회원가입
    * 로그인 : email
    * 비밀번호 : 8글자 이상 + 특수문자 + 숫자 포함
* 매 주별 해야할 일의 등록 / 수정 / 삭제 / 조회 기능
* 일정이 지난 후 진행한 할 일들에 대한 해결여부 기록
* routine_day 테이블에서는 복합키 사용
* 테스트 코드 작성

## 평가항목
* 프로젝트의 구성을 적절히 하였는가?
* 프로젝트 소스 코드의 구성이 가독성 있게 구성되어 있는가?
* 테스트 코드는 적절하게 구현되어 있는가?
* 요구사항에 대한 판단이 적절하게 이루어져 있는가?

## 기간별 현황
* 04-07 목요일
    * DB 설계
* 04-08 금요일
* 04-09 토요일
* 04-10 일요일
* 04-11 월요일
* 04-12 화요일
* 04-13 수요일
* 04-14 목요일

## Database
### routine
| Name        | Type                    | 설명          |
| ----------- | ----------------------- | ------------- |
| routine_id  | INTEGER                 | PK            |
| account_id  | INTEGER                 | -             |
| category_id | ENUM(MIRACLE, HOMEWORK) | -             |
| title       | VARCHAR(100)            | -             |
| is_alarm    | TINYINT(1)              | -             |
| is_deleted  | TINYINT(1)              | -             |
| created_at  | TIMESTAMP               | 제작 시간     |
| modified_at | TIMESTAMP               | 업데이트 시간 |

```
CREATE TABLE routine (
    routine_id   INTEGER AUTO_INCREMENT PRIMARY KEY,
    account_id   INTEGER NOT NULL,
    category_id  INTEGER NOT NULL,
    title        VARCHAR(100) NOT NULL,
    is_alarm     TINYINT(1),
    is_deleted   TINYINT(1),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARACTER SET UTF8;
```

### routine_result
| Name              | Type       | 설명          |
| ----------------- | ---------- | ------------- |
| routine_result_id | INTEGER    | PK            |
| routine_id        | INTEGER    | -             |
| result_id         | INTEGER    | -             |
| is_deleted        | TINYINT(1) | -             |
| created_at        | TIMESTAMP  | 제작 시간     |
| modified_at       | TIMESTAMP  | 업데이트 시간 |

```
CREATE TABLE routine_result (
    routine_result_id   INTEGER AUTO_INCREMENT PRIMARY KEY,
    routine_id          INTEGER NOT NULL,
    result_id           INTEGER NOT NULL,
    is_deleted          TINYINT(1),
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARACTER SET UTF8;
```

### routine_day
| Name        | Type         | 설명          |
| ----------- | ------------ | ------------- |
| day         | VARCHAR(100) | -             |
| routine_id  | INTEGER      | -             |
| created_at  | TIMESTAMP    | 제작 시간     |
| modified_at | TIMESTAMP    | 업데이트 시간 |

```
CREATE TABLE routine_day (
    day          VARCHAR(100),
    routine_id   INTEGER NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARACTER SET UTF8;
```

### account
| Name        | Type         | 설명          |
| ----------- | ------------ | ------------- |
| account_id  | INTEGER      | PK            |
| email       | VARCHAR(100) | -             |
| pwd         | VARCHAR(300) | -             |
| salt        | VARCHAR(100) | -             |
| is_deleted  | TINYINT(1)   | -             |
| created_at  | TIMESTAMP    | 제작 시간     |
| modified_at | TIMESTAMP    | 업데이트 시간 |

```
CREATE TABLE account (
    account_id   INTEGER AUTO_INCREMENT PRIMARY KEY,
    email        VARCHAR(100) NOT NULL,
    pwd          VARCHAR(300) NOT NULL,
    salt         VARCHAR(100) NOT NULL,
    is_deleted   TINYINT(1),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARACTER SET UTF8;
```

### category
| Name        | Type         | 설명          |
| ----------- | ------------ | ------------- |
| category_id | INTEGER      | PK            |
| title       | VARCHAR(100) | -             |
| created_at  | TIMESTAMP    | 제작 시간     |
| modified_at | TIMESTAMP    | 업데이트 시간 |

```
CREATE TABLE category (
    category_id  INTEGER AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(100) NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARACTER SET UTF8;

INSERT INTO result(title) 
VALUES ('MIRACLE'), ('HOMEWORK');
```

### result
| Name        | Type         | 설명          |
| ----------- | ------------ | ------------- |
| result_id   | INTEGER      | PK            |
| title       | VARCHAR(100) | -             |
| created_at  | TIMESTAMP    | 제작 시간     |
| modified_at | TIMESTAMP    | 업데이트 시간 |

```
CREATE TABLE result (
    result_id  INTEGER AUTO_INCREMENT PRIMARY KEY,
    title        VARCHAR(100) NOT NULL,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) DEFAULT CHARACTER SET UTF8;

INSERT INTO result(title) 
VALUES ('NOT'), ('TRY'), ('DONE');
```