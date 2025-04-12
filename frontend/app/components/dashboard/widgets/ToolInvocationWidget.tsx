'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

interface Tool {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
}

const ToolInvocationWidget: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedTool, setSelectedTool] = useState<string | null>(null);
  const router = useRouter();

  // Mock data - in a real implementation, this would be fetched from an API
  const tools: Tool[] = [
    {
      id: 'backup-check',
      name: 'Backup Check',
      description: 'Verify backup status across clients',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
        </svg>
      ),
    },
    {
      id: 'security-scan',
      name: 'Security Scan',
      description: 'Run security assessment',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      ),
    },
    {
      id: 'patch-report',
      name: 'Patch Report',
      description: 'Generate patch compliance report',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      ),
    },
    {
      id: 'user-audit',
      name: 'User Audit',
      description: 'Audit user accounts and permissions',
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      ),
    },
  ];

  const handleToolSelect = (toolId: string) => {
    setSelectedTool(toolId);
  };

  const handlePromptSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt && !selectedTool) return;
    
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      
      // If a tool is selected, navigate to that tool's page
      if (selectedTool) {
        router.push(`/tools/${selectedTool}`);
      } else {
        // If using natural language prompt, parse it and navigate accordingly
        // This is a simple example - in a real app, you'd use NLP to determine intent
        if (prompt.toLowerCase().includes('backup')) {
          router.push('/tools/backup-check');
        } else if (prompt.toLowerCase().includes('security')) {
          router.push('/tools/security-scan');
        } else if (prompt.toLowerCase().includes('patch')) {
          router.push('/tools/patch-report');
        } else if (prompt.toLowerCase().includes('user')) {
          router.push('/tools/user-audit');
        } else {
          // Default to tools page
          router.push('/tools');
        }
      }
    }, 1500);
  };

  return (
    <div className="bg-slate-900 rounded-lg shadow-md overflow-hidden">
      <div className="px-4 py-3 bg-slate-800 border-b border-slate-700">
        <h3 className="text-lg font-medium text-white">Tool Launcher</h3>
      </div>
      <div className="p-4">
        <form onSubmit={handlePromptSubmit}>
          <div className="relative">
            <input
              type="text"
              className="w-full bg-slate-800 border border-slate-700 rounded-md py-2 pl-3 pr-10 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
              placeholder="Ask a question or run a tool..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={isLoading}
            />
            <button
              type="submit"
              className="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-white"
              disabled={isLoading}
            >
              {isLoading ? (
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
                </svg>
              )}
            </button>
          </div>
        </form>
        
        <div className="mt-4">
          <div className="text-xs text-slate-400 mb-2">Quick Access Tools</div>
          <div className="grid grid-cols-2 gap-2">
            {tools.map((tool) => (
              <button
                key={tool.id}
                className={`flex items-center p-2 rounded-md text-left transition-colors ${
                  selectedTool === tool.id
                    ? 'bg-cyan-900 text-white'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
                onClick={() => handleToolSelect(tool.id)}
                disabled={isLoading}
              >
                <div className={`flex-shrink-0 mr-2 ${selectedTool === tool.id ? 'text-cyan-400' : 'text-slate-400'}`}>
                  {tool.icon}
                </div>
                <div>
                  <div className="text-sm font-medium">{tool.name}</div>
                  <div className="text-xs text-slate-400 truncate">{tool.description}</div>
                </div>
              </button>
            ))}
          </div>
        </div>
        
        <div className="mt-4 text-xs text-slate-500">
          <p>Try: "Check backup status for ACME Corp" or "Run security scan on all clients"</p>
        </div>
      </div>
    </div>
  );
};

export default ToolInvocationWidget;
