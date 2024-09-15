// src/Login.js
import React, { useState } from 'react';
import Cookies from 'js-cookie';
import './Login.css';

function Login({ setIsAuthenticated }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const hardcodedUsername = 'htn24';
  const hardcodedPassword = '12345678';

  const handleLogin = (e) => {
    e.preventDefault();
    if (username === hardcodedUsername && password === hardcodedPassword) {
      Cookies.set('authToken', 'valid', { expires: 10 }); // Set cookie for 1 day
      setIsAuthenticated(true); // Update state to redirect to main page
    } else {
      alert('Invalid credentials!');
    }
  };

  return (
    <div className="Login">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
