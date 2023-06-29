import {
  VRMHumanoid,
  VRMLookAt,
  VRMLookAtLoaderPlugin,
} from "@pixiv/three-vrm";
import { GLTF } from "three/examples/jsm/loaders/GLTFLoader";
import { VRMLookAtSmoother } from "./VRMLookAtSmoother";

export class VRMLookAtSmootherLoaderPlugin extends VRMLookAtLoaderPlugin {
  public get name(): string {
    return "VRMLookAtSmootherLoaderPlugin";
  }

  public async afterRoot(gltf: GLTF): Promise<void> {
    await super.afterRoot(gltf);

    const humanoid = gltf.userData.vrmHumanoid as VRMHumanoid | null;
    const lookAt = gltf.userData.vrmLookAt as VRMLookAt | null;

    if (humanoid != null && lookAt != null) {
      const lookAtSmoother = new VRMLookAtSmoother(humanoid, lookAt.applier);
      lookAtSmoother.copy(lookAt);
      gltf.userData.vrmLookAt = lookAtSmoother;
    }
  }
}
