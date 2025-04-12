'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

// Define user type
export interface User {
  id: string;
  name: string;
  email: string;
  roles: string[];
}

// Define auth context type
interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

// Create auth context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth provider component
export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      setIsLoading(true);
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setUser(null);
          setIsLoading(false);
          return;
        }

        // Set default auth header
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        // Get user info
        const response = await axios.get('/api/v1/auth/me');
        setUser(response.data);
      } catch (error) {
        console.error('Auth check failed:', error);
        setUser(null);
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      // Get token
      const response = await axios.post('/api/v1/auth/token', {
        username: email,
        password: password,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      // Save token
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);

      // Set default auth header
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

      // Get user info
      const userResponse = await axios.get('/api/v1/auth/me');
      setUser(userResponse.data);

      // Redirect to dashboard
      router.push('/');
    } catch (error: any) {
      console.error('Login failed:', error);
      setError(error.response?.data?.detail || 'Login failed');
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
    router.push('/login');
  };

  // Auth context value
  const value = {
    user,
    isLoading,
    error,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Auth hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
