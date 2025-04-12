'use client';

import React from 'react';
import ProtectedRoute from './components/ProtectedRoute';
import DashboardGrid from './components/dashboard/DashboardGrid';
import AlertsWidget from './components/dashboard/widgets/AlertsWidget';
import ClientHealthWidget from './components/dashboard/widgets/ClientHealthWidget';
import BackupCoverageWidget from './components/dashboard/widgets/BackupCoverageWidget';
import AgentActivityWidget from './components/dashboard/widgets/AgentActivityWidget';
import PatchComplianceWidget from './components/dashboard/widgets/PatchComplianceWidget';
import ToolInvocationWidget from './components/dashboard/widgets/ToolInvocationWidget';

export default function Home() {
  return (
    <ProtectedRoute>
      <div className="p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-semibold text-white">MSPAlwaysOn Dashboard</h1>
          <p className="text-slate-400">Unified AIOps and alert management platform for MSPs</p>
        </div>

        <DashboardGrid>
          <AlertsWidget />
          <ClientHealthWidget />
          <BackupCoverageWidget />
          <AgentActivityWidget />
          <PatchComplianceWidget />
          <ToolInvocationWidget />
        </DashboardGrid>
      </div>
    </ProtectedRoute>
  );
}
