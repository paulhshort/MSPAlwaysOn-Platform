'use client';

import React, { useState, useEffect } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import { useAuth } from '../../lib/auth/auth-context';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const [mounted, setMounted] = useState(false);

  // Handle hydration mismatch by only rendering after mount
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Header />
      
      {isAuthenticated && <Sidebar />}
      
      <main className={`pt-16 ${isAuthenticated ? 'pl-64' : ''} transition-all duration-300`}>
        <div className="p-6">
          {isLoading ? (
            <div className="flex items-center justify-center h-[calc(100vh-6rem)]">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
            </div>
          ) : (
            children
          )}
        </div>
      </main>
    </div>
  );
};

export default MainLayout;
