'use client';

import { type ConsciousnessProfile } from '@/components/ui/ConsciousnessDataCollector';
import EnhancedWitnessOSBootSequence from '@/components/ui/EnhancedWitnessOSBootSequence';
import IntegratedConsciousnessOnboarding from '@/components/ui/IntegratedConsciousnessOnboarding';
import dynamic from 'next/dynamic';
import { Suspense, useState } from 'react';

// Dynamic import for Portal Chamber to avoid SSR issues
const PortalChamberScene = dynamic(
  () => import('@/components/procedural-scenes/PortalChamberScene'),
  {
    ssr: false,
    loading: () => <EnhancedWitnessOSBootSequence />,
  }
);

export default function Home() {
  const [bootComplete, setBootComplete] = useState(false);
  const [dataCollectionComplete, setDataCollectionComplete] = useState(false);
  const [userProfile, setUserProfile] = useState<ConsciousnessProfile | null>(null);
  const [userInitialized, setUserInitialized] = useState(false);

  // Debug logging
  console.log('🔍 Debug - Current state:', {
    bootComplete,
    dataCollectionComplete,
    userProfile: !!userProfile,
    userInitialized,
  });

  const handleBootComplete = () => {
    console.log('🚀 Boot sequence completed!');
    setBootComplete(true);
  };

  const handleProfileComplete = (profile: ConsciousnessProfile) => {
    console.log('✅ Consciousness profile created:', profile);
    setUserProfile(profile);
    setDataCollectionComplete(true);
  };

  const handleUserInitialization = () => {
    setUserInitialized(true);
  };

  // Show boot sequence first
  if (!bootComplete) {
    return (
      <div>
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            background: 'red',
            color: 'white',
            padding: '10px',
            zIndex: 9999,
          }}
        >
          DEBUG: Boot sequence should show here
        </div>
        <EnhancedWitnessOSBootSequence onBootComplete={handleBootComplete} />
      </div>
    );
  }

  // Show data collection after boot
  if (!dataCollectionComplete) {
    return (
      <IntegratedConsciousnessOnboarding
        onProfileComplete={handleProfileComplete}
        onStepChange={(step, total) => {
          console.log(`Data collection step ${step}/${total}`);
        }}
      />
    );
  }

  // Show Portal Chamber after data collection
  return (
    <div className='w-full h-screen overflow-hidden bg-black'>
      <Suspense fallback={<EnhancedWitnessOSBootSequence />}>
        <PortalChamberScene
          enableBreathDetection={true}
          enableInfiniteZoom={true}
          enablePerformanceStats={true}
          onPortalEnter={handleUserInitialization}
          onConsciousnessEvolution={consciousness => {
            console.log('Consciousness evolution:', consciousness);
          }}
          userData={{
            ...(userProfile?.birthData.birthDate && {
              birthDate: new Date(userProfile.birthData.birthDate),
            }),
            ...(userProfile?.birthData.birthTime && {
              birthTime: userProfile.birthData.birthTime,
            }),
            ...(userProfile?.personalData.fullName && {
              name: userProfile.personalData.fullName,
            }),
          }}
          humanDesignType={userProfile?.archetypalSignature.humanDesignType || 'generator'}
          enneagramType={userProfile?.archetypalSignature.enneagramType || 9}
        />
      </Suspense>
    </div>
  );
}
