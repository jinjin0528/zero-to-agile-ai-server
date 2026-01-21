# AgileBang

> **대학생의 첫 자취 의사결정을 돕는 기술 중심 AI 기반 주거 매물 추천 서비스**

**Team**: Zero-to-Agile

---

## 1. 프로젝트 개요

AgileBang은 정보 비대칭이 심한 부동산 시장에서 **대학생·대학원생(사회 초년생)** 이 합리적인 주거 의사결정을 할 수 있도록 지원하는 **설명 가능한(Explainable) 매물 추천 서비스**입니다.

기존 부동산 플랫폼의 *탐색 중심 구조*에서 벗어나,

* 데이터 기반 **객관적 관측(Observation)**
* 정책적 **판단(Decision) 로직**
* 추천 매물 + 탈락 매물의 **동시 노출 및 사유 제공**

을 통해 **“왜 이 매물이 나에게 맞는지”를 이해할 수 있는 사용자 경험**을 제공합니다.

---

## 2. 문제 정의 (Problem Statement)

### 2.1 시장 문제

* 부동산 데이터는 구조적으로 **비대칭적**
* 대학생은 대표적인 **부동산 정보 취약 계층**

  * 시세, 통학 거리, 생활 인프라, 거래 리스크 등
  * 고려 요소는 많으나 이를 종합적으로 판단하기 어려움

### 2.2 사용자 문제

* 정보 부족 + 불안 + 시간 압박이 동시에 존재
* 추천 결과보다 **설명과 근거**가 필요한 사용자군

---

## 3. 서비스 목표 (Goal)

* 대학생의 실제 니즈를 반영한 **의사결정 보조 시스템 구축**
* 가격 / 통학 거리 / 리스크 / 편의성에 대한 **객관적 정보 제공**
* 최종 판단은 사용자에게 남기되, 판단에 필요한 맥락을 제공

---

## 4. 타겟 시장 정의 (TAM · SAM · SOM)

### TAM

* 인터넷 부동산 중개 시장

### SAM

* **20~30대 자취를 희망하는 대학(원)생**

  * AI 기반 서비스에 대한 거부감이 낮음
  * 설명과 이해를 필요로 하는 사용자

* 주요 타겟 지역

  * 대학 밀집 지역 (마포구, 서대문구, 은평구 등)

### SOM

* 매칭 성공 수수료
* 광고 수익 모델
* 향후 프리미엄 분석/추천 기능 확장 가능


---

## 📁 Project Structure

```text
├── README.md                     # 프로젝트 개요, 아키텍처 규칙, 실행 방법
│
├── app                           # FastAPI 애플리케이션 엔트리 포인트
│   ├── __init__.py               # app 패키지 선언
│   └── main.py                   # 서버 실행, router 등록, middleware 설정
│
├── infrastructure                # ⭐ 공통 기술 인프라 (DB, ORM, 설정 등)
│   ├── __init__.py               # infrastructure 패키지 선언
│   │
│   ├── config                    # 인프라 관련 설정 모음
│   │   └── __init__.py           # DB / MQ / LLM 등 설정 관리
│   │
│   ├── db                        # DB 연결 및 세션 관리
│   │   └── __init__.py           # DB engine, session factory
│   │
│   └── orm                       # ORM 모델 정의
│       └── __init__.py           # SQLAlchemy Base, 테이블 매핑 클래스
│
├── shared                        # ⭐ 공통 유틸/설정 모음
│   ├── __init__.py               # shared 패키지 선언
│   │
│   ├── infrastructure            # 공통 인프라 설정
│   │   ├── __init__.py
│   │   └── config                # 공통 설정 (예: LLM, 환경변수)
│   │       └── __init__.py
│   │
│   └── common                    # 공통 유틸리티/헬퍼
│       ├── __init__.py
│       └── utils                 # 토큰 카운터 등
│           └── __init__.py
│
├── modules                       # ⭐ 도메인별 모듈 (팀원 단위 협업의 핵심)
│   ├── __init__.py               # modules 패키지 선언
│   │
│   └── mq                        # MQ 도메인 (예: 메시지 큐 처리)
│       ├── __init__.py           # mq 모듈 선언
│       │
│       ├── adapter               # Hexagonal Adapter 계층
│       │   ├── __init__.py
│       │   │
│       │   ├── input             # Inbound Adapter (외부 → 내부)
│       │   │   ├── __init__.py
│       │   │   │
│       │   │   └── web            # Web API 진입점 (FastAPI)
│       │   │       ├── __init__.py
│       │   │       │
│       │   │       ├── request    # API 요청 DTO (Pydantic Model)
│       │   │       │   └── __init__.py
│       │   │       │
│       │   │       ├── response   # API 응답 DTO
│       │   │       │   └── __init__.py
│       │   │       │
│       │   │       └── router     # FastAPI router 정의
│       │   │           └── __init__.py
│       │   │
│       │   └── output            # Outbound Adapter (내부 → 외부)
│       │       ├── __init__.py
│       │       │
│       │       └── repository     # DB / MQ / 외부 시스템 접근 구현체
│       │           └── __init__.py
│       │
│       ├── application           # Application Layer (유스케이스 계층)
│       │   ├── __init__.py
│       │   │
│       │   ├── dto                # 유스케이스용 DTO
│       │   │   └── __init__.py
│       │   │
│       │   ├── port_in            # Inbound Port (입력 인터페이스)
│       │   │   └── __init__.py
│       │   │
│       │   ├── port_out           # Outbound Port (출력 인터페이스)
│       │   │   └── __init__.py
│       │   │
│       │   └── usecase            # 실제 비즈니스 흐름 구현
│       │       └── __init__.py
│       │
│       └── domain                # ⭐ 순수 도메인 계층
│           ├── __init__.py        # 도메인 패키지
│           └── model.py           # 도메인 모델 / 엔티티 / 규칙
│
└── test                          # 테스트 코드
    ├── __init__.py               # test 패키지 선언
    └── dev_lsy                   # 개인 / 실험용 테스트 영역
        └── __init__.py
```

