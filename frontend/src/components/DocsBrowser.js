import React, { useEffect, useState } from 'react';
import axios from 'axios';
// Optionally: import ReactMarkdown from 'react-markdown';

export default function DocsBrowser({ user }) {
  const [docs, setDocs] = useState([]);
  const [selected, setSelected] = useState(null);
  const [content, setContent] = useState("");
  const [edit, setEdit] = useState(false);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    axios.get('/api/docs/').then(res => setDocs(res.data));
  }, []);

  const openDoc = fname => {
    axios.get(`/api/docs/${fname}`).then(res => {
      setSelected(fname);
      setContent(res.data);
      setEdit(false);
      setMsg("");
    });
  };

  const handleSave = () => {
    axios.post(`/api/docs/${selected}`, { content })
      .then(() => setMsg("Saved!"))
      .catch(() => setMsg("Save failed!"));
  };

  return (
    <div style={{background: "#23272a", borderRadius: 8, padding: 12, margin: "16px 0", maxWidth: 700}}>
      <h4>Team Documentation</h4>
      <div style={{display: "flex", gap: 16}}>
        <div>
          <ul>
            {docs.map(fname => (
              <li key={fname}>
                <button onClick={() => openDoc(fname)}>{fname}</button>
              </li>
            ))}
          </ul>
        </div>
        <div style={{flex: 1}}>
          {selected && (
            <>
              <h5>{selected}</h5>
              {edit ? (
                <>
                  <textarea
                    value={content}
                    onChange={e => setContent(e.target.value)}
                    rows={20} style={{width: "100%"}}
                  />
                  <button onClick={handleSave}>Save</button>
                  <button onClick={() => setEdit(false)}>Cancel</button>
                  {msg && <div>{msg}</div>}
                </>
              ) : (
                <>
                  <pre style={{whiteSpace: "pre-wrap", background: "#181a1b"}}>{content}</pre>
                  {user.role === "admin" && (
                    <button onClick={() => setEdit(true)}>Edit</button>
                  )}
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}