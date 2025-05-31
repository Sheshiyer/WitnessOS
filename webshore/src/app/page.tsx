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

  const handleBootComplete = () => {
    setBootComplete(true);
  };

  const handleProfileComplete = (profile: ConsciousnessProfile) => {
    setUserProfile(profile);
    setDataCollectionComplete(true);
  };

  const handleUserInitialization = () => {
    setUserInitialized(true);
  };

  // Show boot sequence first
  if (!bootComplete) {
    return <EnhancedWitnessOSBootSequence onBootComplete={handleBootComplete} />;
  }

  // Show data collection after boot
  if (!dataCollectionComplete) {
    return (
      <IntegratedConsciousnessOnboarding
        onProfileComplete={handleProfileComplete}
        onStepChange={(step, total) => {
          // Data collection progress tracking
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
