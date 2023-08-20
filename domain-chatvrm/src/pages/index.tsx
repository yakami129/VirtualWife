import { useCallback, useContext, useEffect, useRef, useState } from "react";
import VrmViewer from "@/components/vrmViewer";
import { ViewerContext } from "@/features/vrmViewer/viewerContext";
import {
  Message,
  textsToScreenplay,
  Screenplay,
} from "@/features/messages/messages";
import { speakCharacter } from "@/features/messages/speakCharacter";
import { MessageInputContainer } from "@/components/messageInputContainer";
import { SYSTEM_PROMPT } from "@/features/constants/systemPromptConstants";
import { KoeiroParam, DEFAULT_PARAM } from "@/features/constants/koeiroParam";
import { chat, getChatResponseStream } from "@/features/chat/openAiChat";
import { connect } from "@/features/blivedm/blivedm";
import { chatPriorityQueue } from "@/features/queue/ChatPriorityQueue";
// import { PhotoFrame } from '@/features/game/photoFrame';
// import { M_PLUS_2, Montserrat } from "next/font/google";
import { Introduction } from "@/components/introduction";
import { Menu } from "@/components/menu";
import { GitHubLink } from "@/components/githubLink";
import { Meta } from "@/components/meta";
import { translation } from "@/features/translation/translationApi";
import { getConfig, FormDataType, initialFormData } from "@/features/config/configApi";

// const m_plus_2 = M_PLUS_2({
//   variable: "--font-m-plus-2",
//   display: "swap",
//   preload: false,
// });

// const montserrat = Montserrat({
//   variable: "--font-montserrat",
//   display: "swap",
//   subsets: ["latin"],
// });

const socket = connect()
let bind_message_event = false;

