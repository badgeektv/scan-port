import { useMemo } from "react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Info } from "lucide-react";

export default function TargetField({ value, onChange }:{ value:string; onChange:(v:string)=>void }) {
  const detected = useMemo(() => {
    try { const u = new URL(value); if (["http:","https:"].includes(u.protocol)) return "url"; } catch {}
    const ipv4 = /^(25[0-5]|2[0-4]\d|[01]?\d?\d)(\.(25[0-5]|2[0-4]\d|[01]?\d?\d)){3}$/.test(value);
    const ipv6 = /^[0-9a-f:]+$/i.test(value) && value.includes(":");
    const domain = /^(?!-)[A-Za-z0-9-]{1,63}(\.(?!-)[A-Za-z0-9-]{1,63})+$/.test(value);
    return ipv4 || ipv6 ? "ip" : domain ? "domain" : "";
  }, [value]);

  return (
    <div className="space-y-1">
      <div className="flex items-center gap-2">
        <label className="text-sm font-medium">Cible (URL, IP ou domaine)</label>
        <TooltipProvider delayDuration={150}>
          <Tooltip>
            <TooltipTrigger className="inline-flex"><Info className="w-4 h-4 opacity-70" /></TooltipTrigger>
            <TooltipContent className="max-w-xs text-sm">
              Exemple URL: https://example.com — IP: 203.0.113.10 — Domaine: target.example
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
        {detected && <span className="ml-auto text-xs px-2 py-0.5 rounded bg-muted">{detected.toUpperCase()}</span>}
      </div>
      <input
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder="https://site.tld ou 203.0.113.10"
        className="w-full border rounded-xl px-3 py-2 focus:outline-none focus:ring"
      />
    </div>
  );
}
