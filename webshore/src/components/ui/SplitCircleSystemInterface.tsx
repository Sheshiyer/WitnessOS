/**
 * Split Circle System Interface
 *
 * Phase 4.2 - CRITICAL Missing Component
 * Creates split circle system interface for data visualization
 * Displays consciousness data in sacred geometric circular patterns
 */

'use client';

import { useConsciousness } from '@/hooks/useConsciousness';
import type { ConsciousnessState } from '@/types';
import { SACRED_MATHEMATICS } from '@/utils/consciousness-constants';
import { useFrame } from '@react-three/fiber';
import React, { useMemo, useRef, useState } from 'react';
import * as THREE from 'three';

interface SplitCircleSystemInterfaceProps {
  position?: [number, number, number];
  radius?: number;
  consciousness: ConsciousnessState;
  data?: Record<string, number>;
  onSegmentClick?: (segment: CircleSegment) => void;
  animated?: boolean;
}

interface CircleSegment {
  id: string;
  startAngle: number;
  endAngle: number;
  value: number;
  color: THREE.Color;
  label: string;
  data: unknown;
}

interface DataVisualization {
  segments: CircleSegment[];
  centerValue: number;
  totalValue: number;
}

export const SplitCircleSystemInterface: React.FC<SplitCircleSystemInterfaceProps> = ({
  position = [0, 0, 0],
  radius = 2,
  consciousness,
  data = {},
  onSegmentClick,
  animated = true,
}) => {
  const groupRef = useRef<THREE.Group>(null);
  const [selectedSegment, setSelectedSegment] = useState<string | null>(null);
  const [rotationSpeed, setRotationSpeed] = useState(0.1);
  const { consciousnessLevel } = useConsciousness();

  // Default consciousness data if none provided
  const defaultData = useMemo(
    () => ({
      awareness: consciousnessLevel * 100,
      intuition: Math.sin(Date.now() * 0.001) * 50 + 50,
      creativity: Math.cos(Date.now() * 0.0015) * 40 + 60,
      wisdom: consciousnessLevel * 80 + 20,
      compassion: Math.sin(Date.now() * 0.0008) * 30 + 70,
      clarity: consciousnessLevel * 90 + 10,
      balance: Math.cos(Date.now() * 0.0012) * 35 + 65,
      presence: consciousnessLevel * 85 + 15,
    }),
    [consciousnessLevel]
  );

  const visualizationData = useMemo(() => ({ ...defaultData, ...data }), [defaultData, data]);

  // Create split circle visualization
  const createSplitCircleVisualization = useMemo((): DataVisualization => {
    const entries = Object.entries(visualizationData);
    const totalValue = entries.reduce((sum, [, value]) => sum + value, 0);
    const phi = SACRED_MATHEMATICS.PHI;

    // Color palette based on golden ratio
    const colors = [
      new THREE.Color('#FF6B35'), // Warm orange
      new THREE.Color('#4ECDC4'), // Teal
      new THREE.Color('#45B7D1'), // Blue
      new THREE.Color('#96CEB4'), // Mint
      new THREE.Color('#FFEAA7'), // Yellow
      new THREE.Color('#DDA0DD'), // Plum
      new THREE.Color('#98D8C8'), // Mint green
      new THREE.Color('#F7DC6F'), // Light yellow
    ];

    let currentAngle = 0;
    const segments: CircleSegment[] = entries.map(([label, value], index) => {
      const normalizedValue = value / totalValue;
      const segmentAngle = normalizedValue * Math.PI * 2;

      // Apply golden ratio spacing
      const adjustedAngle = segmentAngle * (1 + 1 / phi);

      const segment: CircleSegment = {
        id: `segment-${label}`,
        startAngle: currentAngle,
        endAngle: currentAngle + adjustedAngle,
        value,
        color: colors[index % colors.length],
        label,
        data: { normalizedValue, originalValue: value },
      };

      currentAngle += adjustedAngle;
      return segment;
    });

    return {
      segments,
      centerValue: totalValue / entries.length,
      totalValue,
    };
  }, [visualizationData]);

  // Create segment geometry
  const createSegmentGeometry = (
    segment: CircleSegment,
    innerRadius: number,
    outerRadius: number
  ): THREE.BufferGeometry => {
    const geometry = new THREE.RingGeometry(
      innerRadius,
      outerRadius,
      Math.max(8, Math.floor((segment.endAngle - segment.startAngle) * 16)),
      1,
      segment.startAngle,
      segment.endAngle - segment.startAngle
    );

    return geometry;
  };

  // Split circle shader material
  const splitCircleMaterial = useMemo(() => {
    return new THREE.ShaderMaterial({
      uniforms: {
        time: { value: 0 },
        consciousnessLevel: { value: consciousnessLevel },
        segmentColor: { value: new THREE.Color('#4ECDC4') },
        selected: { value: 0.0 },
        value: { value: 0.5 },
      },
      vertexShader: `
        uniform float time;
        uniform float consciousnessLevel;
        uniform float selected;
        uniform float value;
        
        varying vec2 vUv;
        varying vec3 vPosition;
        varying float vIntensity;
        
        void main() {
          vUv = uv;
          vPosition = position;
          
          // Calculate intensity based on value and consciousness
          vIntensity = value * consciousnessLevel * (1.0 + selected * 0.5);
          
          // Pulsing effect for selected segments
          vec3 pos = position;
          if (selected > 0.5) {
            float pulse = sin(time * 4.0) * 0.05 + 1.0;
            pos *= pulse;
          }
          
          // Consciousness-based elevation
          pos.z += vIntensity * 0.1;
          
          gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
        }
      `,
      fragmentShader: `
        uniform float time;
        uniform vec3 segmentColor;
        uniform float selected;
        uniform float consciousnessLevel;
        
        varying vec2 vUv;
        varying vec3 vPosition;
        varying float vIntensity;
        
        void main() {
          vec2 center = vec2(0.5, 0.5);
          float dist = distance(vUv, center);
          
          // Create radial pattern
          float radialPattern = sin(dist * 20.0 + time * 2.0) * 0.1 + 0.9;
          
          // Color based on intensity and selection
          vec3 color = segmentColor;
          if (selected > 0.5) {
            color = mix(color, vec3(1.0, 1.0, 1.0), 0.3);
          }
          
          // Apply intensity and pattern
          color *= vIntensity * radialPattern;
          
          // Add consciousness glow
          float glow = 1.0 - smoothstep(0.0, 1.0, dist);
          color += glow * segmentColor * consciousnessLevel * 0.2;
          
          // Transparency based on distance and intensity
          float alpha = (1.0 - smoothstep(0.0, 1.0, dist)) * vIntensity;
          alpha = max(alpha, 0.3); // Minimum visibility
          
          gl_FragColor = vec4(color, alpha);
        }
      `,
      transparent: true,
      side: THREE.DoubleSide,
    });
  }, [consciousnessLevel]);

  // Handle segment interaction
  const handleSegmentClick = (segment: CircleSegment) => {
    setSelectedSegment(segment.id === selectedSegment ? null : segment.id);
    if (onSegmentClick) {
      onSegmentClick(segment);
    }
  };

  // Animation loop
  useFrame((state, delta) => {
    const time = state.clock.getElapsedTime();

    // Update shader uniforms for all materials
    splitCircleMaterial.uniforms.time.value = time;
    splitCircleMaterial.uniforms.consciousnessLevel.value = consciousnessLevel;

    // Animate group rotation
    if (groupRef.current && animated) {
      groupRef.current.rotation.z += delta * rotationSpeed * consciousnessLevel;
    }
  });

  return (
    <group ref={groupRef} position={position}>
      {/* Split Circle Segments */}
      {visualizationData.segments.map(segment => {
        const innerRadius = radius * 0.3;
        const outerRadius = radius * (0.6 + (segment.value / 100) * 0.4);
        const segmentGeometry = createSegmentGeometry(segment, innerRadius, outerRadius);
        const isSelected = segment.id === selectedSegment;

        // Create material for this segment
        const segmentMaterial = splitCircleMaterial.clone();
        segmentMaterial.uniforms.segmentColor.value = segment.color;
        segmentMaterial.uniforms.selected.value = isSelected ? 1.0 : 0.0;
        segmentMaterial.uniforms.value.value = segment.value / 100;

        return (
          <group key={segment.id}>
            {/* Main segment */}
            <mesh
              geometry={segmentGeometry}
              material={segmentMaterial}
              onClick={() => handleSegmentClick(segment)}
              onPointerOver={() => setRotationSpeed(0.05)}
              onPointerOut={() => setRotationSpeed(0.1)}
            />

            {/* Segment label */}
            <group
              position={[
                Math.cos((segment.startAngle + segment.endAngle) / 2) * (radius * 0.8),
                Math.sin((segment.startAngle + segment.endAngle) / 2) * (radius * 0.8),
                0.1,
              ]}
            >
              <mesh>
                <sphereGeometry args={[0.02, 8, 8]} />
                <meshBasicMaterial color={segment.color} />
              </mesh>
            </group>

            {/* Value indicator */}
            {isSelected && (
              <group
                position={[
                  Math.cos((segment.startAngle + segment.endAngle) / 2) * (radius * 1.1),
                  Math.sin((segment.startAngle + segment.endAngle) / 2) * (radius * 1.1),
                  0.2,
                ]}
              >
                <mesh>
                  <boxGeometry args={[0.1, 0.02, segment.value / 100]} />
                  <meshBasicMaterial color={segment.color} transparent opacity={0.8} />
                </mesh>
              </group>
            )}
          </group>
        );
      })}

      {/* Center circle */}
      <mesh position={[0, 0, 0.05]}>
        <circleGeometry args={[radius * 0.25, 32]} />
        <meshBasicMaterial color='#FFFFFF' transparent opacity={0.8 + consciousnessLevel * 0.2} />
      </mesh>

      {/* Center value indicator */}
      <mesh position={[0, 0, 0.1]}>
        <cylinderGeometry args={[0.02, 0.02, visualizationData.centerValue / 100]} />
        <meshBasicMaterial color='#FFD700' transparent opacity={0.9} />
      </mesh>

      {/* Consciousness level ring */}
      <mesh position={[0, 0, -0.05]}>
        <ringGeometry args={[radius * 1.1, radius * 1.15, 64]} />
        <meshBasicMaterial color='#E6E6FA' transparent opacity={consciousnessLevel * 0.5} />
      </mesh>

      {/* Data flow particles */}
      {visualizationData.segments.map(segment => {
        const particleCount = Math.floor(segment.value / 20);
        return Array.from({ length: particleCount }, (_, i) => {
          const angle =
            segment.startAngle + (segment.endAngle - segment.startAngle) * (i / particleCount);
          const particleRadius = radius * (0.4 + Math.sin(Date.now() * 0.001 + i) * 0.2);
          const x = Math.cos(angle) * particleRadius;
          const y = Math.sin(angle) * particleRadius;
          const z = Math.sin(Date.now() * 0.001 + i * 0.5) * 0.1;

          return (
            <mesh key={`${segment.id}-particle-${i}`} position={[x, y, z]}>
              <sphereGeometry args={[0.005, 4, 4]} />
              <meshBasicMaterial
                color={segment.color}
                transparent
                opacity={0.6 + Math.sin(Date.now() * 0.001 + i) * 0.3}
              />
            </mesh>
          );
        });
      })}

      {/* Interactive overlay */}
      <mesh position={[0, 0, 0.01]}>
        <circleGeometry args={[radius * 1.2, 64]} />
        <meshBasicMaterial transparent opacity={0} />
      </mesh>
    </group>
  );
};

export default SplitCircleSystemInterface;
