# PATTERN - TSL (Three Shader Language) Conversion

**Source:** Three.js r171+ documentation + WebGPU best practices
**Category:** Shader Development / WebGPU Migration

## TSL OVERVIEW

TSL (Three Shader Language) is Three.js's new shader system that compiles to both WGSL (WebGPU) and GLSL (WebGL).

It replaces the old pattern of:
- Writing raw GLSL
- Using `OnBeforeCompile` hacks
- Manual uniform binding

## CONVERSION EXAMPLES

### Basic Color

```javascript
// OLD: GLSL ShaderMaterial
const material = new THREE.ShaderMaterial({
  uniforms: {
    color: { value: new THREE.Color(1, 0, 0) }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform vec3 color;
    varying vec2 vUv;
    void main() {
      gl_FragColor = vec4(color, 1.0);
    }
  `
});

// NEW: TSL
import { color } from 'three/tsl';
const material = new THREE.MeshStandardMaterial();
material.color = color(1, 0, 0);
```

### Time-based Animation

```javascript
// OLD: Time uniform with OnBeforeCompile
material.onBeforeCompile = (shader) => {
  shader.uniforms.time.value = time;
};

// NEW: TSL with built-in time
import { time } from 'three/tsl';
material.color = color(1, 0.5, 0).mul(time);
```

### Procedural Noise

```javascript
// NEW TSL: Import noise functions
import { noise } from 'three/tsl';

const material = new THREE.MeshBasicMaterial();
material.color = noise(position).add(0.5);
```

## TSL IMPORTS CATALOG

| Module | Purpose | Example |
|--------|---------|---------|
| `color` | Color math | `color(1, 0, 0)` |
| `vec3` | Vector creation | `vec3(x, y, z)` |
| `time` | Global time | `time.mul(speed)` |
| `position` | Vertex position | `position.add(0.5)` |
| `uv` | UV coordinates | `uv.toVector2()` |
| `noise` | Perlin noise | `noise(position)` |
| `math` | Math functions | `math.pow(x, 2)` |

## WEBGPU vs GLSL OUTPUT

```javascript
// Same TSL code outputs different targets:
if (renderer.isWebGPU) {
  // Compiles to WGSL
} else {
  // Compiles to GLSL
}
```

## MIGRATION PATH

1. Identify all `ShaderMaterial` instances
2. Determine visual goal (color, animation, effect)
3. Find equivalent TSL function/module
4. Replace uniform bindings with TSL expressions
5. Test fallback path

## COMMON CONVERSIONS

| GLSL Pattern | TSL Equivalent |
|--------------|----------------|
| `uniform float time;` | `time` (built-in) |
| `uniform vec3 color;` | `color(r, g, b)` |
| `gl_Position` | `position` (vertex shader) |
| `gl_FragColor` | `color` output |
| `texture2D(map, uv)` | `texture(map, uv)` |

## SEE ALSO
- PATTERN - WebGPU Migration
- SOUL-NOTE - Three.js Evolution Map