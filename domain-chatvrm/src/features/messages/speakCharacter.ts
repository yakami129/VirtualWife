import { wait } from "@/utils/wait";
import { synthesizeVoice } from "../koeiromap/koeiromap";
import { Viewer } from "../vrmViewer/viewer";
import { Screenplay } from "./messages";
import { Talk } from "./messages";
import axios from 'axios';
import { postRequestArraybuffer } from "../httpclient/httpclient";


const createSpeakCharacter = () => {
  let lastTime = 0;
  let prevFetchPromise: Promise<unknown> = Promise.resolve();
  let prevSpeakPromise: Promise<unknown> = Promise.resolve();

  return (
    screenplay: Screenplay,
    viewer: Viewer,
    onStart?: () => void,
    onComplete?: () => void
  ) => {
    const fetchPromise = prevFetchPromise.then(async () => {
      const now = Date.now();
      if (now - lastTime < 1000) {
        await wait(1000 - (now - lastTime));
      }

      const buffer = await fetchAudio(screenplay.talk).catch(() => null);
      lastTime = Date.now();
      return buffer;
    });

    prevFetchPromise = fetchPromise;
    prevSpeakPromise = Promise.all([fetchPromise, prevSpeakPromise])
      .then(([audioBuffer]) => {
        onStart?.();
        if (!audioBuffer) {
          return;
        }
        return viewer.model?.speak(audioBuffer, screenplay);
      }).catch(e => {
        onComplete?.();
      })
    prevSpeakPromise.then(() => {
      onComplete?.();
    });
  };
}

export const speakCharacter = createSpeakCharacter();

export const fetchAudio = async (talk: Talk): Promise<ArrayBuffer> => {
  // const ttsVoice = await synthesizeVoice(
  //   talk.message,
  //   talk.speakerX,
  //   talk.speakerY,
  //   talk.style
  // );
  // const url = ttsVoice.audio;
  // if (url == null) {
  //   throw new Error("Something went wrong");
  // }

  // const resAudio = await fetch(url);
  // const buffer = await resAudio.arrayBuffer();
  // return buffer;

  const requestBody = {
    text: talk.message,
    voice: "xiaoyi",
  };

  const headers = {
    'Content-Type': 'application/json',
  }

  const data = await postRequestArraybuffer("/speech/tts/generate", headers, requestBody);
  return data;
};
