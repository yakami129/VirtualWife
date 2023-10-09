import * as THREE from 'three';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader';
import { mixamoVRMRigMap } from './mixamoVRMRigMap';
import { VRM, VRMHumanBoneName } from '@pixiv/three-vrm';

/**
 * Load Mixamo animation, convert for three-vrm use, and return it.
 *
 * @param {string} url A url of mixamo animation data
 * @param {VRM} vrm A target VRM
 * @returns {Promise<THREE.AnimationClip>} The converted AnimationClip
 */
export function loadMixamoAnimation(url: string, vrm: VRM) {
	const loader = new FBXLoader(); // A loader which loads FBX
	return loader.loadAsync(url).then((asset: THREE.Group) => {

		const clip = THREE.AnimationClip.findByName(asset.animations, 'mixamo.com'); // extract the AnimationClip

		const tracks: THREE.KeyframeTrack[] | undefined = []; // KeyframeTracks compatible with VRM will be added here

		const restRotationInverse = new THREE.Quaternion();
		const parentRestWorldRotation = new THREE.Quaternion();
		const _quatA = new THREE.Quaternion();
		const _vec3 = new THREE.Vector3();

		// Adjust with reference to hips height.
		let motionHipsHeight = asset.getObjectByName('mixamorigHips')?.position.y;
		if(motionHipsHeight == null){
			motionHipsHeight = 1
		}
		let vrmHipsY = vrm.humanoid?.getNormalizedBoneNode('hips')?.getWorldPosition(_vec3).y;
		if(vrmHipsY == null){
			vrmHipsY = 1
		}
		const vrmRootY = vrm.scene?.getWorldPosition(_vec3).y;
		const vrmHipsHeight = Math.abs(vrmHipsY - vrmRootY);
		const hipsPositionScale = vrmHipsHeight / motionHipsHeight;

		clip.tracks.forEach((track) => {

			// Convert each tracks for VRM use, and push to `tracks`
			const trackSplitted = track.name.split('.');
			const mixamoRigName = trackSplitted[0];
			const vrmBoneName = mixamoVRMRigMap[mixamoRigName];
			const vrmNodeName = vrm.humanoid?.getNormalizedBoneNode(vrmBoneName as VRMHumanBoneName)?.name;
			const mixamoRigNode = asset.getObjectByName(mixamoRigName);

			if (vrmNodeName != null) {

				const propertyName = trackSplitted[1];

				// Store rotations of rest-pose.
				mixamoRigNode?.getWorldQuaternion(restRotationInverse).invert();
				mixamoRigNode?.parent?.getWorldQuaternion(parentRestWorldRotation);

				if (track instanceof THREE.QuaternionKeyframeTrack) {

					// Retarget rotation of mixamoRig to NormalizedBone.
					for (let i = 0; i < track.values.length; i += 4) {

						const flatQuaternion = track.values.slice(i, i + 4);

						_quatA.fromArray(flatQuaternion);

						// 親のレスト時ワールド回転 * トラックの回転 * レスト時ワールド回転の逆
						_quatA
							.premultiply(parentRestWorldRotation)
							.multiply(restRotationInverse);

						_quatA.toArray(flatQuaternion);

						flatQuaternion.forEach((v, index) => {

							track.values[index + i] = v;

						});

					}

					tracks.push(
						new THREE.QuaternionKeyframeTrack(
							`${vrmNodeName}.${propertyName}`,
							track.times,
							track.values.map((v, i) => (vrm.meta?.metaVersion === '0' && i % 2 === 0 ? - v : v)),
						),
					);

				} else if (track instanceof THREE.VectorKeyframeTrack) {

					const value = track.values.map((v, i) => (vrm.meta?.metaVersion === '0' && i % 3 !== 1 ? - v : v) * hipsPositionScale);
					tracks.push(new THREE.VectorKeyframeTrack(`${vrmNodeName}.${propertyName}`, track.times, value));

				}

			}

		});

		return new THREE.AnimationClip('vrmAnimation', clip.duration, tracks);

	});

}
