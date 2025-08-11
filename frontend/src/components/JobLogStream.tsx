import { useEffect, useRef, useState } from 'react';

export default function JobLogStream({ jobId }:{ jobId:string }) {
  const [lines, setLines] = useState<string[]>([]);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const es = new EventSource(`/api/jobs/${jobId}/stream`);
    es.onmessage = e => setLines(l => [...l, e.data]);
    es.onerror = () => es.close();
    return () => es.close();
  }, [jobId]);

  useEffect(() => {
    ref.current?.scrollTo(0, ref.current.scrollHeight);
  }, [lines]);

  return <div ref={ref} className="bg-black text-green-500 p-2 h-64 overflow-auto text-sm whitespace-pre-wrap">{lines.join('\n')}</div>;
}
