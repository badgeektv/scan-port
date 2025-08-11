import ipaddress
import re
import urllib.parse

DOMAIN_RE = re.compile(r"(?!-)[A-Za-z0-9-]{1,63}(?:\.(?!-)[A-Za-z0-9-]{1,63})+")


def is_url(v: str) -> bool:
    try:
        p = urllib.parse.urlparse(v)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def is_ip(v: str) -> bool:
    try:
        ipaddress.ip_address(v)
        return True
    except Exception:
        return False


def is_domain(v: str) -> bool:
    return bool(DOMAIN_RE.fullmatch(v))


def detect_kind(v: str) -> str:
    if is_url(v):
        return "url"
    if is_ip(v):
        return "ip"
    if is_domain(v):
        return "domain"
    raise ValueError("Cible invalide : URL http(s), IP ou domaine attendu.")


def normalize_for_tool(tool_id: str, target_value: str) -> str:
    """Uniformise la cible selon l’outil : certains exigent une URL, d'autres un domaine."""
    kind = detect_kind(target_value)
    needs_url = tool_id in {
        "nuclei",
        "nikto",
        "ffuf",
        "dirsearch",
        "zap",
        "whatweb",
        "wapiti",
        "gobuster-dir",
        "sqlmap",
    }
    domain_only = tool_id in {"amass", "sublist3r", "gobuster-dns"}
    if needs_url:
        return target_value if kind == "url" else f"http://{target_value}"
    if domain_only and kind == "url":
        return urllib.parse.urlparse(target_value).netloc
    return target_value
