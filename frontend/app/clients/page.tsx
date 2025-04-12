'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import ProtectedRoute from '../components/ProtectedRoute';

interface Client {
  id: string;
  name: string;
  logo?: string;
  industry?: string;
  size?: string;
  status: 'healthy' | 'degraded' | 'critical';
  healthScore: number;
  tags: string[];
  alerts: {
    critical: number;
    warning: number;
    info: number;
  };
  lastActivity: string;
}

export default function ClientsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [tagFilter, setTagFilter] = useState<string>('all');
  
  // Mock data - in a real implementation, this would be fetched from an API
  const clients: Client[] = [
    {
      id: '1',
      name: 'ACME Corporation',
      industry: 'Manufacturing',
      size: '50-100',
      status: 'healthy',
      healthScore: 92,
      tags: ['VIP', 'Manufacturing'],
      alerts: {
        critical: 0,
        warning: 2,
        info: 3,
      },
      lastActivity: '2023-04-12T10:30:00Z',
    },
    {
      id: '2',
      name: 'Globex Industries',
      industry: 'Technology',
      size: '100-250',
      status: 'degraded',
      healthScore: 78,
      tags: ['Technology', 'M365'],
      alerts: {
        critical: 1,
        warning: 3,
        info: 2,
      },
      lastActivity: '2023-04-12T09:15:00Z',
    },
    {
      id: '3',
      name: 'Initech',
      industry: 'Finance',
      size: '250-500',
      status: 'critical',
      healthScore: 45,
      tags: ['Finance', 'VIP', 'Compliance'],
      alerts: {
        critical: 3,
        warning: 5,
        info: 1,
      },
      lastActivity: '2023-04-12T08:45:00Z',
    },
    {
      id: '4',
      name: 'Umbrella Corporation',
      industry: 'Healthcare',
      size: '500+',
      status: 'healthy',
      healthScore: 88,
      tags: ['Healthcare', 'Compliance'],
      alerts: {
        critical: 0,
        warning: 1,
        info: 4,
      },
      lastActivity: '2023-04-12T07:30:00Z',
    },
    {
      id: '5',
      name: 'Stark Industries',
      industry: 'Technology',
      size: '100-250',
      status: 'degraded',
      healthScore: 65,
      tags: ['Technology', 'Manufacturing'],
      alerts: {
        critical: 2,
        warning: 2,
        info: 3,
      },
      lastActivity: '2023-04-12T06:15:00Z',
    },
  ];
  
  // Get unique tags for filter
  const allTags = Array.from(new Set(clients.flatMap(client => client.tags)));
  
  // Filter clients based on search query and filters
  const filteredClients = clients.filter(client => {
    // Search filter
    const matchesSearch = searchQuery === '' || 
      client.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      client.industry?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      client.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    
    // Status filter
    const matchesStatus = statusFilter === 'all' || client.status === statusFilter;
    
    // Tag filter
    const matchesTag = tagFilter === 'all' || client.tags.includes(tagFilter);
    
    return matchesSearch && matchesStatus && matchesTag;
  });
  
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
  
  const getStatusText = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'Healthy';
      case 'degraded':
        return 'Degraded';
      case 'critical':
        return 'Critical';
      default:
        return status;
    }
  };
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };
  
  return (
    <ProtectedRoute>
      <div className="p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-white">Clients</h1>
          <p className="text-slate-400">Manage and monitor your clients</p>
        </div>
        
        {/* Filters */}
        <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-slate-400 mb-1">Search</label>
            <input
              type="text"
              id="search"
              className="w-full bg-slate-800 border border-slate-700 rounded-md py-2 px-3 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
              placeholder="Search clients..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          
          <div>
            <label htmlFor="status-filter" className="block text-sm font-medium text-slate-400 mb-1">Status</label>
            <select
              id="status-filter"
              className="w-full bg-slate-800 border border-slate-700 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="all">All Statuses</option>
              <option value="healthy">Healthy</option>
              <option value="degraded">Degraded</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          
          <div>
            <label htmlFor="tag-filter" className="block text-sm font-medium text-slate-400 mb-1">Tag</label>
            <select
              id="tag-filter"
              className="w-full bg-slate-800 border border-slate-700 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
              value={tagFilter}
              onChange={(e) => setTagFilter(e.target.value)}
            >
              <option value="all">All Tags</option>
              {allTags.map(tag => (
                <option key={tag} value={tag}>{tag}</option>
              ))}
            </select>
          </div>
        </div>
        
        {/* Client Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredClients.map(client => (
            <Link 
              key={client.id} 
              href={`/clients/${client.id}`}
              className="bg-slate-900 border border-slate-700 rounded-lg overflow-hidden hover:border-cyan-500 transition-colors"
            >
              <div className="p-4">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center">
                    <div className="h-10 w-10 rounded-md bg-slate-700 flex items-center justify-center text-white font-semibold mr-3">
                      {client.name.charAt(0)}
                    </div>
                    <div>
                      <h3 className="text-lg font-medium text-white">{client.name}</h3>
                      <p className="text-sm text-slate-400">{client.industry} • {client.size} employees</p>
                    </div>
                  </div>
                  <div className={`${getStatusColor(client.status)} h-3 w-3 rounded-full mt-1`}></div>
                </div>
                
                <div className="mb-3">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-slate-400">Health Score</span>
                    <span className="text-sm font-medium text-white">{client.healthScore}%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
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
                </div>
                
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center">
                    <span className="text-sm text-slate-400 mr-2">Status:</span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      client.status === 'healthy' ? 'bg-emerald-900 text-emerald-300' :
                      client.status === 'degraded' ? 'bg-amber-900 text-amber-300' :
                      'bg-rose-900 text-rose-300'
                    }`}>
                      {getStatusText(client.status)}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    {client.alerts.critical > 0 && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-rose-900 text-rose-300">
                        {client.alerts.critical} Critical
                      </span>
                    )}
                    {client.alerts.warning > 0 && (
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-amber-900 text-amber-300">
                        {client.alerts.warning} Warning
                      </span>
                    )}
                  </div>
                </div>
                
                <div className="flex flex-wrap gap-2 mb-3">
                  {client.tags.map(tag => (
                    <span key={tag} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-700 text-slate-300">
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="text-xs text-slate-500">
                  Last activity: {formatDate(client.lastActivity)}
                </div>
              </div>
            </Link>
          ))}
        </div>
        
        {filteredClients.length === 0 && (
          <div className="bg-slate-900 border border-slate-700 rounded-lg p-8 text-center">
            <p className="text-slate-400">No clients found matching your filters.</p>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
