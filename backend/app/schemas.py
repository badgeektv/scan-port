from typing import List, Optional, Literal
from pydantic import BaseModel, Field, model_validator


class Target(BaseModel):
    value: str = Field(..., description="URL http(s), IP ou domaine")
    kind: Optional[Literal["url", "ip", "domain"]] = None

    @model_validator(mode="after")
    def detect_kind(self):
        from .utils.targets import detect_kind

        k = detect_kind(self.value)
        if self.kind and self.kind != k:
            raise ValueError(f"kind={self.kind} ne correspond pas à {k}.")
        self.kind = self.kind or k
        return self


class NmapOptions(BaseModel):
    top_ports: int = Field(
        1000, ge=1, le=65535, description="Nombre de ports les plus courants."
    )
    service_version: bool = Field(
        True, description="Active -sV pour détection de versions."
    )
    os_detection: bool = Field(False, description="Active -O pour détection d'OS.")
    scripts: List[str] = Field(
        default_factory=list, description="Scripts NSE (ex: http-*)"
    )
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class NucleiOptions(BaseModel):
    templates: List[str] = Field(
        default_factory=lambda: ["cves", "vulnerabilities"],
        description="Templates/dirs.",
    )
    severity: List[str] = Field(
        default_factory=lambda: ["low", "medium", "high", "critical"],
        description="Sévérités.",
    )
    rateLimit: int = Field(150, ge=1, description="Requêtes par seconde.")
    concurrency: int = Field(10, ge=1, description="Threads.")
    timeout: int = Field(1200, ge=10, description="Timeout (s).")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class GobusterDirOptions(BaseModel):
    wordlist: str = Field("/wordlists/common.txt", description="Chemin de la wordlist.")
    threads: int = Field(50, ge=1, le=200, description="Nombre de threads.")
    status_codes: str = Field(
        "200,204,301,302,307,401,403", description="Codes HTTP considérés."
    )
    extensions: Optional[str] = Field(
        None, description="Extensions à tester (php,asp,js)."
    )
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class GobusterDnsOptions(BaseModel):
    wordlist: str = Field(
        "/wordlists/subdomains.txt", description="Chemin de la wordlist."
    )
    threads: int = Field(50, ge=1, le=200, description="Nombre de threads.")
    resolvers: Optional[str] = Field(None, description="Serveurs DNS custom.")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class FfufOptions(BaseModel):
    wordlist: str = Field("/wordlists/common.txt", description="Chemin de la wordlist.")
    threads: int = Field(40, ge=1, le=200, description="Threads de scan.")
    recursion: bool = Field(False, description="Active la récursion.")
    extensions: Optional[str] = Field(None, description="Extensions à tester.")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class DirsearchOptions(BaseModel):
    wordlist: str = Field("/wordlists/common.txt", description="Chemin de la wordlist.")
    extensions: Optional[str] = Field("php,asp,js", description="Extensions à tester.")
    threads: int = Field(50, ge=1, le=200, description="Nombre de threads.")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class NiktoOptions(BaseModel):
    useragent: Optional[str] = Field(None, description="User-Agent custom.")
    ssl: bool = Field(True, description="Force SSL.")
    timeout: int = Field(500, ge=1, description="Timeout (s).")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class WapitiOptions(BaseModel):
    modules: Optional[str] = Field(None, description="Modules à utiliser.")
    depth: int = Field(2, ge=1, description="Profondeur de parcours.")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class WhatWebOptions(BaseModel):
    aggressive: bool = Field(False, description="Mode agressif.")
    plugins: Optional[str] = Field(None, description="Plugins à activer.")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class Sublist3rOptions(BaseModel):
    bruteforce: bool = Field(False, description="Bruteforce des sous-domaines.")
    threads: int = Field(10, ge=1, le=200, description="Nombre de threads.")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class AmassOptions(BaseModel):
    passive: bool = Field(True, description="Mode passif uniquement.")
    timeout: int = Field(60, ge=1, description="Timeout (s).")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class ZapOptions(BaseModel):
    mode: str = Field("baseline", description="Mode baseline ou full scan.")
    timeout: int = Field(600, ge=1, description="Timeout (s).")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )


class SqlmapOptions(BaseModel):
    dbms: Optional[str] = Field(None, description="Forcer le SGBD.")
    threads: int = Field(1, ge=1, le=10, description="Nombre de threads.")
    risk: int = Field(1, ge=1, le=3, description="Niveau de risque.")
    level: int = Field(1, ge=1, le=5, description="Niveau de tests.")
    extra_args: List[str] = Field(
        default_factory=list, description="Paramètres bruts additionnels."
    )
