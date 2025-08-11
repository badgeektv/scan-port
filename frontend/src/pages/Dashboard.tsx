import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api';

export default function Dashboard() {
  const [jobs,setJobs]=useState<string[]>([]);
  useEffect(()=>{ api.get('/jobs').then(r=>setJobs(r.jobs||[])); },[]);
  return (
    <div className="p-4">
      <h1 className="text-xl mb-4">Jobs</h1>
      <ul className="list-disc pl-6 space-y-1">
        {jobs.map(id => <li key={id}><Link className="text-blue-600" to={`/jobs/${id}`}>{id}</Link></li>)}
      </ul>
    </div>
  );
}
