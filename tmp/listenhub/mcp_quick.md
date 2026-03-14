Title: 快速开始

URL Source: http://listenhub.ai/docs/zh/mcp/quick-start

Markdown Content:
快速开始
===============

[ListenHub MCP](http://listenhub.ai/docs/zh/mcp)

[EN](http://listenhub.ai/docs/en/mcp/quick-start)[中文](http://listenhub.ai/docs/zh/mcp/quick-start)

[ListenHub MCP](http://listenhub.ai/docs/zh/mcp)

[EN](http://listenhub.ai/docs/en/mcp/quick-start)[中文](http://listenhub.ai/docs/zh/mcp/quick-start)

Search

⌘K

[文档首页](http://listenhub.ai/docs/zh/mcp)[快速开始](http://listenhub.ai/docs/zh/mcp/quick-start)[使用示例](http://listenhub.ai/docs/zh/mcp/usage-examples)[核心功能](http://listenhub.ai/docs/zh/mcp/core-capabilities)[传输模式](http://listenhub.ai/docs/zh/mcp/transport-modes)[可用工具](http://listenhub.ai/docs/zh/mcp/available-tools)

[](https://listenhub.ai/welcome)[](https://x.com/listenhub)[](https://discord.gg/9gBPVG6m6x)[](https://github.com/marswaveai/listenhub-website-fe)

快捷跳转

[文档站首页](http://listenhub.ai/docs/zh)[Agent Skills 指南](http://listenhub.ai/docs/zh/skills)[OpenAPI 指南](http://listenhub.ai/docs/zh/openapi)[MCP 指南](http://listenhub.ai/docs/zh/mcp)

快速开始

快速开始
====

环境准备与各客户端配置方式。

[ListenHub](https://listenhub.ai/) 官方 MCP Server，支持生成 AI 播客（单人或双人）、FlowSpeech 等功能。所有用户均可使用。

[快速开始](http://listenhub.ai/docs/zh/mcp/quick-start#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
----------------------------------------------------------------------------------------

### [环境配置](http://listenhub.ai/docs/zh/mcp/quick-start#%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)

安装 Node.js

本服务器需要 Node.js 18 或更高版本。如果您还未安装 Node.js，请按照以下说明操作：

*   macOS

**方式 1：使用官方安装器**

    1.   访问 [Node.js 官方网站](https://nodejs.org/)，下载 Node.js 长期支持版本，如 [v24.11.0(LTS)](https://nodejs.org/dist/v24.11.0/node-v24.11.0.pkg)
    2.   打开下载的 `.pkg` 文件并按照安装向导操作
    3.   打开终端并运行以下命令验证安装：

```
node --version
npm --version
```

**方式 2：使用 Homebrew**

如果没有安装 [Homebrew](https://brew.sh/)，请使用如下的脚本进行安装：

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

```
# 安装成功之后可以使用 brew 进行下载
brew install node
```

然后验证安装：

```
node --version
npm --version
```

*   Windows

**方式 1：使用官方安装器**

    1.   访问 [Node.js 官方网站](https://nodejs.org/)
    2.   下载 Windows 的 LTS（长期支持）版本
    3.   运行下载的 `.msi` 安装程序
    4.   按照安装向导操作
    5.   打开 PowerShell 并运行以下命令验证安装：

```
node --version
npm --version
```

**方式 2：使用 winget（Windows 包管理器）**

如果您使用 Windows 10 版本 1809 或更高版本：

`winget install OpenJS.NodeJS.LTS`

然后验证安装：

```
node --version
npm --version
```

**方式 3：使用 Chocolatey**

如果您已安装 Chocolatey：

`choco install nodejs-lts`

然后验证安装：

```
node --version
npm --version
```

*   Linux

**Ubuntu/Debian**

 ```
# 安装 Node.js 20.x (LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
``` 
**Fedora/RHEL/CentOS**

 ```
# 安装 Node.js 20.x (LTS)
curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
sudo yum install -y nodejs
``` 
验证安装：

 ```
node --version
npm --version
``` 

获取 ListenHub API Key

从 [ListenHub API 密钥设置](https://listenhub.ai/zh/settings/api-keys) 页面获取您的 API 密钥，将其作为环境变量中 `LISTENHUB_API_KEY` 的值

### [各客户端配置方法](http://listenhub.ai/docs/zh/mcp/quick-start#%E5%90%84%E5%AE%A2%E6%88%B7%E7%AB%AF%E9%85%8D%E7%BD%AE%E6%96%B9%E6%B3%95)

*   Claude Desktop

编辑您的 Claude Desktop 配置文件：

**macOS**：`~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**：`%APPDATA%\Claude\claude_desktop_config.json`

添加以下配置：

 ```
{
    "mcpServers": {
        "listenhub": {
            "command": "npx",
            "args": [
                "-y",
                "@marswave/listenhub-mcp-server@latest"
            ],
            "env": {
                "LISTENHUB_API_KEY": "your_api_key_here"
            }
        }
    }
}
``` 
将 `your_api_key_here` 替换为您从 ListenHub 获取的实际 API 密钥。

*   Cursor

    1.   打开 Cursor 设置
    2.   导航至 **Features** → **Model Context Protocol**
    3.   点击 **Add MCP Server** 或直接编辑配置文件

**配置文件位置**：

    *   **macOS/Linux**：`~/.cursor/mcp.json`
    *   **Windows**：`%APPDATA%\Cursor\mcp.json`

添加以下配置：

```
{
    "mcpServers": {
        "listenhub": {
            "command": "npx",
            "args": [
                "-y",
                "@marswave/listenhub-mcp-server@latest"
            ],
            "env": {
                "LISTENHUB_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

将 `your_api_key_here` 替换为您从 ListenHub 获取的实际 API 密钥。

**可选：HTTP 模式**

如需使用 HTTP 传输方式，手动启动服务器：

```
export LISTENHUB_API_KEY="your_api_key_here"
npx @marswave/listenhub-mcp-server --transport http --port 3000
```

然后配置 Cursor：

```
{
    "mcpServers": {
        "listenhub": {
            "url": "http://localhost:3000/mcp"
        }
    }
}
```

*   Windsurf

    1.   打开 Windsurf 设置
    2.   导航至 **MCP Servers** 部分
    3.   添加新的服务器配置

**配置文件位置**：

    *   **macOS/Linux**：`~/.windsurf/mcp_server_config.json`
    *   **Windows**：`%APPDATA%\Windsurf\mcp_server_config.json`

添加以下配置：

```
{
    "mcpServers": {
        "listenhub": {
            "command": "npx",
            "args": [
                "-y",
                "@marswave/listenhub-mcp-server@latest"
            ],
            "env": {
                "LISTENHUB_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

将 `your_api_key_here` 替换为您从 ListenHub 获取的实际 API 密钥。

*   VS Code（通过 Cline 扩展）

    1.   从 VS Code 市场安装 [Cline 扩展](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
    2.   打开 VS Code 设置
    3.   搜索 “Cline: MCP Settings”
    4.   点击 “Edit in settings.json”

添加以下配置：

```
{
    "cline.mcpServers": {
        "listenhub": {
            "command": "npx",
            "args": [
                "-y",
                "@marswave/listenhub-mcp-server@latest"
            ],
            "env": {
                "LISTENHUB_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

将 `your_api_key_here` 替换为您从 ListenHub 获取的实际 API 密钥。

*   Zed 编辑器

    1.   打开 Zed 设置
    2.   导航至 MCP 部分
    3.   编辑配置文件

**配置文件位置**：

    *   **macOS/Linux**：`~/.config/zed/mcp.json`
    *   **Windows**：`%APPDATA%\Zed\mcp.json`

添加以下配置：

```
{
    "mcpServers": {
        "listenhub": {
            "command": "npx",
            "args": [
                "-y",
                "@marswave/listenhub-mcp-server@latest"
            ],
            "env": {
                "LISTENHUB_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

将 `your_api_key_here` 替换为您从 ListenHub 获取的实际 API 密钥。

*   Claude CLI

在终端中运行以下命令：

 `claude mcp add listenhub --env LISTENHUB_API_KEY=<insert-your-api-key-here> -- npx -y @marswave/listenhub-mcp-server` 
将 `<insert-your-api-key-here>` 替换为您从 ListenHub 获取的实际 API 密钥。

*   Codex CLI

在终端中运行以下命令：

 `codex mcp add listenhub --env LISTENHUB_API_KEY=<insert-your-api-key-here> -- npx -y @marswave/listenhub-mcp-server` 
将 `<insert-your-api-key-here>` 替换为您从 ListenHub 获取的实际 API 密钥。

*   ChatWise

    1.   打开 ChatWise 设置，选择 MCP，选择 “+” 添加新的 MCP 服务

    2.   在 MCP 配置模块填写以下信息：

![Image 1: image.png](https://storage.googleapis.com/listenhub-public-prod/static/mcp/listenhub-mcp-guide-v1/chatwise-mcp-config.png)

        *   **Command：`npx -y @marswave/listenhub-mcp-server@latest`**
        *   **勾选 ”Run tools automatically“：**确保自动执行工具
        *   **Environment Variables**：添加 `LISTENHUB_API_KEY`，值为您的 API 密钥

    3.   在聊天输入框下方启用工具后即可开始使用

*   其他 MCP 客户端

对于其他兼容 MCP 的客户端，使用标准 MCP 配置格式：

 ```
{
    "mcpServers": {
        "listenhub": {
            "command": "npx",
            "args": [
                "-y",
                "@marswave/listenhub-mcp-server@latest"
            ],
            "env": {
                "LISTENHUB_API_KEY": "your_api_key_here"
            }
        }
    }
}
``` 
将 `your_api_key_here` 替换为您从 ListenHub 获取的实际 API 密钥。

[文档首页 ListenHub MCP Server 的接入总览与主文档入口。](http://listenhub.ai/docs/zh/mcp)[使用示例 中文与英文播客生成示例截图。](http://listenhub.ai/docs/zh/mcp/usage-examples)

### On this page

[快速开始](http://listenhub.ai/docs/zh/mcp/quick-start#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)[环境配置](http://listenhub.ai/docs/zh/mcp/quick-start#%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE)[各客户端配置方法](http://listenhub.ai/docs/zh/mcp/quick-start#%E5%90%84%E5%AE%A2%E6%88%B7%E7%AB%AF%E9%85%8D%E7%BD%AE%E6%96%B9%E6%B3%95)
