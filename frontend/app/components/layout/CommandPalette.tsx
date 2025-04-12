'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';

interface CommandPaletteProps {
  onClose: () => void;
}

interface CommandItem {
  id: string;
  name: string;
  description?: string;
  icon?: React.ReactNode;
  action: () => void;
  category: 'navigation' | 'client' | 'agent' | 'tool';
}

const CommandPalette: React.FC<CommandPaletteProps> = ({ onClose }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const router = useRouter();

  // Mock data - in a real implementation, this would be fetched from an API
  const commands: CommandItem[] = [
    // Navigation commands
    {
      id: 'nav-dashboard',
      name: 'Go to Dashboard',
      description: 'Navigate to the main dashboard',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
        </svg>
      ),
      action: () => router.push('/'),
      category: 'navigation',
    },
    {
      id: 'nav-clients',
      name: 'Go to Clients',
      description: 'View all clients',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
      ),
      action: () => router.push('/clients'),
      category: 'navigation',
    },
    {
      id: 'nav-agents',
      name: 'Go to Agents',
      description: 'View and run agents',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      ),
      action: () => router.push('/agents'),
      category: 'navigation',
    },
    
    // Client commands
    {
      id: 'client-acme',
      name: 'ACME Corp',
      description: 'View client details',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
      action: () => router.push('/clients/1'),
      category: 'client',
    },
    {
      id: 'client-globex',
      name: 'Globex Industries',
      description: 'View client details',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      ),
      action: () => router.push('/clients/2'),
      category: 'client',
    },
    
    // Agent commands
    {
      id: 'agent-backup',
      name: 'Run Backup Check',
      description: 'Check backup status across all clients',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
        </svg>
      ),
      action: () => {
        router.push('/agents/backup-check');
        onClose();
      },
      category: 'agent',
    },
    {
      id: 'agent-security',
      name: 'Run Security Scan',
      description: 'Scan for security issues',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      ),
      action: () => {
        router.push('/agents/security-scan');
        onClose();
      },
      category: 'agent',
    },
    
    // Tool commands
    {
      id: 'tool-report',
      name: 'Generate Report',
      description: 'Create a new client report',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      ),
      action: () => {
        router.push('/tools/report-generator');
        onClose();
      },
      category: 'tool',
    },
  ];

  // Filter commands based on search query
  const filteredCommands = searchQuery
    ? commands.filter(command => 
        command.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (command.description && command.description.toLowerCase().includes(searchQuery.toLowerCase()))
      )
    : commands;

  // Focus input on mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < filteredCommands.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => (prev > 0 ? prev - 1 : 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (filteredCommands[selectedIndex]) {
          filteredCommands[selectedIndex].action();
          onClose();
        }
        break;
      case 'Escape':
        e.preventDefault();
        onClose();
        break;
      default:
        break;
    }
  };

  // Group commands by category
  const groupedCommands = filteredCommands.reduce<Record<string, CommandItem[]>>(
    (acc, command) => {
      if (!acc[command.category]) {
        acc[command.category] = [];
      }
      acc[command.category].push(command);
      return acc;
    },
    {}
  );

  // Category labels
  const categoryLabels: Record<string, string> = {
    navigation: 'Navigation',
    client: 'Clients',
    agent: 'Agents',
    tool: 'Tools',
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="command-palette-title" role="dialog" aria-modal="true">
      <div className="min-h-screen px-4 text-center">
        {/* Background overlay */}
        <div className="fixed inset-0 bg-slate-900 bg-opacity-75 transition-opacity" aria-hidden="true" onClick={onClose}></div>
        
        {/* Command palette */}
        <div className="command-palette">
          <div className="p-2">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                ref={inputRef}
                type="text"
                className="block w-full pl-10 pr-3 py-3 border-0 bg-slate-800 text-white placeholder-slate-400 focus:outline-none focus:ring-0 text-sm"
                placeholder="Search commands, clients, agents..."
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setSelectedIndex(0);
                }}
                onKeyDown={handleKeyDown}
              />
            </div>
          </div>
          
          <div className="max-h-96 overflow-y-auto">
            {Object.keys(groupedCommands).length === 0 ? (
              <div className="py-14 px-6 text-center">
                <p className="text-slate-400">No results found</p>
              </div>
            ) : (
              <div className="py-2">
                {Object.entries(groupedCommands).map(([category, items]) => (
                  <div key={category} className="mb-2">
                    <div className="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                      {categoryLabels[category]}
                    </div>
                    <ul className="mt-1">
                      {items.map((command, index) => {
                        const commandIndex = filteredCommands.findIndex(c => c.id === command.id);
                        const isSelected = commandIndex === selectedIndex;
                        
                        return (
                          <li key={command.id}>
                            <button
                              className={`w-full text-left px-3 py-2 flex items-center space-x-3 ${
                                isSelected ? 'bg-slate-700 text-white' : 'text-slate-200 hover:bg-slate-800'
                              }`}
                              onClick={() => {
                                command.action();
                                onClose();
                              }}
                              onMouseEnter={() => setSelectedIndex(commandIndex)}
                            >
                              <div className={`flex-shrink-0 ${isSelected ? 'text-cyan-400' : 'text-slate-400'}`}>
                                {command.icon}
                              </div>
                              <div>
                                <div className="font-medium">{command.name}</div>
                                {command.description && (
                                  <div className="text-xs text-slate-400">{command.description}</div>
                                )}
                              </div>
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="px-3 py-2 border-t border-slate-700">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <div className="flex space-x-4">
                <div className="flex items-center">
                  <span className="mr-1">↑↓</span>
                  <span>Navigate</span>
                </div>
                <div className="flex items-center">
                  <span className="mr-1">↵</span>
                  <span>Select</span>
                </div>
                <div className="flex items-center">
                  <span className="mr-1">Esc</span>
                  <span>Close</span>
                </div>
              </div>
              <div>
                <span className="text-xs text-slate-500">MSPAlwaysOn Command Palette</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CommandPalette;
