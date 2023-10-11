# Overview

VirtualWife是一个虚拟数字人项目，项目还处于孵化阶段，有很多需要优化的地方，作者想打造一个拥有自己“灵魂”的虚拟数字人，你可以像朋友一样和她相识，作者希望虚拟数字人融入人类生活，作为恋爱导师，心理咨询师，解决人类的情感需求。项目制作不易，占用了作者大量的业余时间，如果对你有用，请点star，拜托啦~

# Features
- 支持一键通过Docker快速部署
- 支持在Linux/Windows/MacOS系统进行部署
- 支持自定义角色设定
- 支持更换角色模型，可从VRM模型市场[Vroid](https://hub.vroid.com/)下载
- 支持长短期记忆功能
- 支持多LLM模型切换，并且支持私有化模型，具体使用说明请查阅[FAQ](FAQ.md)
- 支持文字驱动表情，文字驱动动作
- 支持B站进行直播，具体使用说明请查阅[FAQ](FAQ.md)
- 支持通过中文进行语音对话
- 支持Edge（微软）、Bert-VITS2语音切换
- 流式传输数据，拥有更快的响应速度

# Example Video

https://github.com/yakami129/VirtualWife/assets/36467094/51de1c07-f468-4987-8648-dc6b810550ad

# Roadmap

- [ ] 记忆模块优化
    - [ ] 支持联想记忆
    - [ ] 提高记忆检索的准确度
    - [ ] 支持记忆遗忘机制，去除不重要的记忆，让AI更加专注
- [ ] 情感涌现模块优化
    - [x] 支持模型肢体动作控制
    - [ ] ~~支持人物的语气、语速控制~~
- [ ] 语音模块
    - [x] 支持Edge（微软）、Bert-VITS2语音切换
- [ ] 角色扮演深化
    - [ ] LoRA微调RWKV，完成猫娘、傲娇、御姐等性格塑造
- [ ] 反思模块开发
    - [ ] 给定角色一个初始设定，通过反思+计划进行自我升级
- [ ] 知识检索
    - [ ] 融合FastGPT

# Get Started

## 一、安装[Docker](https://www.docker.com/)环境

- 方式一：命令行方式安装
    - [docker安装手册](https://www.runoob.com/docker/macos-docker-install.html)
    - [docker-compose安装手册](https://www.runoob.com/docker/docker-compose.html)
- 方式二：下载Docker桌面程序（桌面程序一般自带docker-compose）
    - [下载Docker桌面程序](https://www.docker.com/)
    - 然后下一步下一步就安装好了，如果拉取镜像比较慢，可以更改为国内镜像地址

- 检查是否安装成功，安装正常会打印日志
```
docker -v
docker-compose -v
```
![](docs/docker-version-log.png)

## 二、进入VirtualWife安装程序目录

```
cd installer
```

```
├── README.md               # 安装程序使用说明
├── docker-compose.yaml     # docker编排文件
├── env_example             # 环境变量配置模版，使用时需要将文件名改成.env
├── milvus                  # 长期记忆，数据存储模块，启动程序
├── linux                   # linux 启动和关闭程序
│   ├── start.sh
│   └── stop.sh
└── windows                 # windows 启动和关闭程序
    ├── start.bat
    └── stop.bat
```

## 三、设置环境变量

- 更改境变量配置模版文件名为.env
```
mv env_example .env
```
- 设置环境变量
```
# B站直播间ID（计划放在页面设置，目前有问题，暂时使用环境变量解决）
B_STATION_ID=27892212
# 主播UID 获取方法：https://sdl.moe/post/bili-live-wss/
# 在页面上登录B站后，打开https://api.bilibili.com/x/web-interface/nav
# 找到uid
B_UID=38ccccc
# 打开b站页面后登录，然后F12随便找一个B站接口，从请求头中获取cookie，一定要复制完整的cookie
B_COOKIE="buvid3=Fggggg28116infoc;xxxxxxxxxxxxxxxxxxxxxxxxxx";....... 此处略去其他的

# 时区
TIMEZONE=Asia/Shanghai

# 程序版本号，程序版本号可以查阅项目的release发布版本号，latest代表最新版本
CHATBOT_TAG=latest
CHATVRM_TAG=latest
GATEWAY_TAG=latest
```

## 四、启动程序

- 以Linux系统为例，启动程序示例如下
```
## 进入linux脚本目录
cd linux

## 启动程序，初次启动需要下载镜像，整个过程可能需要5分钟
sh start.sh
```

## 五、访问页面

- Web访问路径
```shell
http://localhost/
```
- 页面展示
![](docs/16925232398938.jpg)

## 六、初始化数字人配置

### （1）基础配置
```
选择自己喜欢的角色和人物模型，并且选择大语言模型
如果是使用openai请将语言模型设置为openai
```
![](docs/16925233912142.jpg)

### （2）大语言模型配置
```
这以openai模型为例，你只需要将OPENAI_API_KEY填写好即可
如果有API代理可以将地址填写到OPENAI_BASE_URL
```
![](docs/16925238212736.jpg)

### （3）高级设置
```
如果没有OPENAI_BASE_URL，你需要配置http-proxy，
如果是使用docker启动的程序，需要使用docker的dns，
例如这样HTTP_PROXY=http://host.docker.internal:23457
```
![](docs/16925239975597.jpg)

### （4）保存
保存、保存、保存，重要的事情说三遍
![](docs/16925241544548.jpg)

> 保存成功后，无需重启服务，可以开始聊天了，如果出现异常请查阅[FAQ](FAQ.md)

# FAQ
- 项目答疑以及部署中遇到问题的解决方案，请查阅[FAQ](FAQ.md)
- 本地开发请查阅[develop](develop.md)

# LICENSE

依据 MIT 协议，使用者需自行承担使用本项目的风险与责任，本开源项目开发者与此无关。

## 联系我们

| 技术交流群 | 打赏入股 |
|-------|------|
| ![winxin05.jpg](docs/winxin05.jpg)  | ![wx-skm.jpg](docs/wx-skm.jpg) |





