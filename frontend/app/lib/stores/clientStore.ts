import { create } from 'zustand';
import axios from 'axios';

export interface Client {
  id: number;
  name: string;
  external_id?: string;
  external_system?: string;
  is_active: boolean;
}

interface ClientState {
  clients: Client[];
  selectedClientId: string;
  isLoading: boolean;
  error: string | null;
  fetchClients: () => Promise<void>;
  setSelectedClientId: (clientId: string) => void;
}

export const useClientStore = create<ClientState>((set, get) => ({
  clients: [],
  selectedClientId: 'all',
  isLoading: false,
  error: null,
  
  fetchClients: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get('/api/v1/msp/clients');
      set({ clients: response.data, isLoading: false });
    } catch (error) {
      console.error('Error fetching clients:', error);
      set({ 
        error: error instanceof Error ? error.message : 'An error occurred', 
        isLoading: false 
      });
    }
  },
  
  setSelectedClientId: (clientId: string) => {
    set({ selectedClientId: clientId });
  }
}));
