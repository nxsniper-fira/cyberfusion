import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Analytics() {
  const [usage, setUsage] = useState([]);

  useEffect(() => {
    axios.get('/api/analytics/tool-usage')
      .then(res => setUsage(res.data));
  }, []);

  return (
    <div style={{
      background: "#23272a",
      borderRadius: 8,
      padding: 12,
      margin: "16px 0",
      maxWidth: 500
    }}>
      <h4>Tool Usage Analytics</h4>
      <table>
        <thead>
          <tr>
            <th>Tool</th>
            <th>Launch Count</th>
          </tr>
        </thead>
        <tbody>
          {usage.map(u => (
            <tr key={u.tool}>
              <td>{u.tool}</td>
              <td>{u.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {usage.length === 0 && <div>No usage data yet.</div>}
    </div>
  );
}