'use client';

import React from 'react';
import Link from 'next/link';

interface AgentRun {
  id: string;
  agentName: string;
  status: 'success' | 'failed' | 'running';
  timestamp: string;
  duration: string;
  client?: string;
}

const AgentActivityWidget: React.FC = () => {
  // Mock data - in a real implementation, this would be fetched from an API
  const agentRuns: AgentRun[] = [
    {
      id: '1',
      agentName: 'Backup Verification',
      status: 'success',
      timestamp: '2023-04-12T10:30:00Z',
      duration: '45s',
      client: 'ACME Corp',
    },
    {
      id: '2',
      agentName: 'Security Scan',
      status: 'running',
      timestamp: '2023-04-12T10:15:00Z',
      duration: '2m',
      client: 'Globex Industries',
    },
    {
      id: '3',
      agentName: 'Patch Compliance',
      status: 'failed',
      timestamp: '2023-04-12T09:45:00Z',
      duration: '1m 30s',
      client: 'Initech',
    },
    {
      id: '4',
      agentName: 'User Audit',
      status: 'success',
      timestamp: '2023-04-12T09:30:00Z',
      duration: '2m 15s',
      client: 'Umbrella Corporation',
    },
    {
      id: '5',
      agentName: 'System Health Check',
      status: 'success',
      timestamp: '2023-04-12T09:00:00Z',
      duration: '1m',
      client: 'Stark Industries',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'bg-emerald-500';
      case 'running':
        return 'bg-cyan-500';
      case 'failed':
        return 'bg-rose-500';
      default:
        return 'bg-slate-500';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'success':
        return 'Success';
      case 'running':
        return 'Running';
      case 'failed':
        return 'Failed';
      default:
        return status;
    }
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="bg-slate-900 rounded-lg shadow-md overflow-hidden">
      <div className="px-4 py-3 bg-slate-800 border-b border-slate-700">
        <h3 className="text-lg font-medium text-white">Agent Activity</h3>
      </div>
      <div className="divide-y divide-slate-700">
        {agentRuns.map((run) => (
          <div key={run.id} className="px-4 py-3 hover:bg-slate-800 transition-colors">
            <div className="flex items-start">
              <div className={`${getStatusColor(run.status)} h-3 w-3 rounded-full mt-1.5 mr-3 flex-shrink-0 ${
                run.status === 'running' ? 'animate-pulse' : ''
              }`}></div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <Link href={`/agents/runs/${run.id}`} className="text-sm font-medium text-white hover:text-cyan-400 truncate">
                    {run.agentName}
                  </Link>
                  <div className="ml-2 flex items-center">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                      run.status === 'success' ? 'bg-emerald-900 text-emerald-300' :
                      run.status === 'running' ? 'bg-cyan-900 text-cyan-300' :
                      'bg-rose-900 text-rose-300'
                    }`}>
                      {getStatusText(run.status)}
                    </span>
                  </div>
                </div>
                <div className="mt-1 flex items-center text-xs">
                  {run.client && (
                    <>
                      <span className="text-slate-300">{run.client}</span>
                      <span className="mx-1.5 text-slate-500">•</span>
                    </>
                  )}
                  <span className="text-slate-400">{formatTime(run.timestamp)}</span>
                  <span className="mx-1.5 text-slate-500">•</span>
                  <span className="text-slate-400">{run.duration}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="px-4 py-3 bg-slate-800 border-t border-slate-700">
        <Link
          href="/agents"
          className="text-sm text-cyan-400 hover:text-cyan-300 flex items-center justify-center"
        >
          View all agent runs
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  );
};

export default AgentActivityWidget;
