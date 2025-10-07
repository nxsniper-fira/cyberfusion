import React, { useState } from 'react';
import axios from 'axios';

export default function Login({ setUser }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);

  const handleSubmit = e => {
    e.preventDefault();
    axios.post('/api/auth/login', { username, password })
      .then(res => setUser({ loggedIn: true, ...res.data }))
      .catch(() => setErr("Login failed"));
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>CyberFusion Login</h2>
      {err && <div style={{ color: "red" }}>{err}</div>}
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" required />
      <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  );
}