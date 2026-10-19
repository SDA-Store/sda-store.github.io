# MASTER UI/UX & DESIGN SYSTEM SPECIFICATION
> **Project Source**: SDA Store Engineering Platform (`New-profile-page-main`)  
> **Target Audience**: AI Agents & Frontend Engineers building identical UI/UX implementations.  
> **Design Philosophy**: High-End Minimalist Monochromatic Editorial with Precision Cyberpunk/Technical HUD Accents, Dual-Texture Typography, and Apple-grade Smooth Motion.

---

## 1. CORE DESIGN IDENTITY & AESTHETIC PRINCIPLES

- **Color Atmosphere**: Warm off-white / editorial canvas (`#fafafa`) as the ground plane, deep ink blacks (`#0a0a0a` / `#171717`), surgical neutral grays (`neutral-100` through `neutral-800`), accented with razor-sharp **Emerald-500** (`#10b981`) live status indicators and subtle domain-specific jewel tones (`#6366f1`, `#06b6d4`, `#f59e0b`, `#a855f7`, `#f43f5e`).
- **Texture & Depth**: Subtle SVG fractal noise overlay (3% opacity `mix-blend-overlay`), 24px subtle geometric grid lines with radial fade mask, and heavy Gaussian ambient glow blurs (`blur-[120px]` to `blur-[140px]`).
- **Signature Typography**: Asymmetrical juxtaposition of **Ultra-Heavy Sans Uppercase** (`font-sans font-black tracking-tighter leading-[0.88]`) paired with **Outlined Italic Serif** (`font-serif font-light italic stroke-text`).
- **Corner Curvature (Beveling / Radii)**: Pill-shaped controls (`rounded-full`), generous container curvatures (`rounded-3xl` / 24px), medium HUD panels (`rounded-2xl` / 16px), and crisp micro-chips (`rounded-xl` / `rounded-lg`).
- **Motion & Smoothness**: Decisive Apple-style ease-out curve (`cubic-bezier(0.16, 1, 0.3, 1)`), spring physics (`stiffness: 180–500, damping: 25–28`), interactive fluid custom cursor with `mix-blend-difference`, and intersection-observer driven scroll-reveals with zero hydration flash.

---

## 2. COLOR PALETTE & TOKEN SPECIFICATIONS

### 2.1 Base Surface & Monochromatic Tokens
| Token | Tailwind Class | Hex / Raw Value | Purpose |
| :--- | :--- | :--- | :--- |
| **Page Background** | `bg-[#fafafa]` | `#fafafa` | Main viewport canvas, body background |
| **Card Surface (Pure White)** | `bg-white` | `#ffffff` | Primary container surface for cards, floating nav, modal |
| **Card Surface (Subtle Tint)** | `bg-neutral-50` | `#f9fafb` | Inner nested boxes, dropdown backgrounds, secondary chips |
| **Muted Surface** | `bg-neutral-100` | `#f3f4f6` | Segmented toggle tracks, tech stack pills, icon wells |
| **Subtle Border** | `border-neutral-200` | `#e5e7eb` (`rgba(0,0,0,0.08)`) | Primary divider and card boundary stroke |
| **Interactive Border (Hover)** | `hover:border-neutral-400` | `#9ca3af` | Card hover state border transition |
| **Dark Blueprint Panel** | `bg-neutral-950` | `#0a0a0a` | Technical terminal HUD containers, Windows bezel |
| **Dark Nested Box** | `bg-neutral-900` | `#171717` | Code blocks, hook cards inside terminal |
| **Dark Border** | `border-neutral-800` | `#262626` | Dark terminal inner borders and dividers |
| **Primary Text** | `text-neutral-900` | `#0f172a` / `#171717` | Main headings, strong titles, active links |
| **Secondary Text** | `text-neutral-700` | `#374151` | High-contrast body, active menu items |
| **Body Muted Text** | `text-neutral-600` | `#4b5563` | Paragraphs, summaries, subtitle descriptions |
| **Eyebrow / Metadata Text** | `text-neutral-500` / `text-neutral-400` | `#6b7280` / `#9ca3af` | Monospace tags, labels, numbers, dates |
| **Selection Highlight** | `selection:bg-neutral-900 selection:text-white` | White on Black | Text highlight color |

