import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function AdminPanel({ user, setUser }) {
  const [users, setUsers] = useState([]);
  const [logs, setLogs] = useState([]);
  const [newUser, setNewUser] = useState({ username: "", password: "", role: "whitehat" });

  useEffect(() => {
    axios.get('/api/admin/users').then(res => setUsers(res.data));
    axios.get('/api/admin/audit').then(res => setLogs(res.data));
  }, []);

  const handleAddUser = e => {
    e.preventDefault();
    axios.post('/api/admin/users', newUser)
      .then(() => {
        setNewUser({ username: "", password: "", role: "whitehat" });
        return axios.get('/api/admin/users');
      })
      .then(res => setUsers(res.data));
  };

  return (
    <div>
      <h2>Admin Panel ({user.username})</h2>
      <button onClick={() => {
        axios.post('/api/auth/logout').then(() => setUser(null));
      }}>Logout</button>

      <h3>Add User</h3>
      <form onSubmit={handleAddUser}>
        <input
          value={newUser.username}
          onChange={e => setNewUser({...newUser, username: e.target.value})}
          placeholder="Username"
          required
        />
        <input
          value={newUser.password}
          onChange={e => setNewUser({...newUser, password: e.target.value})}
          type="password"
          placeholder="Password"
          required
        />
        <select
          value={newUser.role}
          onChange={e => setNewUser({...newUser, role: e.target.value})}
        >
          <option value="whitehat">White Hat</option>
          <option value="blue">Blue Team</option>
          <option value="red">Red Team</option>
          <option value="gray">Gray Hat</option>
          <option value="black">Black Hat</option>
          <option value="admin">Admin</option>
        </select>
        <button type="submit">Add User</button>
      </form>

      <h3>Users</h3>
      <ul>
        {users.map(u => <li key={u.id}>{u.username} ({u.role}) {u.active ? "" : "[inactive]"}</li>)}
      </ul>

      <h3>Audit Log (last 100)</h3>
      <table>
        <thead><tr><th>User</th><th>Tool</th><th>Time</th><th>Action</th><th>Details</th></tr></thead>
        <tbody>
        {logs.map(log => (
          <tr key={log.id}>
            <td>{log.user}</td><td>{log.tool}</td><td>{log.timestamp}</td><td>{log.action}</td><td>{log.details}</td>
          </tr>
        ))}
        </tbody>
      </table>
    </div>
  );
}