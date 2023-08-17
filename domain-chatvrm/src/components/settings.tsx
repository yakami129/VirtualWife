// 引入过渡动画组件
import { TransitionGroup, CSSTransition } from 'react-transition-group';
import React, { useEffect, useState } from "react";
import { IconButton } from "./iconButton";
import { TextButton } from "./textButton";
import { Message } from "@/features/messages/messages";
import { customroleList, vrmModelList } from "@/features/customRole/customRoleApi";
import { getConfig, saveConfig, FormDataType } from "@/features/config/configApi";
import {
  KoeiroParam,
  PRESET_A,
  PRESET_B,
  PRESET_C,
  PRESET_D,
} from "@/features/constants/koeiroParam";
import { Link } from "./link";
import { damp } from 'three/src/math/MathUtils';

const tabNames = ['基础设置', '大语言模型设置', '记忆模块设置', '高级设置'];
const llm_enums = ["openai", "text_generation"]

type Props = {
  globalsConfig: FormDataType;
  openAiKey: string;
  systemPrompt: string;
  chatLog: Message[];
  koeiroParam: KoeiroParam;
  onClickClose: () => void;
  onChangeAiKey: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onChangeSystemPrompt: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  onChangeChatLog: (index: number, text: string) => void;
  onChangeKoeiroParam: (x: number, y: number) => void;
  onClickOpenVrmFile: () => void;
  onClickResetChatLog: () => void;
  onClickResetSystemPrompt: () => void;
};

