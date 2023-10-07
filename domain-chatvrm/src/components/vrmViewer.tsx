import { useContext, useCallback } from "react";
import { ViewerContext } from "../features/vrmViewer/viewerContext";
import { buildVrmModelUrl, generateMediaUrl } from "@/features/media/mediaApi";
import { GlobalConfig, getConfig } from "@/features/config/configApi";

type Props = {
  globalConfig: GlobalConfig;
};

export default function VrmViewer({
  globalConfig,
}: Props) {

  const { viewer } = useContext(ViewerContext);

  const canvasRef = useCallback(
    (canvas: HTMLCanvasElement) => {
      if (canvas) {
        viewer.setup(canvas);
        getConfig().then(data => {
          const url = buildVrmModelUrl(data.characterConfig.vrmModel,data.characterConfig.vrmModelType);
          viewer.loadVrm(url);
          // Drag and DropでVRMを差し替え
          canvas.addEventListener("dragover", function (event) {
            event.preventDefault();
          });
          canvas.addEventListener("drop", function (event) {
            event.preventDefault();

            const files = event.dataTransfer?.files;
            if (!files) {
              return;
            }

            const file = files[0];
            if (!file) {
              return;
            }

            const file_type = file.name.split(".").pop();
            if (file_type === "vrm") {
              const blob = new Blob([file], { type: "application/octet-stream" });
              const url = window.URL.createObjectURL(blob);
              viewer.loadVrm(url);
            }
          });
        })
      }
    },
    [viewer]
  );

  return (
    <div className={"absolute top-0 left-0 w-screen h-[100svh] -z-10"} >
      <canvas ref={canvasRef} className={"h-full w-full"}></canvas>
    </div>
  );
}
