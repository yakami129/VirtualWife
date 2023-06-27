# VirtualWife

VirtualWife 是一个虚拟主播项目，目前支持在B站进行直播，用户可以自由更换VRM人物模型，大家可以将他作为一个虚拟主播入门demo，在上面扩展自己喜欢功能。

本项目只是一个实验品，满足基本聊天能力，用户可以通过弹幕与虚拟主播进行对话

## 演示视频

<video width="320" height="240" controls>
    <source src="docs/d1.mp4" type="video/mp4">
</video>

## 项目技术栈说明

- React：前端服务框架
- Django：后端服务框架
- LangChain: 支撑聊天核心功能
- OpenAI: GPT大语言模型 
- Edge-tts: 微软语音合成模型
- VRM: VRM人物模型

## 项目结构说明

### 核心服务说明

- ChatBot: AI核心服务
- ChatVRM: 聊天客户端

### 环境要求

- python: 3.9.6
- node: 14.21.3

## 快速开始

### 如何启动ChatBot？

- 进入ChatBot文件夹
```shell
cd ChatBot
```

- 如何获取OpenAIKey?
    - https://platform.openai.com/overview

- 如何获取B站直播间ID？
    - 获取B站直播ID，前提是需要你自行注册B站直播用户
![](docs/16878718322092.jpg)
- 创建.env文件，添加OpenAIKey和B站直播间ID
```shell
# OpenAIKey
OPENAI_API_KEY=xxxxxx
# B站直播间ID
B_STATION_ID=xxxxx
```
- 安装ChatBot项目依赖
```shell
pip3 install -r requirements.txt
```
- 启动ChatBot项目
```shell
python manage.py runserver
```

### 如何启动ChatVRM？

- 进入ChatVRM文件夹
```shell
cd ChatVRM
```
- 安装ChatVRM项目依赖
```shell
npm install
```
- 启动ChatVRM项目
```shell
npm run dev
```
- Web访问路径
```shell
http://localhost:3000/
```
- 页面展示
![](docs/16878738708227.jpg)

### 如何在B站上进行直播呢？

作者是Mac系统，使用OBS进行直播，具体直播布置教程，可以参考以下视频
- [新手MacBook直播OBS教程](https://www.bilibili.com/video/BV1aB4y1P7BK/?spm_id_from=333.999.0.0)

### 如何更换VRM模型呢？

- VRM模型市场：[Vroid](https://hub.vroid.com/)
- 点击设置后，点击打开VRM模型按钮，上传VRM（这块作者还没优化，刷新页面会加载默认模型）
![](docs/16878743210162.jpg)

### 如何更换虚拟AI的prompt？

- 默认使用虚拟主播爱莉的prompt
![](docs/16878744329269.jpg)

![](docs/16878744548863.jpg)

- 训练自己的prompt，可以参照爱莉的prompt迭代自己的虚拟人物

### 如何更换中文语音包？

- 本系统已经内置了很多中文语音包
![](docs/16878746478694.jpg)

## 后记

本项目是作者第一次接触数字人开发的实验型demo，基于[ChatVRM](https://github.com/pixiv/ChatVRM)+Edge-tts+LangChain+OpenAI实现，希望能通过这个项目让大家快速搭建自己的虚拟主播，如果项目对你有用，可以帮忙点个start（下次一定。。。），优化建议、bug可以提issues

## 技术交流群

![IMG_3896](docs/IMG_3897.JPG)

