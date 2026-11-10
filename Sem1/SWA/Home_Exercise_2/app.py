"""Streamlit entry point: python -m streamlit run app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from earlybird.dashboard import main

main()
