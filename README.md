# zero-to-agile-ai-server
It's for Zero to Agile AI Server

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
│   │   └── __init__.py           # DB/MQ/LLM 등 설정용 모듈
│   │
│   ├── db                        # DB 연결 및 세션 관리
│   │   └── __init__.py           # DB engine, session factory 위치
│   │
│   └── orm                       # ORM 모델 정의
│       └── __init__.py           # SQLAlchemy Base, 테이블 매핑 클래스
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
│       │       └── repository     # DB/MQ/외부 시스템 접근 구현체
│       │           └── __init__.py
│       │
│       ├── application           # 유스케이스 계층 (Application Layer)
│       │   ├── __init__.py
│       │   │
│       │   ├── dto                # 유스케이스용 DTO
│       │   │   └── __init__.py
│       │   │
│       │   ├── port               # Application Port (외부 의존 인터페이스)
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
    └── dev_lsy                   # 개인/실험용 테스트 영역
        └── __init__.py