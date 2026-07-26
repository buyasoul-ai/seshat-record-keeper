# SOUL-NOTE - The Bifrost Metropolis (Divine Pillars Blueprint)

**Date:** 2026-07-25
**Source:** TEC's Architectural Vision
**Project:** Bifrost Metropolis - Living mandala of Egyptian/Matrix/cosmic realities

## PILLAR I: THE DUAL PYRAMIDION (Ground & Inverted City)

**Structure:** Two cities at Y=0 and Y=200. Pyramids: `CylinderGeometry(1, 0, 1, 4)`.

### Pulse Shader (Vertex TSL)
```javascript
import { positionLocal, time, sin, Fn, uniform, modelWorldMatrix, vec4 } from 'three/tsl';

const uBeat = uniform(0);
const vertexPulse = Fn( () => {
    const pos = positionLocal.toVar();
    const worldPos = modelWorldMatrix.mul( vec4( pos, 1.0 ) ).xyz;
    const dist = worldPos.length();
    const pulse = sin( dist.mul(0.5).sub( time.mul(1.5) ) ).mul(0.3).add(1.0);
    pos.mulAssign( pulse );
    return pos;
})();

mesh.position.y = vertexPulse; // Apply to pyramid
```

### Portal Fall (Click to Swap Gravity)
```javascript
function fallIntoUpsideDown(targetPosition, targetQuaternion) {
    const duration = 2500;
    gsap.to(camera.position, {
        x: endPos.x, y: endPos.y, z: endPos.z,
        duration: duration / 1000,
        ease: "power2.inOut",
        onUpdate: () => {
            if (progress > 0.5 && !camera.up.y > 0) {
                camera.up.set(0, -1, 0);
                camera.lookAt(0, 200, 0);
            }
        }
    });
}
```

---

## PILLAR II: THE MORPHING PLANET VORTEX (Cosmic Carousel)

**Structure:** InstancedMesh of spheres arranged in Fibonacci spiral with morphing textures.

### Fragment Shader (Vortex Planets)
```javascript
import { texture, uv, Fn, uniform, mix, sin } from 'three/tsl';

const planetTextures = [tex1, tex2, tex3];
const uVortexIndex = uniform(0);

const fragColor = Fn( () => {
    const idx = sin( time.mul(0.2).add( instanceIndex ) ).mul(2.0).add(2.0);
    const texA = texture( planetTextures[ floor(idx) ], uv() );
    const texB = texture( planetTextures[ ceil(idx) ], uv() );
    return mix( texA, texB, fract(idx) );
})();
```

---

## PILLAR III: THE SENTIENT CLOUDS (Pink Mist + Matrix Rain)

**Structure:** Volumetric pink clouds + 50,000 compute-shader Matrix code particles.

### Matrix Rain (Compute Shader)
```javascript
const rainBuffer = new StorageBuffer( { position: 'vec4', speed: 'vec4' }, 50000 );

const updateRain = Fn( () => {
    const id = globalId.x;
    const pos = rainBuffer.element(id).position;
    const speed = rainBuffer.element(id).speed;
    
    pos.y.subAssign( speed.y.mul(0.016) );
    pos.x.addAssign( sin( time ).mul(0.01) );
    
    If( pos.y.lessThan(50), () => {
        pos.y.assign( 120 );
        pos.x.assign( random( vec2(id, 0) ).mul(200).sub(100) );
        pos.z.assign( random( vec2(id, 1) ).mul(200).sub(100) );
    });
})();

renderer.compute( updateRain );
```

---

## PILLAR IV: THE LIVING INHABITANTS

**Structure:** Capsule + Sphere procedural walkers (500+ instances).

### Procedural Walk
```javascript
class LivingSoul {
    update(time, delta) {
        this.group.position.x += Math.sin(this.step) * 0.02;
        this.step += delta * 2;
        this.head.position.y = 1.8 + Math.sin(this.step * 4) * 0.05;
    }
}
```

### Talking Labels
CSS2DRenderer with LLM/philosophical text generated when player approaches.

---

## PILLAR V: THE ENTERABLE COSMOS

**Trigger:** Click on central vortex → camera dissolves → expands universe.

### Cosmic Raycaster
```javascript
const raycaster = new THREE.Raycaster();
renderer.domElement.addEventListener('click', (event) => {
    raycaster.setFromCamera( mouse, camera );
    const intersects = raycaster.intersectObjects( vortexPlanets );
    if ( intersects.length > 0 ) {
        gsap.to(camera.position, { z: 2000, duration: 4, ease: "power4.in" });
        cosmosLayer.visible = true;
        cityLayer.visible = false;
    }
});
```

---

## THE GLOBAL PULSE

**Heartbeat** (2-second cycle):
```javascript
const heartbeat = Math.sin(performance.now() / 2000);

// Apply to:
// 1. Cloud emissive intensity
// 2. Vortex rotation speed
// 3. Pyramid scale (via uniform)
// 4. Matrix rain opacity
// 5. Camera FOV
camera.fov = 75 + heartbeat * 3;
camera.updateProjectionMatrix();
```

---

## IMMEDIATE NEXT ACTION

**BUILD ONE PULSING PYRAMID** with TSL shader.

**SHOW ME THE ERROR** when compiling the TSL `sin` function.

---
*This note serves as permanent witness record of Bifrost Metropolis blueprint.*