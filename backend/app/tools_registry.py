from dataclasses import dataclass
from typing import Callable, Dict, Type
from pydantic import BaseModel
from .schemas import (
    Target,
    NmapOptions,
    NucleiOptions,
    GobusterDirOptions,
    GobusterDnsOptions,
    FfufOptions,
    DirsearchOptions,
    NiktoOptions,
    WapitiOptions,
    WhatWebOptions,
    Sublist3rOptions,
    AmassOptions,
    ZapOptions,
    SqlmapOptions,
)
from .utils.targets import normalize_for_tool


@dataclass
class ToolSpec:
    id: str
    label: str
    allowed_kinds: set[str]
    options_model: Type[BaseModel]
    build_cmd: Callable[[Target, BaseModel, str], list]
    timeout_default: int = 1200


def build_nmap(target: Target, opts: NmapOptions, job_dir: str) -> list:
    t = normalize_for_tool("nmap", target.value)
    cmd = ["nmap", "-Pn", "--top-ports", str(opts.top_ports)]
    if opts.service_version:
        cmd.append("-sV")
    if opts.os_detection:
        cmd.append("-O")
    if opts.scripts:
        cmd += ["--script", ",".join(opts.scripts)]
    if opts.extra_args:
        cmd += opts.extra_args
    cmd += ["-oN", f"{job_dir}/nmap.txt", t]
    return cmd


def build_nuclei(target: Target, opts: NucleiOptions, job_dir: str) -> list:
    url = normalize_for_tool("nuclei", target.value)
    cmd = [
        "nuclei",
        "-u",
        url,
        "-jsonl",
        "-nmhe",
        "-rate-limit",
        str(opts.rateLimit),
        "-c",
        str(opts.concurrency),
        "-timeout",
        str(opts.timeout),
    ]
    if opts.templates:
        cmd += ["-t", ",".join(opts.templates)]
    if opts.severity:
        cmd += ["-severity", ",".join(opts.severity)]
    if opts.extra_args:
        cmd += opts.extra_args
    cmd += ["-o", f"{job_dir}/nuclei.jsonl"]
    return cmd


def build_gobuster_dir(target: Target, opts: GobusterDirOptions, job_dir: str) -> list:
    base = normalize_for_tool("gobuster-dir", target.value)
    cmd = [
        "gobuster",
        "dir",
        "-u",
        base,
        "-w",
        opts.wordlist,
        "-t",
        str(opts.threads),
        "-s",
        opts.status_codes,
    ]
    if opts.extensions:
        cmd += ["-x", opts.extensions]
    if opts.extra_args:
        cmd += opts.extra_args
    cmd += ["-o", f"{job_dir}/gobuster.txt"]
    return cmd


def build_gobuster_dns(target: Target, opts: GobusterDnsOptions, job_dir: str) -> list:
    domain = normalize_for_tool("gobuster-dns", target.value)
    cmd = [
        "gobuster",
        "dns",
        "-d",
        domain,
        "-w",
        opts.wordlist,
        "-t",
        str(opts.threads),
    ]
    if opts.resolvers:
        cmd += ["-r", opts.resolvers]
    if opts.extra_args:
        cmd += opts.extra_args
    cmd += ["-o", f"{job_dir}/gobuster-dns.txt"]
    return cmd


def build_ffuf(target: Target, opts: FfufOptions, job_dir: str) -> list:
    url = normalize_for_tool("ffuf", target.value)
    cmd = [
        "ffuf",
        "-u",
        f"{url}/FUZZ",
        "-w",
        opts.wordlist,
        "-t",
        str(opts.threads),
    ]
    if opts.recursion:
        cmd.append("-recursion")
    if opts.extensions:
        cmd += ["-e", opts.extensions]
    if opts.extra_args:
        cmd += opts.extra_args
    cmd += ["-o", f"{job_dir}/ffuf.json", "-of", "json"]
    return cmd


def build_dirsearch(target: Target, opts: DirsearchOptions, job_dir: str) -> list:
    url = normalize_for_tool("dirsearch", target.value)
    cmd = ["dirsearch", "-u", url, "-w", opts.wordlist, "-t", str(opts.threads)]
    if opts.extensions:
        cmd += ["-e", opts.extensions]
    if opts.extra_args:
        cmd += opts.extra_args
    cmd += ["-o", f"{job_dir}/dirsearch.txt"]
    return cmd


def build_nikto(target: Target, opts: NiktoOptions, job_dir: str) -> list:
    url = normalize_for_tool("nikto", target.value)
    cmd = ["nikto", "-host", url]
    if opts.useragent:
        cmd += ["-useragent", opts.useragent]
    if opts.ssl:
        cmd.append("-ssl")
    cmd += ["-timeout", str(opts.timeout)]
    if opts.extra_args:
        cmd += opts.extra_args
    cmd += ["-o", f"{job_dir}/nikto.txt"]
    return cmd