---

## 📁 DB
<img width="1228" height="408" alt="db 1" src="https://github.com/user-attachments/assets/a442797a-8cb2-4459-b1a7-e5252b2fd5b8" />
<img width="1192" height="668" alt="db 2" src="https://github.com/user-attachments/assets/276d6de5-c1d0-456d-9b4a-0e0d1714ec3a" />

---

## 5. 기술적 실현 가능성 및 접근 전략

### 5.1 데이터 수집 및 제약 사항

* 부동산 원본 데이터 크롤링 시 제재 리스크 존재
* 건축물대장 등 공공 데이터 API 일일 조회 제한
* 원본 데이터에 대한 임의 해석 시 법적 리스크 발생 가능

➡️ **해결 전략**
원본 데이터를 직접 해석·가공하지 않고,

* 관측(Observation)
* 판단(Decision)

을 명확히 분리한 구조로 설계

---

## 6. 추천 시스템 아키텍처

### 6.1 Layered Decision Architecture

```
Raw Data Layer
   ↓
Observation Layer (객관적 관측 정보)
   ↓
Policy / Decision Layer (정책·비즈니스 판단)
   ↓
추천 결과 + 탈락 사유
```

### 6.2 설계 철학

* **관측 vs 판단 분리**

  * Observation Layer: 판단 없는 재현 가능한 관측값
  * Decision Layer: 정책·컷·추천 로직 적용

* **설명 가능한 추천(Explainable Recommendation)**

  * 추천 매물과 함께 탈락 매물 및 탈락 근거 제공

* **비선형성 반영**

  * 체감 거리, 효용 중심 Feature 기록

* **확장성 확보**

  * 정책 변경, 통계 기반 개선, ML 모델 적용 가능

---

## 7. 경쟁 서비스 분석 및 차별화

### 기존 서비스 한계

* 직방 / 다방

  * 탐색 중심 UI
  * 비교·판단 책임이 사용자에게 집중

### AgileBang 차별점

* 추천 결과 + 판단 근거 동시 제공
* 임차인 ↔ 임대인 **Direct 매칭 구조**
* 단순 매물 플랫폼이 아닌 **의사결정 지원 시스템**

---

## 8. 주요 기능

* 소셜 로그인
* 사용자 개인정보 CRUD
* 임차인 매물 의뢰서 CRUD
* 임차인 맞춤형 매물 추천
* 임대인 매물 CRUD
* 임대인 맞춤형 임차인 추천
* 임차인 ↔ 임대인 직접 컨텍

---

## 9. 팀 구성 및 역할

| 이름  | 역할                            |
| --- | ----------------------------- |
| 이상훈 | PM, 매물 원본 데이터 관측 및 결정 구조 설계   |
| 박장훈 | 매물 데이터 크롤링, 정책적 판단 설계, 임차인 추천 |
| 성해인 | 임차인 매물 의뢰서 / 임대인 매물 CRUD      |
| 이다영 | 프론트엔드 리드 (UI/UX, API 연계)      |
| 이승연 | 큐 구조 설계, 데이터 관측 보조            |
| 이효진 | 관측 정보 기반 AI 응답                |
| 최재현 | 배포, 임대인 추천                    |

---

## 10. 협업 및 개발 방법론

### Git 브랜치 전략

* `main ← dev ← dev_<name>`
* 개인 작업은 `dev_<name>`에서 진행
* 기능 단위 테스트 후 `dev` 병합
* 배포 관리자가 검증 후 `main` 반영

### OKR 기반 개발

**Objective**
대학생의 첫 자취 의사결정을 돕는 주거 매물 추천 서비스

**Key Results**

* 대학생–임대인 매칭 경험 제공
* 검색 기반 응답 속도 5초 이내
* MVP 유료 전환 사용자 확보
* 추천 매물 클릭률 50% 이상

---

> AgileBang은 **데이터 관측과 판단을 분리한 구조적 설계**를 통해, 사용자에게 신뢰 가능한 추천과 설명을 제공하는 것을 목표로 합니다.

