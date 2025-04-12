'use client';

import React from 'react';
import Link from 'next/link';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface DataPoint {
  date: string;
  windows: number;
  linux: number;
  macos: number;
}

const PatchComplianceWidget: React.FC = () => {
  // Mock data - in a real implementation, this would be fetched from an API
  const data: DataPoint[] = [
    { date: 'Jan', windows: 85, linux: 92, macos: 88 },
    { date: 'Feb', windows: 83, linux: 90, macos: 87 },
    { date: 'Mar', windows: 87, linux: 93, macos: 90 },
    { date: 'Apr', windows: 90, linux: 95, macos: 92 },
    { date: 'May', windows: 88, linux: 94, macos: 91 },
    { date: 'Jun', windows: 92, linux: 96, macos: 93 },
  ];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="p-3 border rounded-md shadow-lg bg-slate-800 border-slate-700">
          <p className="mb-1 text-sm font-medium text-slate-300">{label}</p>
          {payload.map((entry: any, index: number) => (
            <div key={`item-${index}`} className="flex items-center">
              <div
                className="w-2 h-2 mr-2 rounded-full"
                style={{ backgroundColor: entry.color }}
              ></div>
              <p className="text-xs">
                <span className="text-slate-400">{entry.name}: </span>
                <span className="font-medium text-white">{entry.value}%</span>
              </p>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="overflow-hidden rounded-lg shadow-md bg-slate-900">
      <div className="px-4 py-3 border-b bg-slate-800 border-slate-700">
        <h3 className="text-lg font-medium text-white">Patch Compliance</h3>
      </div>
      <div className="p-4">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={data}
              margin={{ top: 5, right: 5, left: 0, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="date" tick={{ fill: '#94a3b8' }} />
              <YAxis domain={[60, 100]} tick={{ fill: '#94a3b8' }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ paddingTop: '10px' }}
                formatter={(value) => <span className="text-slate-300">{value}</span>}
              />
              <Line
                type="monotone"
                dataKey="windows"
                name="Windows"
                stroke="#06b6d4"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line
                type="monotone"
                dataKey="linux"
                name="Linux"
                stroke="#10b981"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
              <Line
                type="monotone"
                dataKey="macos"
                name="macOS"
                stroke="#f59e0b"
                strokeWidth={2}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        <div className="grid grid-cols-3 gap-2 mt-4">
          <div className="p-3 text-center rounded-md bg-slate-800">
            <div className="mb-1 text-xs text-slate-400">Windows</div>
            <div className="text-lg font-semibold text-cyan-400">92%</div>
            <div className="text-xs text-slate-500">+2% from last month</div>
          </div>
          <div className="p-3 text-center rounded-md bg-slate-800">
            <div className="mb-1 text-xs text-slate-400">Linux</div>
            <div className="text-lg font-semibold text-emerald-400">96%</div>
            <div className="text-xs text-slate-500">+1% from last month</div>
          </div>
          <div className="p-3 text-center rounded-md bg-slate-800">
            <div className="mb-1 text-xs text-slate-400">macOS</div>
            <div className="text-lg font-semibold text-amber-400">93%</div>
            <div className="text-xs text-slate-500">+1% from last month</div>
          </div>
        </div>
      </div>
      <div className="px-4 py-3 border-t bg-slate-800 border-slate-700">
        <Link
          href="/reports/patch-compliance"
          className="flex items-center justify-center text-sm text-cyan-400 hover:text-cyan-300"
        >
          View detailed report
          <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
        </Link>
      </div>
    </div>
  );
};

export default PatchComplianceWidget;
