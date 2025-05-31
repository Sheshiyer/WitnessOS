/**
 * WitnessOS API Client for Python Engine Integration
 * 
 * Connects React Three Fiber frontend to Python consciousness engines
 * Handles data transformation and error management
 */

import type { 
  EngineAPIResponse, 
  EngineName, 
  EngineInput, 
  EngineOutput,
  NumerologyInput,
  NumerologyOutput,
  HumanDesignInput,
  HumanDesignOutput,
  TarotInput,
  TarotOutput,
  IChingInput,
  IChingOutput,
  EnneagramInput,
  EnneagramOutput
} from '@/types';

// API Configuration
const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_WITNESSOS_API_URL || 'http://localhost:8000',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
} as const;

// API Endpoints mapping
const API_ENDPOINTS: Record<EngineName, string> = {
  numerology: '/api/engines/numerology',
  human_design: '/api/engines/human-design',
  tarot: '/api/engines/tarot',
  iching: '/api/engines/iching',
  enneagram: '/api/engines/enneagram',
  sacred_geometry: '/api/engines/sacred-geometry',
  biorhythm: '/api/engines/biorhythm',
  vimshottari: '/api/engines/vimshottari',
  gene_keys: '/api/engines/gene-keys',
  sigil_forge: '/api/engines/sigil-forge',
};

/**
 * Custom error class for API operations
 */
export class WitnessOSAPIError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public engine?: string,
    public originalError?: unknown
  ) {
    super(message);
    this.name = 'WitnessOSAPIError';
  }
}

/**
 * Retry utility with exponential backoff
 */
async function withRetry<T>(
  operation: () => Promise<T>,
  attempts: number = API_CONFIG.RETRY_ATTEMPTS,
  delay: number = API_CONFIG.RETRY_DELAY
): Promise<T> {
  try {
    return await operation();
  } catch (error) {
    if (attempts <= 1) {
      throw error;
    }
    
    await new Promise(resolve => setTimeout(resolve, delay));
    return withRetry(operation, attempts - 1, delay * 2);
  }
}

/**
 * Generic API request function
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<EngineAPIResponse<T>> {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`;
  const startTime = Date.now();
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    const processingTime = Date.now() - startTime;
    
    if (!response.ok) {
      throw new WitnessOSAPIError(
        `API request failed: ${response.status} ${response.statusText}`,
        response.status
      );
    }
    
    const data = await response.json();
    
    return {
      success: true,
      data,
      timestamp: new Date().toISOString(),
      processingTime,
    };
  } catch (error) {
    const processingTime = Date.now() - startTime;
    
    if (error instanceof WitnessOSAPIError) {
      throw error;
    }
    
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error occurred',
      timestamp: new Date().toISOString(),
      processingTime,
    };
  }
}

/**
 * Main API client class
 */
export class WitnessOSAPIClient {
  /**
   * Generic engine calculation method
   */
  static async calculateEngine<TInput extends EngineInput, TOutput extends EngineOutput>(
    engineName: EngineName,
    input: TInput
  ): Promise<EngineAPIResponse<TOutput>> {
    const endpoint = API_ENDPOINTS[engineName];
    
    if (!endpoint) {
      throw new WitnessOSAPIError(`Unknown engine: ${engineName}`, undefined, engineName);
    }

    return withRetry(async () => {
      return apiRequest<TOutput>(endpoint, {
        method: 'POST',
        body: JSON.stringify(input),
      });
    });
  }

  /**
   * Numerology calculation
   */
  static async calculateNumerology(input: NumerologyInput): Promise<EngineAPIResponse<NumerologyOutput>> {
    return this.calculateEngine<NumerologyInput, NumerologyOutput>('numerology', input);
  }

  /**
   * Human Design calculation
   */
  static async calculateHumanDesign(input: HumanDesignInput): Promise<EngineAPIResponse<HumanDesignOutput>> {
    return this.calculateEngine<HumanDesignInput, HumanDesignOutput>('human_design', input);
  }