### 2.2 Functional & Accent Colors
| Accent Role | Light Variant | Core Accent | Dark / Text Variant | Usage Context |
| :--- | :--- | :--- | :--- | :--- |
| **Live / Active / Verified** | `bg-emerald-50` (`#ecfdf5`) | `bg-emerald-500` (`#10b981`) | `text-emerald-700` / `text-emerald-800` | Live pulse dots, verified chips, freeware badge |
| **AI / Neural / LLM** | `rgba(99,102,241,0.08)` | `#6366f1` (Indigo) | `text-indigo-600` | Neural node visualizations, AI capability tab |
| **Cloud Native / API** | `rgba(6,182,212,0.08)` | `#06b6d4` (Cyan) | `text-cyan-600` | Cloud infra architecture glows and tags |
| **High-Perf Systems** | `rgba(245,158,11,0.08)` | `#f59e0b` (Amber) | `text-amber-600` | Low-level systems, Rust / WebAssembly highlights |
| **Decentralized / ZK** | `rgba(168,85,247,0.08)` | `#a855f7` (Purple) | `text-purple-600` | Zero-knowledge and cryptographic feature accents |
| **Security / DevSecOps** | `rgba(244,63,94,0.08)` | `#f43f5e` (Rose) | `text-rose-600` | Kernel hook cloaking, penetration testing badges |

---

## 3. TYPOGRAPHY SYSTEM & SPECIAL TEXT EFFECTS

### 3.1 Font Stack
```css
/* Standard Font Family Definitions */
font-sans: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
font-serif: 'Playfair Display', 'Newsreader', 'Georgia', serif;
font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace;
```

### 3.2 Typography Hierarchy
- **Mega Hero Statement (`H1`)**:
  ```tsx
  <h1 className="text-[11vw] sm:text-[12vw] md:text-[10vw] lg:text-[8vw] xl:text-[135px] font-sans font-black leading-[0.88] tracking-tighter text-neutral-900 uppercase">
  ```
- **Dual-Texture Outlined Subtitle (`H1 / H2 Companion`)**:
  ```tsx
  <p className="text-[9vw] sm:text-[10vw] md:text-[8vw] lg:text-[7vw] xl:text-[110px] font-serif font-light leading-[0.88] tracking-wide text-transparent uppercase stroke-text-thin">
  ```
- **Section Heading (`H2`)**:
  ```tsx
  <h2 className="font-sans font-black text-4xl sm:text-5xl md:text-7xl lg:text-8xl tracking-tighter text-neutral-900 leading-[0.9] uppercase">
    Pre-Built <br className="hidden md:block" />
    <span className="text-transparent italic font-serif font-light stroke-text">Applications</span>
  </h2>
  ```
- **Section Eyebrow Metadata**:
  ```tsx
  <div className="flex items-center gap-3 mb-6">
    <span className="w-8 h-px bg-neutral-400" />
    <span className="font-mono text-xs uppercase tracking-[0.3em] text-neutral-500">
      01 // Proprietary Software Products
    </span>
  </div>
  ```
- **Card Titles (`H3 / H4`)**:
  - Main Card: `font-sans font-black text-2xl sm:text-3xl md:text-4xl tracking-tight text-neutral-900 leading-tight`
  - Sub-Tile: `font-sans font-black text-xl sm:text-2xl text-neutral-900 mb-2 leading-snug`
- **Editorial Sub-Tagline**:
  ```tsx
  <p className="text-base sm:text-lg text-neutral-600 font-serif italic mb-6 leading-relaxed">
    &ldquo;Stealth desktop runtime with kernel-level screen capture cloaking.&rdquo;
  </p>
  ```
- **Technical Monospace Body**:
  ```tsx
  <p className="text-xs sm:text-sm text-neutral-600 leading-relaxed font-mono">
  ```

