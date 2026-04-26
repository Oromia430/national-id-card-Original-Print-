// API utility functions for backend communication

const API_BASE_URL = '/api';

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface ConvertResponse {
  success: boolean;
  data: {
    isValid: boolean;
    format?: string;
    extractedInfo?: {
      dateOfBirth?: string;
      gender?: string;
      placeOfIssue?: string;
      checksum?: string;
    };
    convertedFormats?: {
      [key: string]: string;
    };
  };
}

export interface ValidateResponse {
  success: boolean;
  isValid: boolean;
  format?: string;
  data: {
    isValid: boolean;
    format?: string;
    extractedInfo?: {
      dateOfBirth?: string;
      gender?: string;
      placeOfIssue?: string;
      checksum?: string;
    };
    convertedFormats?: {
      [key: string]: string;
    };
  };
}

export interface BatchResponse {
  success: boolean;
  total: number;
  successCount: number;
  failureCount: number;
  results: Array<{
    index: number;
    id: string;
    success: boolean;
    data?: any;
    error?: string;
  }>;
}

// Convert ID using API
export async function convertID(id: string): Promise<ConvertResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/convert`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to convert ID');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}

// Validate ID using API
export async function validateID(id: string, format?: 'egyptian' | 'saudi'): Promise<ValidateResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/validate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id, format }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to validate ID');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}

// Batch convert IDs
export async function batchConvert(ids: string[]): Promise<BatchResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ids }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to batch convert IDs');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}

// Convert format
export async function convertFormat(id: string, format: 'dashes' | 'spaces' | 'dots' | 'no-separator'): Promise<{ success: boolean; original: string; format: string; converted: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/formats`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id, format }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to convert format');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
}

// Health check
export async function healthCheck(): Promise<{ status: string; service: string; version: string; timestamp: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return await response.json();
  } catch (error) {
    throw error;
  }
}

