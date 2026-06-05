import { ModelType, ModelParams, GenerateResponse, AssemblyRequest } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';
const API_ORIGIN = API_BASE_URL.startsWith('http')
  ? new URL(API_BASE_URL).origin
  : window.location.origin;

async function handleResponseError(response: Response): Promise<GenerateResponse> {
  const errorData = await response.json().catch(() => null);
  let parsedError = errorData?.error || errorData?.detail?.error || errorData?.detail;

  if (Array.isArray(parsedError)) {
    parsedError = parsedError.map((err: any) => {
      const loc = err.loc ? err.loc.filter((l: string) => l !== 'body').join('.') : 'field';
      return `${loc}: ${err.msg}`;
    }).join(' | ');
  } else if (typeof parsedError === 'object' && parsedError !== null) {
    parsedError = JSON.stringify(parsedError);
  } else {
    parsedError = String(parsedError || `HTTP ${response.status}: ${response.statusText}`);
  }

  return {
    success: false,
    message: 'Validation Failed',
    error: parsedError,
  };
}

export const apiService = {
  /**
   * Generate a CAD file based on model type and parameters.
   * Calls the correct endpoint per model type:
   *   POST /api/{modelType}/generate
   */
  async generateCAD(
    modelType: ModelType,
    params: ModelParams,
  ): Promise<GenerateResponse> {
    try {
      const endpoint = `${API_BASE_URL}/${modelType}/generate`;

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(params),
      });

      if (!response.ok) {
        return handleResponseError(response);
      }

      const data: GenerateResponse = await response.json();
      return data;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Network error occurred';
      return {
        success: false,
        message: 'Failed to connect to the server',
        error: errorMessage,
      };
    }
  },

  async generateAssembly(request: AssemblyRequest): Promise<GenerateResponse> {
    try {
      const endpoint = `${API_BASE_URL}/assembly/generate`;
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      });

      if (!response.ok) return handleResponseError(response);
      return await response.json();
    } catch (error) {
      return {
        success: false,
        message: 'Failed to connect to the server',
        error: error instanceof Error ? error.message : 'Network error occurred',
      };
    }
  },

  async generateAssemblyFromConfig(file: File): Promise<GenerateResponse> {
    try {
      const endpoint = `${API_BASE_URL}/assembly/config`;
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) return handleResponseError(response);
      return await response.json();
    } catch (error) {
      return {
        success: false,
        message: 'Failed to connect to the server',
        error: error instanceof Error ? error.message : 'Network error occurred',
      };
    }
  },

  /**
   * Download a file from the provided URL
   */
  downloadFile(fileUrl: string, fileName: string = 'cad-model'): void {
    const resolvedUrl = fileUrl.startsWith('http')
      ? fileUrl
      : `${API_ORIGIN}${fileUrl.startsWith('/') ? fileUrl : `/${fileUrl}`}`;

    const link = document.createElement('a');
    link.href = resolvedUrl;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },
};
