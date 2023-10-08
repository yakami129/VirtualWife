import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import VrmViewer from "@/components/vrmViewer";
import { ViewerContext } from "@/features/vrmViewer/viewerContext";
import { EmotionType, Message, Screenplay, textsToScreenplay, } from "@/features/messages/messages";
import { speakCharacter } from "@/features/messages/speakCharacter";
import { MessageInputContainer } from "@/components/messageInputContainer";
import { SYSTEM_PROMPT } from "@/features/constants/systemPromptConstants";
import { DEFAULT_PARAM, KoeiroParam } from "@/features/constants/koeiroParam";
import { chat } from "@/features/chat/openAiChat";
import { connect } from "@/features/blivedm/blivedm";
// import { PhotoFrame } from '@/features/game/photoFrame';
// import { M_PLUS_2, Montserrat } from "next/font/google";
import { Introduction } from "@/components/introduction";
import { Menu } from "@/components/menu";
import { GitHubLink } from "@/components/githubLink";
import { Meta } from "@/components/meta";
import { GlobalConfig, getConfig, initialFormData } from "@/features/config/configApi";
import { buildUrl } from "@/utils/buildUrl";
import { generateMediaUrl } from "@/features/media/mediaApi";


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
let webGlobalConfig = initialFormData

export default function Home() {

    const { viewer } = useContext(ViewerContext);
    const [systemPrompt, setSystemPrompt] = useState(SYSTEM_PROMPT);
    const [openAiKey, setOpenAiKey] = useState("");
    const [koeiroParam, setKoeiroParam] = useState<KoeiroParam>(DEFAULT_PARAM);
    const [chatProcessing, setChatProcessing] = useState(false);
    const [chatLog, setChatLog] = useState<Message[]>([]);
    const [assistantMessage, setAssistantMessage] = useState("");
    const [imageUrl, setImageUrl] = useState('');
    const [globalConfig, setGlobalConfig] = useState<GlobalConfig>(initialFormData);
    const [subtitle, setSubtitle] = useState("");
    const [displayedSubtitle, setDisplayedSubtitle] = useState("");
    const [vrmModels, setVrmModels] = useState([vrmModelData]);
    const [backgroundImageUrl, setBackgroundImageUrl] = useState<string>(buildUrl("/bg-c.png"));
    const typingDelay = 100; // 每个字的延迟时间，可以根据需要进行调整
    const MAX_SUBTITLES = 30;
    const handleSubtitle = (newSubtitle: string) => {

        setDisplayedSubtitle((prevSubtitle: string) => {
            const updatedSubtitle = prevSubtitle + newSubtitle;
            if (updatedSubtitle.length > MAX_SUBTITLES) {
                const startIndex = updatedSubtitle.length - MAX_SUBTITLES;
                return updatedSubtitle.substring(startIndex);
            }
            return updatedSubtitle;
        });
    };

    useEffect(() => {
        vrmModelList().then(data => setVrmModels(data))
        console.log("vrmModelList")
    }, [])

    useEffect(() => {
        getConfig().then(data => {
            webGlobalConfig = data
            setGlobalConfig(data)
            if (data.background_url != '') {
                setBackgroundImageUrl(generateMediaUrl(data.background_url))
            }
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
                return i === targetIndex ? { role: v.role, content: text, user_name: v.user_name } : v;
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
            globalConfig: GlobalConfig,
            screenplay: Screenplay,
            onStart?: () => void,
            onEnd?: () => void
        ) => {
            speakCharacter(globalConfig, screenplay, viewer, onStart, onEnd);
        },
        [viewer]
    );

    const handleChatMessage = useCallback((
        globalConfig: GlobalConfig,
        type: string,
        user_name: string,
        content: string,
        emote: string) => {

        console.log("RobotMessage:" + content + " emote:" + emote)
        // 如果content为空，不进行处理
        // 如果与上一句content完全相同，不进行处理
        if (content == null || content == '' || content == ' ') {
            return
        }
        let aiTextLog = "";
        const sentences = new Array<string>();
        const aiText = content;
        const aiTalks = textsToScreenplay([aiText], koeiroParam, emote);
        aiTextLog += aiText;
        // 文ごとに音声を生成 & 再生、返答を表示
        const currentAssistantMessage = sentences.join(" ");
        setSubtitle(aiTextLog);
        handleSpeakAi(globalConfig, aiTalks[0], () => {
            setAssistantMessage(currentAssistantMessage);
            // handleSubtitle(aiText + " "); // 添加空格以区分不同的字幕
            startTypewriterEffect(aiTextLog);

            // アシスタントの返答をログに追加
            const params = JSON.parse(
                window.localStorage.getItem("chatVRMParams") as string
            );
            const messageLogAssistant: Message[] = [
                ...params.chatLog,
                { role: "assistant", content: aiTextLog, "user_name": user_name },
            ];
            setChatLog(messageLogAssistant);
        });
    }, [])

    const handleBehaviorAction = (
        type: string,
        content: string,
        emote: string) => {

        console.log("BehaviorActionMessage:" + content + " emote:" + emote)

        viewer.model?.emote(emote as EmotionType)
        viewer.model?.loadFBX(buildUrl(content))
    }

    const startTypewriterEffect = (text: string) => {
        let currentIndex = 0;
        const subtitleInterval = setInterval(() => {
            const newSubtitle = text[currentIndex];
            handleSubtitle(newSubtitle);
            currentIndex++;
            if (currentIndex >= text.length) {
                clearInterval(subtitleInterval);
            }
        }, 100); // 每个字符的间隔时间
    };

    /**
     * アシスタントとの会話を行う
     */
    const handleSendChat = useCallback(
        async (globalConfig: GlobalConfig,type: string, user_name: string, content: string) => {

            console.log("UserMessage:" + content)

            setChatProcessing(true);
            const yourName = user_name == null || user_name == '' ? globalConfig?.characterConfig?.yourName : user_name
            // ユーザーの発言を追加して表示
            const messageLog: Message[] = [
                ...chatLog,
                { role: "user", content: content, "user_name": yourName },
            ];
            setChatLog(messageLog);
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

    let lastSwitchTime = 0;

    const onChangeGlobalConfig = useCallback((
        globalConfig: GlobalConfig) => {
            setGlobalConfig(globalConfig);
            webGlobalConfig = globalConfig;
        },[])

    const handleWebSocketMessage = (event: MessageEvent) => {
        const data = event.data;
        const chatMessage = JSON.parse(data);
        const type = chatMessage.message.type;
        if (type === "user") {
            handleChatMessage(
                webGlobalConfig,
                chatMessage.message.type,
                chatMessage.message.user_name,
                chatMessage.message.content,
                chatMessage.message.emote,
            );
        } else if (type === "behavior_action") {
            handleBehaviorAction(
                chatMessage.message.type,
                chatMessage.message.content,
                chatMessage.message.emote,
            );
        }
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
        if (!bind_message_event) {
            console.log(">>>> setupWebSocket")
            setupWebSocket(); // Set up WebSocket when component mounts
            bind_message_event = true;
        }
    }, []);

    return (
        <div
            style={{
                backgroundImage: `url(${backgroundImageUrl})`,
                backgroundSize: 'cover',
                width: '100%',
                height: '100vh',
                position: 'relative',
                zIndex: 1,
            }}>
            <div>
                <Meta />
                <Introduction openAiKey={openAiKey} onChangeAiKey={setOpenAiKey} />
                <VrmViewer globalConfig={globalConfig} />
                <div className="flex items-center justify-center">
                    <div className="absolute bottom-1/4 z-10" style={{
                        fontFamily: "fzfs",
                        fontSize: "24px",
                        color: "#555",
                    }}>
                        {displayedSubtitle}
                    </div>
                </div>
                <MessageInputContainer
                    isChatProcessing={chatProcessing}
                    onChatProcessStart={handleSendChat}
                    globalConfig={globalConfig}
                />
                <Menu
                    globalConfig={globalConfig}
                    openAiKey={openAiKey}
                    systemPrompt={systemPrompt}
                    chatLog={chatLog}
                    koeiroParam={koeiroParam}
                    assistantMessage={assistantMessage}
                    onChangeAiKey={setOpenAiKey}
                    onChangeBackgroundImageUrl={data =>
                        setBackgroundImageUrl(generateMediaUrl(data))
                    }
                    onChangeSystemPrompt={setSystemPrompt}
                    onChangeChatLog={handleChangeChatLog}
                    onChangeKoeiromapParam={setKoeiroParam}
                    onChangeGlobalConfig={onChangeGlobalConfig}
                    handleClickResetChatLog={() => setChatLog([])}
                    handleClickResetSystemPrompt={() => setSystemPrompt(SYSTEM_PROMPT)}
                />
                <GitHubLink />
            </div>
        </div>
    )
}
