import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Scheduler({ tools, user }) {
  const [jobs, setJobs] = useState([]);
  const [toolId, setToolId] = useState("");
  const [delay, setDelay] = useState(1);

  const fetchJobs = () => {
    axios.get('/api/scheduler/jobs').then(res => setJobs(res.data));
  };

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 5000);
    return () => clearInterval(interval);
  }, []);

  const scheduleJob = e => {
    e.preventDefault();
    if (!toolId) return;
    axios.post('/api/scheduler/jobs', { tool_id: toolId, delay })
      .then(() => {
        setToolId("");
        setDelay(1);
        fetchJobs();
      });
  };

  return (
    <div style={{background: "#23272a", borderRadius: 8, padding: 12, margin: "16px 0", maxWidth: 500}}>
      <h4>Schedule Tool Launch</h4>
      <form onSubmit={scheduleJob} style={{display: "flex", gap: 8, alignItems: 'center'}}>
        <select value={toolId} onChange={e => setToolId(e.target.value)} required>
          <option value="">Select Tool</option>
          {tools.map(t => (
            <option key={t.id} value={t.id}>{t.name} ({t.category})</option>
          ))}
        </select>
        <input type="number" value={delay} min={1} max={1440}
          onChange={e => setDelay(e.target.value)} style={{width: "60px"}} />
        <span>min</span>
        <button type="submit">Schedule</button>
      </form>
      <h5>Scheduled Jobs</h5>
      <ul>
        {jobs.map((j, idx) => (
          <li key={idx}>
            {j.user} will run Tool #{j.tool_id} in {j.delay} min (created {j.created})
          </li>
        ))}
      </ul>
    </div>
  );
}