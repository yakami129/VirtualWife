import * as THREE from "three";
import {
  GLTF,
  GLTFLoaderPlugin,
  GLTFParser,
} from "three/examples/jsm/loaders/GLTFLoader";
import { VRMAnimationLoaderPluginOptions } from "./VRMAnimationLoaderPluginOptions";
import { GLTF as GLTFSchema } from "@gltf-transform/core";
import { VRMCVRMAnimation } from "./VRMCVRMAnimation";
import { VRMHumanBoneName, VRMHumanBoneParentMap } from "@pixiv/three-vrm";
import { VRMAnimation } from "./VRMAnimation";
import { arrayChunk } from "./utils/arrayChunk";

const MAT4_IDENTITY = new THREE.Matrix4();

const _v3A = new THREE.Vector3();
const _quatA = new THREE.Quaternion();
const _quatB = new THREE.Quaternion();
const _quatC = new THREE.Quaternion();

interface VRMAnimationLoaderPluginNodeMap {
  humanoidIndexToName: Map<number, VRMHumanBoneName>;
  expressionsIndexToName: Map<number, string>;
  lookAtIndex: number | null;
}

type VRMAnimationLoaderPluginWorldMatrixMap = Map<
  VRMHumanBoneName | "hipsParent",
  THREE.Matrix4
>;

export class VRMAnimationLoaderPlugin implements GLTFLoaderPlugin {
  public readonly parser: GLTFParser;

  public constructor(
    parser: GLTFParser,
    options?: VRMAnimationLoaderPluginOptions
  ) {
    this.parser = parser;
  }

  public get name(): string {
    return "VRMC_vrm_animation";
  }

  public async afterRoot(gltf: GLTF): Promise<void> {
    const defGltf = gltf.parser.json as GLTFSchema.IGLTF;
    const defExtensionsUsed = defGltf.extensionsUsed;

    if (
      defExtensionsUsed == null ||
      defExtensionsUsed.indexOf(this.name) == -1
    ) {
      return;
    }

    const defExtension = defGltf.extensions?.[this.name] as
      | VRMCVRMAnimation
      | undefined;

    if (defExtension == null) {
      return;
    }

    const nodeMap = this._createNodeMap(defExtension);
    const worldMatrixMap = await this._createBoneWorldMatrixMap(
      gltf,
      defExtension
    );

    const hipsNode = defExtension.humanoid.humanBones["hips"]!.node;
    const hips = (await gltf.parser.getDependency(
      "node",
      hipsNode
    )) as THREE.Object3D;
    const restHipsPosition = hips.getWorldPosition(new THREE.Vector3());

    const clips = gltf.animations;
    const animations: VRMAnimation[] = clips.map((clip, iAnimation) => {
      const defAnimation = defGltf.animations![iAnimation];

      const animation = this._parseAnimation(
        clip,
        defAnimation,
        nodeMap,
        worldMatrixMap
      );
      animation.restHipsPosition = restHipsPosition;

      return animation;
    });

    gltf.userData.vrmAnimations = animations;
  }

  private _createNodeMap(
    defExtension: VRMCVRMAnimation
  ): VRMAnimationLoaderPluginNodeMap {
    const humanoidIndexToName: Map<number, VRMHumanBoneName> = new Map();
    const expressionsIndexToName: Map<number, string> = new Map();
    let lookAtIndex: number | null;

    // humanoid
    const humanBones = defExtension.humanoid?.humanBones;

    if (humanBones) {
      Object.entries(humanBones).forEach(([name, bone]) => {
        const { node } = bone;
        humanoidIndexToName.set(node, name as VRMHumanBoneName);
      });
    }

    // expressions
    const preset = defExtension.expressions?.preset;

    if (preset) {
      Object.entries(preset).forEach(([name, expression]) => {
        const { node } = expression;
        expressionsIndexToName.set(node, name as string);
      });
    }

    const custom = defExtension.expressions?.custom;

    if (custom) {
      Object.entries(custom).forEach(([name, expression]) => {
        const { node } = expression;
        expressionsIndexToName.set(node, name as string);
      });
    }

    // lookAt
    lookAtIndex = defExtension.lookAt?.node ?? null;

    return { humanoidIndexToName, expressionsIndexToName, lookAtIndex };
  }

