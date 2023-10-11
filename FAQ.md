### 如何在B站上进行直播呢？

作者是Mac系统，使用OBS进行直播，具体直播布置教程，可以参考以下视频
- [新手MacBook直播OBS教程](https://www.bilibili.com/video/BV1aB4y1P7BK/?spm_id_from=333.999.0.0)
- 最近B站已经上线了新的直播姬，支持win和mac，可以去官网下载

### 如何更换VRM模型呢？

- VRM模型市场：[Vroid](https://hub.vroid.com/)
- 点击设置后，点击打开VRM模型按钮，上传VRM（这块作者还没优化，刷新页面会加载默认模型）
![](docs/16925246168293.jpg)

### 如何更换虚拟AI的prompt？

- 新增角色，提交后可以在基础设置中选择你的角色
![](docs/16925246793101.jpg)

### 如何更换中文语音包？
- 本系统已经内置了很多中文语音包
![](docs/16925247438437.jpg)

### 支持私有化模型，需要安装text-generation-webui

- [text-generation-webui官网](https://github.com/oobabooga/text-generation-webui)
- [text-generation-webui详细安装教程](https://www.bilibili.com/video/BV1gM4y1J7dD/?spm_id_from=333.788&vd_source=11f40bfaa73ba3e80ac4ad36fb18f359)
> 注意整个安装过程中，一定需要挂梯子

### 目前支持的llama2模型

- ziqingyang_chinese-alpaca-2-13b
- ziqingyang_chinese-alpaca-2-7b

### 关于长期记忆中的Milvus如何安装？
```
cd installer/milvus
sudo docker compose up -d
```
- 注意前提你需要将docker和docker-compose安装好，如果使用官方的安装方式，请注意Milvus的版本号，需要与项目中的installer/milvus/docker-compose.yml 保持一致
- 文档地址：https://milvus.io/docs/install_standalone-docker.md

### 关于使用Docker启动后，无法访问OpenAI问题，如何解决
- 第一步请排查：你的梯子是否正常
- 第二步请排查：在高级设置中，将http-proxy设置开启，设置地址http://host.docker.internal:23457，注意这里的端口号请配置你代理的端口号


### 关于使用docker启动后，通过127.0.0.1访问text-generation-webui或者Milvus网络问题
- 可以使用Docker自带的DNS，将请求转发到宿主机，
- DNS:http://host.docker.internal:xxxx


### windows 系统安装Docker，需要安装WSL

- 安装文档：https://learn.microsoft.com/zh-cn/windows/wsl/install

### npm run dev 出现错误

- 错误日志
```
> chat-vrm@1.0 dev 
> next dev
```
- 解决方案：
```
cd domain-chatvrm
rm package-lock.json
npm install
npm run dev
```

### B站弹幕监听不到

- 检查B站直播间ID，主播UID 
    - 在页面上登录B站后，打开https://api.bilibili.com/x/web-interface/nav
    - 找到uid
- 检查B_COOKIE是否设置正确
    - 注意一定要复制完整的cookie,
    - 错误示例：
    ```
    B_COOKIE="buvid3=Fggggg28116infoc;"
    ```
    - 正确示例
    ```
    B_COOKIE="buvid3=8B473137-DAF1-B326-XXXXX-CA8A06BEE16802942infoc; b_nut=1681972902; _uuid=106F868A4-19CC-4D4B-XXX-2651010333D7E1003163infoc; buvid4=A628284B-D833-9256-XXX-903BA100474C03740-023042014-7G54s1lO7XHCknT6D8RZoQ%3D%3D; nostalgia_conf=-1; CURRENT_FNVAL=4048; ....... 此处略去其他的"
    ```