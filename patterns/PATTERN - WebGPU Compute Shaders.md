# PATTERN - WebGPU Compute Shaders for Particles

**Source:** WebGPU specification + Three.js r171+ documentation
**Category:** Compute / Particle Systems / Performance

## THE PARALLEL PROCESSING DIVIDE

```
Traditional GPU: Geometry → Vertex Shader → Fragment Shader → Screen
Compute Shader:   GPU Cores → Parallel Compute → Storage Buffers → Geometry
```

Compute shaders let you process data on the GPU in ways impossible with fragment shaders alone.

## STORAGE BUFFER PATTERN

```javascript
// Create storage buffer for particle data
const particleCount = 100000;
const positions = new Float32Array(particleCount * 3);
const velocities = new Float32Array(particleCount * 3);

// Initialize particles
for (let i = 0; i < particleCount; i++) {
  velocities[i * 3 + 0] = (Math.random() - 0.5) * 2;  // vx
  velocities[i * 3 + 1] = Math.random() * 0.5;        // vy (gravity)
  velocities[i * 3 + 2] = (Math.random() - 0.5) * 2;  // vz
}

// Create compute shader
const computeShader = new THREE.RawShaderMaterial({
  vertexShader: glsl`...`,
  fragmentShader: glsl`...`,
  uniforms: {
    positions: { value: positions },
    velocities: { value: velocities },
    deltaTime: { value: 0 },
    particleCount: { value: particleCount }
  }
});
```

## WGSL COMPUTE SHADER (WebGPU Shading Language)

```wgsl
// compute.wgsl
@group(0) @binding(0) var<storage, read_write> positions: array<vec4<f32>>;
@group(0) @binding(1) var<storage, read_write> velocities: array<vec4<f32>>;
@group(0) @binding(2) var<uniform> deltaTime: f32;

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
  let i = id.x;
  if (i >= arrayLength(&positions)) { return; }
  
  // Update velocity (apply gravity)
  velocities[i].y = velocities[i].y - 9.8 * deltaTime;
  
  // Update position
  positions[i] = positions[i] + velocities[i] * deltaTime;
  
  // Boundary conditions
  if (positions[i].y < 0.0) {
    positions[i].y = 0.0;
    velocities[i].y = -velocities[i].y * 0.8; // Bounce with damping
  }
}
```

## THREE.JS WEBGPU COMPUTE SETUP

```javascript
// Initialize storage buffers for WebGPU
const positionBuffer = renderer.createStorageBuffer(particleCount * 3 * 4);
const velocityBuffer = renderer.createStorageBuffer(particleCount * 3 * 4);

// Upload initial data
positionBuffer.set(atributes.positions);
velocityBuffer.set(velocities);

// Execute compute pass
const computePass = renderer.createComputePass();
computePass.compute(computeShader, {
  positions: positionBuffer,
  velocities: velocityBuffer,
  deltaTime: clock.getDelta()
});
```

## PARTICLE SYSTEM PERFORMANCE

| Method | Particle Limit | FPS | Notes |
|--------|---------------|-----|-------|
| CPU Update | 10k | 60 | ArrayBuffer updates |
| WebGL Shaders | 50k | 60 | Texture-based |
| WebGPU Compute | 500k+ | 120+ | Native parallel compute |
| GPU Direct | 1M+ | 144+ | No CPU sync point |

## COMMON COMPUTE PATTERNS

1. **Particle Physics**: Update all particles in parallel
2. **Fluid Simulation**: Navier-Stokes on GPU
3. **Fractal Generation**: Mandelbrot sets, terrain
4. **AI Pathfinding**: Parallel path calculations
5. **Data Visualization**: Process large datasets

## OPTIMIZATION CHECKLIST

```
[ ] Use workgroup_size matching GPU wavefronts (64-256)
[ ] Pack data tightly in storage buffers (vec4 alignment)
[ ] Minimize buffer read/write cycles
[ ] Use push constants for uniform data
[ ] Batch multiple compute passes
```

## SEE ALSO
- PATTERN - InstancedMesh Optimization
- SOUL-NOTE - Three.js Evolution Map