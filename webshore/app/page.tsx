'use client';

import dynamic from 'next/dynamic';
import { useState } from 'react';

// Dynamically import the Portal Chamber Scene to avoid SSR issues with Three.js
const PortalChamberScene = dynamic(
  () =>
    import('../src/components/procedural-scenes/PortalChamberScene')
      .then(mod => {
        console.log('Portal Chamber Scene loaded successfully:', mod);
        return { default: mod.PortalChamberScene };
      })
      .catch(error => {
        console.error('Failed to load Portal Chamber Scene:', error);
        throw error;
      }),
  {
    ssr: false,
    loading: () => (
      <div className='min-h-screen bg-black text-white flex items-center justify-center'>
        <div className='text-center'>
          <h1 className='text-4xl font-bold text-purple-400 mb-4'>Portal Chamber Loading...</h1>
          <p className='text-lg text-purple-300'>Initializing consciousness field...</p>
          <div className='mt-4 animate-spin w-8 h-8 border-2 border-purple-400 border-t-transparent rounded-full mx-auto'></div>
        </div>
      </div>
    ),
  }
);

export default function Home() {
  const [showPortal, setShowPortal] = useState(false);

  if (showPortal) {
    return (
      <div className='min-h-screen bg-black'>
        <div className='relative w-full h-full'>
          <PortalChamberScene
            humanDesignType='generator'
            enneagramType={9}
            enableBreathDetection={true}
            enableInfiniteZoom={true}
            enablePerformanceStats={true}
            onPortalEnter={() => {
              console.log('Portal activated!');
            }}
            onConsciousnessEvolution={consciousness => {
              console.log('Consciousness evolved:', consciousness);
            }}
          />
          <button
            onClick={() => setShowPortal(false)}
            className='absolute top-4 left-4 bg-purple-600/80 hover:bg-purple-500 text-white px-4 py-2 rounded-lg backdrop-blur-sm z-10'
          >
            ← Back to Dashboard
          </button>

          {/* Debug info */}
          <div className='absolute bottom-4 left-4 bg-black/50 text-white p-2 rounded text-xs z-10'>
            Portal Chamber Active - Check console for logs
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className='min-h-screen bg-black text-white'>
      <div className='flex items-center justify-center h-screen'>
        <div className='text-center max-w-2xl px-8'>
          <h1 className='text-6xl font-bold text-purple-400 mb-6'>WitnessOS Webshore</h1>
          <p className='text-xl text-purple-300 mb-8'>
            Consciousness exploration through procedural generation
          </p>
          <div className='text-lg text-purple-200 mb-6'>
            Phase 5.5: Engine Component Integration & Testing
          </div>

          {/* Status indicators */}
          <div className='grid grid-cols-2 gap-4 text-sm text-purple-400 mb-8'>
            <div className='bg-purple-900/30 p-4 rounded-lg'>
              <div className='text-green-400 mb-2'>✅ Development Server</div>
              <div>Running at localhost:3000</div>
            </div>
            <div className='bg-purple-900/30 p-4 rounded-lg'>
              <div className='text-green-400 mb-2'>✅ TypeScript Errors</div>
              <div>All errors fixed!</div>
            </div>
            <div className='bg-purple-900/30 p-4 rounded-lg'>
              <div className='text-blue-400 mb-2'>🎯 Current Focus</div>
              <div>Portal Chamber Scene</div>
            </div>
            <div className='bg-purple-900/30 p-4 rounded-lg'>
              <div className='text-purple-400 mb-2'>🌟 Progress</div>
              <div>3D Scene Ready!</div>
            </div>
          </div>

          <button
            onClick={() => setShowPortal(true)}
            className='bg-purple-600 hover:bg-purple-500 text-white px-8 py-3 rounded-lg text-lg font-semibold transition-colors mb-6'
          >
            🌀 Test Portal Chamber
          </button>

          <div className='text-sm text-purple-500 opacity-75'>
            Click to test the 3D consciousness exploration interface
          </div>

          <div className='mt-8 text-xs text-purple-600'>
            <div>React Three Fiber • Next.js 15.3.3 • React 19</div>
            <div className='mt-2'>Debugging-enabled development setup</div>
          </div>
        </div>
      </div>
    </div>
  );
}