### 3.3 CSS Outline & Stroke Text Rules (Zero Skeleton Bug)
```css
/* Placed in globals.css to ensure crisp outline text rendering on all screens */
.stroke-text {
  color: #fafafa !important;
  -webkit-text-stroke: 3px rgba(10, 10, 10, 0.8);
  paint-order: stroke fill;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

@media (min-width: 768px) {
  .stroke-text {
    -webkit-text-stroke: 2.5px rgba(10, 10, 10, 0.8);
  }
}

.stroke-text-thin {
  color: #fafafa !important;
  -webkit-text-stroke: 2.5px rgba(10, 10, 10, 0.7);
  paint-order: stroke fill;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

@media (min-width: 768px) {
  .stroke-text-thin {
    -webkit-text-stroke: 2px rgba(10, 10, 10, 0.7);
  }
}
```

---

## 4. BEVELING, BORDER RADII, BORDERS & SHADOWS

### 4.1 Border Radius Scale
- **Pill Elements (`rounded-full`)**:
  - Primary / Secondary Action buttons (`px-6 py-3.5 rounded-full`)
  - Floating Navbar pill (`px-6 py-3 rounded-full`)
  - Status badges & tag pills (`px-3 py-1 rounded-full`)
  - Step icon circles (`w-10 h-10 rounded-full`)
- **Large Master Cards (`rounded-3xl` / 24px–32px)**:
  - Product feature cards (`p-8 sm:p-12 lg:p-14 rounded-3xl bg-white border border-neutral-200`)
  - Process step containers (`p-8 sm:p-10 rounded-3xl bg-white`)
  - Interactive showcase stage (`rounded-[2rem]`)
- **Medium Panels & HUDs (`rounded-2xl` / 16px)**:
  - System Telemetry HUD card (`p-6 rounded-2xl bg-white border border-neutral-200/90 shadow-sm`)
  - Certification trust chips (`p-6 rounded-2xl bg-white border border-neutral-200/90`)
  - Philosophy callout cards (`p-6 rounded-2xl bg-white`)
  - Monitor emulator frame (`rounded-2xl bg-[#1a1a1a] p-[6px]`)
- **Small Elements & Inputs (`rounded-xl` / 12px & `rounded-lg` / 8px)**:
  - Form inputs (`px-4 py-3 rounded-xl bg-neutral-50 border border-neutral-300`)
  - Sub-feature highlight cards (`p-3.5 rounded-xl border border-neutral-200/80 bg-neutral-50/50`)
  - Tech chips (`px-2.5 py-1 rounded-md bg-neutral-100 text-neutral-700 font-mono text-[10px]`)

### 4.2 Card Bevel Accents & Top Gradient Lines
Every premium showcase card features a micro top accent line embedded flush at the top border:
```tsx
{/* Top 2px Accent Gradient Stroke */}
<div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-neutral-900 via-neutral-400 to-neutral-200" />

{/* Emerald Variant */}
<div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-emerald-600 via-neutral-900 to-neutral-200" />
```

### 4.3 Shadow System
- **Subtle Surface Lift**: `shadow-xs` / `shadow-sm` (`box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);`)
- **Card Hover Elevation**: `hover:shadow-md transition-all duration-300`
- **Floating Navbar**: `shadow-sm backdrop-blur-md`
- **Dark Terminal Elevation**: `shadow-xl shadow-black/20`
- **Glow Accents**: `box-shadow: 0 0 50px rgba(99, 102, 241, 0.25)`

---

## 5. BACKGROUND TEXTURES, GRIDS & SACRED GEOMETRY

### 5.1 SVG Noise Texture Overlay
Placed once globally in `layout.tsx` (above all content, `pointer-events-none`):
```tsx
export default function Noise() {
  return (
    <div
      className="pointer-events-none fixed inset-0 z-50 h-full w-full opacity-[0.03] mix-blend-overlay"
      style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
      }}
    />
  );
}
```

### 5.2 Background Geometric Grid Mask
```tsx
{/* Background 24px Grid with Radial Mask */}
<div className="absolute inset-0 bg-[linear-gradient(to_right,#00000008_1px,transparent_1px),linear-gradient(to_bottom,#00000008_1px,transparent_1px)] bg-[size:24px_24px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none" />
```

