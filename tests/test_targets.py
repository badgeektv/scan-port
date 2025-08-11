import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from backend.app.utils.targets import detect_kind, normalize_for_tool

def test_detect_kind():
    assert detect_kind("https://example.com") == "url"
    assert detect_kind("203.0.113.1") == "ip"
    assert detect_kind("example.com") == "domain"

def test_normalize_for_tool():
    assert normalize_for_tool("nuclei","example.com") == "http://example.com"
    assert normalize_for_tool("amass","https://sub.example.com") == "sub.example.com"
