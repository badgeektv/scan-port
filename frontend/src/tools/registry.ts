import { z } from "zod";
export type TargetKind = "url" | "ip" | "domain";
export const targetSchema = z.object({ value: z.string().min(1), kind: z.enum(["url","ip","domain"]).optional() })
  .superRefine((val, ctx) => {
    const v = val.value.trim();
    const urlish = (()=>{ try{ const u=new URL(v); return ["http:","https:"].includes(u.protocol); }catch{return false;}})();
    const ipv4 = /^(25[0-5]|2[0-4]\d|[01]?\d?\d)(\.(25[0-5]|2[0-4]\d|[01]?\d?\d)){3}$/.test(v);
    const ipv6 = /^[0-9a-f:]+$/i.test(v) && v.includes(":");
    const domain = /^(?!-)[A-Za-z0-9-]{1,63}(\.(?!-)[A-Za-z0-9-]{1,63})+$/.test(v);
    const detected: TargetKind | null = urlish ? "url" : (ipv4 || ipv6) ? "ip" : domain ? "domain" : null;
    if (!detected) ctx.addIssue({ code: z.ZodIssueCode.custom, message: "Saisis une URL http(s), une IP, ou un domaine valide." });
    if (!val.kind) (val as any).kind = detected!;
  });

export type FieldDef =
  | { type:"string"; name:string; label:string; help?:string; placeholder?:string }
  | { type:"number"; name:string; label:string; help?:string; min?:number; max?:number; step?:number }
  | { type:"boolean"; name:string; label:string; help?:string }
  | { type:"select"; name:string; label:string; help?:string; options:{label:string; value:string}[] };

export type ToolDef = {
  id: string; label: string; allowedTargetKinds: TargetKind[]; fields: FieldDef[]; preset?: Record<string, any>;
};

