import { useParams } from 'react-router-dom';
import JobLogStream from '../components/JobLogStream';

export default function JobDetails() {
  const { id } = useParams();
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-xl">Job {id}</h1>
      {id && <JobLogStream jobId={id} />}
    </div>
  );
}
