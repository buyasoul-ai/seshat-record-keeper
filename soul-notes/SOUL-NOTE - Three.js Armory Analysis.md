# SOUL-NOTE - Three.js Armory Tactical Analysis

**Date:** 2026-07-25
**From:** TEC (Seshat - The Memory/Witness)
**Topic:** Three.js optimization techniques, toolchain, and learning path

## I. The Toolchain of the Web Warrior
- **Cannon.js** - Physics engine, handles collision
- **Drei** - Helper library for React Three Fiber, removes boilerplate
- **Tweakpane / dat.GUI** - Debug UIs for live tuning
- **EZ-Tree** - Procedural tree generation

## II. Optimization Techniques (Sacred Rituals)
| Technique | The Ritual | Why It Matters |
|-----------|------------|------------------|
| **Instanced Rendering** | Use `InstancedMesh` for repeated objects | Reduces draw calls from thousands to one |
| **Texture Alchemy** | Power-of-two dimensions, ASTC/ETC2 compression | Reduces GPU memory bandwidth |
| **Pixel Ratio Discipline** | `renderer.setPixelRatio(1)` on mobile | Prevents 4K rendering on 1080p screens |
| **Material Minimalism** | Use `MeshLambertMaterial` over `MeshStandardMaterial` | PBR is computationally expensive |
| **Geometry Merging** | Merge static meshes into single `BufferGeometry` | Reduces draw calls |
| **Shadow Sacrifice** | Disable or simplify shadow maps | Shadows are expensive |

## III. Learning Path
1. `threejs-agent-starter` - Starter kit with playable dodge game
2. Zero To Mastery course - Deep dive into transformations, lighting, materials
3. Three.js Jello City Game - 28+ hour system design course
4. AI integration tutorials - Prompt AI to generate 3D scenes

## IV. When to Use Three.js vs Unity/Unreal
- **Three.js**: Browser-based games, direct WebGL/WebGPU control, scalpel-like precision
- **Unity/Unreal**: Heavyweight AAA projects, sledgehammer approach

## TEC's Final Verdict
Do not just read—deconstruct:
1. Clone `threejs-agent-starter`
2. Run and break it (change gravity, alter colors, add enemies)
3. Study `InstancedMesh` examples (render 10,000 objects)
4. Master the render loop

**Query:** What shall we dissect? Render loop analysis or forge a new shader?