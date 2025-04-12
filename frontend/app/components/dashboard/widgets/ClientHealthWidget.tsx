'use client';

import React from 'react';
import Link from 'next/link';

interface Client {
  id: string;
  name: string;
  healthScore: number;
  status: 'healthy' | 'degraded' | 'critical';
  lastIssue?: string;
}

const ClientHealthWidget: React.FC = () => {
  // Mock data - in a real implementation, this would be fetched from an API
  const clients: Client[] = [
    {
      id: '1',
      name: 'ACME Corp',
      healthScore: 92,
      status: 'healthy',
    },
    {
      id: '2',
      name: 'Globex Industries',
      healthScore: 78,
      status: 'degraded',
      lastIssue: 'Backup failure',
    },
    {
      id: '3',
      name: 'Initech',
      healthScore: 45,
      status: 'critical',
      lastIssue: 'Security breach',
    },
    {
      id: '4',
      name: 'Umbrella Corporation',
      healthScore: 88,
      status: 'healthy',
    },
    {
      id: '5',
      name: 'Stark Industries',
      healthScore: 65,
      status: 'degraded',
      lastIssue: 'High CPU usage',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-emerald-500';
      case 'degraded':
        return 'bg-amber-500';
      case 'critical':
        return 'bg-rose-500';
      default:
        return 'bg-slate-500';
    }
  };

  const getStatusTextColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-emerald-500';
      case 'degraded':
        return 'text-amber-500';
      case 'critical':
        return 'text-rose-500';
      default:
        return 'text-slate-500';
    }
  };

  return (
    <div className="bg-slate-900 rounded-lg shadow-md overflow-hidden">
      <div className="px-4 py-3 bg-slate-800 border-b border-slate-700">
        <h3 className="text-lg font-medium text-white">Client Health Summary</h3>
      </div>
      <div className="divide-y divide-slate-700">
        {clients.map((client) => (
          <div key={client.id} className="px-4 py-3 hover:bg-slate-800 transition-colors">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className={`${getStatusColor(client.status)} h-3 w-3 rounded-full mr-3`}></div>
                <Link href={`/clients/${client.id}`} className="text-sm font-medium text-white hover:text-cyan-400">
                  {client.name}
                </Link>
              </div>
              <div className="flex items-center">
                <div className="w-12 bg-slate-700 rounded-full h-2 mr-2">
                  <div
                    className={`h-2 rounded-full ${
                      client.healthScore >= 80
                        ? 'bg-emerald-500'
                        : client.healthScore >= 60
                        ? 'bg-amber-500'
                        : 'bg-rose-500'
                    }`}
                    style={{ width: `${client.healthScore}%` }}
                  ></div>
                </div>
                <span className="text-xs font-medium text-slate-300">{client.healthScore}%</span>
              </div>
            </div>
            {client.lastIssue && (
              <div className="mt-1 ml-6">
                <p className={`text-xs ${getStatusTextColor(client.status)}`}>{client.lastIssue}</p>
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="px-4 py-3 bg-slate-800 border-t border-slate-700">
        <Link
          href="/clients"
          className="text-sm text-cyan-400 hover:text-cyan-300 flex items-center justify-center"
        >
          View all clients
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  );
};

export default ClientHealthWidget;
