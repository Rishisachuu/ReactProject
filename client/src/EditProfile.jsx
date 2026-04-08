import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { profileService } from '../services/api.jsx';
import '../styles/EditProfile.css';

const EditProfile = () => {
  const { user, setUser } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    location: '',
    bio: ''
  });
  const [privacy, setPrivacy] = useState({
    email_visible: false,
    location_visible: true,
    bio_visible: true
  });
  const [avatar, setAvatar] = useState(null);
  const [avatarPreview, setAvatarPreview] = useState(null);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await profileService.getProfile(user?.id);
        const profile = response.data.user;
        setFormData({
          name: profile.name,
          email: profile.email,
          location: profile.location || '',
          bio: profile.bio || ''
        });
        setPrivacy(profile.privacy);
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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handlePrivacyChange = (e) => {
    const { name, checked } = e.target;
    setPrivacy(prev => ({ ...prev, [name]: checked }));
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAvatar(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setAvatarPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await profileService.updateProfile(user?.id, formData);
      setSuccess('Profile updated successfully!');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  const handleUploadAvatar = async (e) => {
    e.preventDefault();
    if (!avatar) {
      setError('Please select an image');
      return;
    }

    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await profileService.uploadAvatar(user?.id, avatar);
      setSuccess('Avatar uploaded successfully!');
      setAvatar(null);
      setAvatarPreview(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload avatar');
    } finally {
      setSaving(false);
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      setSaving(false);
      return;
    }

    try {
      await profileService.changePassword(user?.id, currentPassword, newPassword);
      setSuccess('Password changed successfully!');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to change password');
    } finally {
      setSaving(false);
    }
  };

  const handleUpdatePrivacy = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await profileService.updatePrivacy(user?.id, privacy);
      setSuccess('Privacy settings updated successfully!');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update privacy settings');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="container"><p>Loading...</p></div>;

  return (
    <div className="edit-profile-container">
      <div className="edit-profile-box">
        <h2>Edit Your Profile</h2>
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Profile Information Form */}
        <form onSubmit={handleUpdateProfile} className="profile-form">
          <h3>Personal Information</h3>
          <div className="form-group">
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              placeholder="Enter your location"
            />
          </div>
          <div className="form-group">
            <label htmlFor="bio">Bio</label>
            <textarea
              id="bio"
              name="bio"
              value={formData.bio}
              onChange={handleInputChange}
              placeholder="Tell us about yourself"
              rows="4"
            ></textarea>
          </div>
          <button type="submit" disabled={saving} className="btn-submit">
            {saving ? 'Saving...' : 'Save Profile'}
          </button>
        </form>

        {/* Avatar Upload Form */}
        <form onSubmit={handleUploadAvatar} className="avatar-form">
          <h3>Profile Picture</h3>
          {avatarPreview && (
            <div className="avatar-preview">
              <img src={avatarPreview} alt="Preview" />
            </div>
          )}
          <div className="form-group">
            <label htmlFor="avatar">Choose Image</label>
            <input
              type="file"
              id="avatar"
              accept="image/*"
              onChange={handleAvatarChange}
            />
          </div>
          <button type="submit" disabled={saving || !avatar} className="btn-submit">
            {saving ? 'Uploading...' : 'Upload Avatar'}
          </button>
        </form>

        {/* Change Password Form */}
        <form onSubmit={handleChangePassword} className="password-form">
          <h3>Change Password</h3>
          <div className="form-group">
            <label htmlFor="currentPassword">Current Password</label>
            <input
              type="password"
              id="currentPassword"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="newPassword">New Password</label>
            <input
              type="password"
              id="newPassword"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Min 8 chars, 1 uppercase, 1 digit, 1 special char"
            />
          </div>
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>
          <button 
            type="submit" 
            disabled={saving || !currentPassword || !newPassword || !confirmPassword} 
            className="btn-submit"
          >
            {saving ? 'Changing...' : 'Change Password'}
          </button>
        </form>

        {/* Privacy Settings Form */}
        <form onSubmit={handleUpdatePrivacy} className="privacy-form">
          <h3>Privacy Settings</h3>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="email_visible"
                checked={privacy.email_visible}
                onChange={handlePrivacyChange}
              />
              Make email visible to others
            </label>
          </div>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="location_visible"
                checked={privacy.location_visible}
                onChange={handlePrivacyChange}
              />
              Make location visible to others
            </label>
          </div>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                name="bio_visible"
                checked={privacy.bio_visible}
                onChange={handlePrivacyChange}
              />
              Make bio visible to others
            </label>
          </div>
          <button type="submit" disabled={saving} className="btn-submit">
            {saving ? 'Saving...' : 'Update Privacy Settings'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default EditProfile;
