import React, { createContext, useReducer, useContext } from 'react';

const AuthContext = createContext();

const initialState = {
  user: null,
  token: localStorage.getItem('token') || null,
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  error: null
};

const authReducer = (state, action) => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, loading: true, error: null };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        loading: false,
        error: null
      };
    case 'LOGIN_FAILURE':
      return { ...state, loading: false, error: action.payload };
    case 'LOGOUT':
      return { ...state, user: null, token: null, isAuthenticated: false };
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  const login = (user, token) => {
    dispatch({ type: 'LOGIN_SUCCESS', payload: { user, token } });
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  };

  const logout = () => {
    dispatch({ type: 'LOGOUT' });
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const setUser = (user) => {
    dispatch({ type: 'SET_USER', payload: user });
    localStorage.setItem('user', JSON.stringify(user));
  };

  const setError = (error) => {
    dispatch({ type: 'SET_ERROR', payload: error });
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout, setUser, setError, dispatch }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