def build_wapiti(target: Target, opts: WapitiOptions, job_dir: str) -> list:
    url = normalize_for_tool("wapiti", target.value)
    cmd = ["wapiti", "-u", url, "-f", "json", "-o", f"{job_dir}/wapiti.json"]
    if opts.modules:
        cmd += ["-m", opts.modules]
    cmd += ["-d", str(opts.depth)]
    if opts.extra_args:
        cmd += opts.extra_args
    return cmd


def build_whatweb(target: Target, opts: WhatWebOptions, job_dir: str) -> list:
    url = normalize_for_tool("whatweb", target.value)
    cmd = ["whatweb", url, "--log-json", f"{job_dir}/whatweb.json"]
    if opts.aggressive:
        cmd.append("-a")
        cmd.append("3")
    if opts.plugins:
        cmd += ["-p", opts.plugins]
    if opts.extra_args:
        cmd += opts.extra_args
    return cmd


def build_sublist3r(target: Target, opts: Sublist3rOptions, job_dir: str) -> list:
    domain = normalize_for_tool("sublist3r", target.value)
    cmd = [
        "sublist3r",
        "-d",
        domain,
        "-t",
        str(opts.threads),
        "-o",
        f"{job_dir}/sublist3r.txt",
    ]
    if opts.bruteforce:
        cmd.append("-b")
    if opts.extra_args:
        cmd += opts.extra_args
    return cmd


def build_amass(target: Target, opts: AmassOptions, job_dir: str) -> list:
    domain = normalize_for_tool("amass", target.value)
    cmd = ["amass", "enum", "-d", domain, "-o", f"{job_dir}/amass.txt"]
    if opts.passive:
        cmd.append("-passive")
    cmd += ["-timeout", str(opts.timeout)]
    if opts.extra_args:
        cmd += opts.extra_args
    return cmd


def build_zap(target: Target, opts: ZapOptions, job_dir: str) -> list:
    url = normalize_for_tool("zap", target.value)
    cmd = [
        "zap-baseline.py" if opts.mode == "baseline" else "zap-full-scan.py",
        "-t",
        url,
        "-r",
        f"{job_dir}/zap.html",
    ]
    cmd += ["-m", opts.mode]
    cmd += ["-z", f"timeout={opts.timeout}"]
    if opts.extra_args:
        cmd += opts.extra_args
    return cmd


def build_sqlmap(target: Target, opts: SqlmapOptions, job_dir: str) -> list:
    url = normalize_for_tool("sqlmap", target.value)
    cmd = ["sqlmap", "-u", url, "--batch", "--output-dir", job_dir]
    if opts.dbms:
        cmd += ["--dbms", opts.dbms]
    cmd += [
        "--threads",
        str(opts.threads),
        "--risk",
        str(opts.risk),
        "--level",
        str(opts.level),
    ]
    if opts.extra_args:
        cmd += opts.extra_args
    return cmd


REGISTRY: Dict[str, ToolSpec] = {
    "nmap": ToolSpec("nmap", "Nmap", {"ip", "domain", "url"}, NmapOptions, build_nmap),
    "nuclei": ToolSpec(
        "nuclei", "Nuclei", {"url", "ip", "domain"}, NucleiOptions, build_nuclei
    ),
    "gobuster-dir": ToolSpec(
        "gobuster-dir",
        "Gobuster (dir)",
        {"url", "ip", "domain"},
        GobusterDirOptions,
        build_gobuster_dir,
    ),
    "gobuster-dns": ToolSpec(
        "gobuster-dns",
        "Gobuster (dns)",
        {"domain"},
        GobusterDnsOptions,
        build_gobuster_dns,
    ),
    "ffuf": ToolSpec("ffuf", "FFUF", {"url", "ip", "domain"}, FfufOptions, build_ffuf),
    "dirsearch": ToolSpec(
        "dirsearch",
        "dirsearch",
        {"url", "ip", "domain"},
        DirsearchOptions,
        build_dirsearch,
    ),
    "nikto": ToolSpec(
        "nikto", "Nikto", {"url", "ip", "domain"}, NiktoOptions, build_nikto
    ),
    "wapiti": ToolSpec(
        "wapiti", "Wapiti", {"url", "ip", "domain"}, WapitiOptions, build_wapiti
    ),
    "whatweb": ToolSpec(
        "whatweb", "WhatWeb", {"url", "ip", "domain"}, WhatWebOptions, build_whatweb
    ),
    "sublist3r": ToolSpec(
        "sublist3r", "Sublist3r", {"domain"}, Sublist3rOptions, build_sublist3r
    ),
    "amass": ToolSpec("amass", "Amass", {"domain"}, AmassOptions, build_amass),
    "zap": ToolSpec("zap", "OWASP ZAP", {"url", "ip", "domain"}, ZapOptions, build_zap),
    "sqlmap": ToolSpec(
        "sqlmap", "SQLMap", {"url", "ip", "domain"}, SqlmapOptions, build_sqlmap
    ),
}
