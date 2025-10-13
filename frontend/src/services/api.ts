// API Configuration
const API_BASE_URL = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_URL) 
  ? import.meta.env.VITE_API_URL 
  : 'http://localhost:8000/api';

// Types
export interface Report {
  id: string;
  incidentType: string;
  location: string;
  urgency: string;
  date: string;
  description: string;
  abuserInfo: string;
  status: string;
  submittedAt: string;
  verifiedAt?: string;
  notes?: string;
}

export interface SupportService {
  id: number;
  name: string;
  type: string;
  location: string;
  phone: string;
  services: string[];
  hours: string;
  verified: boolean;
}

export interface Testimonial {
  id: number;
  quote: string;
  location: string;
  type: string;
  year: string;
}

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}

// Generic fetch wrapper with error handling
async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw {
        message: errorData.message || `API Error: ${response.status}`,
        status: response.status,
        details: errorData,
      } as ApiError;
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      // Network error
      throw {
        message: 'Network error. Please check your connection and try again.',
        status: 0,
      } as ApiError;
    }
    throw error;
  }
}

// Report API
export const reportAPI = {
  // Create a new report
  create: async (reportData: Omit<Report, 'id' | 'status' | 'submittedAt'>): Promise<Report> => {
    return fetchAPI<Report>('/reports/', {
      method: 'POST',
      body: JSON.stringify(reportData),
    });
  },

  // Get all reports (for admin)
  list: async (): Promise<Report[]> => {
    return fetchAPI<Report[]>('/reports/');
  },

  // Get a single report
  get: async (id: string): Promise<Report> => {
    return fetchAPI<Report>(`/reports/${id}/`);
  },

  // Update report status
  updateStatus: async (
    id: string,
    status: string,
    notes?: string
  ): Promise<Report> => {
    return fetchAPI<Report>(`/reports/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify({ status, notes }),
    });
  },
};

// Support Services API
export const supportAPI = {
  // Get all support services
  list: async (search?: string): Promise<SupportService[]> => {
    const queryParams = search ? `?search=${encodeURIComponent(search)}` : '';
    return fetchAPI<SupportService[]>(`/support/${queryParams}`);
  },

  // Get a single support service
  get: async (id: number): Promise<SupportService> => {
    return fetchAPI<SupportService>(`/support/${id}/`);
  },
};

// Testimonials API
export const testimonialsAPI = {
  // Get all testimonials
  list: async (): Promise<Testimonial[]> => {
    return fetchAPI<Testimonial[]>('/testimonials/');
  },

  // Get a single testimonial
  get: async (id: number): Promise<Testimonial> => {
    return fetchAPI<Testimonial>(`/testimonials/${id}/`);
  },
};

// Export API base URL for reference
export { API_BASE_URL };
