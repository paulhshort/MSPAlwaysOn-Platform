'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '../../lib/auth/auth-context';
import ClientSelector from '../ClientSelector';
import CommandPalette from './CommandPalette';

const Header = () => {
  const pathname = usePathname();
  const { user, isAuthenticated } = useAuth();
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/' },
    { name: 'Clients', href: '/clients' },
    { name: 'Agents', href: '/agents' },
    { name: 'Alerts', href: '/alerts' },
    { name: 'Tools', href: '/tools' },
    { name: 'Tickets', href: '/tickets' },
    { name: 'Reports', href: '/reports' },
  ];

  const openCommandPalette = () => {
    setCommandPaletteOpen(true);
  };

  const closeCommandPalette = () => {
    setCommandPaletteOpen(false);
  };

  // Handle keyboard shortcut for command palette
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Command/Ctrl + K
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen(prev => !prev);
      }
      // Escape key to close
      if (e.key === 'Escape' && commandPaletteOpen) {
        setCommandPaletteOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [commandPaletteOpen]);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-40 bg-slate-900 border-b border-slate-700 h-16">
        <div className="h-full px-4 flex items-center justify-between">
          {/* Logo and Navigation */}
          <div className="flex items-center space-x-8">
            <Link href="/" className="flex items-center">
              <span className="text-xl font-bold text-cyan-500">MSPAlwaysOn</span>
            </Link>
            
            {isAuthenticated && (
              <nav className="hidden md:flex space-x-1">
                {navigation.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.name}
                      href={item.href}
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isActive
                          ? 'bg-slate-800 text-white'
                          : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                      }`}
                    >
                      {item.name}
                    </Link>
                  );
                })}
              </nav>
            )}
          </div>

          {/* Right Side - Client Selector, Command Palette, User */}
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              <div className="hidden md:block w-64">
                <ClientSelector />
              </div>
              
              <button
                onClick={openCommandPalette}
                className="flex items-center px-3 py-1.5 text-sm bg-slate-800 text-slate-300 rounded-md border border-slate-700 hover:bg-slate-700 transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="mr-2">Search...</span>
                <span className="flex items-center justify-center px-1.5 py-0.5 text-xs bg-slate-700 rounded">⌘K</span>
              </button>
              
              <div className="relative">
                <button className="flex items-center justify-center w-8 h-8 rounded-full bg-cyan-600 text-white hover:bg-cyan-500 transition-colors">
                  {user?.name ? user.name.charAt(0).toUpperCase() : 'U'}
                </button>
              </div>
            </div>
          ) : (
            <div>
              <Link
                href="/login"
                className="px-4 py-2 text-sm font-medium text-white bg-cyan-600 rounded-md hover:bg-cyan-500 transition-colors"
              >
                Sign In
              </Link>
            </div>
          )}
        </div>
      </header>

      {/* Command Palette */}
      {commandPaletteOpen && (
        <CommandPalette onClose={closeCommandPalette} />
      )}
    </>
  );
};

export default Header;
