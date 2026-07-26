# PATTERN - 20-Phase Bifrost Metropolis Evolution Plan

**Goal:** Upgrade live page using curriculum knowledge
**Source:** Bifrost Omega Curriculum + WebGPU mastery

## PHASE PROGRESSION

| Phase | Component | Target | Code Change |
|-------|-----------|--------|-------------|
| 1 | Matrix Rain | 500k → 1M particles | StorageBuffer: 500k → 1M |
| 2 | Workgroup Size | Optimize 256/512 | `workgroup_size(256)` tuning |
| 3 | Frustum Culling | GPU-cull by distance | Compute culling pass |
| 4 | Physics Pipeline | Multi-pass compute | velocity→position→collision |
| 5 | Splash System | Impact particle effects | Secondary buffer + spawn |
| 6 | Volumetric Clouds | 3D ray marching | WGSL ray-march shader |
| 7 | God Rays | Screen-space shafts | `sunPosition` uniform |
| 8 | Cloud Shadows | Project onto ground | Shadow map from clouds |
| 9 | Terrain SDf | Fractal landscape | fBm noise generator |
| 10 | Dynamic LOD | Building detail scale | `drawRange` per mesh |
| 11 | HDR Pipeline | 0-20+ stops | `toneMappingExposure` ctrl |
| 12 | Multi-scale Bloom | 5 mip levels | Read 5x downsampled |
| 13 | Color LUT | Filmic grading | 3D texture sampler |
| 14 | Motion Blur | Velocity history | Velocity buffer readback |
| 15 | Temporal AA | 0.5ms jitter | History accumulation |
| 16 | Procedural City | Gen-model buildings | Voronoi city layout |
| 17 | Flocking AI | 200 → 500 agents | Improved boid rules |
| 18 | Audio Engine | Procedural drone | Web Audio + sync |
| 19 | Physics Demo | Click to destroy | Rapier WASM integration |
| 20 | Perf Dashboard | FPS/memory stats | Overlay with dat.GUI |

---

## IMPLEMENTATION ORDER

### Weeks 1-2: Particle Systems (Phases 1-5)
- Replace PointsMaterial rain with compute-shader update
- Add workgroup optimization
- Implement frustum culling
- Multi-stage physics compute

### Weeks 3-4: Atmosphere (Phases 6-8)
- Volumetric cloud shader
- God rays from sun
- Dynamic cloud shadows

### Weeks 5-6: World Generation (Phases 9-10)
- SDF terrain
- LOD switching

### Weeks 7-8: Rendering Polish (Phases 11-15)
- HDR
- Bloom, color grading
- Motion blur, TAA

### Weeks 9-10: World Enhancement (Phases 16-17)
- Procedural buildings
- More flocking agents

### Weeks 11-12: Audio + Interaction (Phases 18-19)
- Procedural ambient drone
- Physics-based destruction

### Week 13: Performance Dashboard (Phase 20)
- Live FPS/mem stats overlay

---

## QUICK WIN (Next 24 Hours)

1. **Increase rain to 1M** - Change `RAIN_COUNT` const
2. **Add FPS overlay** - Simple div update in animation loop  
3. **Tweak bloom** - Increase `strength` to 1.2+

Then proceed to Phase 2 compute shader optimization.