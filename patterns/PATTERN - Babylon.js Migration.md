# PATTERN - Three.js to Babylon.js Migration Guide

**Source:** TEC's Tactical Map + Babylon.js documentation
**Category:** Engine Migration / Ecosystem Evolution

## DECISION TREE

```
THREE.JS → BABYLON.JS when you need:
✓ Built-in physics (Havok/Cannon/Ammo)
✓ Visual debugging inspector
✓ Native GUI system
✓ WebGPU-first architecture
✓ Batteries-included approach
```

## CODE MIGRATION PATTERNS

### Scene Creation

```javascript
// THREE.js
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, width/height, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();

// Babylon.js
const scene = new BABYLON.Scene(engine);
const camera = new BABYLON.ArcRotateCamera("cam", 0, 0, 10, BABYLON.Vector3.Zero(), scene);
const renderer = new BABYLON.Engine(canvas, true);
```

### Lighting

```javascript
// THREE.js
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(1, 1, 1);
scene.add(light);

// Babylon.js
const light = new BABYLON.DirectionalLight("dir", new BABYLON.Vector3(1, 1, 1), scene);
```

### Mesh Creation

```javascript
// THREE.js
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial({ color: 0xff0000 });
const mesh = new THREE.Mesh(geometry, material);

// Babylon.js
const mesh = BABYLON.MeshBuilder.CreateBox("box", { size: 1 }, scene);
mesh.material = new BABYLON.StandardMaterial("mat", scene);
mesh.material.diffuseColor = new BABYLON.Color3(1, 0, 0);
```

### Animation Loop

```javascript
// THREE.js
function animate() {
  requestAnimationFrame(animate);
  // update logic
  renderer.render(scene, camera);
}

// Babylon.js
scene.registerBeforeRender(() => {
  // update logic
});
engine.runRenderLoop(() => {
  scene.render();
});
```

## MIGRATION CHECKLIST

```
[ ] Install Babylon.js: npm install babylonjs
[ ] Replace THREE imports with BABYLON
[ ] Convert Scene/Camera/Renderer setup
[ ] Migrate all Lights
[ ] Convert Mesh materials
[ ] Rewrite animation loop
[ ] Test physics (if used)
[ ] Verify WebGPU works
```

## PERFORMANCE NOTES

- Babylon.js often faster out-of-box due to optimizations
- Memory management differences (automatic vs manual)
- Physics integration is seamless (no community plugins)

## SEE ALSO
- SOUL-NOTE - Three.js Evolution Map
- PATTERN - WebGPU Migration