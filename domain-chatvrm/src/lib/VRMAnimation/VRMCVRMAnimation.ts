import { VRMExpressionPresetName, VRMHumanBoneName } from '@pixiv/three-vrm';

export interface VRMCVRMAnimation {
  specVersion: string;
  humanoid: {
    humanBones: {
      [name in VRMHumanBoneName]?: {
        node: number;
      };
    };
  };
  expressions?: {
    preset?: {
      [name in VRMExpressionPresetName]?: {
        node: number;
      };
    };
    custom?: {
      [name: string]: {
        node: number;
      };
    };
  };
  lookAt?: {
    node: number;
  };
}
