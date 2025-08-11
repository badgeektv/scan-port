import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Info } from "lucide-react";
import { FieldDef } from "../tools/registry";

export function ToolForm({ fields, values, onChange }:{ fields:FieldDef[]; values:any; onChange:(v:any)=>void }) {
  const handle = (name:string,value:any)=>onChange({...values,[name]:value});
  return (
    <div className="space-y-4">
      {fields.map(f => (
        <div key={f.name} className="space-y-1">
          <label className="text-sm font-medium flex items-center gap-1">
            {f.label}
            {f.help && (
              <TooltipProvider delayDuration={150}>
                <Tooltip>
                  <TooltipTrigger className="inline-flex"><Info className="w-3 h-3 opacity-70" /></TooltipTrigger>
                  <TooltipContent className="max-w-xs text-sm">{f.help}</TooltipContent>
                </Tooltip>
              </TooltipProvider>
            )}
          </label>
          {f.type === 'string' && (
            <input className="border rounded px-2 py-1 w-full" value={values[f.name]||''} onChange={e=>handle(f.name,e.target.value)} placeholder={f.placeholder} />
          )}
          {f.type === 'number' && (
            <input type="number" className="border rounded px-2 py-1 w-full" value={values[f.name]??''} onChange={e=>handle(f.name,Number(e.target.value))} min={f.min} max={f.max} step={f.step} />
          )}
          {f.type === 'boolean' && (
            <input type="checkbox" checked={values[f.name]||false} onChange={e=>handle(f.name,e.target.checked)} />
          )}
          {f.type === 'select' && (
            <select className="border rounded px-2 py-1 w-full" value={values[f.name]||''} onChange={e=>handle(f.name,e.target.value)}>
              {f.options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          )}
        </div>
      ))}
    </div>
  );
}
