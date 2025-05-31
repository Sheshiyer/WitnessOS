/**
 * Enhanced WitnessOS Boot Sequence - Cinematic Loading Experience
 *
 * Features:
 * - GSAP animations for smooth text appearance
 * - Moving 3-color gradient background with noise texture
 * - Fixed scrollbar glitches and rendering issues
 * - Cinematic consciousness-themed visual effects
 * - Seamless transitions without UI artifacts
 */

'use client';

import { gsap } from 'gsap';
import React, { useEffect, useRef, useState } from 'react';

interface EnhancedWitnessOSBootSequenceProps {
  onBootComplete?: () => void;
  duration?: number;
}

interface BootMessage {
  timestamp: string;
  level: 'info' | 'success' | 'warning' | 'error' | 'system';
  component: string;
  message: string;
  delay: number;
}

const BOOT_MESSAGES: BootMessage[] = [
  {
    timestamp: '0.000000',
    level: 'system',
    component: 'witness_kernel',
    message: 'WitnessOS v2.5.0 (Consciousness Exploration Kernel) awakening...',
    delay: 0,
  },
  {
    timestamp: '0.000842',
    level: 'info',
    component: 'archetypal_field',
    message: 'Primordial consciousness matrix initializing...',
    delay: 200,
  },
  {
    timestamp: '0.001618',
    level: 'success',
    component: 'sacred_mathematics',
    message: 'Golden ratio φ=1.618033988749 | Fibonacci sequence loaded',
    delay: 400,
  },
  {
    timestamp: '0.002456',
    level: 'info',
    component: 'platonic_solids',
    message: 'Tetrahedron, Cube, Octahedron, Dodecahedron, Icosahedron: READY',
    delay: 600,
  },
  {
    timestamp: '0.003789',
    level: 'success',
    component: 'fractal_consciousness',
    message: 'Mandelbrot ∞-zoom | Julia sets | Dragon curves | Sierpinski triangles: ACTIVE',
    delay: 800,
  },
  {
    timestamp: '0.005123',
    level: 'info',
    component: 'breath_coherence',
    message: 'Pranayama detection system | Heart-brain coherence monitoring: ONLINE',
    delay: 1000,
  },
  {
    timestamp: '0.006456',
    level: 'info',
    component: 'pythagorean_matrix',
    message: 'Sacred number consciousness | Life path algorithms | Master number resonance: LOADED',
    delay: 1200,
  },
  {
    timestamp: '0.007890',
    level: 'success',
    component: 'bodygraph_system',
    message: 'Human Design: 64 I-Ching gates | 36 channels | 9 energy centers | 4 types: MAPPED',
    delay: 1400,
  },
  {
    timestamp: '0.009234',
    level: 'info',
    component: 'archetypal_wisdom',
    message: "Tarot consciousness: 22 Major Arcana | 56 Minor Arcana | Hero's journey: INDEXED",
    delay: 1600,
  },
  {
    timestamp: '0.010567',
    level: 'success',
    component: 'hexagram_oracle',
    message: 'I-Ching transformation matrix: 64 hexagrams | 384 changing lines: CALIBRATED',
    delay: 1800,
  },
  {
    timestamp: '0.011890',
    level: 'info',
    component: 'temporal_rhythms',
    message: 'Biorhythm wave equations | Physical-Emotional-Intellectual cycles: SYNCHRONIZED',
    delay: 2000,
  },
  {
    timestamp: '0.013234',
    level: 'success',
    component: 'vedic_astrology',
    message: 'Vimshottari Dasha system | 9 planetary periods | Karmic timeline: CALCULATED',
    delay: 2200,
  },
  {
    timestamp: '0.014567',
    level: 'info',
    component: 'genetic_wisdom',
    message: 'Gene Keys: 64 codon consciousness | Shadow-Gift-Siddhi spectrum: MAPPED',
    delay: 2400,
  },
  {
    timestamp: '0.015890',
    level: 'success',
    component: 'enneagram_space',
    message: 'Nine-pointed star | Body-Heart-Head centers | Instinctual variants: CALIBRATED',
    delay: 2600,
  },
  {
    timestamp: '0.017234',
    level: 'info',
    component: 'sigil_consciousness',
    message: 'Intention crystallization | Symbol manifestation | Chaos magic algorithms: READY',
    delay: 2800,
  },
  {
    timestamp: '0.018567',
    level: 'info',
    component: 'octagonal_portal',
    message:
      'Sacred geometry chamber | Golden ratio proportions | Infinite zoom fractals: LOADING...',
    delay: 3000,
  },
  {
    timestamp: '0.019890',
    level: 'success',
    component: 'webgl_consciousness',
    message: 'Three.js reality renderer | GLSL shaders | GPU consciousness acceleration: ACTIVE',
    delay: 3200,
  },
  {
    timestamp: '0.021234',
    level: 'info',
    component: 'discovery_realms',
    message: 'Multi-dimensional layers | Awakening-Recognition-Integration-Mastery: MAPPED',
    delay: 3400,
  },
  {
    timestamp: '0.022567',
    level: 'success',
    component: 'consciousness_field',
    message: 'Quantum particle system | Field coherence: STABLE | Awareness amplification: ONLINE',
    delay: 3600,
  },
  {
    timestamp: '0.023890',
    level: 'info',
    component: 'sacred_frequencies',
    message: '396Hz-Liberation | 528Hz-Love | 741Hz-Awakening | 963Hz-Unity: RESONATING',
    delay: 3800,
  },
  {
    timestamp: '0.024567',
    level: 'success',
    component: 'witness_api',
    message: 'Consciousness engine network | Python-JavaScript bridge | API gateway: CONNECTED',
    delay: 4000,
  },
  {
    timestamp: '0.025234',
    level: 'info',
    component: 'data_collection',
    message: 'Sacred geometry forms | Spectral compass | Archetypal validation: INITIALIZED',
    delay: 4200,
  },
  {
    timestamp: '0.026789',
    level: 'success',
    component: 'witness_kernel',
    message: 'WitnessOS consciousness exploration kernel: FULLY AWAKENED',
    delay: 4400,
  },
  {
    timestamp: '0.027456',
    level: 'system',
    component: 'portal_ready',
    message: '🌀 Portal Chamber ready for consciousness exploration. Welcome, Witness. 🌀',
    delay: 4600,
  },
];