export default function Home() {

  const { viewer } = useContext(ViewerContext);
  const [systemPrompt, setSystemPrompt] = useState(SYSTEM_PROMPT);
  const [openAiKey, setOpenAiKey] = useState("");
  const [koeiroParam, setKoeiroParam] = useState<KoeiroParam>(DEFAULT_PARAM);
  const [chatProcessing, setChatProcessing] = useState(false);
  const [chatLog, setChatLog] = useState<Message[]>([]);
  const [assistantMessage, setAssistantMessage] = useState("");
  const [imageUrl, setImageUrl] = useState('');
  const [globalsConfig, setGlobalsConfig] = useState<FormDataType>(initialFormData);

  useEffect(() => {
    getConfig().then(data => {
      setGlobalsConfig(data)
    })
    if (window.localStorage.getItem("chatVRMParams")) {
      const params = JSON.parse(
        window.localStorage.getItem("chatVRMParams") as string
      );
      setSystemPrompt(params.systemPrompt);
      setKoeiroParam(params.koeiroParam);
      setChatLog(params.chatLog);
    }
  }, []);

  useEffect(() => {
    process.nextTick(() =>
      window.localStorage.setItem(
        "chatVRMParams",
        JSON.stringify({ systemPrompt, koeiroParam, chatLog })
      )
    );
  }, [systemPrompt, koeiroParam, chatLog]);

  const handleChangeChatLog = useCallback(
    (targetIndex: number, text: string) => {
      const newChatLog = chatLog.map((v: Message, i) => {
        return i === targetIndex ? { role: v.role, content: text } : v;
      });
      setChatLog(newChatLog);
    },
    [chatLog]
  );

  /**
   * 文ごとに音声を直列でリクエストしながら再生する
   */
  const handleSpeakAi = useCallback(
    async (
      screenplay: Screenplay,
      onStart?: () => void,
      onEnd?: () => void
    ) => {
      speakCharacter(screenplay, viewer, onStart, onEnd);
    },
    [viewer]
  );



  /**
   * アシスタントとの会話を行う
   */
  const handleSendChat = useCallback(
    async (type: string, user_name: string, content: string) => {

      let newMessage = content;
      let oldMessage = content;
      if (newMessage == null) return;
      console.log("UserMessage:" + newMessage)
      newMessage = await translation(newMessage, "en").catch(
        (e) => {
          console.error(e);
          return oldMessage;
        }
      );

      setChatProcessing(true);
      // ユーザーの発言を追加して表示
      const messageLog: Message[] = [
        ...chatLog,
        { role: "user", content: newMessage },
      ];
      setChatLog(messageLog);

      // Chat GPTへ
      const messages: Message[] = [
        {
          role: "system",
          content: systemPrompt,
        },
        ...messageLog,
      ];

      let aiTextLog = "";
      let tag = "";
      const sentences = new Array<string>();

      const yourName = user_name == null || user_name == '' ? globalsConfig?.characterConfig?.yourName : user_name
      let receivedMessage = await chat(newMessage, yourName).catch(
        (e) => {
          console.error(e);
          return null;
        }
      );

      receivedMessage = await translation(receivedMessage, "zh").catch(
        (e) => {
          console.error(e);
          return oldMessage;
        }
      );
      console.log("ChatbotMessage:" + receivedMessage)

      try {

        // let done = false;
        // let w_index = 0;

        // while (true) {

        //   if (w_index === 5) {
        //     console.log("done");
        //     break;
        //   }


        //   w_index = w_index + 1;

        // const tagMatch = receivedMessage.match(/^\[(.*?)\]/);
        // if (tagMatch && tagMatch[0]) {
        //   tag = tagMatch[0];
        //   receivedMessage = receivedMessage.slice(tag.length);
        // }

        // // 返答を一文単位で切り出して処理する
        // const sentenceMatch = receivedMessage.match(
        //   /^(.+[。．！？\n]|.{10,}[、,])/
        // );
        // if (sentenceMatch && sentenceMatch[0]) {
        //   const sentence = sentenceMatch[0];
        //   sentences.push(sentence);
        //   receivedMessage = receivedMessage
        //     .slice(sentence.length)
        //     .trimStart();

        //   console.log("a:" + receivedMessage)

        //   // 発話不要/不可能な文字列だった場合はスキップ
        //   if (
        //     !sentence.replace(
        //       /^[\s\[\(\{「［（【『〈《〔｛«‹〘〚〛〙›»〕》〉』】）］」\}\)\]]+$/g,
        //       ""
        //     )
        //   ) {
        //     //continue;
        //   }

        const aiText = oldMessage + "，" + receivedMessage;
        const aiTalks = textsToScreenplay([aiText], koeiroParam);
        aiTextLog += aiText;

        // 文ごとに音声を生成 & 再生、返答を表示
        const currentAssistantMessage = sentences.join(" ");
        handleSpeakAi(aiTalks[0], () => {
          setAssistantMessage(currentAssistantMessage);
        });

        //}
        // }
      } catch (e) {
        setChatProcessing(false);
        console.error(e);
      } finally {
        // reader.releaseLock();
      }

      // アシスタントの返答をログに追加
      const messageLogAssistant: Message[] = [
        ...messageLog,
        { role: "assistant", content: aiTextLog },
      ];
      setChatLog(messageLogAssistant);
      setChatProcessing(false);
    },
    [systemPrompt, chatLog, setChatLog, handleSpeakAi, setImageUrl, openAiKey, koeiroParam]
  );



  useEffect(() => {

    if (!bind_message_event) {

      socket.then(webSocket => {
        webSocket.onmessage = (event) => {
          const data = event.data;
          var chatMessage = JSON.parse(data);
          chatPriorityQueue.queue({ message: chatMessage.message, priority: chatMessage.priority });
          console.log('Received WebSocket data:', chatMessage);
        };
      })

      setInterval(() => {
        if (chatPriorityQueue.length > 0) {
          const chatMessage = chatPriorityQueue.dequeue();
          handleSendChat(chatMessage.message.type, chatMessage.message.user_name, chatMessage.message.content).catch(e => {
            console.log(e);
          });
          console.log('run handleSendChat chatMessage:', chatMessage);
        }
      }, 1000);
      bind_message_event = true;
    }
  }, [handleSendChat]);


  return (
    <div>
      <Meta />
      <Introduction openAiKey={openAiKey} onChangeAiKey={setOpenAiKey} />
      <VrmViewer
        globalsConfig={globalsConfig}
      />
      <MessageInputContainer
        isChatProcessing={chatProcessing}
        onChatProcessStart={handleSendChat}
      />
      <Menu
        globalsConfig={globalsConfig}
        openAiKey={openAiKey}
        systemPrompt={systemPrompt}
        chatLog={chatLog}
        koeiroParam={koeiroParam}
        assistantMessage={assistantMessage}
        onChangeAiKey={setOpenAiKey}
        onChangeSystemPrompt={setSystemPrompt}
        onChangeChatLog={handleChangeChatLog}
        onChangeKoeiromapParam={setKoeiroParam}
        handleClickResetChatLog={() => setChatLog([])}
        handleClickResetSystemPrompt={() => setSystemPrompt(SYSTEM_PROMPT)}
      />
      <GitHubLink />
    </div>
  )
}
