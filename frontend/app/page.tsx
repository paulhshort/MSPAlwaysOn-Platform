'use client';

import { Card, Title, Text, Grid, Col, Flex, Metric, ProgressBar } from '@tremor/react';
import ClientSelector from './components/ClientSelector';
import AlertDashboard from './components/AlertDashboard';

export default function Home() {
  return (
    <div className="p-6">
      <Flex justifyContent="between" alignItems="center" className="mb-6">
        <div>
          <Title>MSPAlwaysOn Dashboard</Title>
          <Text>Unified AIOps and alert management platform for MSPs</Text>
        </div>
        <ClientSelector />
      </Flex>

      <Grid numItemsMd={2} numItemsLg={4} className="gap-6 mt-6">
        <Card decoration="top" decorationColor="red">
          <Text>Critical Alerts</Text>
          <Metric>5</Metric>
        </Card>

        <Card decoration="top" decorationColor="amber">
          <Text>Warning Alerts</Text>
          <Metric>12</Metric>
        </Card>

        <Card decoration="top" decorationColor="blue">
          <Text>Open Tickets</Text>
          <Metric>24</Metric>
        </Card>

        <Card decoration="top" decorationColor="emerald">
          <Text>Backup Success Rate</Text>
          <Metric>98.5%</Metric>
          <Flex className="mt-4">
            <Text>Last 24 hours</Text>
            <Text>98.5%</Text>
          </Flex>
          <ProgressBar value={98.5} color="emerald" className="mt-2" />
        </Card>
      </Grid>

      <div className="mt-6">
        <AlertDashboard />
      </div>

      <Grid numItemsMd={2} numItemsLg={3} className="gap-6 mt-6">
        <Card>
          <Title>Recent Tickets</Title>
          <Text>Coming soon</Text>
        </Card>

        <Card>
          <Title>Backup Status</Title>
          <Text>Coming soon</Text>
        </Card>

        <Card>
          <Title>Security Events</Title>
          <Text>Coming soon</Text>
        </Card>
      </Grid>
    </div>
  );
}
