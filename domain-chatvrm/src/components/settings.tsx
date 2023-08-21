// 引入过渡动画组件
import { TransitionGroup, CSSTransition } from 'react-transition-group';
import React, { useEffect, useState } from "react";
import { IconButton } from "./iconButton";
import { TextButton } from "./textButton";
import { Message } from "@/features/messages/messages";
import { custoRoleFormData, customrolEdit, customroleCreate, customroleDelete, customroleList, vrmModelData, vrmModelList } from "@/features/customRole/customRoleApi";
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
import { join } from 'path';

const tabNames = ['基础设置', '自定义角色设置', '大语言模型设置', '记忆模块设置', '高级设置'];
const llm_enums = ["openai", "text_generation"]

const publicDir = join(process.cwd(), 'public');

interface TabItemProps {
  name: string;
  isActive: boolean;
  onClick: () => void;
}

type Props = {
  globalsConfig: FormDataType;
  openAiKey: string;
  systemPrompt: string;
  chatLog: Message[];
  koeiroParam: KoeiroParam;
  remoteLoadVrmFile: (url: string) => void;
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
  remoteLoadVrmFile,
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
  const [customRoles, setCustomRoles] = useState([custoRoleFormData]);
  const [vrmModels, setVrmModels] = useState([vrmModelData]);
  const [enableProxy, setEnableProxy] = useState(false);
  const [conversationType, setConversationType] = useState('default');
  const [longTermMemoryType, setLongTermMemoryType] = useState('local');
  const [enableSummary, setEnableSummary] = useState(false);
  const [enableReflection, setEnableReflection] = useState(false);
  const [customRole, setCustomRole] = useState(custoRoleFormData);
  const [enableCreateRole, setEnableCreateRole] = useState(true);
  const [customRoleLog, setCustomRoleLog] = useState("");
  const [deleteCustomRoleLog, setDeleteCustomRoleLog] = useState("");
  const [selectedRoleId, setSelectedRoleId] = useState(-1);

  useEffect(() => {
    customroleList().then(data => {
      setCustomRoles(data)
    })
    setFormData(globalsConfig);
    vrmModelList().then(data => setVrmModels(data))
    setConversationType(globalsConfig.conversationConfig.conversationType)
    setLongTermMemoryType(globalsConfig.memoryStorageConfig.longTermMemoryType)
    setEnableSummary(globalsConfig.memoryStorageConfig.enableSummary)
    setEnableReflection(globalsConfig.memoryStorageConfig.enableSummary)
    setEnableProxy(globalsConfig.enableProxy)
  }, [])

  // 监听变化重新渲染
  useEffect(() => {
    // rerender
  }, [enableProxy, conversationType, longTermMemoryType, enableSummary, enableReflection, formData, customRoles])


  const handleSubmit = () => {
    saveConfig(formData)
    onClickClose()
  }

  // Tab组件添加flex样式  
  const TabItem: React.FC<TabItemProps> = ({ name, isActive, onClick }) => {
    return (
      <div
        className={`tab-item ${isActive ? 'active' : ''}`}
        onClick={onClick}
      >
        {name}
      </div>
    );
  };

  // 基础设置组件
  const BasicSettings = () => {

    return (
      <div className="globals-settings">

        <div className="section">
          <div className="title">角色卡设置</div>

          <div className="field">
            <label>选择角色</label>
            <select
              defaultValue={formData.characterConfig.character+''}
              onChange={e => {
                const selectedRoleId = e.target.options[e.target.selectedIndex].getAttribute('data-key');
                formData.characterConfig.character = Number(selectedRoleId);
                setFormData(formData);
              }}>
              {customRoles.map(role => (
                <option key={role.id} value={role.id} data-key={role.id}>
                  {role.role_name}
                </option>
              ))}
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
                remoteLoadVrmFile(formData.characterConfig.vrmModel)
              }}>
              {
                vrmModels.map(vrm => (
                  <option key={vrm.name} value={vrm.name}>{vrm.name}</option>
                ))
              }
            </select>
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
              checked={conversationType === 'default'} /> 普通对话模式
            {/* <input className='checkbot-input' type="radio" name="chatType" value="thought-chain"
              onChange={() => {
                formData.conversationConfig.conversationType = 'thought_chain';
                setFormData(formData);
                setConversationType(formData.conversationConfig.conversationType);
              }}
              checked={conversationType === 'thought_chain'}
            /> 推理+生成对话模式 */}
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
                  <option key={llm} value={llm}>{llm}</option>
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
              <option key={llm} value={llm}>{llm}</option>
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
              <option  key={llm} value={llm}>{llm}</option>
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
          {/* <div className="section">
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
          </div> */}
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
        {/* <div className="section">
          <div className="title">B站直播配置</div>
          <div className="field">
            <label>直播ID:</label>
            <input type="text" defaultValue={formData.liveStreamingConfig.B_STATION_ID}
              onChange={e => {
                formData.liveStreamingConfig.B_STATION_ID = e.target.value
                setFormData(formData);
              }} />
          </div>
        </div> */}
      </div>
    )
  }



  const CustomRoleSettings = () => {
    // 自定义角色设置
    return (
      <div className="globals-settings">
        <div className="section">
          <div className="field">
            <label>添加或编辑角色</label>
            <div className="flex items-center justify-center space-x-4">
              <select
                value={selectedRoleId}
                onChange={e => {
                  const selectedRoleId = Number(e.target.options[e.target.selectedIndex].getAttribute('data-key'));
                  formData.characterConfig.character = selectedRoleId;
                  setSelectedRoleId(selectedRoleId)
                  setEnableCreateRole(false);
                  setFormData(formData);
                  setCustomRoleLog("")
                  setDeleteCustomRoleLog("")
                  const selectedRole = customRoles.find(role => role.id === selectedRoleId);
                  if (selectedRole) {
                    setCustomRole(selectedRole);
                  }
                }}>
                <option key="-1" value="-1" data-key="-1">请选择</option>
                {customRoles.map(role => (
                  <option key={role.id} value={role.id} data-key={role.id}>
                    {role.role_name}
                  </option>
                ))}
              </select >
              <IconButton
                iconName="16/Add"
                isProcessing={false}
                onClick={e => {
                  setEnableCreateRole(true)
                  setCustomRole(custoRoleFormData)
                }}
              ></IconButton>
              <IconButton
                iconName="16/Remove"
                isProcessing={false}
                onClick={e => {
                  if (selectedRoleId !== -1) {
                    handleCustomRoleDelete(selectedRoleId)
                  }
                }}
              ></IconButton>
              <div className="flex justify-end mt-4">
                {deleteCustomRoleLog}
              </div>
            </div>
            <EditCustomRole />
          </div>
        </div>
        <div className="section">
          <div className="title">自定义VRM模型</div>
          <div className="my-8">
            <TextButton onClick={onClickOpenVrmFile}>上传VRM</TextButton>
          </div>
        </div>
      </div>)
  }

  const handleCustomRole = () => {
    if (enableCreateRole) {
      customroleCreate(customRole)
        .then(data => {
          customroleList().then(data => setCustomRoles(data))
          setCustomRoleLog("OK")
        }).catch(e => {
          setCustomRoleLog("ERROR")
        })

    } else {
      customrolEdit(customRole.id, customRole).then(data => {
        customroleList()
          .then(data => setCustomRoles(data))
        setCustomRoleLog("OK")
      }).catch(e => {
        setCustomRoleLog("ERROR")
      })
    }
  }

  const handleCustomRoleDelete = (selectedRoleId: number) => {
    customroleDelete(selectedRoleId)
      .then(data => {
        customroleList()
          .then(data => setCustomRoles(data))
        setDeleteCustomRoleLog("OK")
      }).catch(e => {
        setDeleteCustomRoleLog("ERROR")
      })
  }

  const EditCustomRole = () => {
    // 编辑角色
    return (
      <div className="globals-settings">
        <div className="section">
          <div className="field-"></div>
          {enableCreateRole == true ? (
            <label>创建角色</label>) : (<label>编辑角色</label>)}
          <label>角色名称</label>
          <input
            type="text"
            name="role_name"
            defaultValue={customRole.role_name}
            onChange={e => {
              customRole.role_name = e.target.value
              setCustomRole(customRole)
            }}
          />
          <div className="input-group">
            <label>角色基本信息定义</label>
            <textarea
              className="resize-y w-full p-2"
              name="persona"
              defaultValue={customRole.persona}
              onChange={e => {
                customRole.persona = e.target.value
                setCustomRole(customRole)
              }}
            />
          </div>
          <div className="input-group">
            <label>角色的性格简短描述</label>
            <textarea
              className="resize-y w-full p-2"
              name="personality"
              defaultValue={customRole.personality}
              onChange={e => {
                customRole.personality = e.target.value
                setCustomRole(customRole)
              }}
            />
          </div>
          <div className="input-group">
            <label>角色的对话的情况和背景</label>
            <textarea
              className="resize-y w-full p-2"
              name="scenario"
              defaultValue={customRole.scenario}
              onChange={e => {
                customRole.scenario = e.target.value
                setCustomRole(customRole)
              }}
            />
          </div>
          <div className="input-group">
            <label>角色的对话样例</label>
            <textarea
              className="resize-y w-full p-2"
              name="examples_of_dialogue"
              defaultValue={customRole.examples_of_dialogue}
              onChange={e => {
                customRole.examples_of_dialogue = e.target.value
                setCustomRole(customRole)
              }}
            />
          </div>
          <label>角色propmt模版</label>
          <select
            name="custom_role_template_type"
            defaultValue={customRole.custom_role_template_type}
            onChange={e => {
              customRole.custom_role_template_type = e.target.value
              console.log(customRole.custom_role_template_type)
              setCustomRole(customRole)
            }}
          >
            <option key="-1" value="-1" data-key="-1">请选择</option>
            <option key="zh" value="zh">zh</option>
            <option key="en" value="en">en</option>
            {/* 可以继续添加更多选项 */}
          </select>
          <div className="flex justify-end mt-4">
            <IconButton
              iconName="24/Save"
              label='提交'
              isProcessing={false}
              onClick={handleCustomRole}></IconButton>
          </div>
          <div className="flex justify-end mt-4">
            {customRoleLog}
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
        <div className="absolute m-24 flex gap-[8px]">
          <IconButton
            label='关闭'
            iconName="24/Close"
            isProcessing={false}
            onClick={onClickClose}
            className="mr-2" // 添加右边间距
          ></IconButton>
          <IconButton
            label='保存'
            iconName="24/Save"
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
          {currentTab === '自定义角色设置' && <CustomRoleSettings />}
          {currentTab === '大语言模型设置' && <LlmSettings />}
          {currentTab === '记忆模块设置' && <MemorySettings />}
          {currentTab === '高级设置' && <AdvancedSettings />}
        </div>
      </div>
    </div>
  )
};