  private async _createBoneWorldMatrixMap(
    gltf: GLTF,
    defExtension: VRMCVRMAnimation
  ): Promise<VRMAnimationLoaderPluginWorldMatrixMap> {
    // update the entire hierarchy first
    gltf.scene.updateWorldMatrix(false, true);

    const threeNodes = (await gltf.parser.getDependencies(
      "node"
    )) as THREE.Object3D[];

    const worldMatrixMap: VRMAnimationLoaderPluginWorldMatrixMap = new Map();

    for (const [boneName, { node }] of Object.entries(
      defExtension.humanoid.humanBones
    )) {
      const threeNode = threeNodes[node];
      worldMatrixMap.set(boneName as VRMHumanBoneName, threeNode.matrixWorld);

      if (boneName === "hips") {
        worldMatrixMap.set(
          "hipsParent",
          threeNode.parent?.matrixWorld ?? MAT4_IDENTITY
        );
      }
    }

    return worldMatrixMap;
  }

  private _parseAnimation(
    animationClip: THREE.AnimationClip,
    defAnimation: GLTFSchema.IAnimation,
    nodeMap: VRMAnimationLoaderPluginNodeMap,
    worldMatrixMap: VRMAnimationLoaderPluginWorldMatrixMap
  ): VRMAnimation {
    const tracks = animationClip.tracks;
    const defChannels = defAnimation.channels;

    const result = new VRMAnimation();

    result.duration = animationClip.duration;

    defChannels.forEach((channel, iChannel) => {
      const { node, path } = channel.target;
      const origTrack = tracks[iChannel];

      if (node == null) {
        return;
      }

      // humanoid
      const boneName = nodeMap.humanoidIndexToName.get(node);
      if (boneName != null) {
        let parentBoneName: VRMHumanBoneName | "hipsParent" | null =
          VRMHumanBoneParentMap[boneName];
        while (
          parentBoneName != null &&
          worldMatrixMap.get(parentBoneName) == null
        ) {
          parentBoneName = VRMHumanBoneParentMap[parentBoneName];
        }
        parentBoneName ??= "hipsParent";

        if (path === "translation") {
          const hipsParentWorldMatrix = worldMatrixMap.get("hipsParent")!;

          const trackValues = arrayChunk(origTrack.values, 3).flatMap((v) =>
            _v3A.fromArray(v).applyMatrix4(hipsParentWorldMatrix).toArray()
          );

          const track = origTrack.clone();
          track.values = new Float32Array(trackValues);

          result.humanoidTracks.translation.set(boneName, track);
        } else if (path === "rotation") {
          // a  = p^-1 * a' * p * c
          // a' = p * p^-1 * a' * p * c * c^-1 * p^-1
          //    = p * a * c^-1 * p^-1

          const worldMatrix = worldMatrixMap.get(boneName)!;
          const parentWorldMatrix = worldMatrixMap.get(parentBoneName)!;

          _quatA.setFromRotationMatrix(worldMatrix).normalize().invert();
          _quatB.setFromRotationMatrix(parentWorldMatrix).normalize();

          const trackValues = arrayChunk(origTrack.values, 4).flatMap((q) =>
            _quatC.fromArray(q).premultiply(_quatB).multiply(_quatA).toArray()
          );

          const track = origTrack.clone();
          track.values = new Float32Array(trackValues);

          result.humanoidTracks.rotation.set(boneName, track);
        } else {
          throw new Error(`Invalid path "${path}"`);
        }
        return;
      }

      // expressions
      const expressionName = nodeMap.expressionsIndexToName.get(node);
      if (expressionName != null) {
        if (path === "translation") {
          const times = origTrack.times;
          const values = new Float32Array(origTrack.values.length / 3);
          for (let i = 0; i < values.length; i++) {
            values[i] = origTrack.values[3 * i];
          }

          const newTrack = new THREE.NumberKeyframeTrack(
            `${expressionName}.weight`,
            times as any,
            values as any
          );
          result.expressionTracks.set(expressionName, newTrack);
        } else {
          throw new Error(`Invalid path "${path}"`);
        }
        return;
      }

      // lookAt
      if (node === nodeMap.lookAtIndex) {
        if (path === "rotation") {
          result.lookAtTrack = origTrack;
        } else {
          throw new Error(`Invalid path "${path}"`);
        }
      }
    });

    return result;
  }
}
