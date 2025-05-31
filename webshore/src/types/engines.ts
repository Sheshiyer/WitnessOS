/**
 * Engine-Specific Types for WitnessOS Webshore
 *
 * TypeScript interfaces for all 10 consciousness engines
 * Based on Python data models from WitnessOS engine implementations
 */

import { BaseEngineInput, BaseEngineOutput, BirthData, PersonalData, QuestionInput } from './consciousness';

// ===== NUMEROLOGY ENGINE =====
export interface NumerologyInput extends BaseEngineInput, PersonalData {
  system: 'pythagorean' | 'chaldean';
  currentYear?: number;
}

export interface NumerologyOutput extends BaseEngineOutput {
  lifePath: number;
  expression: number;
  soulUrge: number;
  personality: number;
  maturity: number;
  personalYear: number;
  lifeExpressionBridge: number;
  soulPersonalityBridge: number;
  masterNumbers: number[];
  karmicDebt: number[];
  numerologySystem: string;
  calculationYear: number;
  nameBreakdown: Record<string, unknown>;
  coreMeanings: Record<string, string>;
  yearlyGuidance: string;
  lifePurpose: string;
  compatibilityNotes: string[];
  favorablePeriods: string[];
  challengePeriods: string[];
}

// ===== HUMAN DESIGN ENGINE =====
export interface HumanDesignInput extends BaseEngineInput, BirthData {
  includeDesignCalculation: boolean;
  detailedGates: boolean;
}

export interface HumanDesignGate {
  number: number;
  name: string;
  line: number;
  planet: string;
  activation: 'personality' | 'design';
  description: string;
  keywords: string[];
}

export interface HumanDesignCenter {
  name: string;
  defined: boolean;
  gates: number[];
  function: string;
  whenDefined: string;
  whenUndefined: string;
}

export interface HumanDesignProfile {
  personalityLine: number;
  designLine: number;
  profileName: string;
  description: string;
  lifeTheme: string;
  role: string;
}

export interface HumanDesignType {
  typeName: 'Generator' | 'Projector' | 'Manifestor' | 'Reflector';
  strategy: string;
  authority: string;
  signature: string;
  notSelf: string;
  percentage: number;
  description: string;
  lifePurpose: string;
}

export interface HumanDesignChart {
  typeInfo: HumanDesignType;
  profile: HumanDesignProfile;
  personalityGates: Record<string, HumanDesignGate>;
  designGates: Record<string, HumanDesignGate>;
  centers: Record<string, HumanDesignCenter>;
  definedChannels: string[];
  definitionType: string;
}

export interface HumanDesignOutput extends BaseEngineOutput {
  chart: HumanDesignChart;
  incarnationCross: string;
  variables: Record<string, unknown>;
  bodyGraph: Record<string, unknown>;
}

// ===== TAROT ENGINE =====
export interface TarotInput extends BaseEngineInput, QuestionInput {
  spread: string;
  deckType: string;
  shuffleMethod: string;
}

export interface TarotCard {
  name: string;
  suit?: string;
  number?: number;
  arcana: 'major' | 'minor';
  upright: boolean;
  keywords: string[];
  meaning: string;
  reversedMeaning?: string;
  imagery: string;
  symbolism: string[];
}

export interface DrawnCard {
  card: TarotCard;
  position: string;
  positionMeaning: string;
  interpretation: string;
}

export interface SpreadLayout {
  name: string;
  positions: string[];
  description: string;
  focus: string;
}

export interface TarotOutput extends BaseEngineOutput {
  spread: SpreadLayout;
  drawnCards: DrawnCard[];
  overallTheme: string;
  pastInfluences: string;
  presentSituation: string;
  futureOutlook: string;
  advice: string;
  outcome: string;
}

// ===== I-CHING ENGINE =====
export interface IChingInput extends BaseEngineInput, QuestionInput {
  method: 'coins' | 'yarrow' | 'random';
  includeChangingLines: boolean;
}

export interface Trigram {
  name: string;
  symbol: string;
  element: string;
  attribute: string;
  family: string;
  direction: string;
}

export interface HexagramLine {
  position: number;
  type: 'yin' | 'yang' | 'changing_yin' | 'changing_yang';
  meaning: string;
}

export interface Hexagram {
  number: number;
  name: string;
  chineseName: string;
  upperTrigram: Trigram;
  lowerTrigram: Trigram;
  lines: HexagramLine[];
  judgment: string;
  image: string;
  meaning: string;
  advice: string;
}

export interface IChingReading {
  primaryHexagram: Hexagram;
  relatingHexagram?: Hexagram;
  changingLines: number[];
  interpretation: string;
}

export interface IChingOutput extends BaseEngineOutput {
  reading: IChingReading;
  divination: string;
  guidance: string;
  timing: string;
  action: string;
}

// ===== ENNEAGRAM ENGINE =====
export interface EnneagramInput extends BaseEngineInput {
  responses: Record<string, number>; // question_id -> response_value
  includeWings: boolean;
  includeInstincts: boolean;
}

export interface EnneagramWing {
  type: number;
  influence: number; // 0.0 - 1.0
  description: string;
}

export interface EnneagramArrow {
  direction: 'integration' | 'disintegration';
  targetType: number;
  description: string;
  conditions: string;
}

export interface InstinctualVariant {
  primary: 'self_preservation' | 'social' | 'sexual';
  secondary?: 'self_preservation' | 'social' | 'sexual';
  stacking: string;
  description: string;
}

export interface EnneagramType {
  number: number;
  name: string;
  description: string;
  coreMotivation: string;
  coreFear: string;
  coreDesire: string;
  keyMotivations: string[];
  basicFear: string;
  basicDesire: string;
  healthyLevels: string[];
  averageLevels: string[];
  unhealthyLevels: string[];
}

export interface EnneagramProfile {
  primaryType: EnneagramType;
  wings: EnneagramWing[];
  arrows: EnneagramArrow[];
  instinctualVariant: InstinctualVariant;
  center: 'body' | 'heart' | 'head';
  healthLevel: number; // 1-9
}

export interface EnneagramOutput extends BaseEngineOutput {
  profile: EnneagramProfile;
  typeScores: Record<number, number>;
  development: string;
  relationships: string;
  workStyle: string;
  stressResponse: string;
  growthPath: string;
}

// Engine union types for generic handling
export type EngineInput = NumerologyInput | HumanDesignInput | TarotInput | IChingInput | EnneagramInput;

export type EngineOutput = NumerologyOutput | HumanDesignOutput | TarotOutput | IChingOutput | EnneagramOutput;

export type EngineName =
  | 'numerology'
  | 'human_design'
  | 'tarot'
  | 'iching'
  | 'enneagram'
  | 'sacred_geometry'
  | 'biorhythm'
  | 'vimshottari'
  | 'gene_keys'
  | 'sigil_forge';

// Export all types - removed to avoid conflicts, using individual exports above
