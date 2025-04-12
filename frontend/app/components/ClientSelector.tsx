import React, { useState, useEffect } from 'react';
import { Select, SelectItem } from '@tremor/react';
import { useClientStore } from '../lib/stores/clientStore';

interface ClientSelectorProps {
  onChange?: (clientId: string) => void;
}

export default function ClientSelector({ onChange }: ClientSelectorProps) {
  const { clients, selectedClientId, setSelectedClientId, fetchClients } = useClientStore();
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const loadClients = async () => {
      setIsLoading(true);
      try {
        await fetchClients();
      } catch (error) {
        console.error('Error loading clients:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadClients();
  }, [fetchClients]);

  const handleChange = (value: string) => {
    setSelectedClientId(value);
    if (onChange) {
      onChange(value);
    }
  };

  return (
    <div className="w-full max-w-xs">
      <Select
        value={selectedClientId}
        onValueChange={handleChange}
        placeholder="Select a client"
        disabled={isLoading}
      >
        <SelectItem value="all">All Clients</SelectItem>
        {clients.map((client) => (
          <SelectItem key={client.id} value={client.id.toString()}>
            {client.name}
          </SelectItem>
        ))}
      </Select>
    </div>
  );
}
