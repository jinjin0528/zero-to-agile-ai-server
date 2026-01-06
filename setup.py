"""
Setup script for zero-to-agile-ai-server
이 파일은 프로젝트를 Python package로 설치하기 위해 필요합니다.
테스트/로컬 실행 환경에서 import 경로 문제를 줄이기 위한 최소 설정입니다.
개발 모드 설치: pip install -e .
"""
from setuptools import setup, find_packages

setup(
    name="zero-to-agile-ai-server",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.13",
)
