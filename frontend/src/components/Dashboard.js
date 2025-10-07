import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ToolCard from './ToolCard';
import Chat from './Chat';
import Scheduler from './Scheduler';
import Analytics from './Analytics';
import DocsBrowser from './DocsBrowser';

export default function Dashboard({ user, setUser }) {
  const [tools, setTools] = useState([]);
  const [msg, setMsg] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    axios.get('/api/tools/')
      .then(res => setTools(res.data));
  }, []);

  const handleLaunch = id => {
    axios.post(`/api/tools/launch/${id}`)
      .then(res => setMsg(res.data.message))
      .catch(() => setMsg('Error launching tool'));
  };

  const filteredTools = tools.filter(tool =>
    tool.name.toLowerCase().includes(search.toLowerCase()) ||
    tool.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <h2>Welcome, {user.username} ({user.role})</h2>
      <button onClick={() => {
        axios.post('/api/auth/logout').then(() => setUser(null));
      }}>Logout</button>
      <Chat user={user} />
      <Scheduler tools={tools} user={user} />
      <Analytics />
      <DocsBrowser user={user} />
      <h3>Tools</h3>
      <input
        value={search}
        onChange={e => setSearch(e.target.value)}
        placeholder="Search by name or category"
        style={{width: "220px"}}
      />
      {msg && <div style={{color: "#1f8ef1"}}>{msg}</div>}
      <div>
        {filteredTools.map(tool => (
          <ToolCard key={tool.id} tool={tool} onLaunch={handleLaunch} />
        ))}
      </div>
    </div>
  );
}