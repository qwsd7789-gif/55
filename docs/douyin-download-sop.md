# 抖音视频下载 SOP（全局）
适用场景：用户提供抖音分享链接，要求“下载视频”“保存视频”“提取视频到本地”。
## 默认方案
优先使用本地仓库：
- 仓库：`C:\Users\Administrator\.openclaw\workspace\video-expert-analyzer`
- 专用脚本：`scripts\download_douyin.py`
原因：
- 已验证可成功下载抖音短链
- 比仓库里的 `pipeline_enhanced.py` 更稳
- 当前 `pipeline_enhanced.py` 存在错误导入：引用了不存在的 `douyin_downloader`
## 已验证可用命令
先创建输出目录，再以 UTF-8 运行：
```powershell
New-Item -ItemType Directory -Force -Path "C:\Users\Administrator\.openclaw\workspace\video-expert-analyzer\output\douyin_task" | Out-Null
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python "C:\Users\Administrator\.openclaw\workspace\video-expert-analyzer\scripts\download_douyin.py" "<抖音链接>" "C:\Users\Administrator\.openclaw\workspace\video-expert-analyzer\output\douyin_task\video.mp4"
```
## 必须注意的坑
1. **不要直接先跑 `pipeline_enhanced.py` 下载抖音**
   - 当前仓库版本会报：`ModuleNotFoundError: No module named 'douyin_downloader'`
   - 原因：脚本引用错模块名
2. **Windows 控制台要强制 UTF-8**
   - 否则 `download_douyin.py` 里的 emoji/中文打印可能触发：
   - `UnicodeEncodeError: 'gbk' codec can't encode character ...`
   - 必须先设置：
     - `$env:PYTHONUTF8='1'`
     - `$env:PYTHONIOENCODING='utf-8'`
3. **输出目录要先创建**
   - 否则下载阶段可能报：
   - `No such file or directory: '...\video.mp4'`
## 标准执行步骤
1. 克隆/确认仓库存在：`video-expert-analyzer`
2. 确认 Python 依赖可用（至少 `requests`）
3. 创建输出目录
4. 设置 UTF-8 环境变量
5. 调用 `scripts\download_douyin.py`
6. 用 `Get-Item` 校验文件大小、路径、时间
7. 把最终落地路径回复给用户
## 成功案例
已验证成功下载：
- 链接：`https://v.douyin.com/mRpPEo-5HjY/`
- 输出文件：`C:\Users\Administrator\.openclaw\workspace\video-expert-analyzer\output\douyin_mrhong\mrhong.mp4`
- 文件大小：`2182753` bytes
## 给所有 agent 的统一规则
- 以后遇到“下载抖音视频”，默认优先使用本 SOP
- 默认不要先走 `pipeline_enhanced.py`
- 默认先建目录 + 开 UTF-8 + 直接跑 `download_douyin.py`
