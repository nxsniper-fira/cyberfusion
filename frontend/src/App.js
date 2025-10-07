import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import AdminPanel from './components/AdminPanel';

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios.get('/api/auth/me')
      .then(res => setUser(res.data))
      .catch(() => setUser(null));
  }, []);

  if (!user || !user.loggedIn) {
    return <Login setUser={setUser} />;
  }

  if (user.role === 'admin') {
    return <AdminPanel user={user} setUser={setUser} />;
  }

  return <Dashboard user={user} setUser={setUser} />;
}

export default App;