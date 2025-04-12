'use client';

import React from 'react';
import Link from 'next/link';

interface Alert {
  id: string;
  severity: 'critical' | 'warning' | 'info';
  title: string;
  source: string;
  timestamp: string;
  client: string;
}

const AlertsWidget: React.FC = () => {
  // Mock data - in a real implementation, this would be fetched from an API
  const alerts: Alert[] = [
    {
      id: '1',
      severity: 'critical',
      title: 'Server offline',
      source: 'SentinelOne',
      timestamp: '2023-04-12T10:30:00Z',
      client: 'ACME Corp',
    },
    {
      id: '2',
      severity: 'warning',
      title: 'Backup failed',
      source: 'Veeam',
      timestamp: '2023-04-12T09:15:00Z',
      client: 'Globex Industries',
    },
    {
      id: '3',
      severity: 'critical',
      title: 'Ransomware detected',
      source: 'SentinelOne',
      timestamp: '2023-04-12T08:45:00Z',
      client: 'Initech',
    },
    {
      id: '4',
      severity: 'warning',
      title: 'High CPU usage',
      source: 'ConnectWise',
      timestamp: '2023-04-12T07:30:00Z',
      client: 'ACME Corp',
    },
    {
      id: '5',
      severity: 'info',
      title: 'User password expired',
      source: 'Azure AD',
      timestamp: '2023-04-12T06:15:00Z',
      client: 'Globex Industries',
    },
  ];

  const criticalCount = alerts.filter(alert => alert.severity === 'critical').length;
  const warningCount = alerts.filter(alert => alert.severity === 'warning').length;
  const infoCount = alerts.filter(alert => alert.severity === 'info').length;

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-rose-500';
      case 'warning':
        return 'bg-amber-500';
      case 'info':
        return 'bg-cyan-500';
      default:
        return 'bg-slate-500';
    }
  };

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="bg-slate-900 rounded-lg shadow-md overflow-hidden">
      <div className="px-4 py-3 bg-slate-800 border-b border-slate-700 flex items-center justify-between">
        <h3 className="text-lg font-medium text-white">Open Alerts</h3>
        <div className="flex space-x-2">
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-500 text-white">
            {criticalCount} Critical
          </span>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500 text-white">
            {warningCount} Warning
          </span>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-cyan-500 text-white">
            {infoCount} Info
          </span>
        </div>
      </div>
      <div className="divide-y divide-slate-700">
        {alerts.map((alert) => (
          <div key={alert.id} className="px-4 py-3 hover:bg-slate-800 transition-colors">
            <div className="flex items-start">
              <div className={`${getSeverityColor(alert.severity)} h-3 w-3 rounded-full mt-1.5 mr-3 flex-shrink-0`}></div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium text-white truncate">{alert.title}</p>
                  <p className="ml-2 text-xs text-slate-400">{formatTime(alert.timestamp)}</p>
                </div>
                <div className="mt-1 flex items-center">
                  <p className="text-xs text-slate-300">{alert.client}</p>
                  <span className="mx-1.5 text-slate-500">•</span>
                  <p className="text-xs text-slate-400">{alert.source}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="px-4 py-3 bg-slate-800 border-t border-slate-700">
        <Link
          href="/alerts"
          className="text-sm text-cyan-400 hover:text-cyan-300 flex items-center justify-center"
        >
          View all alerts
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  );
};

export default AlertsWidget;