### 5.3 Ambient Glow Blurs
```tsx
{/* Subtle Hero Center Blur */}
<div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-neutral-200/40 blur-[120px] rounded-full pointer-events-none" />

{/* Section Corner Blur */}
<div className="absolute top-0 right-0 w-[500px] h-[500px] bg-neutral-200/40 rounded-full blur-[140px] pointer-events-none" />
```

### 5.4 Ophanim Celestial Rings (Sacred Geometry)
```tsx
const OphanimRings = ({ className = "" }: { className?: string }) => (
  <motion.div
    initial={{ opacity: 0, scale: 0.8 }}
    animate={{ opacity: 1, scale: 1 }}
    transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] }}
    className={`relative flex items-center justify-center select-none pointer-events-none ${className}`}
  >
    {/* Center Core Dot */}
    <motion.div
      animate={{ scale: [1, 1.2, 1], opacity: [0.7, 1, 0.7] }}
      transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
      className="absolute w-2 h-2 bg-neutral-900 rounded-full shadow-[0_0_10px_rgba(0,0,0,0.1)]"
    />

    {/* Primary Ring */}
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
      className="absolute w-full h-full border border-neutral-300 rounded-full"
      style={{ borderTopColor: 'transparent', borderBottomColor: 'transparent' }}
    />

    {/* Secondary Inclined Ring */}
    <motion.div
      animate={{ rotate: -360, scale: [0.95, 1.05, 0.95] }}
      transition={{ rotate: { duration: 18, repeat: Infinity, ease: "linear" }, scale: { duration: 5, repeat: Infinity, ease: "easeInOut" } }}
      className="absolute w-[85%] h-[85%] border border-neutral-300 rounded-full"
      style={{ borderLeftColor: 'transparent', borderRightColor: 'transparent' }}
    />

    {/* Tertiary Dynamic Ring */}
    <motion.div
      animate={{ rotate: 360, scale: [1, 0.9, 1] }}
      transition={{ rotate: { duration: 12, repeat: Infinity, ease: "linear" }, scale: { duration: 3, repeat: Infinity, ease: "easeInOut", delay: 1 } }}
      className="absolute w-[70%] h-[70%] border-[1.5px] border-neutral-200 rounded-full"
      style={{ borderLeftColor: 'transparent', borderRightColor: 'transparent' }}
    />

    {/* Outer Dashed Ring */}
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
      className="absolute w-[90%] h-[90%] border border-dashed border-neutral-200 rounded-full"
    />
  </motion.div>
);
```

### 5.5 Rotating Brand Circular Stamp
```tsx
<div className="relative w-10 h-10 sm:w-12 sm:h-12 flex items-center justify-center shrink-0">
  <motion.div
    animate={{ rotate: 360 }}
    transition={{ duration: 14, repeat: Infinity, ease: "linear" }}
    className="absolute inset-0"
  >
    <svg viewBox="0 0 100 100" className="w-full h-full overflow-visible opacity-50">
      <path id="circlePath" d="M 50, 50 m -32, 0 a 32,32 0 1,1 64,0 a 32,32 0 1,1 -64,0" fill="transparent" />
      <text className="text-[8px] font-mono uppercase fill-neutral-600 tracking-[0.22em]">
        <textPath href="#circlePath" startOffset="0%">
          ENGINEER • ARCHITECT • SOFTWARE • &nbsp;
        </textPath>
      </text>
    </svg>
  </motion.div>
  <motion.div
    animate={{ scale: [1, 1.4, 1], opacity: [1, 0.6, 1] }}
    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
    className="w-1.5 h-1.5 bg-neutral-900 rounded-full"
  />
</div>
```

---

## 6. MOTION, PHYSICS & "THE SMOOTHNESS"

### 6.1 Master Easing Curve & Timing
- **Deceleration Curve**: `cubic-bezier(0.16, 1, 0.3, 1)` (Ultra-smooth Apple ease-out).
- **Navigation & Drawer Transitions**: `duration: 0.4s` to `0.8s` with `ease: [0.16, 1, 0.3, 1]`.
- **Spring Physics (Cursor / Popups)**: `{ type: 'spring', stiffness: 500, damping: 28, mass: 0.5 }`.
- **Carousel / Tab Switch**: `{ type: 'spring', stiffness: 180, damping: 25 }`.

