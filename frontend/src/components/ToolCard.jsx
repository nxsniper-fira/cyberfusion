import React from 'react';

function ToolCard({ tool, onLaunch }) {
  return (
    <div className="tool-card">
      <h3>{tool.name}</h3>
      <p>{tool.description}</p>
      <span className={`status ${tool.status}`}>{tool.status}</span>
      <button onClick={() => onLaunch(tool.id)}>Launch</button>
    </div>
  );
}

export default ToolCard;