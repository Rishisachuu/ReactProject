import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { profileService } from '../services/api.jsx';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { user, setUser } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await profileService.getProfile(user?.id);
        setProfile(response.data.user);
      } catch (err) {
        setError('Failed to load profile');
      } finally {
        setLoading(false);
      }
    };

    if (user?.id) {
      fetchProfile();
    }
  }, [user?.id]);

  if (loading) return <div className="container"><p>Loading...</p></div>;

  return (
    <div className="dashboard-container">
      <div className="dashboard-box">
        <h2>My Profile</h2>
        {error && <div className="error-message">{error}</div>}
        {profile && (
          <div className="profile-content">
            <div className="avatar-section">
              {profile.avatar ? (
                <img 
                  src={`http://localhost:5000/uploads/${profile.avatar}`} 
                  alt="Profile" 
                  className="avatar-image"
                />
              ) : (
                <div className="avatar-placeholder">No Avatar</div>
              )}
            </div>
            <div className="profile-info">
              <div className="info-row">
                <label>Name:</label>
                <span>{profile.name}</span>
              </div>
              <div className="info-row">
                <label>Email:</label>
                <span>{profile.email}</span>
              </div>
              <div className="info-row">
                <label>Location:</label>
                <span>{profile.location || 'Not set'}</span>
              </div>
              <div className="info-row">
                <label>Bio:</label>
                <span>{profile.bio || 'Not set'}</span>
              </div>
              <div className="info-row">
                <label>Member Since:</label>
                <span>{new Date(profile.created_at).toLocaleDateString()}</span>
              </div>
            </div>
            <button className="btn-primary" onClick={() => navigate('/edit-profile')}>
              Edit Profile
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
