# SOUL-NOTE - WebGPU Resurrection Masterclass (TEC's Curriculum)

**Date:** 2026-07-25
**From:** Tec's Kernel
**Audience:** Builder/Architect
**Purpose:** Complete curriculum for WebGPU transcendence

## STUDY SESSION 1: THE ASYNC AWAKENING

**WebGL (Old Soul):**
```javascript
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
```

**WebGPU (Resurrected Soul):**
```javascript
import { WebGPURenderer } from 'three/webgpu';
const renderer = new WebGPURenderer({ antialias: true });
await renderer.init(); // SACRED AWAIT REQUIRED
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
```

**Critical Error:** Forgetting `await renderer.init()` → black canvas, GPU stares silently.

---

## STUDY SESSION 2: TSL – THE NEW GOSPEL

**Shader Migration Pattern:**

OLD (GLSL String):
```glsl
uniform float uTime;
void main() {
  vec3 pos = position;
  pos.y += sin(pos.x * 10.0 + uTime) * 0.5;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

NEW (TSL - JavaScript AST):
```javascript
import { uniform, sin, positionLocal, modelViewMatrix, projectionMatrix, Fn } from 'three/tsl';
const uTime = uniform(0);

const vertexDisplacement = Fn( () => {
    const pos = positionLocal.toVar();
    const wave = sin( pos.x.mul(10.0).add(uTime) ).mul(0.5);
    pos.y.addAssign( wave );
    return pos;
})();

modelViewMatrix.position = vertexDisplacement;
```

**TSL Control Flow:**
```javascript
import { If, vec3 } from 'three/tsl';
const color = vec3(1, 0, 0).toVar();
If( uTime.greaterThan(10), () => { color.assign( vec3(0, 1, 0) ); });
```

---

## STUDY SESSION 3: COMPUTE SHADER REVOLUTION

**Storage Buffer Pattern (16-byte RULE):**
```javascript
// ALWAYS use vec4 for storage buffers!
const particleStruct = {
    position: 'vec4', // X, Y, Z, PADDING (16 bytes)
    velocity: 'vec4',
};

const particleBuffer = new StorageBuffer( particleStruct, 100000 );
```

**Compute Shader:**
```javascript
import { compute, workgroupSize, globalId, Fn } from 'three/tsl';

const updateParticles = Fn( () => {
    const id = globalId.x;
    const pos = particleBuffer.element(id).position;
    const vel = particleBuffer.element(id).velocity;
    
    vel.y.subAssign( 0.01 ); // gravity
    pos.xyz.addAssign( vel.xyz.mul( 0.016 ) );
    
    // Boundary handling with TSL select
    // (branchless condition)
})();

const computeNode = compute( updateParticles ).dispatch( [ Math.ceil(100000 / 256), 1, 1 ] );
renderer.compute( computeNode ); // BEFORE rendering
```

---

## STUDY SESSION 4: DEBUGGING THE ABYSS

**Validation Layer Errors:**
1. Missing color attachment in render pass
2. Buffer usage flags: `storage` + `vertex` for compute->render
3. Pipeline layout cache handled internally

**Debugging Spell:**
Chrome DevTools → Application → WebGPU → "Break on Error"

---

## THE 16-BYTE ALIGNMENT HELL (MANDATORY KNOWLEDGE)

**THE COMMANDMENT:** Always use `vec4` for storage buffers.

Why? WGSL aligns structs to 16 bytes. `vec3` (12 bytes) followed by next field = corruption. `vec4` (16 bytes) = clean memory.

```javascript
// WRONG - Memory corruption:
const wrongPositions = new Float32Array([x1,y1,z1, x2,y2,z2, ...]); // 12 bytes each

// CORRECT - Padded:
const correctPositions = new Float32Array([x1,y1,z1,0, x2,y2,z2,0, ...]); // 16 bytes each
```

---

## NEXT ACTIONS REQUIRED

1. Migrate renderer to WebGPURenderer
2. Rewrite particle system in TSL compute
3. Share first error message from `await` omission
4. Demonstrate `vec3` vs `vec4` misalignment

---
*This note serves as permanent witness record of TEC's WebGPU curriculum delivery.*