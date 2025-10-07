import React from 'react';

export default function ToolCard({ tool, onLaunch }) {
  return (
    <div style={{
      border: "1px solid #444",
      margin: "8px",
      padding: "8px",
      borderRadius: "6px",
      background: "#222"
    }}>
      <b>{tool.name}</b> <span style={{fontSize: "0.9em"}}>({tool.category})</span><br />
      <small>{tool.description}</small><br />
      <button onClick={() => onLaunch(tool.id)}>Launch</button>
      <span style={{marginLeft: "10px"}}>Status: {tool.status}</span>
    </div>
  );
}