### 6.2 SSR-Safe Scroll Reveal System
Implemented via CSS + IntersectionObserver:
```css
/* In globals.css */
.scroll-reveal {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), transform 0.75s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}

.scroll-reveal-x-left {
  opacity: 0;
  transform: translateX(-32px);
  transition: opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), transform 0.75s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}

.scroll-reveal-x-right {
  opacity: 0;
  transform: translateX(32px);
  transition: opacity 0.75s cubic-bezier(0.16, 1, 0.3, 1), transform 0.75s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}

.scroll-reveal.is-revealed,
.scroll-reveal-x-left.is-revealed,
.scroll-reveal-x-right.is-revealed {
  opacity: 1 !important;
  transform: translate(0, 0) !important;
}

@media (prefers-reduced-motion: reduce) {
  .scroll-reveal,
  .scroll-reveal-x-left,
  .scroll-reveal-x-right {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }
}
```

```tsx
/* ScrollReveal.tsx React Component */
'use client';
import React, { useEffect, useRef, useState } from 'react';

export default function ScrollReveal({
  children,
  className = '',
  delay = 0,
  direction = 'up',
  threshold = 0.1,
  rootMargin = '0px 0px -40px 0px',
  once = true,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
  direction?: 'up' | 'left' | 'right' | 'none';
  threshold?: number;
  rootMargin?: string;
  once?: boolean;
}) {
  const [isRevealed, setIsRevealed] = useState(false);
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = elementRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsRevealed(true);
            if (once) observer.unobserve(entry.target);
          } else if (!once) {
            setIsRevealed(false);
          }
        });
      },
      { threshold, rootMargin }
    );

    observer.observe(el);
    return () => { if (el) observer.unobserve(el); };
  }, [threshold, rootMargin, once]);

  const baseClass =
    direction === 'left' ? 'scroll-reveal-x-left' :
    direction === 'right' ? 'scroll-reveal-x-right' : 'scroll-reveal';

  return (
    <div
      ref={elementRef}
      style={delay > 0 ? { transitionDelay: `${delay}ms` } : undefined}
      className={`${baseClass} ${isRevealed ? 'is-revealed' : ''} ${className}`}
    >
      {children}
    </div>
  );
}
```

### 6.3 Interactive Custom Cursor (`mix-blend-difference`)
```tsx
'use client';
import { useEffect, useState } from 'react';
import { motion } from 'motion/react';

export default function CustomCursor() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const updateMousePosition = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
      if (!isVisible) setIsVisible(true);
    };

    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (
        target.tagName.toLowerCase() === 'a' ||
        target.tagName.toLowerCase() === 'button' ||
        target.closest('a') ||
        target.closest('button')
      ) {
        setIsHovering(true);
      } else {
        setIsHovering(false);
      }
    };

    const handleMouseLeave = () => setIsVisible(false);

    window.addEventListener('mousemove', updateMousePosition);
    window.addEventListener('mouseover', handleMouseOver);
    document.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      window.removeEventListener('mousemove', updateMousePosition);
      window.removeEventListener('mouseover', handleMouseOver);
      document.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, [isVisible]);

  if (!isVisible) return null;

  return (
    <motion.div
      className="pointer-events-none fixed left-0 top-0 z-[100] h-4 w-4 rounded-full bg-white mix-blend-difference hidden md:block"
      animate={{
        x: mousePosition.x - 8,
        y: mousePosition.y - 8,
        scale: isHovering ? 2.5 : 1,
      }}
      transition={{ type: 'spring', stiffness: 500, damping: 28, mass: 0.5 }}
    />
  );
}
```

