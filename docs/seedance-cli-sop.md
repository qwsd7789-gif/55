# 即梦 / Dreamina CLI 提交视频 SOP
## 目标
把“用本机 Dreamina 官方 CLI 直接提交视频任务、查询任务、下载结果”的流程固定下来，后续所有 agent 都按这套标准执行，避免只写提示词、不真正提交。
---
## 适用场景
当用户出现以下需求时，优先使用本 SOP：
- 用即梦直接生成视频
- 提交 15s fast 模式视频
- 查 submit_id
- 查即梦任务状态
- 下载即梦生成结果
- 查 Dreamina 余额
- 用图片 / 多图 / 音频 / 视频参考生成视频
不适用场景：
- 用户只是要“写提示词”，不要求真实提交
- 用户要做平台能力介绍，而不是执行任务
- 用户要的是别的平台（不是即梦 / Dreamina）
---
## 本机环境
### CLI 路径
`C:\Users\Administrator\dreamina-bin\dreamina.exe`
### 共享 skill 路径
`C:\Users\Administrator\.openclaw\skills\seedance-cli\SKILL.md`
### 当前默认模型
- 默认视频模型：`seedance2.0fast`
- 默认适合：快速出草稿、15 秒 fast 模式
---
## 执行原则
1. **用户明确说“提交 / 生成 / 跑一下”时，要真实提交，不要只写提示词。**
2. **默认优先 `seedance2.0fast`。** 用户没特别指定质量优先时，不要默认切慢模型。
3. **先用短轮询拿 submit_id。** 即使还在排队，也要先回任务号。
4. **回复必须可追踪。** 至少回：`submit_id`、模式、时长、比例、当前状态、扣点（如返回）。
5. **如果出现合规授权拦截**，明确告诉用户去 Dreamina Web 端先完成一次授权。
6. **如果是本地素材任务**，优先用绝对路径，避免相对路径失效。
---
## 标准流程
### 1. 先确认任务类型
根据用户输入判断走哪条命令：
#### A. 纯文字生成视频
用：`text2video`
适合：
- “用即梦生成一个视频”
- “把这段提示词直接提交”
#### B. 单图生视频
用：`image2video`
适合：
- “拿这张图生成动态视频”
- “把首帧做成视频”
#### C. 多图故事视频
用：`multiframe2video`
适合：
- “用 2-20 张图做一个连续视频”
- “多图过渡叙事”
#### D. 多模态视频
用：`multimodal2video`
适合：
- 图片 + 视频 + 音频混合参考
- 希望参考现有动作、节奏、声音来生成
#### E. 查任务
用：`query_result`
#### F. 看历史任务
用：`list_task`
#### G. 查余额
用：`user_credit`
---
### 2. 参数整理
提交前至少确认这些参数：
- `prompt`
- `duration`
- `ratio`
- `model_version`
- 是否有本地素材（图片 / 视频 / 音频）
默认值：
- `model_version=seedance2.0fast`
- `duration`：按用户要求；没说时按任务场景判断
- `ratio`：按用户要求；短视频优先 `9:16`
- `video_resolution=720p`
- `poll=12`
---
### 3. 提交命令模板
## A. 文生视频 text2video
```powershell
$prompt = @'
这里放最终提示词
'@
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' text2video \
  --model_version=seedance2.0fast \
  --duration=15 \
  --ratio=9:16 \
  --video_resolution=720p \
  --poll=12 \
  --prompt=$prompt
```
适用：用户只给提示词，没有本地素材。
---
## B. 单图生视频 image2video
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' image2video \
  --image='C:\path\to\first.png' \
  --prompt='镜头缓慢推进，人物轻微动作，头发自然飘动' \
  --duration=5 \
  --model_version=seedance2.0fast \
  --video_resolution=720p \
  --poll=12
```
适用：一张首帧图做视频。
---
## C. 多图叙事 multiframe2video
### 两张图
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' multiframe2video \
  --images 'C:\a.png,C:\b.png' \
  --prompt='人物从第一张自然过渡到第二张，动作连贯' \
  --duration=3 \
  --poll=12
```
### 三张及以上
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' multiframe2video \
  --images 'C:\a.png,C:\b.png,C:\c.png' \
  --transition-prompt='从第一张自然过渡到第二张' \
  --transition-prompt='从第二张自然过渡到第三张' \
  --poll=12
