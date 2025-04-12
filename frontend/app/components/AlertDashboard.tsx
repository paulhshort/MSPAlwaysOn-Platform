import React, { useState, useEffect } from 'react';
import { Card, Title, Text, Grid, Col, Badge, Flex, Button, Table, TableHead, TableHeaderCell, TableBody, TableRow, TableCell } from '@tremor/react';
import { useClientStore } from '../lib/stores/clientStore';
import axios from 'axios';

interface Alert {
  id: string;
  name: string;
  description: string;
  source: string;
  severity: 'critical' | 'warning' | 'info';
  status: 'firing' | 'resolved';
  lastReceived: string;
  labels: Record<string, string>;
}

export default function AlertDashboard() {
  const { selectedClientId } = useClientStore();
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const params = selectedClientId !== 'all' 
          ? { client_id: selectedClientId } 
          : {};
        
        const response = await axios.get('/api/v1/keep/alerts', { params });
        setAlerts(response.data);
      } catch (error) {
        console.error('Error fetching alerts:', error);
        setError(error instanceof Error ? error.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAlerts();
  }, [selectedClientId]);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'rose';
      case 'warning':
        return 'amber';
      case 'info':
        return 'blue';
      default:
        return 'gray';
    }
  };

  const getStatusColor = (status: string) => {
    return status === 'firing' ? 'rose' : 'emerald';
  };

  return (
    <Card>
      <Flex justifyContent="between" alignItems="center">
        <Title>Active Alerts</Title>
        <Button size="xs" variant="secondary" onClick={() => window.location.reload()}>
          Refresh
        </Button>
      </Flex>
      
      {isLoading ? (
        <Text>Loading alerts...</Text>
      ) : error ? (
        <Text color="rose">{error}</Text>
      ) : (
        <Table className="mt-4">
          <TableHead>
            <TableRow>
              <TableHeaderCell>Severity</TableHeaderCell>
              <TableHeaderCell>Alert</TableHeaderCell>
              <TableHeaderCell>Source</TableHeaderCell>
              <TableHeaderCell>Status</TableHeaderCell>
              <TableHeaderCell>Client</TableHeaderCell>
              <TableHeaderCell>Last Received</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {alerts.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6}>
                  <Text className="text-center">No alerts found</Text>
                </TableCell>
              </TableRow>
            ) : (
              alerts.map((alert) => (
                <TableRow key={alert.id}>
                  <TableCell>
                    <Badge color={getSeverityColor(alert.severity)}>
                      {alert.severity.toUpperCase()}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Text>{alert.name}</Text>
                    <Text className="text-xs text-gray-500">{alert.description.substring(0, 100)}{alert.description.length > 100 ? '...' : ''}</Text>
                  </TableCell>
                  <TableCell>{alert.source}</TableCell>
                  <TableCell>
                    <Badge color={getStatusColor(alert.status)}>
                      {alert.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{alert.labels.company || 'N/A'}</TableCell>
                  <TableCell>{new Date(alert.lastReceived).toLocaleString()}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      )}
    </Card>
  );
}
