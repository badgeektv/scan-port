import { useState } from 'react';
import TargetField from '../components/TargetField';
import { ToolForm } from '../components/ToolForm';
import { toolsRegistry, ToolDef } from '../tools/registry';
import { api } from '../lib/api';

export default function NewScan() {
  const [toolId,setToolId] = useState<keyof typeof toolsRegistry>('nmap');
  const tool:ToolDef = toolsRegistry[toolId];
  const [target,setTarget] = useState('');
  const [options,setOptions] = useState<any>(tool.preset||{});
  const submit = ()=>{
    api.post(`/scan/${toolId}`,{target:{value:target},options}).then(res=>alert(`Job ${res.id}`));
  };
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl">Nouveau scan</h1>
      <div>
        <label>Outil</label>
        <select value={toolId} onChange={e=>{setToolId(e.target.value as any); setOptions(toolsRegistry[e.target.value as keyof typeof toolsRegistry].preset||{});}} className="border ml-2">
          {Object.values(toolsRegistry).map(t=> <option key={t.id} value={t.id}>{t.label}</option>)}
        </select>
      </div>
      <TargetField value={target} onChange={setTarget} />
      <ToolForm fields={tool.fields} values={options} onChange={setOptions} />
      <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={submit}>Lancer</button>
    </div>
  );
}
