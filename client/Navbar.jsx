import React from 'react';
import '../styles/Navbar.css';
import { useAuth } from '../context/AuthContext.jsx';
import { useNavigate } from 'react-router-dom';

const Navbar = () => {
  const { isAuthenticated, logout, user } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <h1 className="navbar-logo" onClick={() => navigate('/')}>Profile Manager</h1>
        <ul className="nav-menu">
          {isAuthenticated ? (
            <>
              <li className="nav-item">
                <span className="welcome-text">Welcome, {user?.name}</span>
              </li>
              <li className="nav-item">
                <button className="nav-link" onClick={() => navigate('/dashboard')}>Dashboard</button>
              </li>
              <li className="nav-item">
                <button className="nav-link" onClick={() => navigate('/edit-profile')}>Edit Profile</button>
              </li>
              <li className="nav-item">
                <button className="nav-link logout-btn" onClick={handleLogout}>Logout</button>
              </li>
            </>
          ) : (
            <>
              <li className="nav-item">
                <button className="nav-link" onClick={() => navigate('/login')}>Login</button>
              </li>
              <li className="nav-item">
                <button className="nav-link" onClick={() => navigate('/signup')}>Sign Up</button>
              </li>
            </>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
