import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import '../styles/Home.css';

const Home = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="home-content">
        <h1>Welcome to Profile Management System</h1>
        <p>Manage your profile with ease and security</p>
        {!isAuthenticated ? (
          <div className="home-buttons">
            <button className="btn-primary" onClick={() => navigate('/login')}>Login</button>
            <button className="btn-secondary" onClick={() => navigate('/signup')}>Sign Up</button>
          </div>
        ) : (
          <div className="home-buttons">
            <button className="btn-primary" onClick={() => navigate('/dashboard')}>Go to Dashboard</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