```
适用：2-20 张图片连续叙事。
---
## D. 多模态视频 multimodal2video
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' multimodal2video \
  --image 'C:\input.png' \
  --video 'C:\ref.mp4' \
  --audio 'C:\music.mp3' \
  --prompt '参考素材节奏生成15秒视频，画面更电影感' \
  --model_version=seedance2.0fast \
  --duration=15 \
  --ratio=9:16 \
  --video_resolution=720p \
  --poll=12
```
适用：图 / 视频 / 音频混合参考。
---
## E. 查询任务 query_result
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' query_result --submit_id='任务号'
```
下载结果：
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' query_result \
  --submit_id='任务号' \
  --download_dir='C:\Users\Administrator\.openclaw\workspace\outputs\dreamina'
```
---
## F. 查看历史任务 list_task
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' list_task --limit=20
```
---
## G. 查询余额 user_credit
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' user_credit
```
---
## 4. 提交后标准回复模板
### 成功提交但仍在排队
```text
已提交。
- submit_id: <id>
- 模式: <text2video / image2video / multiframe2video / multimodal2video>
- 时长: <duration>
- 比例: <ratio>
- 当前状态: 排队中
- 扣点: <credit_count>
```
### 已完成
```text
已完成。
- submit_id: <id>
- 模式: <mode>
- 当前状态: success
- 结果文件: <路径或下载目录>
```
### 失败
```text
提交失败。
- 模式: <mode>
- 原因: <具体报错>
- 下一步: <修复动作>
```
---
## 5. 常见异常处理
### 1）未登录 / 登录过期
现象：命令返回登录相关错误。
处理：
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' login --headless
```
必要时：
```powershell
& 'C:\Users\Administrator\dreamina-bin\dreamina.exe' relogin --headless
```
---
### 2）AigcComplianceConfirmationRequired
现象：首次使用部分模型时需要合规确认。
处理：
- 告诉用户：先去 Dreamina Web 端完成一次授权确认
- 完成后再重试 CLI 提交
---
### 3）参数不支持
现象：duration / ratio / resolution / model_version 组合非法。
处理原则：
- 先改成支持组合
- 仍不明确时，只问一个最小必要问题
例如：
- `seedance2.0fast` 视频分辨率只用 `720p`
- `text2video` 时长范围是 `4-15s`
---
### 4）本地文件路径错误
现象：图片 / 视频 / 音频找不到。
处理：
- 优先用绝对路径
- 必要时先复制到 workspace 再提交
- 提交前先检查文件存在
示例：
```powershell
Test-Path 'C:\path\to\file.png'
```
---
## 6. 提交前检查清单
每次提交前检查：
- 是否真的是“要提交”，而不是“只写提示词”
- prompt 是否已定稿
- duration 是否在模型允许范围内
- ratio 是否明确
- model_version 是否明确
- 本地素材路径是否存在
- 是否需要先查余额
- 是否需要保留 submit_id 给后续追踪
---
## 7. 任务记录模板
建议每次真实提交后至少记录：
```text
项目名：
任务类型：text2video / image2video / multiframe2video / multimodal2video
提示词版本：
素材路径：
模型：seedance2.0fast
时长：
比例：
submit_id：
提交时间：
当前状态：
备注：
```
---
## 8. 推荐默认路径
### 用户说“用即梦生成一个15秒 fast 视频”
默认动作：
1. 整理提示词
2. 用 `text2video`
3. 参数默认：
   - `--model_version=seedance2.0fast`
   - `--duration=15`
   - `--ratio=9:16`
   - `--video_resolution=720p`
   - `--poll=12`
4. 回 submit_id 与状态
---
## 9. 当前已验证事实
- 本机 `dreamina.exe` 可执行
- 当前账户余额可查
- 已成功提交过即梦视频任务
- 当前问题不在 CLI 能力，而在 skill 注册未进入当前会话 available_skills
- 所以执行层面，**先直接走 CLI 最稳**
---
## 10. 结论
以后凡是用户明确要求“提交即梦视频 / 查任务 / 查余额 / 下载结果”，默认优先走本 SOP，不停留在提示词层。
