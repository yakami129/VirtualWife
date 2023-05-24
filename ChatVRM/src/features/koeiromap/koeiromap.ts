import { TalkStyle } from "../messages/messages";

export async function synthesizeVoice(
  message: string,
  speaker_x: number,
  speaker_y: number,
  style: TalkStyle
) {
  const param = {
    method: "POST",
    body: JSON.stringify({
      text: message,
      speaker_x: speaker_x,
      speaker_y: speaker_y,
      style: style,
    }),
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  };

  const koeiroRes = await fetch(
    "https://api.rinna.co.jp/models/cttse/koeiro",
    param
  );

  const data = (await koeiroRes.json()) as any;

  return { audio: data.audio };
}