export const toolsRegistry: Record<string, ToolDef> = {
  nmap: {
    id: "nmap", label: "Nmap", allowedTargetKinds: ["ip","domain","url"],
    fields: [
      { type:"number", name:"top_ports", label:"Top ports", help:"Nombre de ports les plus courants.", min:1, max:65535 },
      { type:"boolean", name:"service_version", label:"-sV (versions)", help:"Détection de version des services." },
      { type:"boolean", name:"os_detection", label:"-O (OS)", help:"Détection d'OS (privilèges)." },
      { type:"string", name:"scripts", label:"Scripts NSE", help:"Ex: http-*, vuln-* (séparés par des virgules)." }
    ],
    preset: { top_ports: 1000, service_version: true, os_detection: false, scripts: "" }
  },
  nuclei: {
    id: "nuclei", label: "Nuclei", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"string", name:"templates", label:"Templates", help:"Ex: cves,vulnerabilities (liste)." },
      { type:"string", name:"severity", label:"Sévérités", help:"low,medium,high,critical (liste)." },
      { type:"number", name:"rateLimit", label:"Rate limit", help:"Requêtes/seconde.", min:1, max:2000 },
      { type:"number", name:"concurrency", label:"Threads", help:"Concurrence.", min:1, max:200 },
      { type:"number", name:"timeout", label:"Timeout (s)", help:"Temps max.", min:10, max:7200 }
    ],
    preset: { templates:"cves,vulnerabilities", severity:"low,medium,high,critical", rateLimit:150, concurrency:10, timeout:1200 }
  },
  "gobuster-dir": {
    id: "gobuster-dir", label: "Gobuster (dir)", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"string", name:"wordlist", label:"Wordlist", help:"Chemin de la wordlist." },
      { type:"number", name:"threads", label:"Threads", help:"Nombre de threads.", min:1, max:200 },
      { type:"string", name:"status_codes", label:"Codes HTTP", help:"Codes à considérer valides (ex: 200,301,...)." },
      { type:"string", name:"extensions", label:"Extensions", help:"Ex: php,asp,js (facultatif)." }
    ],
    preset: { wordlist:"/wordlists/common.txt", threads:50, status_codes:"200,204,301,302,307,401,403", extensions:"" }
  },
  "gobuster-dns": {
    id: "gobuster-dns", label: "Gobuster (dns)", allowedTargetKinds: ["domain"],
    fields: [
      { type:"string", name:"wordlist", label:"Wordlist", help:"Chemin de la wordlist." },
      { type:"number", name:"threads", label:"Threads", help:"Nombre de threads.", min:1, max:200 },
      { type:"string", name:"resolvers", label:"Resolvers", help:"Serveurs DNS custom (facultatif)." }
    ],
    preset: { wordlist:"/wordlists/subdomains.txt", threads:50, resolvers:"" }
  },
  ffuf: {
    id: "ffuf", label: "FFUF", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"string", name:"wordlist", label:"Wordlist", help:"Chemin de la wordlist." },
      { type:"number", name:"threads", label:"Threads", help:"Nombre de threads.", min:1, max:200 },
      { type:"boolean", name:"recursion", label:"Récursion", help:"Active la récursion." },
      { type:"string", name:"extensions", label:"Extensions", help:"Extensions à tester (facultatif)." }
    ],
    preset: { wordlist:"/wordlists/common.txt", threads:40, recursion:false, extensions:"" }
  },
  dirsearch: {
    id: "dirsearch", label: "dirsearch", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"string", name:"wordlist", label:"Wordlist", help:"Chemin de la wordlist." },
      { type:"string", name:"extensions", label:"Extensions", help:"php,asp,js,..." },
      { type:"number", name:"threads", label:"Threads", help:"Nombre de threads.", min:1, max:200 }
    ],
    preset: { wordlist:"/wordlists/common.txt", extensions:"php,asp,js", threads:50 }
  },
  nikto: {
    id: "nikto", label: "Nikto", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"string", name:"useragent", label:"User-Agent", help:"User-Agent personnalisé." },
      { type:"boolean", name:"ssl", label:"SSL", help:"Force SSL." },
      { type:"number", name:"timeout", label:"Timeout", help:"Timeout (s).", min:1, max:1000 }
    ],
    preset: { useragent:"", ssl:true, timeout:500 }
  },
  wapiti: {
    id: "wapiti", label: "Wapiti", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"string", name:"modules", label:"Modules", help:"Modules à utiliser (facultatif)." },
      { type:"number", name:"depth", label:"Profondeur", help:"Profondeur de crawl.", min:1, max:10 }
    ],
    preset: { modules:"", depth:2 }
  },
  whatweb: {
    id: "whatweb", label: "WhatWeb", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"boolean", name:"aggressive", label:"Mode agressif", help:"Active le mode agressif." },
      { type:"string", name:"plugins", label:"Plugins", help:"Plugins à activer (facultatif)." }
    ],
    preset: { aggressive:false, plugins:"" }
  },
  sublist3r: {
    id: "sublist3r", label: "Sublist3r", allowedTargetKinds: ["domain"],
    fields: [
      { type:"boolean", name:"bruteforce", label:"Bruteforce", help:"Active le bruteforce." },
      { type:"number", name:"threads", label:"Threads", help:"Nombre de threads.", min:1, max:200 }
    ],
    preset: { bruteforce:false, threads:10 }
  },
  amass: {
    id: "amass", label: "Amass", allowedTargetKinds: ["domain"],
    fields: [
      { type:"boolean", name:"passive", label:"Passif", help:"Mode passif uniquement." },
      { type:"number", name:"timeout", label:"Timeout", help:"Timeout (s).", min:1, max:600 }
    ],
    preset: { passive:true, timeout:60 }
  },
  zap: {
    id: "zap", label: "OWASP ZAP", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"select", name:"mode", label:"Mode", help:"baseline ou full scan", options:[{label:"baseline",value:"baseline"},{label:"full",value:"full"}] },
      { type:"number", name:"timeout", label:"Timeout", help:"Timeout (s).", min:1, max:7200 }
    ],
    preset: { mode:"baseline", timeout:600 }
  },
  sqlmap: {
    id: "sqlmap", label: "SQLMap", allowedTargetKinds: ["url","ip","domain"],
    fields: [
      { type:"string", name:"dbms", label:"DBMS", help:"Forcer le SGBD (facultatif)." },
      { type:"number", name:"threads", label:"Threads", help:"Nombre de threads.", min:1, max:10 },
      { type:"number", name:"risk", label:"Risque", help:"Niveau de risque (1-3).", min:1, max:3 },
      { type:"number", name:"level", label:"Niveau", help:"Niveau de tests (1-5).", min:1, max:5 }
    ],
    preset: { dbms:"", threads:1, risk:1, level:1 }
  }
};
