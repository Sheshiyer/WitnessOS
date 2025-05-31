/**
 * Mock API Server for Testing
 * 
 * Provides mock responses for consciousness engine API testing
 * Used when the real Python API server is not available
 */

import type { 
  EngineAPIResponse, 
  EngineName, 
  NumerologyOutput,
  TarotOutput,
  IChingOutput,
  HumanDesignOutput,
  EnneagramOutput
} from '@/types';

// Mock delay to simulate network latency
const MOCK_DELAY = 500 + Math.random() * 1000; // 500-1500ms

// Mock success rate (90% success for testing)
const MOCK_SUCCESS_RATE = 0.9;

/**
 * Generate mock numerology response
 */
const generateMockNumerology = (input: any): NumerologyOutput => ({
  life_path_number: Math.floor(Math.random() * 9) + 1,
  expression_number: Math.floor(Math.random() * 9) + 1,
  soul_urge_number: Math.floor(Math.random() * 9) + 1,
  personality_number: Math.floor(Math.random() * 9) + 1,
  birth_day_number: Math.floor(Math.random() * 31) + 1,
  interpretation: {
    life_path: "Your life path suggests a journey of creative expression and leadership.",
    expression: "You express yourself through innovative thinking and artistic pursuits.",
    soul_urge: "Your soul yearns for harmony, beauty, and meaningful connections.",
    personality: "Others see you as charismatic, confident, and naturally inspiring.",
    overall_guidance: "Focus on balancing your creative ambitions with practical considerations."
  },
  sacred_geometry: {
    primary_shape: "pentagon",
    golden_ratio_connections: ["5-pointed star", "phi spiral"],
    frequency: 528,
    color_palette: ["#FFD700", "#FF6B6B", "#4ECDC4"]
  }
});

/**
 * Generate mock tarot response
 */
const generateMockTarot = (input: any): TarotOutput => ({
  spread_type: "three_card",
  cards: [
    {
      name: "The Fool",
      suit: "major_arcana",
      number: 0,
      position: "past",
      upright: true,
      meaning: "New beginnings, innocence, spontaneity",
      interpretation: "Your past shows a willingness to take risks and embrace new experiences."
    },
    {
      name: "The Magician",
      suit: "major_arcana", 
      number: 1,
      position: "present",
      upright: true,
      meaning: "Manifestation, resourcefulness, power",
      interpretation: "You currently have all the tools needed to manifest your desires."
    },
    {
      name: "The Star",
      suit: "major_arcana",
      number: 17,
      position: "future",
      upright: true,
      meaning: "Hope, faith, purpose, renewal",
      interpretation: "The future holds renewed hope and spiritual guidance."
    }
  ],
  overall_message: "This reading suggests a powerful journey from innocent beginnings through masterful manifestation toward spiritual fulfillment.",
  guidance: "Trust in your abilities and maintain hope for the future.",
  sacred_geometry: {
    pattern: "triangle",
    energy_flow: "ascending spiral",
    color_resonance: ["#4B0082", "#8A2BE2", "#9370DB"]
  }
});

/**
 * Generate mock I-Ching response
 */
const generateMockIChing = (input: any): IChingOutput => ({
  hexagram: {
    number: Math.floor(Math.random() * 64) + 1,
    name: "Thunder over Mountain",
    upper_trigram: "zhen",
    lower_trigram: "gen",
    lines: [true, false, true, true, false, true]
  },
  changing_lines: [false, true, false, false, true, false],
  future_hexagram: {
    number: Math.floor(Math.random() * 64) + 1,
    name: "Wind over Earth",
    upper_trigram: "xun",
    lower_trigram: "kun",
    lines: [true, true, false, false, false, false]
  },
  interpretation: {
    situation: "A time of dynamic change and transformation is upon you.",
    guidance: "Remain grounded while embracing the energy of change.",
    outcome: "Patience and persistence will lead to harmonious resolution."
  },
  oracle_text: "Thunder echoes through the mountain, awakening ancient wisdom.",
  sacred_geometry: {
    hexagram_geometry: "hexagonal crystal",
    transformation_pattern: "yin-yang spiral",
    elemental_balance: ["wood", "earth", "metal"]
  }
});

/**
 * Generate mock responses for other engines
 */
const generateMockResponse = (engineName: EngineName, input: any): any => {
  switch (engineName) {
    case 'numerology':
      return generateMockNumerology(input);
    case 'tarot':
      return generateMockTarot(input);
    case 'iching':
      return generateMockIChing(input);
    case 'human_design':
      return {
        type: "Manifestor",
        strategy: "Inform before acting",
        authority: "Emotional",
        profile: "1/3 Investigator/Martyr",
        centers: {
          defined: ["throat", "emotional"],
          undefined: ["sacral", "spleen", "heart", "head", "ajna", "g", "root"]
        }
      };
    case 'enneagram':
      return {
        type: Math.floor(Math.random() * 9) + 1,
        wing: Math.floor(Math.random() * 2) + 1,
        instinct: ["self-preservation", "social", "sexual"][Math.floor(Math.random() * 3)],
        level: Math.floor(Math.random() * 9) + 1,
        description: "The Reformer - principled, purposeful, self-controlled, and perfectionistic."
      };
    default:
      return {
        message: `Mock response for ${engineName}`,
        timestamp: new Date().toISOString(),
        test_data: true
      };
  }
};

/**
 * Mock API Client
 */
export class MockAPIServer {
  static async calculateEngine<TOutput>(
    engineName: EngineName,
    input: any
  ): Promise<EngineAPIResponse<TOutput>> {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, MOCK_DELAY));
    
    // Simulate occasional failures
    if (Math.random() > MOCK_SUCCESS_RATE) {
      return {
        success: false,
        error: `Mock API error for ${engineName}: Simulated network timeout`,
        timestamp: new Date().toISOString(),
        processingTime: MOCK_DELAY
      };
    }
    
    // Generate mock response
    const mockData = generateMockResponse(engineName, input);
    
    return {
      success: true,
      data: mockData as TOutput,
      timestamp: new Date().toISOString(),
      processingTime: MOCK_DELAY
    };
  }
  
  static async healthCheck(): Promise<EngineAPIResponse<{ status: string; engines: string[] }>> {
    await new Promise(resolve => setTimeout(resolve, 200));
    
    return {
      success: true,
      data: {
        status: "healthy",
        engines: [
          "numerology", "tarot", "iching", "human_design", "enneagram",
          "sacred_geometry", "biorhythm", "vimshottari", "gene_keys", "sigil_forge"
        ]
      },
      timestamp: new Date().toISOString(),
      processingTime: 200
    };
  }
  
  static async batchCalculate(
    requests: Array<{ engine: EngineName; input: any }>
  ): Promise<EngineAPIResponse<any[]>> {
    await new Promise(resolve => setTimeout(resolve, MOCK_DELAY * 2));
    
    const results = requests.map(req => generateMockResponse(req.engine, req.input));
    
    return {
      success: true,
      data: results,
      timestamp: new Date().toISOString(),
      processingTime: MOCK_DELAY * 2
    };
  }
}

export default MockAPIServer;