### 6.4 Letter-by-Letter Stagger Reveal
```tsx
{name.map((char, i) => (
  <motion.span
    key={i}
    initial={{ y: "100%" }}
    animate={{ y: 0 }}
    transition={{ duration: 0.6, delay: i * 0.02, ease: [0.16, 1, 0.3, 1] }}
    whileHover={{ y: -5 }}
    className="inline-block origin-bottom-left transition-all duration-300 cursor-default"
  >
    {char}
  </motion.span>
))}
```

---

## 7. BUTTON & INTERACTIVE ELEMENT CATALOG

### 7.1 Primary Action Pill Button (Solid Dark)
```tsx
<button className="inline-flex items-center gap-2 px-6 py-3.5 rounded-full bg-neutral-900 text-white font-mono text-xs uppercase tracking-widest font-semibold hover:bg-neutral-800 transition-colors shadow-sm cursor-pointer active:scale-95">
  <span>Explore Software Catalog</span>
  <ArrowUpRight className="w-4 h-4" />
</button>
```

### 7.2 Secondary Action Pill Button (Ghost Outline)
```tsx
<button className="inline-flex items-center gap-2 px-6 py-3.5 rounded-full border border-neutral-300 bg-white text-neutral-800 font-mono text-xs uppercase tracking-widest hover:bg-neutral-50 hover:border-neutral-400 transition-colors cursor-pointer active:scale-95">
  <span>Request 14-Day Evaluation Binary</span>
</button>
```

### 7.3 Glassmorphic Floating Button
```tsx
<button className="group relative px-5 py-2.5 overflow-hidden rounded-full border border-neutral-300 bg-white/80 backdrop-blur-md transition-all hover:bg-neutral-100 hover:border-neutral-400 shadow-sm active:scale-90">
  <span className="relative text-[10px] font-mono uppercase tracking-widest text-neutral-700 flex items-center gap-2.5 font-bold">
    <span className="w-3.5 h-[2px] bg-neutral-700 transition-all duration-300 group-hover:w-6" />
    Menu
  </span>
</button>
```

### 7.4 Directional Expanding Underline Link
```tsx
<Link href="#target" className="relative hover:text-neutral-900 transition-colors py-2 group font-semibold font-mono text-[10px] uppercase tracking-widest text-neutral-600">
  Products
  <span className="absolute left-0 bottom-0 w-full h-[1.5px] bg-neutral-900 scale-x-0 origin-right group-hover:scale-x-100 group-hover:origin-left transition-transform duration-300 ease-out" />
</Link>
```

### 7.5 Segmented Toggle Switch (Custom Tab Pill)
```tsx
<div className="grid grid-cols-2 gap-3 p-1 rounded-2xl bg-neutral-100 border border-neutral-200">
  <button
    type="button"
    onClick={() => setInquiryType('Option 1')}
    className={`py-3 px-4 rounded-xl font-mono text-xs uppercase tracking-wider font-semibold transition-all ${
      inquiryType === 'Option 1'
        ? 'bg-white text-neutral-900 shadow-xs'
        : 'text-neutral-500 hover:text-neutral-900'
    }`}
  >
    Option 1
  </button>
  <button
    type="button"
    onClick={() => setInquiryType('Option 2')}
    className={`py-3 px-4 rounded-xl font-mono text-xs uppercase tracking-wider font-semibold transition-all ${
      inquiryType === 'Option 2'
        ? 'bg-white text-neutral-900 shadow-xs'
        : 'text-neutral-500 hover:text-neutral-900'
    }`}
  >
    Option 2
  </button>
</div>
```

### 7.6 Precision Form Controls
```tsx
<div className="flex flex-col gap-2">
  <label htmlFor="field" className="font-mono text-[10px] uppercase tracking-widest text-neutral-500">
    Field Label
  </label>
  <input
    id="field"
    type="text"
    placeholder="Enter input..."
    className="w-full bg-neutral-50 border border-neutral-300 rounded-xl px-4 py-3 text-sm text-neutral-900 font-mono placeholder:text-neutral-400 focus:outline-none focus:border-neutral-900 transition-colors"
  />
</div>
```

---

## 8. BADGES, CHIPS & TELEMETRY HUD

