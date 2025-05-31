/**
 * Integrated Consciousness Onboarding - Seamless Flow Experience
 *
 * Features:
 * - Integrated design matching boot sequence aesthetic
 * - Direction-first user journey (compass selection first)
 * - No popup modals - full-screen immersive experience
 * - Smooth transitions with GSAP animations
 * - Sacred geometry and consciousness theming throughout
 */

'use client';

import { gsap } from 'gsap';
import React, { useEffect, useRef, useState } from 'react';
import { type ConsciousnessProfile } from './ConsciousnessDataCollector';
import {
  BirthDateStoryStep,
  BirthLocationStoryStep,
  BirthTimeStoryStep,
  ConfirmationStep,
  NameStoryStep,
} from './OnboardingSteps';

interface IntegratedConsciousnessOnboardingProps {
  onProfileComplete: (profile: ConsciousnessProfile) => void;
  onStepChange?: (step: number, total: number) => void;
}

type OnboardingStep =
  | 'direction_selection'
  | 'name_story'
  | 'birth_date_story'
  | 'birth_time_story'
  | 'birth_location_story'
  | 'confirmation';

interface ArchetypalDirection {
  id: string;
  name: string;
  symbol: string;
  description: string;
  color: string;
  gradient: string;
  keywords: string[];
}

const ARCHETYPAL_DIRECTIONS: ArchetypalDirection[] = [
  {
    id: 'north',
    name: 'The Sage',
    symbol: '🔮',
    description: 'Wisdom, knowledge, and spiritual insight guide your path',
    color: 'text-blue-300',
    gradient: 'from-blue-600 to-indigo-800',
    keywords: ['Wisdom', 'Knowledge', 'Insight', 'Truth'],
  },
  {
    id: 'northeast',
    name: 'The Mystic',
    symbol: '✨',
    description: 'Intuition and mystical understanding illuminate your journey',
    color: 'text-purple-300',
    gradient: 'from-purple-600 to-violet-800',
    keywords: ['Intuition', 'Mystery', 'Magic', 'Vision'],
  },
  {
    id: 'east',
    name: 'The Creator',
    symbol: '🎨',
    description: 'Innovation and creative expression flow through you',
    color: 'text-yellow-300',
    gradient: 'from-yellow-600 to-orange-800',
    keywords: ['Creation', 'Innovation', 'Art', 'Expression'],
  },
  {
    id: 'southeast',
    name: 'The Healer',
    symbol: '🌿',
    description: 'Compassion and healing energy radiate from your being',
    color: 'text-green-300',
    gradient: 'from-green-600 to-emerald-800',
    keywords: ['Healing', 'Compassion', 'Growth', 'Nurturing'],
  },
  {
    id: 'south',
    name: 'The Warrior',
    symbol: '⚔️',
    description: 'Courage and determination drive your actions',
    color: 'text-red-300',
    gradient: 'from-red-600 to-rose-800',
    keywords: ['Courage', 'Strength', 'Action', 'Protection'],
  },
  {
    id: 'southwest',
    name: 'The Guardian',
    symbol: '🛡️',
    description: 'Protection and stability anchor your presence',
    color: 'text-amber-300',
    gradient: 'from-amber-600 to-yellow-800',
    keywords: ['Protection', 'Stability', 'Security', 'Foundation'],
  },
  {
    id: 'west',
    name: 'The Explorer',
    symbol: '🧭',
    description: 'Adventure and discovery call to your spirit',
    color: 'text-cyan-300',
    gradient: 'from-cyan-600 to-teal-800',
    keywords: ['Adventure', 'Discovery', 'Freedom', 'Journey'],
  },
  {
    id: 'northwest',
    name: 'The Alchemist',
    symbol: '🔬',
    description: 'Transformation and transmutation are your gifts',
    color: 'text-pink-300',
    gradient: 'from-pink-600 to-fuchsia-800',
    keywords: ['Transformation', 'Alchemy', 'Change', 'Evolution'],
  },
];

export const IntegratedConsciousnessOnboarding: React.FC<
  IntegratedConsciousnessOnboardingProps
