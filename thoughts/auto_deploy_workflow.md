# 游戏发布流水线技术方案

## 文档信息

- 创建时间：2026-03-23
- 参与人：平哥、狗蛋、刘雨辰
- 文档用途：用于梳理从 OpenClaw 生成代码到自动部署上线的最小可用流程

---

## 一、背景与目标

### 当前现状

- 团队每天使用 AI（OpenClaw）编写像素级小游戏
- 已有代码托管平台和云服务器（4C4G）
- 尚未跑通自动化发布链路
- 对成本较敏感，优先考虑低成本方案

### 目标

搭建从「OpenClaw 写代码」到「自动部署上线」的最小闭环，优先实现低成本、可维护、易调试的自动发布流程。

---

## 二、技术方案

### 方案 A：最小闭环版

适合先跑通链路，快速上线。

```text
OpenClaw 写代码
  -> Git 提交
  -> GitHub 触发 webhook / workflow
  -> 云服务器执行 git pull
  -> 重启服务
```

**优点**

- 成本低，云服务器可兼作开发机
- 链路简单，排查问题方便
- 无需额外构建机

**适用场景**

- 纯 HTML5 小游戏
- 无需编译或打包

### 方案 B：进阶版

适合后续补充规范化流程。

```text
OpenClaw 写代码
  -> PR / MR
  -> 代码审核
  -> 合并到 main
  -> GitHub Actions 构建 Docker 镜像
  -> 推送镜像到 Docker Hub / 私有 Registry
  -> 服务器 docker-compose pull && docker-compose up -d
```

**优点**

- 用镜像保证环境一致性
- 出问题时更容易回滚
- 可加入审批环节，避免代码直接冲线上

---

## 三、GitHub Actions 是什么

GitHub Actions 可以理解为：代码 `push` 之后，由 GitHub 自动执行的一系列脚本。

### 核心概念

- `Workflow`：完整的自动化流程
- `Job`：工作流中的一个任务
- `Step`：任务中的具体执行步骤
- `Runner`：执行任务的机器，GitHub 提供免费额度

---

## 四、最小可用 Workflow 配置

### 1. 工作流文件

在仓库中创建 [`.github/workflows/deploy.yml`](C:\Users\Noah\Documents\vscode\.github\workflows\deploy.yml)：

```yaml
name: Deploy Game

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            cd /path/to/your/game
            git pull origin main
            systemctl restart your-game.service
```

### 2. 服务器端准备

生成 SSH 密钥：

```bash
ssh-keygen -t ed25519 -C "github-deploy"
cat ~/.ssh/id_ed25519.pub
```

说明：

- 公钥添加到 GitHub
- 私钥写入 GitHub Secrets

### 3. GitHub Secrets 配置

在仓库 `Settings -> Secrets` 中配置：

| Secret 名称 | 说明 |
| --- | --- |
| `SERVER_IP` | 云服务器 IP |
| `SERVER_USER` | 服务器登录用户名 |
| `SERVER_SSH_KEY` | 对应私钥内容 |

### 4. systemd 服务示例

创建服务文件：

```ini
# /etc/systemd/system/game.service
[Unit]
Description=My HTML5 Game

[Service]
WorkingDirectory=/path/to/your/game
ExecStart=/usr/bin/python3 -m http.server 8080
Restart=always

[Install]
WantedBy=multi-user.target
```

启用并启动服务：

```bash
systemctl enable game
systemctl start game
```

---

## 五、完整发布流程

1. OpenClaw 编写游戏代码
2. 执行 `git add . && git commit -m "功能描述" && git push`
3. GitHub 收到 `push` 后自动触发 workflow
4. Workflow 通过 SSH 登录服务器，执行 `git pull` 并重启服务
5. 游戏完成上线

---

## 六、关键环节对照表

| 环节 | 当前状态 | 建议 |
| --- | --- | --- |
| 代码托管 | 已有（GitHub） | 使用私有仓库即可 |
| 云服务器 | 已有（4C4G） | 先按低成本方式复用 |
| 构建触发 | 需配置 | 使用 GitHub Actions 免费额度 |
| Steam 发布 | 后续考虑 | 需支付 100 美元审核费，并经过 Valve 审核 |

> 注意：Steam 发布是独立链路。建议先把“代码 -> 服务器”的自动部署链路打通，确认游戏可稳定运行后，再考虑接入 Steam。

---

## 七、技术栈选择

### 当前建议

纯 HTML5 小游戏。

原因：

- 无需编译，直接部署
- 技术栈简单，OpenClaw 生成代码更快
- 适合像素级小游戏快速试错

### 后续可升级方向

- Godot
- Unity
- WebAssembly

---

## 八、下一步行动

- [ ] 服务器生成 SSH 密钥，并配置 GitHub Deploy Key
- [ ] 在 GitHub 仓库中配置 Secrets
- [ ] 创建 [`.github/workflows/deploy.yml`](C:\Users\Noah\Documents\vscode\.github\workflows\deploy.yml)
- [ ] 在服务器创建 `systemd` 服务
- [ ] 本地初始化 Git 仓库并绑定远程仓库
- [ ] 测试第一次自动化部署

---

## 备注

本文档由 OpenClaw 生成，供团队内部参考。