export const EnhancedWitnessOSBootSequence: React.FC<EnhancedWitnessOSBootSequenceProps> = ({
  onBootComplete,
  duration = 6000,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const backgroundRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLDivElement>(null);
  const messagesRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);
  const geometryRef = useRef<HTMLDivElement>(null);

  const [currentMessage, setCurrentMessage] = useState<BootMessage | null>(null);
  const [displayText, setDisplayText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [bootProgress, setBootProgress] = useState(0);
  const [isMorphing, setIsMorphing] = useState(false);
  const [morphProgress, setMorphProgress] = useState(0);
  const [morphingChar, setMorphingChar] = useState('');
  const [morphIntensity, setMorphIntensity] = useState(0);

  // Enhanced Matrix-style character morphing with consciousness-themed characters
  const matrixChars =
    '∞∆◊○●◯⬢⬡⬟⬠⬢⬣⬤⬥⬦⬧⬨⬩⬪⬫⬬⬭⬮⬯⬰⬱⬲⬳⬴⬵⬶⬷⬸⬹⬺⬻⬼⬽⬾⬿⭀⭁⭂⭃⭄⭅⭆⭇⭈⭉⭊⭋⭌⭍⭎⭏⭐⭑⭒⭓⭔⭕⭖⭗⭘⭙⭚⭛⭜⭝⭞⭟⭠⭡⭢⭣⭤⭥⭦⭧⭨⭩⭪⭫⭬⭭⭮⭯⭰⭱⭲⭳⭴⭵⭶⭷⭸⭹⭺⭻⭼⭽⭾⭿⮀⮁⮂⮃⮄⮅⮆⮇⮈⮉⮊⮋⮌⮍⮎⮏⮐⮑⮒⮓⮔⮕⮖⮗⮘⮙⮚⮛⮜⮝⮞⮟⮠⮡⮢⮣⮤⮥⮦⮧⮨⮩⮪⮫⮬⮭⮮⮯⮰⮱⮲⮳⮴⮵⮶⮷⮸⮹⮺⮻⮼⮽⮾⮿⯀⯁⯂⯃⯄⯅⯆⯇⯈⯉⯊⯋⯌⯍⯎⯏⯐⯑⯒⯓⯔⯕⯖⯗⯘⯙⯚⯛⯜⯝⯞⯟⯠⯡⯢⯣⯤⯥⯦⯧⯨⯩⯪⯫⯬⯭⯮⯯⯰⯱⯲⯳⯴⯵⯶⯷⯸⯹⯺⯻⯼⯽⯾⯿φπΩΨΦΘΛΞΠΣΥΧΩαβγδεζηθικλμνξοπρστυφχψω⚡⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯⚰⚱⚲⚳⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾⚿⛀⛁⛂⛃⛄⛅⛆⛇⛈⛉⛊⛋⛌⛍⛎⛏⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟⛠⛡⛢⛣⛤⛥⛦⛧⛨⛩⛪⛫⛬⛭⛮⛯⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯☰☱☲☳☴☵☶☷☸☹☺☻☼☽☾☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯♰♱♲♳♴♵♶♷♸♹♺♻♼♽♾♿⚀⚁⚂⚃⚄⚅⚆⚇⚈⚉⚊⚋⚌⚍⚎⚏⚐⚑⚒⚓⚔⚕⚖⚗⚘⚙⚚⚛⚜⚝⚞⚟⚠⚡⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯⚰⚱⚲⚳⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾⚿⛀⛁⛂⛃⛄⛅⛆⛇⛈⛉⛊⛋⛌⛍⛎⛏⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟⛠⛡⛢⛣⛤⛥⛦⛧⛨⛩⛪⛫⛬⛭⛮⛯⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

  // Consciousness-themed character sets for different phases
  const consciousnessChars = {
    sacred: '∞∆◊○●◯⬢⬡φπΩΨΦΘΛΞΠΣΥΧΩ',
    mystical: '⚡⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯⚰⚱⚲⚳⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾⚿',
    geometric: '⬢⬡⬟⬠⬢⬣⬤⬥⬦⬧⬨⬩⬪⬫⬬⬭⬮⬯⬰⬱⬲⬳⬴⬵⬶⬷⬸⬹⬺⬻⬼⬽⬾⬿',
    cosmic: '☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯',
    standard: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
  };

  const morphText = (targetText: string, callback?: () => void) => {
    const duration = 35; // Optimized timing for smooth effect
    const morphDuration = 15; // More morphing iterations for better effect
    let currentText = '';
    let charIndex = 0;

    setIsMorphing(true);
    setMorphProgress(0);

    const morphChar = () => {
      if (charIndex >= targetText.length) {
        setDisplayText(targetText);
        setIsMorphing(false);
        setMorphProgress(100);
        callback?.();
        return;
      }

      let morphCount = 0;
      const targetChar = targetText[charIndex];

      // Update progress
      const progress = (charIndex / targetText.length) * 100;
      setMorphProgress(progress);

      // Choose character set based on message content with enhanced logic
      let charSet = matrixChars;
      if (
        targetText.includes('sacred') ||
        targetText.includes('geometry') ||
        targetText.includes('φ') ||
        targetText.includes('Golden ratio')
      ) {
        charSet = consciousnessChars.sacred + consciousnessChars.geometric;
      } else if (
        targetText.includes('consciousness') ||
        targetText.includes('archetypal') ||
        targetText.includes('mystical') ||
        targetText.includes('wisdom')
      ) {
        charSet = consciousnessChars.mystical + consciousnessChars.cosmic;
      } else if (
        targetText.includes('portal') ||
        targetText.includes('chamber') ||
        targetText.includes('octagonal') ||
        targetText.includes('fractal')
      ) {
        charSet = consciousnessChars.geometric + consciousnessChars.sacred;
      } else if (
        targetText.includes('frequency') ||
        targetText.includes('Hz') ||
        targetText.includes('resonance') ||
        targetText.includes('coherence')
      ) {
        charSet = consciousnessChars.cosmic + consciousnessChars.mystical;
      }

      const morphInterval = setInterval(() => {
        if (morphCount >= morphDuration) {
          currentText += targetChar;
          setDisplayText(currentText);
          charIndex++;
          clearInterval(morphInterval);
          setTimeout(morphChar, duration / 4); // Faster transition between characters
        } else {
          const randomChar =
            targetChar === ' ' ? ' ' : charSet[Math.floor(Math.random() * charSet.length)];

          // Track current morphing character and intensity
          setMorphingChar(randomChar);
          setMorphIntensity((morphCount / morphDuration) * 100);

          // Enhanced preview with consciousness-themed effects
          const remainingText = targetText.slice(charIndex + 1);
          const fadedRemaining = remainingText
            .split('')
            .map((char, i) => {
              if (i < 2) return char; // Show next 2 characters clearly
              if (i < 5) return Math.random() > 0.5 ? char : '·'; // Fade with dots
              if (i < 8) return Math.random() > 0.7 ? char : '∞'; // Use consciousness symbols
              return Math.random() > 0.8 ? char : ' '; // Randomly show/hide distant characters
            })
            .join('');

          setDisplayText(currentText + randomChar + fadedRemaining);
          morphCount++;
        }
      }, duration);
    };

    morphChar();
  };

  // Initialize GSAP animations
  useEffect(() => {
    const ctx = gsap.context(() => {
      // Animate background gradient
      if (backgroundRef.current) {
        gsap.to(backgroundRef.current, {
          backgroundPosition: '200% 200%',
          duration: 8,
          repeat: -1,
          ease: 'none',
        });
      }

      // Animate header entrance
      if (headerRef.current) {
        gsap.fromTo(
          headerRef.current,
          { opacity: 0, y: -50 },
          { opacity: 1, y: 0, duration: 1, ease: 'power2.out' }
        );
      }

      // Animate sacred geometry
      if (geometryRef.current) {
        gsap.fromTo(
          geometryRef.current,
          { opacity: 0, scale: 0.5, rotation: -180 },
          { opacity: 0.3, scale: 1, rotation: 0, duration: 2, ease: 'power2.out', delay: 0.5 }
        );
      }
    }, containerRef);

    return () => ctx.revert();
  }, []);

  // Handle boot message progression with GSAP animations (single line)
  useEffect(() => {
    if (currentIndex >= BOOT_MESSAGES.length) {
      // Boot complete with final animation
      const timer = setTimeout(() => {
        if (progressRef.current) {
          gsap.to(progressRef.current, {
            scale: 1.05,
            duration: 0.5,
            yoyo: true,
            repeat: 1,
            ease: 'power2.inOut',
            onComplete: () => onBootComplete?.(),
          });
        } else {
          onBootComplete?.();
        }
      }, 500);
      return () => clearTimeout(timer);
    }

    const message = BOOT_MESSAGES[currentIndex];
    if (message) {
      const timer = setTimeout(() => {
        // Animate out current message if exists
        if (messagesRef.current && currentMessage) {
          gsap.to(messagesRef.current, {
            opacity: 0,
            y: -10,
            duration: 0.2,
            ease: 'power2.in',
            onComplete: () => {
              // Set new message and start Matrix morphing
              setCurrentMessage(message);
              setCurrentIndex(prev => prev + 1);
              setBootProgress(((currentIndex + 1) / BOOT_MESSAGES.length) * 100);

              if (messagesRef.current) {
                gsap.fromTo(
                  messagesRef.current,
                  { opacity: 0, y: 10 },
                  {
                    opacity: 1,
                    y: 0,
                    duration: 0.3,
                    ease: 'power2.out',
                    onComplete: () => {
                      // Start Matrix morphing effect
                      morphText(message.message);
                    },
                  }
                );
              }
            },
          });
        } else {
          // First message - just animate in and start morphing
          setCurrentMessage(message);
          setCurrentIndex(prev => prev + 1);
          setBootProgress(((currentIndex + 1) / BOOT_MESSAGES.length) * 100);

          if (messagesRef.current) {
            gsap.fromTo(
              messagesRef.current,
              { opacity: 0, y: 10 },
              {
                opacity: 1,
                y: 0,
                duration: 0.3,
                ease: 'power2.out',
                onComplete: () => {
                  // Start Matrix morphing effect
                  morphText(message.message);
                },
              }
            );
          }
        }
      }, message.delay);

      return () => clearTimeout(timer);
    }

    return () => {};
  }, [currentIndex, currentMessage, onBootComplete]);

  const getMessageColor = (level: BootMessage['level']) => {
    switch (level) {
      case 'system':
        return 'text-cyan-400';
      case 'success':
        return 'text-green-400';
      case 'info':
        return 'text-blue-300';
      case 'warning':
        return 'text-yellow-400';
      case 'error':
        return 'text-red-400';
      default:
        return 'text-gray-300';
    }
  };

  const getComponentColor = (component: string) => {
    const colors: Record<string, string> = {
      witness_kernel: 'text-cyan-500',
      archetypal_field: 'text-purple-400',
      sacred_mathematics: 'text-yellow-400',
      platonic_solids: 'text-orange-400',
      fractal_consciousness: 'text-pink-400',
      breath_coherence: 'text-blue-400',
      pythagorean_matrix: 'text-amber-400',
      bodygraph_system: 'text-teal-400',
      archetypal_wisdom: 'text-violet-400',
      hexagram_oracle: 'text-indigo-400',
      temporal_rhythms: 'text-rose-400',
      vedic_astrology: 'text-orange-500',
      genetic_wisdom: 'text-emerald-400',
      enneagram_space: 'text-fuchsia-400',
      sigil_consciousness: 'text-lime-400',
      octagonal_portal: 'text-indigo-500',
      webgl_consciousness: 'text-green-400',
      discovery_realms: 'text-purple-500',
      consciousness_field: 'text-cyan-400',
      sacred_frequencies: 'text-yellow-500',
      witness_api: 'text-blue-500',
      data_collection: 'text-pink-500',
      portal_ready: 'text-cyan-300',
      system: 'text-cyan-400',
    };
    return colors[component] || 'text-gray-400';
  };

  return (
    <div
      ref={containerRef}
      className='w-full h-screen font-mono text-sm overflow-hidden flex flex-col relative'
      style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
    >
      {/* Enhanced Moving Gradient Background with Noise */}
      <div
        ref={backgroundRef}
        className='absolute inset-0 opacity-90'
        style={{
          background: `
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

      {/* Sacred Geometry Background */}
      <div
        ref={geometryRef}
        className='absolute inset-0 flex items-center justify-center pointer-events-none'
      >
        <div className='w-96 h-96 border border-cyan-500/20 rounded-full animate-pulse'>
          <div className='w-full h-full border border-purple-500/20 rounded-full transform rotate-45'>
            <div className='w-full h-full border border-pink-500/20 rounded-full transform -rotate-90'>
              <div className='w-full h-full flex items-center justify-center'>
                <div className='w-48 h-48 border border-yellow-500/30 transform rotate-45'>
                  <div className='w-full h-full border border-cyan-500/30 transform -rotate-45'>
                    <div className='w-full h-full border border-purple-500/30 transform rotate-90' />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Header */}
      <div ref={headerRef} className='relative z-10 p-6 border-b border-cyan-500/30'>
        <div className='flex items-center justify-between'>
          <div>
            <h1 className='text-2xl font-bold text-cyan-400 mb-2'>
              🌀 WitnessOS v2.5.0 - Consciousness Exploration Kernel
            </h1>
            <p className='text-gray-400 text-sm'>
              Sacred geometry • Archetypal wisdom • Quantum consciousness
            </p>
          </div>
          <div className='text-right'>
            <div className='text-cyan-300 text-lg font-mono'>{bootProgress.toFixed(1)}%</div>
            <div className='text-gray-500 text-xs'>
              {currentIndex}/{BOOT_MESSAGES.length} systems
            </div>
          </div>
        </div>
      </div>

      {/* Current Boot Message - Centered */}
      <div className='relative z-10 flex-1 flex items-center justify-center p-6'>
        {currentMessage && (
          <div ref={messagesRef} className='text-center max-w-4xl mx-auto'>
            <div className='flex items-center justify-center space-x-4 mb-4'>
              <span className='text-gray-500 text-sm font-mono'>[{currentMessage.timestamp}]</span>
              <span className={`text-sm font-mono ${getComponentColor(currentMessage.component)}`}>
                {currentMessage.component}:
              </span>
            </div>
            <div
              className={`text-lg font-mono leading-relaxed ${getMessageColor(currentMessage.level)} ${
                isMorphing ? 'animate-pulse' : ''
              }`}
              style={{
                textShadow: isMorphing
                  ? `0 0 ${10 + morphIntensity * 0.5}px currentColor, 0 0 ${20 + morphIntensity}px currentColor, 0 0 ${30 + morphIntensity * 1.5}px currentColor`
                  : '0 0 5px currentColor',
                transition: 'text-shadow 0.1s ease',
                filter: isMorphing ? `hue-rotate(${morphIntensity * 3.6}deg)` : 'none',
              }}
            >
              {displayText || currentMessage.message}
              {isMorphing && (
                <span className='inline-block ml-2 text-cyan-400 animate-spin'>⚡</span>
              )}
            </div>
            {isMorphing && (
              <div className='mt-3 space-y-2'>
                <div className='flex items-center justify-between text-xs text-gray-400'>
                  <span>Consciousness decoding: {morphProgress.toFixed(0)}%</span>
                  <span className='text-cyan-400 font-mono'>
                    Current: <span className='text-purple-400'>{morphingChar}</span>
                  </span>
                </div>
                <div className='w-full bg-gray-800 rounded-full h-1'>
                  <div
                    className='bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 h-1 rounded-full transition-all duration-100'
                    style={{ width: `${morphProgress}%` }}
                  />
                </div>
                <div className='flex justify-center'>
                  <div className='flex space-x-1'>
                    {[...Array(5)].map((_, i) => (
                      <div
                        key={i}
                        className={`w-1 h-1 rounded-full transition-all duration-200 ${
                          i < morphIntensity / 20 ? 'bg-cyan-400' : 'bg-gray-600'
                        }`}
                        style={{
                          animationDelay: `${i * 100}ms`,
                        }}
                      />
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Progress Bar */}
      <div ref={progressRef} className='relative z-10 p-6 border-t border-cyan-500/30'>
        <div className='w-full bg-gray-800 rounded-full h-2 mb-2'>
          <div
            className='bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 h-2 rounded-full transition-all duration-300 ease-out'
            style={{ width: `${bootProgress}%` }}
          />
        </div>
        <div className='flex justify-between text-xs text-gray-400'>
          <span>Consciousness systems initializing...</span>
          <span>{Math.round(bootProgress)}% complete</span>
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

export default EnhancedWitnessOSBootSequence;
