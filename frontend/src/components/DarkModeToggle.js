import React from 'react';

export default function DarkModeToggle({ dark, setDark }) {
  return (
    <button onClick={() => setDark(d => !d)}>
      {dark ? "Switch to Light Mode" : "Switch to Dark Mode"}
    </button>
  );
}