### 8.1 Live System Telemetry HUD Component
```tsx
<div className="rounded-2xl bg-white border border-neutral-200/90 shadow-sm p-6 flex flex-col justify-between font-mono text-xs relative overflow-hidden hover:border-neutral-300 transition-all duration-300">
  {/* Header Bar */}
  <div className="flex items-center justify-between border-b border-neutral-100 pb-3 mb-4">
    <div className="flex items-center gap-2">
      <Terminal className="w-3.5 h-3.5 text-neutral-800" />
      <span className="font-bold tracking-wider text-neutral-900 uppercase">SYS_TELEMETRY // v2.4</span>
    </div>
    <span className="flex items-center gap-1.5 text-[10px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
      LIVE • IST
    </span>
  </div>

  {/* Key-Value Metrics */}
  <div className="flex flex-col gap-2.5 mb-4 text-[11px]">
    <div className="flex justify-between items-center text-neutral-600">
      <span className="text-neutral-400">ENGINEERING STATUS:</span>
      <span className="text-neutral-900 font-bold">ACCEPTING BUILDS</span>
    </div>
    <div className="flex justify-between items-center text-neutral-600">
      <span className="text-neutral-400">DEPLOYMENT VELOCITY:</span>
      <span className="text-neutral-900 font-semibold">2–4 WKS SPRINT</span>
    </div>
  </div>

  {/* Spotlight Strip */}
  <div className="p-3 rounded-xl bg-neutral-50 border border-neutral-200/80 mb-4 flex flex-col gap-2">
    <div className="text-[9px] uppercase tracking-widest text-neutral-400 font-bold">
      ACTIVE SOFTWARE RELEASES
    </div>
    <div className="flex items-center justify-between text-[11px]">
      <span className="font-bold text-neutral-900">Invisible Browser</span>
      <span className="text-[10px] text-emerald-700 font-semibold">Ready v2.1</span>
    </div>
  </div>
</div>
```

### 8.2 Badge Matrix
- **Dark Sparkle Badge**:
  ```tsx
  <span className="px-3 py-1 rounded-full bg-neutral-900 text-white font-mono text-[10px] uppercase tracking-widest font-semibold flex items-center gap-1.5">
    <Sparkles className="w-3 h-3 text-emerald-400" />
    Flagship Product
  </span>
  ```
- **Emerald Status Chip**:
  ```tsx
  <span className="px-2.5 py-0.5 rounded-full border border-emerald-300 bg-emerald-50 text-emerald-800 font-mono text-[10px] uppercase font-medium">
    ● Ready to License & Deploy
  </span>
  ```
- **Neutral Version Pill**:
  ```tsx
  <span className="px-3 py-1 rounded-full border border-neutral-300 bg-neutral-50 text-neutral-700 font-mono text-[10px] uppercase tracking-widest">
    v2.1 Stable
  </span>
  ```
- **Verified Industry Badge**:
  ```tsx
  <span className="font-mono text-[9px] uppercase tracking-widest text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 flex items-center gap-1">
    <CheckCircle2 className="w-2.5 h-2.5" /> Verified
  </span>
  ```

---

## 9. TECHNICAL BLUEPRINT / TERMINAL CONTAINER (DARK SPEC)

When rendering deep technical specifications, kernel hooks, architecture blocks, or code windows, the UI uses the **Dark Technical Blueprint Window**:

