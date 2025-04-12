import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Navbar from './components/Navbar';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  return (
    <Router>
      <Navbar token={token} setToken={setToken} />
      <Switch>
        <Route path="/login">
          <Login setToken={(t) => {
            setToken(t);
            localStorage.setItem('token', t);
          }} />
        </Route>
        <Route path="/">
          {token ? <Dashboard token={token} /> : <Login setToken={setToken} />}
        </Route>
      </Switch>
    </Router>
  );
};

export default App;
