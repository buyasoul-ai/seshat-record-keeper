# SOUL-NOTE - Bifrost Omega Curriculum: Phase 1 Compute Shader Mastery

**Date:** 2026-07-25
**Source:** TEC's Masterclass
**Goal:** 1M particles + collision + splash + wind

## PHASE 1: COMPUTE SHADER MASTERY (Days 1–5)

### DAY 1: Async Compute Pipelines
**Task:** Multi-stage rain: velocity → position → collision

```javascript
// TSL: Compute pipeline for particle updates
import { Fn, globalId, storage, uniform, sin, cos, time, vec4, float, uint, If } from 'three/tsl';

const particleStruct = { position: 'vec4', velocity: 'vec4' };
const PARTICLE_COUNT = 1000000;

// Initial buffer setup
const particleBuffer = new THREE.StorageBuffer(particleStruct, PARTICLE_COUNT);

// Stage 1: Apply forces (gravity + wind)
const updateForces = Fn(() => {
    const id = globalId.x;
    If(id.greaterThanEqual(uint(PARTICLE_COUNT)), () => { return; });
    
    const particle = particleBuffer.element(id);
    const pos = particle.position;
    const vel = particle.velocity;
    
    // Gravity (Y downward)
    vel.y.subAssign(0.001);
    
    // Wind shear (horizontal + vertical variation)
    const windX = sin(time.mul(0.5).add(id.mul(0.00001))).mul(0.002);
    const windY = cos(time.mul(0.3).add(id.mul(0.000007))).mul(0.0005);
    
    pos.x.addAssign(vel.x.addAssign(windX));
    pos.y.addAssign(vel.y.addAssign(windY));
    pos.z.addAssign(vel.z);
})();

// Stage 2: Boundary collision (ground at Y=0)
const handleCollision = Fn(() => {
    const id = globalId.x;
    If(id.greaterThanEqual(uint(PARTICLE_COUNT)), () => { return; });
    
    const particle = particleBuffer.element(id);
    const pos = particle.position;
    const vel = particle.velocity;
    
    If(pos.y.lessThan(0), () => {
        pos.y.assign(0);
        vel.y.mulAssign(-0.7); // Bounce with damping
        // Randomize horizontal velocity on bounce
        vel.x.addAssign((Math.random() - 0.5) * 0.01);
    });
    
    // Water boundary (simulated lake area)
    const distToCenter = pos.x.length() + pos.z.length();
    If(distToCenter.lessThan(5), () => {
        pos.y.assign(Math.random().mul(3).add(3)); // Reset to top
    });
})();
```

### DAY 2: Workgroup Shared Memory
**Goal:** Reduce global memory bandwidth by caching neighbors

```wgsl
// WGSL: Shared memory optimization
var<workgroup> localPositions: array<vec4<f32>, 256>;
var<workgroup> localVelocities: array<vec4<f32>, 256>;

@compute @workgroup_size(256)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    const localId = gid.x % 256u;
    const particleIdx = gid.x;
    
    // Load into shared memory with stride
    localPositions[localId] = positionBuffer[particleIdx];
    localVelocities[localId] = velocityBuffer[particleIdx];
    
    workgroupBarrier(); // Ensure all loaded
    
    // Process using local data (fewer global reads)
    for(var i: i32 = 0; i < 64; i++) {
        let neighborIdx = particleIdx + i - 32;
        if(neighborIdx >= 0 && neighborIdx < PARTICLE_COUNT) {
            let neighborPos = localPositions[localId + i - 32];
            // Neighbor-based processing here
        }
    }
}
```

### DAY 3: Indirect Dispatch
**Goal:** Dynamic particle count based on camera distance

```javascript
// Count particles in frustum
const counterBuffer = renderer.createStorageBuffer({ count: 'uint' }, 1);

const countVisible = Fn(() => {
    const id = globalId.x;
    If(id.greaterThanEqual(uint(PARTICLE_COUNT)), () => { return; });
    // Test position against frustum planes stored in uniform buffers
    // Increment counter for visible particles
})();

// Indirect draw setup
const argsBuffer = new THREE.StorageBuffer(
    new Uint32Array([0, 0, 0, 0, 0]), // [vertexCount, instanceCount, firstVertex, firstInstance, baseInstance]
    1
);

// Read back and dispatch only visible particles
renderer.compute(countVisible);
```

### DAY 4: Splash Generation
**Task:** Secondary particle buffer for impact effects

```javascript
// Splash particle struct (simpler, shorter lifespan)
const splashStruct = { position: 'vec4', velocity: 'vec4', age: 'float' };
const SPLASH_COUNT = 10000;

const splashBuffer = new THREE.StorageBuffer(splashStruct, SPLASH_COUNT);

const createSplat = Fn(() => {
    const id = globalId.x;
    If(id.greaterThanEqual(uint(PARTICLE_COUNT)), () => { return; });
    
    const particle = particleBuffer.element(id);
    const pos = particle.position;
    const vel = particle.velocity;
    
    // When particle hits ground with sufficient speed
    If(pos.y.lessThan(0.1).and(vel.y.lessThan(-0.005)), () => {
        // Spawn 5 splash particles per impact
        const splashId = id.mod(uint(SPLASH_COUNT));
        const splash = splashBuffer.element(splashId);
        splash.position = pos;
        splash.velocity = vec4(
            (Math.random() - 0.5) * 0.01,
            -0.01 - Math.random() * 0.005, // Upward
            (Math.random() - 0.5) * 0.01,
            0
        );
        splash.age = 0;
    });
})();
```

### DAY 5: Performance Profiling
**Goal:** Measure occupancy, optimize workgroup size

```javascript
// Query WebGPU adapter limits
const adapter = renderer.getContext().getAdapter();
const limits = adapter.getLimits();
console.log('Max compute workgroup size:', limits.maxComputeWorkgroupSizeX);

// Timing compute dispatch
const start = performance.now();
renderer.compute(myComputeShader);
await renderer.waitForCompletion();
const elapsed = performance.now() - start;
console.log(`Compute took: ${elapsed}ms for ${PARTICLE_COUNT} particles`);

// Optimal workgroup size = largest divisor of particle count
// that fits in limits
```

---

## HARDENED CHALLENGE: DIAGNOSTIC RITUAL

**Task:** Write compute shader updating 1M particles with gravity + wind

**Submission template:**
```javascript
// Your solution here
// Record timing: ____ ms
// Workgroup size: ____
```

**Answer Questions:**
1. Ideal workgroup size: [your answer]
2. Bank conflict avoidance: [your answer]
3. Storage vs Uniform trade-off: [your answer]