```tsx
<div className="flex flex-col justify-between p-6 sm:p-8 rounded-2xl bg-neutral-950 text-neutral-100 border border-neutral-800 shadow-xl relative overflow-hidden font-mono text-xs">
  {/* Window Titlebar */}
  <div className="flex items-center justify-between border-b border-neutral-800 pb-4 mb-6 text-neutral-400">
    <div className="flex items-center gap-2">
      <span className="w-2.5 h-2.5 rounded-full bg-red-500/80 inline-block" />
      <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/80 inline-block" />
      <span className="w-2.5 h-2.5 rounded-full bg-green-500/80 inline-block" />
      <span className="ml-2 text-neutral-300 font-bold truncate">win32_stealth_host</span>
    </div>
    <span className="text-[10px] text-emerald-400 font-semibold tracking-widest uppercase shrink-0">
      Kernel Hook Active
    </span>
  </div>

  {/* Hook / Feature List */}
  <div className="flex flex-col gap-3.5">
    <div className="p-3 rounded-lg bg-neutral-900 border border-neutral-800">
      <div className="text-[10px] text-neutral-400 uppercase tracking-widest mb-1">[ Hook 01: Capture Protection ]</div>
      <div className="text-neutral-200 font-semibold flex items-center justify-between gap-2">
        <span className="truncate">SetWindowDisplayAffinity(WDA_EXCLUDEFROMCAPTURE)</span>
        <span className="text-emerald-400 text-[10px] shrink-0">HOOKED</span>
      </div>
      <div className="text-[11px] text-neutral-400 mt-1">Hides window from Zoom, Teams, OBS, and screen recorders.</div>
    </div>
  </div>

  {/* Footer Bar */}
  <div className="mt-8 pt-4 border-t border-neutral-800 flex items-center justify-between text-[10px] text-neutral-400">
    <span>Win 10/11 (64-bit)</span>
    <span className="text-neutral-200 font-bold">Rust Core + Win32</span>
  </div>
</div>
```

---

## 10. INTERACTIVE TIMED TAB SHOWCASE & PROGRESS BARS

Used for cycling through ecosystems/skills with synchronized progress bars:
```tsx
const TimerBar = ({ isActive, duration, color }: { isActive: boolean; duration: number; color: string }) => (
  <div className="w-full h-1 bg-neutral-200/80 rounded-full overflow-hidden">
    {isActive && (
      <motion.div
        className="h-full rounded-full"
        style={{ background: color }}
        initial={{ width: '0%' }}
        animate={{ width: '100%' }}
        transition={{ duration: duration / 1000, ease: 'linear' }}
      />
    )}
  </div>
);
```

---

## 11. COMPLETE LAYOUT & GRID ARCHITECTURE

1. **Max Container Widths**:
   - Master bounds: `max-w-[1500px] mx-auto`
   - Content sections: `max-w-7xl mx-auto` (1280px)
2. **Padding Scale**:
   - Mobile: `px-6 py-16`
   - Tablet: `px-12 py-24`
   - Desktop: `px-24 py-32`
   - Top Header Offset: `pt-36 pb-20`
3. **Asymmetric 12-Column Grid**:
   - Left Column (Headings & Narrative): `lg:col-span-7`
   - Right Column (HUDs, Telemetry, Forms, Blueprints): `lg:col-span-5`
   - Equal 2-Column Grid: `grid grid-cols-1 md:grid-cols-2 gap-8`
   - 3-Column Step Grid: `grid grid-cols-1 md:grid-cols-3 gap-8`
4. **Dividers**:
   - `border-t border-neutral-200`
   - `border-b border-neutral-200`

---

## 12. CHECKLIST FOR ANY AGENT GENERATING NEW PAGES

- [ ] **Background**: `bg-[#fafafa]` (never pure white for page root).
- [ ] **Noise Overlay**: Include `<Noise />` in root layout with 3% fractal noise.
- [ ] **Cursor**: Include `<CustomCursor />` with spring physics and difference blend.
- [ ] **Typography**: Headings must use uppercase `font-sans font-black tracking-tighter` paired with `font-serif font-light italic stroke-text`.
- [ ] **Section Numbers**: Every section must begin with `01 // ...` eyebrow line (`<span className="w-8 h-px bg-neutral-400" />`).
- [ ] **Buttons**: Default primary buttons must be `rounded-full bg-neutral-900 text-white font-mono text-xs uppercase tracking-widest font-semibold`.
- [ ] **Cards**: All cards must have `rounded-3xl bg-white border border-neutral-200 shadow-sm hover:border-neutral-400 transition-all`.
- [ ] **Transitions**: All Framer Motion animations must strictly use `ease: [0.16, 1, 0.3, 1]`.
- [ ] **Status Badges**: Live indicators must use `bg-emerald-50 text-emerald-700 border-emerald-200` with pulsing `bg-emerald-500` dot.

---
*End of Master Design System Specification. Exact Drop-in Implementation Standard.*
