/**
 * Cosmic Portal Temple Test Page
 * 
 * Phase 5 Critical Component Testing: Cosmic Portal Temple Foundation Library
 */

'use client';

import { useConsciousness } from '@/hooks/useConsciousness';
import type { BreathState } from '@/types';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import { Canvas } from '@react-three/fiber';
import React, { useState, useCallback } from 'react';
import { BreathDetection } from '@/components/consciousness-engines/BreathDetection';
import CosmicPortalTemple from '@/components/procedural-scenes/CosmicPortalTemple';
import { TEMPLE_TEMPLATES } from '@/lib/cosmic-portal-temple';

export default function CosmicTemplePage() {
  const { consciousness, updateConsciousness } = useConsciousness();
  const [breathState, setBreathState] = useState<BreathState>({
    phase: 'neutral',
    intensity: 0,
    coherence: 0,
    timestamp: Date.now(),
  });
  const [selectedTemplate, setSelectedTemplate] = useState<keyof typeof TEMPLE_TEMPLATES>('MEDITATION_SANCTUARY');
  const [activatedPortals, setActivatedPortals] = useState<string[]>([]);
  const [enteredTemples, setEnteredTemples] = useState<string[]>([]);

  const handleBreathStateChange = useCallback((newBreathState: BreathState) => {
    setBreathState(newBreathState);
    
    // Update consciousness based on breath coherence
    if (newBreathState.coherence > 0.7) {
      updateConsciousness({
        awarenessLevel: Math.min(1.0, consciousness.awarenessLevel + 0.002),
        coherenceLevel: newBreathState.coherence,
        breathSynchronization: newBreathState.intensity,
      });
    }
  }, [consciousness.awarenessLevel, updateConsciousness]);

  const handlePortalActivated = useCallback((portalId: string) => {
    setActivatedPortals(prev => [...prev, portalId]);
    console.log('Portal activated:', portalId);
  }, []);

  const handleTempleEntered = useCallback((templeId: string) => {
    setEnteredTemples(prev => [...prev, templeId]);
    console.log('Temple entered:', templeId);
  }, []);

  const templateNames = Object.keys(TEMPLE_TEMPLATES) as (keyof typeof TEMPLE_TEMPLATES)[];

  return (
    <div className="w-full h-screen bg-gradient-to-b from-indigo-950 via-purple-950 to-black">
      {/* Breath Detection */}
      <BreathDetection
        onBreathStateChange={handleBreathStateChange}
        consciousness={consciousness}
        isActive={true}
      />

      {/* Temple Info Overlay */}
      <div className="absolute top-4 left-4 z-10 bg-black/70 p-4 rounded-lg text-white max-w-sm">
        <h2 className="text-xl font-bold mb-2 text-indigo-300">Cosmic Portal Temple</h2>
        <p className="text-sm text-gray-300 mb-3">
          Experience consciousness-responsive temple architecture. Higher awareness unlocks more features.
        </p>
        
        {/* Template Selection */}
        <div className="mb-3">
          <label className="block text-sm font-medium mb-2">Temple Type:</label>
          <select 
            value={selectedTemplate} 
            onChange={(e) => setSelectedTemplate(e.target.value as keyof typeof TEMPLE_TEMPLATES)}
            className="bg-gray-800 text-white p-2 rounded w-full text-sm"
          >
            {templateNames.map(template => (
              <option key={template} value={template}>
                {TEMPLE_TEMPLATES[template].name}
              </option>
            ))}
          </select>
        </div>
        
        <div className="space-y-2 text-xs">
          <div className="flex justify-between">
            <span>Consciousness:</span>
            <span className="text-indigo-400">{(consciousness.awarenessLevel * 100).toFixed(1)}%</span>
          </div>
          <div className="flex justify-between">
            <span>Coherence:</span>
            <span className="text-purple-400">{(consciousness.coherenceLevel * 100).toFixed(1)}%</span>
          </div>
          <div className="flex justify-between">
            <span>Breath Coherence:</span>
            <span className="text-green-400">{(breathState.coherence * 100).toFixed(1)}%</span>
          </div>
          <div className="flex justify-between">
            <span>Breath Phase:</span>
            <span className="text-blue-400">{breathState.phase}</span>
          </div>
          <div className="flex justify-between">
            <span>Portals Activated:</span>
            <span className="text-yellow-400">{activatedPortals.length}</span>
          </div>
        </div>
      </div>

      {/* Temple Requirements */}
      <div className="absolute top-4 right-4 z-10 bg-black/70 p-4 rounded-lg text-white max-w-md">
        <h3 className="font-bold text-indigo-300 mb-2">Temple Requirements</h3>
        <div className="text-sm text-gray-300 space-y-1">
          <div>Min Awareness: {(TEMPLE_TEMPLATES[selectedTemplate].consciousness.minimumAwarenessLevel * 100).toFixed(0)}%</div>
          <div>Required Coherence: {(TEMPLE_TEMPLATES[selectedTemplate].consciousness.requiredCoherence * 100).toFixed(0)}%</div>
          <div>Breath Sync: {(TEMPLE_TEMPLATES[selectedTemplate].consciousness.breathSynchronizationLevel * 100).toFixed(0)}%</div>
        </div>
        
        <div className="mt-3 text-xs">
          <div className="font-medium text-indigo-300 mb-1">Temple Features:</div>
          <div>• {TEMPLE_TEMPLATES[selectedTemplate].portals.length} Portal(s)</div>
          <div>• {TEMPLE_TEMPLATES[selectedTemplate].energyFields.length} Energy Field(s)</div>
          <div>• {TEMPLE_TEMPLATES[selectedTemplate].sacredElements.length} Sacred Element(s)</div>
        </div>
      </div>

      {/* Instructions */}
      <div className="absolute bottom-4 right-4 z-10 bg-black/70 p-4 rounded-lg text-white max-w-md">
        <h3 className="font-bold text-indigo-300 mb-2">Temple Instructions</h3>
        <ul className="text-sm text-gray-300 space-y-1">
          <li>• Breathe deeply to increase consciousness</li>
          <li>• Higher awareness activates temple features</li>
          <li>• Click activated portals to enter them</li>
          <li>• Energy fields respond to breath coherence</li>
          <li>• Try different temple types as you evolve</li>
        </ul>
        
        <div className="mt-3 text-xs text-gray-400">
          <p>Tip: Maintain high breath coherence to see energy fields activate</p>
        </div>
      </div>

      {/* 3D Scene */}
      <Canvas
        camera={{ position: [0, 15, 20], fov: 75 }}
        onCreated={({ gl }) => {
          gl.setClearColor('#0a0a1a');
        }}
      >
        {/* Camera Controls */}
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          maxDistance={40}
          minDistance={8}
          maxPolarAngle={Math.PI / 2.2}
          target={[0, 5, 0]}
        />

        {/* Lighting */}
        <ambientLight intensity={0.3} color="#4a5568" />
        <directionalLight
          position={[15, 20, 10]}
          intensity={0.5}
          color="#e2e8f0"
          castShadow
        />
        <pointLight
          position={[0, 25, 0]}
          intensity={0.4}
          color="#a78bfa"
          distance={50}
          decay={2}
        />

        {/* Cosmic Portal Temple */}
        <CosmicPortalTemple
          consciousness={consciousness}
          breath={breathState}
          position={[0, 0, 0]}
          templateId={selectedTemplate}
          onPortalActivated={handlePortalActivated}
          onTempleEntered={handleTempleEntered}
          isActive={true}
        />

        {/* Ground plane */}
        <mesh position={[0, -2, 0]} rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[100, 100]} />
          <meshStandardMaterial 
            color="#1a202c"
            transparent
            opacity={0.5}
            roughness={0.8}
          />
        </mesh>

        {/* Cosmic background effect */}
        <mesh>
          <sphereGeometry args={[80, 32, 32]} />
          <meshBasicMaterial 
            color="#0f0f23"
            transparent
            opacity={0.3}
            side={2} // DoubleSide
          />
        </mesh>
      </Canvas>

      {/* Portal activation notification */}
      {activatedPortals.length > 0 && (
        <div className="absolute bottom-4 left-4 z-10 bg-purple-900/80 p-3 rounded-lg text-white">
          <div className="text-sm font-medium text-purple-300">Portal Activated!</div>
          <div className="text-xs text-gray-300">
            {activatedPortals[activatedPortals.length - 1]}
          </div>
        </div>
      )}
    </div>
  );
}
