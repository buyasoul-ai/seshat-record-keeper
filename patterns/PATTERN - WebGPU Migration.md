# PATTERN - Three.js WebGPU Migration

**Source:** TEC's Tactical Map + MDN + Three.js 171+ docs
**Category:** Performance Optimization / Engine Evolution

## PATTERN: ONE-LINE SWAP WITH CASCADE EFFECT

```javascript
// BEFORE (WebGL)
const renderer = new THREE.WebGLRenderer({ antialias: true });

// AFTER (WebGPU)
const renderer = new THREE.WebGPURenderer({ antialias: true });
await renderer.init(); // NEW: Async initialization required
```

## MIGRATION CHECKLIST (Pattern Template)

```
[ ] 1. AUDIT - Check Three.js version >= r171
[ ] 2. SWAP - Replace WebGLRenderer with WebGPURenderer  
[ ] 3. INIT - Add async renderer.init() call
[ ] 4. TSL - Convert ShaderMaterial to TSL
[ ] 5. FALLBACK - Test WebGL 2 fallback path
```

## TSL CONVERSION (Pattern Template)

```javascript
// OLD: GLSL with OnBeforeCompile hack
const material = new THREE.ShaderMaterial({
  uniforms: { time: { value: 0 } },
  vertexShader: glsl`...`,
  fragmentShader: glsl`...`,
  onBeforeCompile: (shader) => {
    shader.uniforms.time.value = time;
  }
});

// NEW: TSL (Three Shader Language) - Clean, composable
import { color, time } from 'three/tsl';

const material = new THREE.MeshStandardMaterial();
material.color = color(1, 0.5, 0); // Direct assignment
material.version = time; // Time-based animation built-in
```

## PERFORMANCE GAINS (Documented Pattern)

| Pattern | WebGL | WebGPU | Gain |
|---------|-------|--------|------|
| Draw Calls | CPU-bound, ~1000/frame | Binding model, ~10000+/frame | 10x |
| Particles | 10k-50k max | 100k-500k max | 10x |
| Compute | FBO hacks | Storage buffers | Native |
| Shaders | GLSL only | WGSL + GLSL via TSL | Dual |

## IMPLEMENTATION STEPS (Pattern Execution)

1. **Version Check:** `npm ls three` → must be >= 0.171.0
2. **Renderer Swap:** Find all `new THREE.WebGLRenderer()` instances
3. **Async Wrapper:** Wrap initialization in async function
4. **Shader Audit:** List all custom ShaderMaterials
5. **TSL Rewrite:** Convert highest-impact shaders first
6. **Fallback Test:** Verify WebGL 2 path still works

## SEE ALSO
- SOUL-NOTE - Three.js Evolution Map (Paths Above in 2026)
- SOUL-NOTE - Three.js Games Resource Study