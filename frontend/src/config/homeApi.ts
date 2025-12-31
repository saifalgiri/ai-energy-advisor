
// Configure your FastAPI backend URL here
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const API_ENDPOINTS = {
  homes: `${API_BASE_URL}/homes`,
  home: (id: string) => `${API_BASE_URL}/homes/${id}`,
  advice: (id: string) => `${API_BASE_URL}/homes/${id}/advice`,
} as const;
