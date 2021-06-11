# 🍦Team CREAM

## ✅ 프로젝트 소개

- 프로젝트 개요: CREAM(Code Rules Everything Around me) 팀의 KREAM 클론 코딩

- 프로젝트 기간: 2021.05.24 ~ 2021.06.04

<br>

## 🎯 기획 목표

- 한정판 중고 **의류품 거래**를 위한 **중개 플랫폼**

- 가격별 제품 **오름**차순, **내림**차순

- 브랜드, 사이즈, 색상 및 컬렉션별 제품 **필터링**

- 단순 구매 및 판매 + **입찰 시스템** 구현

- 입찰 및 체결 거래 **데이터 실시간 그래프화**

<br>

## 🎯 프로젝트 목표

### Frontend

- **React function component, React Hooks** 사용을 통한 컴포넌트 관리

- **styled-component** 사용을 통한 스타일링

- **관련 라이브러리 사용 경험** 쌓기

- **AWS** 사용을 통한 사이트 배포

<br>

### Backend

- django 사용을 통한 DB 관리

- AWS 사용을 통한 사이트 배포

<br>

### 공통

- 백엔드-프론트엔드 커뮤니케이션 및 통신으로 **협업 경험 쌓기**

<br>

## 👥 팀원 구성

- **Frontend**

  - 김수연 [Github](https://github.com/ksy4568) / [블로그](https://velog.io/@syeon02)
  - 권오재 [Github](https://github.com/geborenik) / [블로그](https://velog.io/@geborenik)

  - 전용민 [Github](https://github.com/J-Ymini) / [블로그](https://velog.io/@dydalsdl1414)

  **Backend**

  - 양미화 [Github](https://github.com/hwaya2828) / [블로그](https://velog.io/@hwaya2828)
  - 김하민(PM) [Github](https://github.com/HaMin-Kim) / [블로그](https://velog.io/@khmin1017)

    <br>

## 🎥 시연 영상

업로드 예정입니다.

<br>

## 👨‍💻 적용 기술

- Frontend: JavaScript, React, React-Router, React-hooks, styled-component, CRA

- Backend: Python, Django

- 협업 tool: Trello, Git & Github, Slack, AWS

<br>

## 🖊 주 구현 기능

- 소셜 로그인 기능

- 메인 페이지

- 제품 상세 페이지

- 구매 및 판매 결제 진행 페이지

- 마이페이지

<br>

## 💻 팀원별 상세 구현 기능

## Frontend

- 공통: styled-component 사용하여 페이지, 컴포넌트 및 담당 페이지별 레이아웃 구현

**김수연**

- 상세 페이지

  - chart.js 라이브러리를 통한 체결 및 입찰 거래 내역 데이터 Line chart 로 그래프화 구현

  - 모달 창 안 무한 스크롤 구현

  - URLSearchParams를 사용하여 거래내역 모달창 안, 제품 사이즈별 필터링 기능 구현

  - path parameter를 사용하여 상품 리스트 페이지 및 결제 진행 페이지와의 동적 라우팅 기능 구현

  - Query parameter를 사용하여 결제 진행 페이지와의 사이즈별 제품 라우팅 기능 구현

- 공용 컴포넌트
  - 공용으로 사용할 modal component 구현

<br>
  
**권오재**

- 프로젝트 CRA 초기세팅

- Nav

  - QueryString을 사용한 상품 리스트 검색 기능 구현

- 메인 페이지 상단 배너

  - 배너 부분 Carousel 무한 슬라이더 구현 (라이브러리 사용 X)

- 메인 페이지 제품 리스트

  - checkBox + QueryString을 사용한 상품 다중 필터링 기능 구현

  - QueryString을 사용한 상품 리스트 정렬 기능 구현 (가겨별 오름차순)

  - path parameter를 사용하여 제품 상세 페이지와의 동적 라우팅 기능 구현

<br>

**전용민**

- 로그인 페이지

  - 카카오 소셜 로그인 API (JavaScript SDK) 사용을 통한 소셜 로그인 기능 및 CREAM 사이트 전용 JWT 발행 기능 구현

- 마이 페이지

  - fetch(GET)함수를 통해, 카카오 소셜 로그인 api 사용으로부터 받은 회원 정보 및 포인트 확인 기능 구현

- 구매 및 판매 결제 진행 페이지

  - path parameter를 사용하여 제품 상세 페이지와의 동적 라우팅 기능 구현

  - Query parameter, fetch(GET) 를 사용하여 해당 제품의 사이즈별 가격 (즉시 거래, 입찰 데이터) 확인 기능 구현

  - fetch(POST)를 사용하여 거래 (즉시 거래, 입찰) 가격 지정 기능 구현

<br>

## Backend

**김하민**

- 상세 페이지

  - 사이즈 별 즉시 구매가, 즉시 판매가 데이터 전달,
  - 상품 기본정보 전달(상품 이름, 이미지 등)

  - 판매 입찰 & 구매 입찰 내역
    - 구매 및 판매에 대한 입찰내역 정보 전달,
    - 사용하여 입찰 내역 정보 filter 기능 구현 (size별 필터, 가격 및 사이즈 sort)
  - 거래 내역

    - 거래 내역 정보 전달,
    - 거래 내역 정보 filter 기능(최근 1주일, 1개월 등 날짜별 filter)

  - 추천 상품
    - 동일 컬렉션 내 다른 상품 추천(해당 상품과 동일 컬렉션 내에서 랜덤으로 추천)

- 구매 및 판매 결제 진행 페이지
  - 즉시 거래 및 입찰 기능 구현
    - 해당 사이즈에 대해 판매 입찰 건이 있을 경우 즉시 구매 가능(판매 입찰 건이 없다면 구매할 수 있는 수량이 없으므로 즉시 구매 불가하고 구매 입찰만 가능하도록 구현),
    - 해당 사이즈에 대해 구매 입찰 건이 있을 경우 즉시 판매 가능(구매 입찰 건이 없다면 판매할 수 있는 - 수량이 없으므로 즉시 판매 불가하고 판매 입찰만 가능하도록 구현)
- 유저의 보유 포인트를 확인하여 모자른 경우 적절한 에러 반환

<br/>
  
**양미화**

- 카카오톡 소셜 로그인

  - 카카오톡에서 제공해주는 엑세스 토큰을 이용해 사용자 정보를 취득

  - 토큰에 담긴 사용자 정보를 이용하여 회원 데이터를 만들고 회원 번호 부여
  - 만들어진 회원 번호를 이용한 새로운 엑세스 토큰을 전달

- 마이 페이지

  - 이메일 닉네임 포인트 등의 회원 정보를 전송

  - 회원별 판매 & 구매 거래 내역 전송

- 상품 리스트 페이지

  - Query parameter를 사용하여 브랜드별 상품 데이터 전송

- 필터링 : 콜렉션별, 사이즈별, 색상별, 한정판별 상품 필터링
  - Query parameter & Q 객체를 사용하여 필터 조건에 따라 상품을 거르고 해당 상품들의 데이터 전송
- 검색 : 상품 검색
  - 상품명에 검색어가 포함된 상품들의 데이터 전송

<br>