export const Settings = ({
  globalsConfig,
  openAiKey,
  chatLog,
  systemPrompt,
  koeiroParam,
  onClickClose,
  onChangeSystemPrompt,
  onChangeAiKey,
  onChangeChatLog,
  onChangeKoeiroParam,
  onClickOpenVrmFile,
  onClickResetChatLog,
  onClickResetSystemPrompt,
}: Props) => {

  const [currentTab, setCurrentTab] = useState('基础设置');
  const [formData, setFormData] = useState(globalsConfig);
  const [customRoles, setCustomRoles] = useState([]);
  const [vrmModels, setVrmModels] = useState([]);
  const [enableProxy, setEnableProxy] = useState(false);
  const [conversationType, setConversationType] = useState('default');
  const [longTermMemoryType, setLongTermMemoryType] = useState('local');
  const [enableSummary, setEnableSummary] = useState(false);
  const [enableReflection, setEnableReflection] = useState(false);

  useEffect(() => {
    customroleList().then(data => setCustomRoles(data))
    vrmModelList().then(data => setVrmModels(data))
    setFormData(globalsConfig);
    setConversationType(globalsConfig.conversationConfig.conversationType)
    setLongTermMemoryType(globalsConfig.memoryStorageConfig.longTermMemoryType)
    setEnableSummary(globalsConfig.memoryStorageConfig.enableSummary)
    setEnableReflection(globalsConfig.memoryStorageConfig.enableSummary)
    setEnableProxy(globalsConfig.enableProxy)
  }, [])

  // 监听变化重新渲染
  useEffect(() => {
    // rerender
  }, [enableProxy, conversationType, longTermMemoryType, enableSummary, enableReflection, formData])


  const handleSubmit = () => {
    saveConfig(formData)
    onClickClose()
  }

  // Tab组件添加flex样式  
  const TabItem = ({ name, isActive, onClick }) => {
    return (
      <div
        className={`tab-item ${isActive ? 'active' : ''}`}
        onClick={onClick}
      >
        {name}
      </div>
    )
  }

  // 基础设置组件
  const BasicSettings = () => {

    return (
      <div className="globals-settings">

        <div className="section">
          <div className="title">角色卡设置</div>

          <div className="field">
            <label>选择角色</label>
            <select
              defaultValue={formData.characterConfig.character}
              onChange={e => {
                formData.characterConfig.character = e.target.value;
                setFormData(formData);
              }}>
              {
                customRoles.map(role => (
                  <option key={role}>{role}</option>
                ))
              }
            </select >
          </div>

          <div className="field">
            <label>你的名字</label>
            <input type="text" defaultValue={formData.characterConfig.yourName}
              onChange={e => {
                formData.characterConfig.yourName = e.target.value
                setFormData(formData);
              }} />
          </div>

          <div className="field">
            <label>VRM角色模型</label>
            <select
              defaultValue={formData.characterConfig.vrmModel}
              onChange={e => {
                formData.characterConfig.vrmModel = e.target.value;
                setFormData(formData);
              }}>
              {
                vrmModels.map(vrm => (
                  <option key={vrm.id}>{vrm.name}</option>
                ))
              }
            </select>
          </div>
        </div>

        <div className="section">
          <div className="title">自定义角色卡</div>
          <div className="my-8">
            <TextButton onClick={onClickOpenVrmFile}>上传VRM</TextButton>
          </div>
        </div>

        <div className="section">
          <div className="title">对话设置</div>
          <div className="checkbot-field">
            <label>对话模式:</label>
            <input className='checkbot-input' type="radio" name="chatType" value="default"
              onChange={() => {
                formData.conversationConfig.conversationType = 'default';
                setFormData(formData);
                setConversationType(formData.conversationConfig.conversationType);
              }}
              checked={conversationType === 'default'} /> 默认（直接生成对话）
            <input className='checkbot-input' type="radio" name="chatType" value="thought-chain"
              onChange={() => {
                formData.conversationConfig.conversationType = 'thought_chain';
                setFormData(formData);
                setConversationType(formData.conversationConfig.conversationType);
              }}
              checked={conversationType === 'thought_chain'}
            /> 思维链(先推理，再生成对话)
          </div>
          <div className="field">
            <label>选择大语言模型:</label>
            <select
              defaultValue={formData.conversationConfig.languageModel}
              onChange={e => {
                formData.conversationConfig.languageModel = e.target.value;
                setFormData(formData);
              }}>
              {
                llm_enums.map(llm => (
                  <option key={llm}>{llm}</option>
                ))
              }
            </select>
          </div>
        </div>
      </div>
    );
  }

  const LlmSettings = () => {
    // 大语言模型设置
    return (
      <div className="globals-settings">
        <div className="section">
          <div className="title">OpenAI配置</div>
          <div className="field">
            <label>OPENAI_API_KEY</label>
            <input type="text" defaultValue={formData.languageModelConfig.openai.OPENAI_API_KEY}
              onChange={e => {
                formData.languageModelConfig.openai.OPENAI_API_KEY = e.target.value
                setFormData(formData);
              }}
            />
          </div>
          <div className="field">
            <label>OPENAI_BASE_URL</label>
            <input type="text" defaultValue={formData.languageModelConfig.openai.OPENAI_BASE_URL}
              onChange={e => {
                formData.languageModelConfig.openai.OPENAI_BASE_URL = e.target.value
                setFormData(formData);
              }}
            />
          </div>
        </div>
        <div className="section">
          <div className="title">text-generation-webui配置</div>
          <div className="field">
            <label>TEXT_GENERATION_API_URL</label>
            <input type="text" defaultValue={formData.languageModelConfig.textGeneration.TEXT_GENERATION_API_URL}
              onChange={e => {
                formData.languageModelConfig.textGeneration.TEXT_GENERATION_API_URL = e.target.value
                setFormData(formData);
              }}
            />
          </div>
        </div>
      </div >
    )
  }

  const LocalMemory = () => {
    // 本地存储设置  
    return (
      <div className="section">
        <div className="title">local记忆存储配置</div>
        <div className="field">
          <label>最大记忆条数</label>
          <input type="number" defaultValue={formData.memoryStorageConfig.localMemory.maxMemoryLoads}
            onChange={e => {
              formData.memoryStorageConfig.localMemory.maxMemoryLoads = Number(e.target.value)
              setFormData(formData);
            }}
          />
        </div>
      </div>)
  };

  const MilvusMemory = () => {
    // Milvus存储设置
    return (
      <div className="section">
        <div className="title">milvus记忆存储配置</div>
        <div className="field">
          <label>host</label>
          <input type="text" defaultValue={formData.memoryStorageConfig.milvusMemory.host}
            onChange={e => {
              formData.memoryStorageConfig.milvusMemory.host = e.target.value
              setFormData(formData);
            }} />
          <label>port</label>
          <input type="text" defaultValue={formData.memoryStorageConfig.milvusMemory.port}
            onChange={e => {
              formData.memoryStorageConfig.milvusMemory.port = e.target.value
              setFormData(formData);
            }} />
          <label>user</label>
          <input type="text" defaultValue={formData.memoryStorageConfig.milvusMemory.user}
            onChange={e => {
              formData.memoryStorageConfig.milvusMemory.user = e.target.value
              setFormData(formData);
            }} />
          <label>password</label>
          <input type="text" defaultValue={formData.memoryStorageConfig.milvusMemory.password}
            onChange={e => {
              formData.memoryStorageConfig.milvusMemory.password = e.target.value
              setFormData(formData);
            }} />
          <label>dbName</label>
          <input type="text" defaultValue={formData.memoryStorageConfig.milvusMemory.dbName}
            onChange={e => {
              formData.memoryStorageConfig.milvusMemory.dbName = e.target.value
              setFormData(formData);
            }} />
        </div>
      </div>
    )
  };

  const SummaryLLM = () => {
    return (
      <div className="field">
        <label>选择大语言模型:</label>
        <select
          defaultValue={formData.memoryStorageConfig.languageModelForSummary}
          onChange={e => {
            formData.memoryStorageConfig.languageModelForSummary = e.target.value;
            setFormData(formData);
          }}>
          {
            llm_enums.map(llm => (
              <option key={llm}>{llm}</option>
            ))
          }
        </select>
      </div>)
  }

  const ReflectionLLM = () => {
    return (
      <div className="field">
        <label>选择大语言模型:</label>
        <select
          defaultValue={formData.memoryStorageConfig.languageModelForReflection}
          onChange={e => {
            formData.memoryStorageConfig.languageModelForReflection = e.target.value;
            setFormData(formData);
          }}>
          {
            llm_enums.map(llm => (
              <option key={llm}>{llm}</option>
            ))
          }
        </select>
      </div>)
  }

  const MemorySettings = () => {
    // 记忆模块设置
    return (
      <div className="globals-settings">
        <div className="section">
          <div className="title">基础功能</div>
          <div className="checkbot-field">
            <label>长期记忆存储类型:</label>
            <input className='checkbot-input' type="radio" name="longTermMemoryType" value="locol"
              onChange={() => {
                formData.memoryStorageConfig.longTermMemoryType = "local";
                setFormData(formData)
                setLongTermMemoryType(formData.memoryStorageConfig.longTermMemoryType)
              }}
              checked={longTermMemoryType === 'local'} /> local
            <input className='checkbot-input' type="radio" name="longTermMemoryType" value="milvus"
              onChange={() => {
                formData.memoryStorageConfig.longTermMemoryType = "milvus";
                setFormData(formData)
                setLongTermMemoryType(formData.memoryStorageConfig.longTermMemoryType)
              }}
              checked={longTermMemoryType === 'milvus'}
            /> milvus
          </div>
          {
            longTermMemoryType === 'local' ? (
              <div>
                <LocalMemory />
              </div>
            ) : (
              <div>
                <MilvusMemory />
              </div>
            )
          }
        </div>
        <div className="section">
          <div className="title">高级功能</div>
          <div className="section">
            <div className="checkbot-field">
              <label>是否开启对话摘要:</label>
              <input className='checkbot-input' type="radio" name="enableSummary" value="true"
                onChange={() => {
                  formData.memoryStorageConfig.enableSummary = true;
                  setFormData(formData);
                  setEnableSummary(formData.memoryStorageConfig.enableSummary);
                }}
                checked={enableSummary === true} /> 是
              <input className='checkbot-input' type="radio" name="enableSummary" value="false"
                onChange={() => {
                  formData.memoryStorageConfig.enableSummary = false;
                  setFormData(formData)
                  setEnableSummary(formData.memoryStorageConfig.enableSummary);
                }}
                checked={enableSummary === false} /> 否
            </div>
            {
              enableSummary === true ? (
                <div>
                  <SummaryLLM />
                </div>
              ) : (
                <div></div>
              )
            }
          </div>
          <div className="section">
            <div className="checkbot-field">
              <label>是否开启记忆反思:</label>
              <input className='checkbot-input' type="radio" name="enableReflection" value="true"
                onChange={() => {
                  formData.memoryStorageConfig.enableReflection = true;
                  setFormData(formData);
                  setEnableReflection(formData.memoryStorageConfig.enableReflection);
                }}
                checked={enableReflection === true} /> 是
              <input className='checkbot-input' type="radio" name="enableReflection" value="false"
                onChange={() => {
                  formData.memoryStorageConfig.enableReflection = false;
                  setFormData(formData);
                  setEnableReflection(formData.memoryStorageConfig.enableReflection);
                }}
                checked={enableReflection === false} /> 否
            </div>
            {
              enableReflection === true ? (
                <div>
                  <ReflectionLLM />
                </div>
              ) : (
                <div></div>
              )
            }
          </div>
        </div >
      </div>
    )
  }

  const AdvancedSettings = () => {
    // 高级设置
    return (
      <div className="globals-settings">
        <div className="section">
          <div className="title">http-proxy设置</div>
          <div className="checkbot-field">
            <input className='checkbot-input' type="radio" name="enableProxy" value="true"
              onChange={() => {
                formData.enableProxy = true;
                setFormData(formData);
                setEnableProxy(formData.enableProxy);
              }}
              checked={enableProxy === true} /> 开启
            <input className='checkbot-input' type="radio" name="enableProxy" value="false"
              onChange={() => {
                formData.enableProxy = false;
                setFormData(formData);
                setEnableProxy(formData.enableProxy);
              }}
              checked={enableProxy === false} /> 关闭
          </div>
          {
            enableProxy === true ? (
              <div className="field">
                <label>httpProxy</label>
                <input type="text" defaultValue={formData.httpProxy}
                  onChange={e => {
                    formData.httpProxy = e.target.value
                    setFormData(formData);
                  }} />
                <label>httpsProxy</label>
                <input type="text" defaultValue={formData.httpsProxy}
                  onChange={e => {
                    formData.httpsProxy = e.target.value
                    setFormData(formData);
                  }} />
                <label>socks5Proxy</label>
                <input type="text" defaultValue={formData.socks5Proxy}
                  onChange={e => {
                    formData.socks5Proxy = e.target.value
                    setFormData(formData);
                  }} />
              </div>
            ) : (
              <div></div>
            )
          }
        </div>
        <div className="section">
          <div className="title">B站直播配置</div>
          <div className="field">
            <label>直播ID:</label>
            <input type="text" defaultValue={formData.liveStreamingConfig.B_STATION_ID}
              onChange={e => {
                formData.liveStreamingConfig.B_STATION_ID = e.target.value
                setFormData(formData);
              }} />
          </div>
        </div>
      </div>
    )
  }

  // Tab内容使用过渡动画
  <TransitionGroup>
    <CSSTransition
      timeout={500}
      classNames="fade"
      key={currentTab}
    >
      <div className="tab-content">
        {/* 当前tab内容 */}
      </div>
    </CSSTransition>
  </TransitionGroup>

  return (
    <div className="container">
      <div className="absolute z-40 w-full h-full bg-white/80 backdrop-blur ">
        <div className="absolute m-24">
          <IconButton
            iconName="24/Close"
            isProcessing={false}
            onClick={onClickClose}
          ></IconButton>
          <IconButton
            iconName="24/Projects"
            isProcessing={false}
            onClick={handleSubmit}
          ></IconButton>
        </div>
        <div className="settings">
          {/* 添加Tab菜单 */}
          <div className="tab-menu">
            {tabNames.map(name => (
              <TabItem
                key={name}
                name={name}
                isActive={name === currentTab}
                onClick={() => setCurrentTab(name)}
              />
            ))}
          </div>
          {/* 根据currentTab渲染对应的内容 */}
          {currentTab === '基础设置' && <BasicSettings />}
          {currentTab === '大语言模型设置' && <LlmSettings />}
          {currentTab === '记忆模块设置' && <MemorySettings />}
          {currentTab === '高级设置' && <AdvancedSettings />}
        </div>
      </div>
    </div>
  )
};

