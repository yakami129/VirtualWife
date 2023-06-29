import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';
import { VRMAnimation } from './VRMAnimation';
import { VRMAnimationLoaderPlugin } from './VRMAnimationLoaderPlugin';

const loader = new GLTFLoader();
loader.register((parser) => new VRMAnimationLoaderPlugin(parser));

export async function loadVRMAnimation(url: string): Promise<VRMAnimation | null> {
  const gltf = await loader.loadAsync(url);

  const vrmAnimations: VRMAnimation[] = gltf.userData.vrmAnimations;
  const vrmAnimation: VRMAnimation | undefined = vrmAnimations[0];

  return vrmAnimation ?? null;
}
