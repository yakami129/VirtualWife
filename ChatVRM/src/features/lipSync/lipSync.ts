import { LipSyncAnalyzeResult } from "./lipSyncAnalyzeResult";

const TIME_DOMAIN_DATA_LENGTH = 2048;

export class LipSync {
  public readonly audio: AudioContext;
  public readonly analyser: AnalyserNode;
  public readonly timeDomainData: Float32Array;

  public constructor(audio: AudioContext) {
    this.audio = audio;

    this.analyser = audio.createAnalyser();
    this.timeDomainData = new Float32Array(TIME_DOMAIN_DATA_LENGTH);
  }

  public update(): LipSyncAnalyzeResult {
    this.analyser.getFloatTimeDomainData(this.timeDomainData);

    let volume = 0.0;
    for (let i = 0; i < TIME_DOMAIN_DATA_LENGTH; i++) {
      volume = Math.max(volume, Math.abs(this.timeDomainData[i]));
    }

    // cook
    volume = 1 / (1 + Math.exp(-45 * volume + 5));
    if (volume < 0.1) volume = 0;

    return {
      volume,
    };
  }

  public async playFromArrayBuffer(buffer: ArrayBuffer, onEnded?: () => void) {
      try {
        const audioBuffer = await this.audio.decodeAudioData(buffer);
        const bufferSource = this.audio.createBufferSource();
        bufferSource.buffer = audioBuffer;

        bufferSource.connect(this.audio.destination);
        bufferSource.connect(this.analyser);
        bufferSource.start();
        if (onEnded) {
          bufferSource.addEventListener("ended", onEnded);
        }
      } catch (error) {
        // 这里捕获了所有的错误，你可以在这里处理错误，比如打印错误信息
        console.error('Error while trying to play from array buffer:', error);
        // 或者你也可以向用户显示一个错误提示，或者是抛出这个异常让上层函数处理
      }
  }

  public async playFromURL(url: string, onEnded?: () => void) {
    const res = await fetch(url);
    const buffer = await res.arrayBuffer();
    this.playFromArrayBuffer(buffer, onEnded);
  }
}
