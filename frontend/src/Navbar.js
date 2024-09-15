// src/Navbar.js
import React from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Navbar.css';
import logo from './NeuroGuard.jpg'; // Adjust this path if necessary

function Navbar() {
  const handleLogout = () => {
    Cookies.remove('authToken');
    window.location.href = '/login';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo and Name */}
        <Link to="/" className="navbar-logo">
          <img src={logo} alt="NeuroGuard Logo" className="logo-image" />
          <span className="logo-text">NeuroGuard</span>
        </Link>

        {/* Centered Navbar Links */}
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