> = ({ onProfileComplete, onStepChange }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const backgroundRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);
  const compassRef = useRef<HTMLDivElement>(null);

  const [currentStep, setCurrentStep] = useState<OnboardingStep>('direction_selection');
  const [selectedDirection, setSelectedDirection] = useState<ArchetypalDirection | null>(null);
  const [userName, setUserName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [birthTime, setBirthTime] = useState('');
  const [birthCity, setBirthCity] = useState('');
  const [birthCountry, setBirthCountry] = useState('');

  const [profile, setProfile] = useState<ConsciousnessProfile>({
    personalData: {
      fullName: '',
      name: '',
      preferredName: '',
      birthDate: '',
    },
    birthData: {
      birthDate: '',
      birthTime: '',
      birthLocation: [0, 0],
      timezone: '',
      date: '',
      time: '',
      location: [0, 0],
    },
    location: {
      city: '',
      country: '',
      latitude: 0,
      longitude: 0,
      timezone: '',
    },
    preferences: {
      primaryShape: 'circle',
      spectralDirection: 'north',
      consciousnessLevel: 1,
    },
    archetypalSignature: {},
  });

  // Initialize GSAP animations
  useEffect(() => {
    const ctx = gsap.context(() => {
      // Animate background gradient
      if (backgroundRef.current) {
        gsap.to(backgroundRef.current, {
          backgroundPosition: '200% 200%',
          duration: 12,
          repeat: -1,
          ease: 'none',
        });
      }

      // Animate content entrance
      if (contentRef.current) {
        gsap.fromTo(
          contentRef.current,
          { opacity: 0, y: 50 },
          { opacity: 1, y: 0, duration: 1, ease: 'power2.out' }
        );
      }

      // Animate compass if on direction selection
      if (currentStep === 'direction_selection' && compassRef.current) {
        gsap.fromTo(
          compassRef.current,
          { opacity: 0, scale: 0.8, rotation: -180 },
          { opacity: 1, scale: 1, rotation: 0, duration: 1.5, ease: 'power2.out', delay: 0.5 }
        );
      }
    }, containerRef);

    return () => ctx.revert();
  }, [currentStep]);

  // Update step tracking
  useEffect(() => {
    const stepMap: Record<OnboardingStep, number> = {
      direction_selection: 1,
      name_story: 2,
      birth_date_story: 3,
      birth_time_story: 4,
      birth_location_story: 5,
      confirmation: 6,
    };
    onStepChange?.(stepMap[currentStep], 6);
  }, [currentStep, onStepChange]);

  const handleDirectionSelect = (direction: ArchetypalDirection) => {
    setSelectedDirection(direction);

    // Animate selection
    if (compassRef.current) {
      gsap.to(compassRef.current, {
        scale: 1.1,
        duration: 0.3,
        yoyo: true,
        repeat: 1,
        ease: 'power2.inOut',
        onComplete: () => {
          setTimeout(() => setCurrentStep('name_story'), 500);
        },
      });
    }
  };

  const handleNameSubmit = (name: string) => {
    setUserName(name);
    setProfile(prev => ({
      ...prev,
      personalData: {
        fullName: name,
        name: name,
        preferredName: name.split(' ')[0] || name,
        birthDate: prev.personalData?.birthDate || '',
      },
    }));
    setCurrentStep('birth_date_story');
  };

  const handleBirthDateSubmit = (date: string) => {
    setBirthDate(date);
    setProfile(prev => ({
      ...prev,
      personalData: {
        fullName: prev.personalData?.fullName || '',
        name: prev.personalData?.name || '',
        preferredName:
          prev.personalData?.preferredName || prev.personalData?.fullName?.split(' ')[0] || '',
        birthDate: date,
      },
      birthData: {
        birthDate: date,
        birthTime: prev.birthData?.birthTime || '',
        birthLocation: prev.birthData?.birthLocation || [0, 0],
        timezone: prev.birthData?.timezone || '',
        date: date,
        time: prev.birthData?.time || '',
        location: prev.birthData?.location || [0, 0],
      },
    }));
    setCurrentStep('birth_time_story');
  };

  const handleBirthTimeSubmit = (time: string) => {
    setBirthTime(time);
    setProfile(prev => ({
      ...prev,
      birthData: {
        birthDate: prev.birthData?.birthDate || '',
        birthTime: time,
        birthLocation: prev.birthData?.birthLocation || [0, 0],
        timezone: prev.birthData?.timezone || '',
        date: prev.birthData?.date || '',
        time: time,
        location: prev.birthData?.location || [0, 0],
      },
    }));
    setCurrentStep('birth_location_story');
  };

  const handleLocationSubmit = (city: string, country: string) => {
    setBirthCity(city);
    setBirthCountry(country);
    setProfile(prev => ({
      ...prev,
      location: {
        city,
        country,
        latitude: 0,
        longitude: 0,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      },
      birthData: {
        birthDate: prev.birthData?.birthDate || '',
        birthTime: prev.birthData?.birthTime || '',
        birthLocation: [0, 0],
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        date: prev.birthData?.date || '',
        time: prev.birthData?.time || '',
        location: [0, 0],
      },
    }));
    setCurrentStep('confirmation');
  };

  const handleConfirmation = () => {
    const finalProfile: ConsciousnessProfile = {
      ...profile,
      preferences: {
        ...profile.preferences,
        spectralDirection: (selectedDirection?.id as any) || 'north',
      },
      archetypalSignature: {
        ...profile.archetypalSignature,
        // Store direction info in a way that's compatible with the interface
        ...(selectedDirection?.name && { humanDesignType: selectedDirection.name }),
      },
    };
    onProfileComplete(finalProfile);
  };

  return (
    <div
      ref={containerRef}
      className='w-full h-screen font-mono overflow-hidden flex flex-col relative'
      style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
    >
      {/* Enhanced Moving Gradient Background */}
      <div
        ref={backgroundRef}
        className='absolute inset-0 opacity-90'
        style={{
          background: selectedDirection
            ? `
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 226, 0.3) 0%, transparent 50%),
                linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0a0a0a 100%)
              `
            : `
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 226, 0.3) 0%, transparent 50%),
                linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0a0a0a 100%)
              `,
          backgroundSize: '400% 400%',
          filter: 'contrast(1.1) brightness(0.9)',
        }}
      />

      {/* Noise Texture Overlay */}
      <div
        className='absolute inset-0 opacity-20 mix-blend-overlay'
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Main Content */}
      <div ref={contentRef} className='relative z-10 flex-1 flex items-center justify-center p-8'>
        {currentStep === 'direction_selection' && (
          <DirectionSelectionStep
            directions={ARCHETYPAL_DIRECTIONS}
            onSelect={handleDirectionSelect}
            compassRef={compassRef}
          />
        )}

        {currentStep === 'name_story' && selectedDirection && (
          <NameStoryStep direction={selectedDirection} onSubmit={handleNameSubmit} />
        )}

        {currentStep === 'birth_date_story' && selectedDirection && (
          <BirthDateStoryStep
            direction={selectedDirection}
            userName={userName}
            onSubmit={handleBirthDateSubmit}
          />
        )}

        {currentStep === 'birth_time_story' && selectedDirection && (
          <BirthTimeStoryStep
            direction={selectedDirection}
            userName={userName}
            onSubmit={handleBirthTimeSubmit}
          />
        )}

        {currentStep === 'birth_location_story' && selectedDirection && (
          <BirthLocationStoryStep
            direction={selectedDirection}
            userName={userName}
            onSubmit={handleLocationSubmit}
          />
        )}

        {currentStep === 'confirmation' && selectedDirection && (
          <ConfirmationStep
            direction={selectedDirection}
            profile={profile}
            onConfirm={handleConfirmation}
          />
        )}
      </div>

      {/* Progress Indicator */}
      <div className='relative z-10 p-6 border-t border-cyan-500/30'>
        <div className='flex items-center justify-between mb-4'>
          <div className='text-cyan-400 text-sm'>
            {selectedDirection && (
              <span className={selectedDirection.color}>
                {selectedDirection.symbol} {selectedDirection.name}
              </span>
            )}
          </div>
          <div className='text-gray-400 text-sm'>
            Step{' '}
            {currentStep === 'direction_selection'
              ? 1
              : currentStep === 'name_story'
                ? 2
                : currentStep === 'birth_date_story'
                  ? 3
                  : currentStep === 'birth_time_story'
                    ? 4
                    : currentStep === 'birth_location_story'
                      ? 5
                      : 6}{' '}
            of 6
          </div>
        </div>
        <div className='w-full bg-gray-800 rounded-full h-2'>
          <div
            className={`h-2 rounded-full transition-all duration-500 ease-out ${
              selectedDirection
                ? `bg-gradient-to-r ${selectedDirection.gradient}`
                : 'bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500'
            }`}
            style={{
              width: `${
                ((currentStep === 'direction_selection'
                  ? 1
                  : currentStep === 'name_story'
                    ? 2
                    : currentStep === 'birth_date_story'
                      ? 3
                      : currentStep === 'birth_time_story'
                        ? 4
                        : currentStep === 'birth_location_story'
                          ? 5
                          : 6) /
                  6) *
                100
              }%`,
            }}
          />
        </div>
      </div>

      {/* Hide scrollbars */}
      <style jsx>{`
        div::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </div>
  );
};

// Direction Selection Step Component
const DirectionSelectionStep: React.FC<{
  directions: ArchetypalDirection[];
  onSelect: (direction: ArchetypalDirection) => void;
  compassRef: React.RefObject<HTMLDivElement | null>;
}> = ({ directions, onSelect, compassRef }) => {
  return (
    <div className='text-center max-w-4xl mx-auto'>
      <div className='mb-8'>
        <h1 className='text-4xl font-bold text-cyan-400 mb-4'>
          🌀 Choose Your Archetypal Direction
        </h1>
        <p className='text-gray-300 text-lg'>
          Every consciousness journey begins with a direction. Which archetypal energy calls to your
          spirit?
        </p>
      </div>

      <div ref={compassRef} className='relative'>
        <div className='grid grid-cols-3 gap-6 max-w-3xl mx-auto'>
          {directions.map((direction, index) => (
            <div
              key={direction.id}
              className={`
                relative p-6 rounded-lg border-2 border-gray-600/50
                hover:border-cyan-500/70 transition-all duration-300 cursor-pointer
                bg-gray-900/50 backdrop-blur-sm hover:bg-gray-800/70
                transform hover:scale-105 hover:shadow-lg
                ${index === 1 || index === 4 || index === 7 ? 'col-start-2' : ''}
              `}
              onClick={() => onSelect(direction)}
            >
              <div className='text-center'>
                <div className='text-4xl mb-3'>{direction.symbol}</div>
                <h3 className={`text-xl font-bold mb-2 ${direction.color}`}>{direction.name}</h3>
                <p className='text-gray-400 text-sm mb-3'>{direction.description}</p>
                <div className='flex flex-wrap gap-1 justify-center'>
                  {direction.keywords.map(keyword => (
                    <span
                      key={keyword}
                      className='px-2 py-1 bg-gray-700/50 rounded text-xs text-gray-300'
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default IntegratedConsciousnessOnboarding;
