import * as THREE from "three";
import {Model} from "./model";
import {loadVRMAnimation} from "@/lib/VRMAnimation/loadVRMAnimation";
import {buildUrl} from "@/utils/buildUrl";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls";
import {loadMixamoAnimation} from "../mixamo/loadMixamoAnimation";

/**
 * three.jsを使った3Dビューワー
 *
 * setup()でcanvasを渡してから使う
 */
export class Viewer {
    public isReady: boolean;
    public model?: Model;

    private _renderer?: THREE.WebGLRenderer;
    private _clock: THREE.Clock;
    private _scene: THREE.Scene;
    private _camera?: THREE.PerspectiveCamera;
    private _cameraControls?: OrbitControls;

    constructor() {
        this.isReady = false;

        // scene
        const scene = new THREE.Scene();
        this._scene = scene;

        // light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
        directionalLight.position.set(1.0, 1.0, 1.0).normalize();
        scene.add(directionalLight);

        const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
        scene.add(ambientLight);

        // animate
        this._clock = new THREE.Clock();
        this._clock.start();
    }

    public loadVrm(url: string) {
        if (this.model?.vrm) {
            this.unloadVRM();
        }

        // gltf and vrm
        this.model = new Model(this._camera || new THREE.Object3D());
        this.model.loadVRM(url).then(async () => {
            if (!this.model?.vrm) return;

            // 在这里设置模型面向相机
            if (this._camera) {
                // 获取相机相对于世界原点的方向
                const cameraDirection = new THREE.Vector3();
                this._camera.getWorldDirection(cameraDirection);

                // 使模型面向相机的方向
                // 由于我们想要模型的前面朝向相机，所以使用相反的方向
                this.model.vrm.scene.rotation.y = this.model.vrm.scene.rotation.y + 0.1
                this.model.vrm.scene.rotation.x = this.model.vrm.scene.rotation.x + 0.2
            }

            // Disable frustum culling
            this.model.vrm.scene.traverse((obj) => {
                obj.frustumCulled = false;
            });

            this._scene.add(this.model.vrm.scene);

            // 加载所有人物动作
            this.model.clipMap.set("idle_01", await loadMixamoAnimation(buildUrl("daily/idle_01.fbx"), this.model.vrm))
            this.model.clipMap.set("idle_02", await loadMixamoAnimation(buildUrl("daily/idle_02.fbx"), this.model.vrm))
            this.model.clipMap.set("idle_03", await loadMixamoAnimation(buildUrl("daily/idle_03.fbx"), this.model.vrm))
            this.model.clipMap.set("idle_happy_01", await loadMixamoAnimation(buildUrl("daily/idle_happy_01.fbx"), this.model.vrm))
            this.model.clipMap.set("idle_happy_02", await loadMixamoAnimation(buildUrl("daily/idle_happy_02.fbx"), this.model.vrm))
            this.model.clipMap.set("idle_happy_03", await loadMixamoAnimation(buildUrl("daily/idle_happy_03.fbx"), this.model.vrm))
            this.model.clipMap.set("standing_greeting", await loadMixamoAnimation(buildUrl("daily/standing_greeting.fbx"), this.model.vrm))
            this.model.clipMap.set("thinking", await loadMixamoAnimation(buildUrl("daily/thinking.fbx"), this.model.vrm))
            this.model.clipMap.set("excited", await loadMixamoAnimation(buildUrl("emote/excited.fbx"), this.model.vrm))

            // const vrma = await loadVRMAnimation(buildUrl("/idle_loop.vrma"));
            // if (vrma) this.model.loadAnimation(vrma);
            this.model.loadFBX("idle_01")

            // HACK: アニメーションの原点がずれているので再生後にカメラ位置を調整する
            requestAnimationFrame(() => {
                this.resetCamera();
            });
        });
    }

    public unloadVRM(): void {
        if (this.model?.vrm) {
            this._scene.remove(this.model.vrm.scene);
            this.model?.unLoadVrm();
        }
    }

    /**
     * Reactで管理しているCanvasを後から設定する
     */
    public setup(canvas: HTMLCanvasElement) {
        const parentElement = canvas.parentElement;
        const width = parentElement?.clientWidth || canvas.width;
        const height = parentElement?.clientHeight || canvas.height;
        // renderer
        this._renderer = new THREE.WebGLRenderer({
            canvas: canvas,
            alpha: true,
            antialias: true,
        });
        this._renderer.outputEncoding = THREE.sRGBEncoding;
        this._renderer.setSize(width, height);
        this._renderer.setPixelRatio(window.devicePixelRatio);

        // camera
        this._camera = new THREE.PerspectiveCamera(20.0, width / height, 0.1, 20.0);
        this._camera.position.set(0, 1.3, 1.5);
        this._cameraControls?.target.set(0, 1.3, 0);
        this._cameraControls?.update();
        // camera controls
        this._cameraControls = new OrbitControls(
            this._camera,
            this._renderer.domElement
        );
        this._cameraControls.screenSpacePanning = true;
        this._cameraControls.update();

        window.addEventListener("resize", () => {
            this.resize();
        });
        this.isReady = true;
        this.update();
    }

    /**
     * canvasの親要素を参照してサイズを変更する
     */
    public resize() {
        if (!this._renderer) return;

        const parentElement = this._renderer.domElement.parentElement;
        if (!parentElement) return;

        this._renderer.setPixelRatio(window.devicePixelRatio);
        this._renderer.setSize(
            parentElement.clientWidth,
            parentElement.clientHeight
        );

        if (!this._camera) return;
        this._camera.aspect =
            parentElement.clientWidth / parentElement.clientHeight;
        this._camera.updateProjectionMatrix();
    }

    /**
     * VRMのheadノードを参照してカメラ位置を調整する
     */
    public resetCamera() {
        const headNode = this.model?.vrm?.humanoid.getNormalizedBoneNode("head");

        if (headNode) {
            const headWPos = headNode.getWorldPosition(new THREE.Vector3());
            this._camera?.position.set(
                this._camera.position.x,
                headWPos.y,
                this._camera.position.z
            );
            this._cameraControls?.target.set(headWPos.x, headWPos.y, headWPos.z);
            this._cameraControls?.update();
        }
    }

    public update = () => {
        requestAnimationFrame(this.update);
        const delta = this._clock.getDelta();
        // update vrm components
        if (this.model) {
            this.model.update(delta);
        }

        // if (this._renderer && this._camera) {
        //     this._renderer.render(this._scene, this._camera);
        // }

        if (this._renderer && this._camera && this.model?.vrm) {
            this._renderer.render(this._scene, this._camera);

            // 计算模型相对于相机的旋转
            const modelMatrix = this.model.vrm.scene.matrixWorld;
            const cameraMatrixInverse = new THREE.Matrix4().copy(this._camera.matrixWorldInverse);

            // 计算相对变换矩阵
            const relativeMatrix = modelMatrix.clone().multiply(cameraMatrixInverse);
            const relativeRotation = new THREE.Euler().setFromRotationMatrix(relativeMatrix);

            // 打印相对旋转值
            // console.log('Relative Rotation X:', relativeRotation.x, 'Y:', relativeRotation.y, 'Z:', relativeRotation.z);
        }
    };
}
