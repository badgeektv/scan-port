import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import NewScan from './pages/NewScan';
import JobDetails from './pages/JobDetails';
import Settings from './pages/Settings';

export default function App() {
  return (
    <BrowserRouter>
      <nav className="p-2 space-x-4 bg-gray-100">
        <Link to="/">Dashboard</Link>
        <Link to="/new">Nouveau scan</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/new" element={<NewScan />} />
        <Route path="/jobs/:id" element={<JobDetails />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}
