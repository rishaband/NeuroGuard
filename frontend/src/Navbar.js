// src/Navbar.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Navbar.css'; // Import the CSS file

function Navbar() {
//   const navigate = useNavigate();

  const handleLogout = () => {
    // Remove the authToken cookie
    Cookies.remove('authToken');
    
    // Redirect to the login page
    window.location.href = '/login';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          NeuroGuard
        </Link>
        <ul className="navbar-menu">
          <li className="navbar-item">
            <Link to="/main" className="navbar-link">Home</Link>
          </li>
          <li className="navbar-item">
            <Link to="/fallHistory" className="navbar-link">Fall History</Link>
          </li>
          <li className="navbar-item">
            <button onClick={handleLogout} className="navbar-link logout-button">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
