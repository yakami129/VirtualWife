import { LipSyncAnalyzeResult } from "./lipSyncAnalyzeResult";

const TIME_DOMAIN_DATA_LENGTH = 2048;

export class LipSync {
  public readonly audio: AudioContext;
  public readonly analyser: AnalyserNode;
  public readonly timeDomainData: Float32Array;
  public previousValue: number ;

  public constructor(audio: AudioContext) {
    this.audio = audio;
    this.previousValue = 0
    this.analyser = audio.createAnalyser();
    this.timeDomainData = new Float32Array(TIME_DOMAIN_DATA_LENGTH);
  }

  public update(): LipSyncAnalyzeResult {
    this.analyser.getFloatTimeDomainData(this.timeDomainData);
    
    let volume = 0.0;
    for (let i = 0; i < TIME_DOMAIN_DATA_LENGTH; i++) {
      volume = Math.max(volume, Math.abs(this.timeDomainData[i]));
    }
    
    // 引入随机性因素
    const randomFactor = (Math.random() * 0.1) + 0.95;
    volume = 1 / (1 + Math.exp(-45 * volume * randomFactor + 5));
    
    if (volume < 0.1) {
      volume = 0;
    } else if (volume > 0.9) {
      volume = 1;
    }
    
    // 应用缓动函数进行平滑和细腻的变化
    const easedVolume = this.easeValue(volume, 0.3) * 3; // 调整缓动因子以控制变化速度
    return {
      volume: easedVolume,
    };
  }
  
  private easeValue(currentValue: number, easingFactor: number): number {
    // 使用缓动函数调整数值变化速度
    const targetValue = currentValue;
    const easedValue = (targetValue - this.previousValue) * easingFactor + this.previousValue;
    this.previousValue = easedValue;
    return easedValue;
  }

  public async playFromArrayBuffer(buffer: ArrayBuffer, onEnded?: () => void) {

    let bufferSource;

    try {
      const audioBuffer = await this.audio.decodeAudioData(buffer);
      bufferSource = this.audio.createBufferSource();
      bufferSource.buffer = audioBuffer;
      bufferSource.connect(this.audio.destination);
      bufferSource.connect(this.analyser);
      bufferSource.start();
    } catch (error) {
      console.error('Error while trying to play from array buffer:', error);
    } finally {
      if (onEnded) {
        bufferSource?.addEventListener("ended", onEnded);
      }
      if (!bufferSource) {
        onEnded?.apply("")
      }
    }
  }

  public async playFromURL(url: string, onEnded?: () => void) {
    const res = await fetch(url);
    const buffer = await res.arrayBuffer();
    this.playFromArrayBuffer(buffer, onEnded);
  }
}
