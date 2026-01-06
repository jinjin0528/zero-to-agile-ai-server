"""
Pytest configuration file
"""
import sys
import os

# house_analysis 테스트에서 import 경로 문제를 피하기 위해 프로젝트 루트를 PYTHONPATH에 추가합니다.
# (import 전에 실행되어야 합니다)
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
