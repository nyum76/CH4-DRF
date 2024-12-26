# CH4-DRF
챕터 4 DRF 를 활용한 스파르타 마켓 백엔드 기능 구현

## 초기 설정
- [x] : `.gitignore` 설정
- [X] : 가상환경 설정
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```
- [X] : `spartamarket_DRF` 프로젝트 생성
```bash
django-admin startproject spartamarket_DRF .
```
- [X] : `accounts`, `products` 앱 생성
```bash
python3 manage.py startapp accounts
python3 manage.py startapp products
```