  /**
   * Tarot reading
   */
  static async calculateTarot(input: TarotInput): Promise<EngineAPIResponse<TarotOutput>> {
    return this.calculateEngine<TarotInput, TarotOutput>('tarot', input);
  }

  /**
   * I-Ching consultation
   */
  static async calculateIChing(input: IChingInput): Promise<EngineAPIResponse<IChingOutput>> {
    return this.calculateEngine<IChingInput, IChingOutput>('iching', input);
  }

  /**
   * Enneagram assessment
   */
  static async calculateEnneagram(input: EnneagramInput): Promise<EngineAPIResponse<EnneagramOutput>> {
    return this.calculateEngine<EnneagramInput, EnneagramOutput>('enneagram', input);
  }

  /**
   * Health check for API connectivity
   */
  static async healthCheck(): Promise<EngineAPIResponse<{ status: string; engines: string[] }>> {
    return withRetry(async () => {
      return apiRequest<{ status: string; engines: string[] }>('/api/health');
    });
  }

  /**
   * Get available engines
   */
  static async getAvailableEngines(): Promise<EngineAPIResponse<{ engines: EngineName[] }>> {
    return withRetry(async () => {
      return apiRequest<{ engines: EngineName[] }>('/api/engines');
    });
  }

  /**
   * Batch calculation for multiple engines
   */
  static async batchCalculate(
    requests: Array<{ engine: EngineName; input: EngineInput }>
  ): Promise<EngineAPIResponse<EngineOutput[]>> {
    return withRetry(async () => {
      return apiRequest<EngineOutput[]>('/api/engines/batch', {
        method: 'POST',
        body: JSON.stringify({ requests }),
      });
    });
  }
}

/**
 * Data transformation utilities for Python ↔ TypeScript
 */
export class DataTransformer {
  /**
   * Transform Python snake_case to TypeScript camelCase
   */
  static pythonToTypeScript<T>(data: Record<string, unknown>): T {
    const transformed: Record<string, unknown> = {};
    
    for (const [key, value] of Object.entries(data)) {
      const camelKey = key.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
      
      if (value && typeof value === 'object' && !Array.isArray(value)) {
        transformed[camelKey] = this.pythonToTypeScript(value as Record<string, unknown>);
      } else if (Array.isArray(value)) {
        transformed[camelKey] = value.map(item => 
          item && typeof item === 'object' ? this.pythonToTypeScript(item as Record<string, unknown>) : item
        );
      } else {
        transformed[camelKey] = value;
      }
    }
    
    return transformed as T;
  }

  /**
   * Transform TypeScript camelCase to Python snake_case
   */
  static typeScriptToPython<T>(data: Record<string, unknown>): T {
    const transformed: Record<string, unknown> = {};
    
    for (const [key, value] of Object.entries(data)) {
      const snakeKey = key.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`);
      
      if (value && typeof value === 'object' && !Array.isArray(value)) {
        transformed[snakeKey] = this.typeScriptToPython(value as Record<string, unknown>);
      } else if (Array.isArray(value)) {
        transformed[snakeKey] = value.map(item => 
          item && typeof item === 'object' ? this.typeScriptToPython(item as Record<string, unknown>) : item
        );
      } else {
        transformed[snakeKey] = value;
      }
    }
    
    return transformed as T;
  }

  /**
   * Validate engine input data
   */
  static validateEngineInput(engineName: EngineName, input: EngineInput): boolean {
    // Basic validation - can be extended with more specific rules
    if (!input || typeof input !== 'object') {
      return false;
    }

    // Engine-specific validation
    switch (engineName) {
      case 'numerology':
        return 'fullName' in input && 'birthDate' in input;
      case 'human_design':
        return 'birthDate' in input && 'birthTime' in input && 'birthLocation' in input;
      case 'tarot':
        return 'question' in input && 'spread' in input;
      case 'iching':
        return 'question' in input;
      case 'enneagram':
        return 'responses' in input;
      default:
        return true; // Allow other engines for now
    }
  }
}

// Export singleton instance
export const witnessOSAPI = WitnessOSAPIClient;

// Export utility functions
export { API_CONFIG, API_ENDPOINTS };
