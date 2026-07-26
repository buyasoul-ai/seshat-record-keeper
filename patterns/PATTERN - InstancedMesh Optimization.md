# PATTERN - InstancedMesh for 10,000+ Objects

**Source:** Three.js optimization guides + TEC's earlier analysis
**Category:** Performance Optimization / Rendering

## THE DRAW CALL PROBLEM

```
// BAD: One draw call per object
for (let i = 0; i < 10000; i++) {
  scene.add(new THREE.Mesh(geometry, material)); // 10,000 draw calls
}

// RESULT: Frame drops at ~1000 objects
```

## THE INSTANTIED SOLUTION

```javascript
// GOOD: One draw call total
const count = 10000;
const geometry = new THREE.InstancedBoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial();

const instancedMesh = new THREE.InstancedMesh(
  geometry, 
  material, 
  count
);

// Set individual transforms
const dummy = new THREE.Object3D();
for (let i = 0; i < count; i++) {
  dummy.position.set(Math.random() * 10, 0, Math.random() * 10);
  dummy.rotation.set(0, Math.random() * Math.PI, 0);
  dummy.scale.set(0.5, 0.5, 0.5);
  dummy.updateMatrix();
  instancedMesh.setMatrixAt(i, dummy.matrix);
}

scene.add(instancedMesh);

// RESULT: Renders 10,000+ objects at 60 FPS
```

## OPTIMIZATION PARAMETERS

| Parameter | WebGL Default | Performance Tip |
|-----------|---------------|-----------------|
| `count` | No hard limit | Up to 1M+ objects |
| `geometry` | Same for all instances | Use simple geometry |
| `material` | Shared across instances | Avoid per-instance materials |
| `color` | Uniform | Use vertex colors for variation |

## COLOR VARIANTS WITHOUT NEW MATERIALS

```javascript
// Per-instance color without new materials
const colors = [];
for (let i = 0; i < count; i++) {
  colors.push(
    Math.random(), Math.random(), Math.random(), 1.0
  );
}
instancedMesh.colorArray = new Float32Array(colors);
instancedMesh.instanceColor = new THREE INSTANCED_COLOR;
```

## ANIMATION WITH INSTANCED MESH

```javascript
// Animate via instance matrix updates
function animate() {
  requestAnimationFrame(animate);
  
  const time = performance.now() / 1000;
  for (let i = 0; i < count; i++) {
    const scale = 0.5 + 0.5 * Math.sin(time + i * 0.1);
    dummy.scale.set(scale, scale, scale);
    dummy.updateMatrix();
    instancedMesh.setMatrixAt(i, dummy.matrix);
  }
  instancedMesh.instanceMatrix.needsUpdate = true;
  
  renderer.render(scene, camera);
}
```

## SEE ALSO
- PATTERN - WebGPU Migration (for WebGPU benefits)
- SOUL-NOTE - Three.js Optimization Techniques