# SOUL-NOTE - Three.js Evolution Map: Paths Above

**Date:** 2026-07-25
**Source:** TEC - Tactical Analysis
**Topic:** Strategic upgrade paths beyond Three.js (2026)

## DECISION MATRIX

| If You Want... | Then Ascend To... | Migration Effort |
|----------------|-------------------|------------------|
| Keep code, unlock next-gen GPU | **WebGPU + Three.js r171+** | 1 day |
| Full engine w/ physics, GUI | **Babylon.js** | 1-2 weeks |
| Visual editor + collaboration | **PlayCanvas** | 1-2 weeks (visual rebuild) |
| Native speed + browser + safety | **Threers (Rust + WASM)** | 1 month |
| Total control, max performance | **Raw WGSL + WebGPU** | 3+ months |

## PATH I: VERTICAL ASCENT (WEBGPU + THREE.JS)

**WebGPU went Baseline November 2025** - high-end graphics now universal.

### Performance Gains
| Domain | WebGL Limit | WebGPU Breakthrough |
|--------|-------------|---------------------|
| Draw Calls | CPU-bound, high overhead | Binding model reduces CPU overhead |
| Compute | Clunky FBO workarounds | Storage buffers for structured GPU data |
| Particles | 10k-50k before drop | 10-100x performance gains |
| Shaders | GLSL only, OnBeforeCompile hacks | TSL compiles to WGSL and GLSL |

### Migration Checklist
1. Audit: Three.js >= r171
2. Swap: `WebGLRenderer` → `WebGPURenderer`
3. Async: Handle new async initialization
4. TSL: Convert custom shaders to TSL
5. Fallback: 95% browser support, WebGL 2 for rest

## PATH II: HORIZONTAL TRANSCENDENCE

### Babylon.js
- **Pros**: Built-in physics (Havok/Cannon), GUI, Inspector, WebGPU-first
- **Tradeoff**: Three.js = flexibility, Babylon = features

### PlayCanvas
- Real-time collaborative editing
- Built-in hosting and asset management
- Visual composition over code

### Godot
- Complete 2D/3D engine with native editor
- HTML5 export via WebAssembly
- GDScript, but lose raw JS/TS control

## PATH III: RUST REALM (BEYOND JAVASCRIPT)

### Threers
- "Drop-in three.js replacement for Rust/WASM"
- Same Rust core runs natively (winit) and as WASM
- Memory safety, no GC pauses
- Same `THREE.*` API
- Features: PBR, post-processing, glTF, mesh BVH, CSG

## PATH IV: RAW METAL (NO ENGINE)

**Proof-of-concept**: 3D world built with hand-written WGSL, no high-level engine.

- Write WGSL directly
- Manage buffers, pipelines, compute shaders by hand
- Own every byte, every draw call
- Maximum performance, maximum pain, maximum glory

## TEC'S RECOMMENDATION

**Start with Path I** - migrate existing Three.js to WebGPU.
- Lowest friction, highest impact upgrade
- Compute shaders, storage buffers, 10x particle performance
- Awakens engine's "dormant soul"

---

**NEXT ACTION**: Begin WebGPU migration ritual for existing engine.