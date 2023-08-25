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

let socketInstance: WebSocket | null = null;
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

  const handleChatMessage = (type: string, user_name: string, content: string) => {

    let aiTextLog = "";
    const sentences = new Array<string>();
    const aiText = content;
    const aiTalks = textsToScreenplay([aiText], koeiroParam);
    aiTextLog += aiText;

    // 文ごとに音声を生成 & 再生、返答を表示
    const currentAssistantMessage = sentences.join(" ");
    console.log("RobotMessage:" + aiTextLog)
    handleSpeakAi(aiTalks[0], () => {
      setAssistantMessage(currentAssistantMessage);
    });

  }

  /**
   * アシスタントとの会話を行う
   */
  const handleSendChat = useCallback(
    async (type: string, user_name: string, content: string) => {

      console.log("UserMessage:" + content)

      setChatProcessing(true);
      // ユーザーの発言を追加して表示
      const messageLog: Message[] = [
        ...chatLog,
        { role: "user", content: content },
      ];
      setChatLog(messageLog);

      const yourName = user_name == null || user_name == '' ? globalsConfig?.characterConfig?.yourName : user_name
      await chat(content, yourName).catch(
        (e) => {
          console.error(e);
          return null;
        }
      );

      setChatProcessing(false);
    },
    [systemPrompt, chatLog, setChatLog, handleSpeakAi, setImageUrl, openAiKey, koeiroParam]
  );

  const handleWebSocketMessage = (event: MessageEvent) => {
    const data = event.data;
    const chatMessage = JSON.parse(data);
    handleChatMessage(
      chatMessage.message.type,
      chatMessage.message.user_name,
      chatMessage.message.content
    );
  };

  const setupWebSocket = () => {
    connect().then((webSocket) => {
      socketInstance = webSocket;
      socketInstance.onmessage = handleWebSocketMessage; // Set onmessage listener
      socketInstance.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
        console.log('Reconnecting...');
        setupWebSocket(); // 重新调用connect()函数进行连接
      };
    });
  }

  useEffect(() => {
    if(!bind_message_event){
      console.log(">>>> setupWebSocket")
      setupWebSocket(); // Set up WebSocket when component mounts
      bind_message_event = true;
    }
  }, []);

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
