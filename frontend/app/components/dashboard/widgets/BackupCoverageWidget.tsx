'use client';

import React from 'react';
import Link from 'next/link';

interface BackupDay {
  date: string;
  status: 'success' | 'partial' | 'failed' | 'none';
  successCount?: number;
  totalCount?: number;
}

const BackupCoverageWidget: React.FC = () => {
  // Generate the last 14 days for the heatmap
  const generateDays = (): BackupDay[] => {
    const days: BackupDay[] = [];
    const today = new Date();
    
    for (let i = 13; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      
      // Generate random status for demo
      const rand = Math.random();
      let status: 'success' | 'partial' | 'failed' | 'none';
      let successCount: number;
      const totalCount = 10;
      
      if (rand > 0.8) {
        status = 'partial';
        successCount = Math.floor(Math.random() * 5) + 5; // 5-9
      } else if (rand > 0.95) {
        status = 'failed';
        successCount = Math.floor(Math.random() * 5); // 0-4
      } else if (rand > 0.98) {
        status = 'none';
        successCount = 0;
      } else {
        status = 'success';
        successCount = 10;
      }
      
      days.push({
        date: date.toISOString().split('T')[0],
        status,
        successCount,
        totalCount
      });
    }
    
    return days;
  };
  
  const days = generateDays();
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'bg-emerald-500';
      case 'partial':
        return 'bg-amber-500';
      case 'failed':
        return 'bg-rose-500';
      case 'none':
      default:
        return 'bg-slate-700';
    }
  };
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };
  
  const getDayOfWeek = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
  };

  return (
    <div className="bg-slate-900 rounded-lg shadow-md overflow-hidden">
      <div className="px-4 py-3 bg-slate-800 border-b border-slate-700">
        <h3 className="text-lg font-medium text-white">Backup Coverage</h3>
      </div>
      <div className="p-4">
        <div className="grid grid-cols-7 gap-2">
          {days.map((day, index) => (
            <div key={day.date} className="flex flex-col items-center">
              <div className="text-xs text-slate-400 mb-1">{index % 2 === 0 ? formatDate(day.date) : ''}</div>
              <div 
                className={`w-full aspect-square rounded-md ${getStatusColor(day.status)} relative group`}
                title={`${formatDate(day.date)}: ${day.successCount}/${day.totalCount} successful backups`}
              >
                <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-slate-900 bg-opacity-80 rounded-md">
                  <span className="text-xs font-medium text-white">{day.successCount}/{day.totalCount}</span>
                </div>
              </div>
              <div className="text-xs text-slate-500 mt-1">{getDayOfWeek(day.date)}</div>
            </div>
          ))}
        </div>
        
        <div className="mt-4 flex items-center justify-center space-x-4">
          <div className="flex items-center">
            <div className="h-3 w-3 rounded-sm bg-emerald-500 mr-1"></div>
            <span className="text-xs text-slate-400">Success</span>
          </div>
          <div className="flex items-center">
            <div className="h-3 w-3 rounded-sm bg-amber-500 mr-1"></div>
            <span className="text-xs text-slate-400">Partial</span>
          </div>
          <div className="flex items-center">
            <div className="h-3 w-3 rounded-sm bg-rose-500 mr-1"></div>
            <span className="text-xs text-slate-400">Failed</span>
          </div>
          <div className="flex items-center">
            <div className="h-3 w-3 rounded-sm bg-slate-700 mr-1"></div>
            <span className="text-xs text-slate-400">No Data</span>
          </div>
        </div>
      </div>
      <div className="px-4 py-3 bg-slate-800 border-t border-slate-700">
        <Link
          href="/reports/backups"
          className="text-sm text-cyan-400 hover:text-cyan-300 flex items-center justify-center"
        >
          View backup report
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  );
};

export default BackupCoverageWidget;
