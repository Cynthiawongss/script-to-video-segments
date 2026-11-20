# 剧本转连续视频生成包

[English](README.md) · 中文

**把已确认剧本拆成可独立使用的生成片段，统一镜头、动作、对白和声音，并核对连续状态。**

![剧本转连续视频生成包](assets/hero.png)

## 得到什么

一体化分段提示词、原台词映射、开场与结尾状态、时长核对和剪辑备注。

[阅读完整 Skill](skills/script-to-video-segments/SKILL.zh-CN.md) · [英文入口](skills/script-to-video-segments/SKILL.md)

## 先看案例

最后一张标签是虚构的 30 秒场景，拆为三个连续片段；每段 10 秒是规划假设，不是厂商规格。

[案例说明](skills/script-to-video-segments/examples/the-last-label/script.zh-CN.md) · [中文交互示例](skills/script-to-video-segments/examples/the-last-label/index.zh-CN.html) · [English demo](skills/script-to-video-segments/examples/the-last-label/index.html)

下载仓库后，在浏览器打开示例 HTML。GitHub 的文件预览显示源码，不直接运行 HTML。示例可离线使用，材料均为虚构。

## 安装

把下面的地址交给支持 GitHub Skill 安装的助手，安装整个 Skill 文件夹：

```text
https://github.com/Cynthiawongss/script-to-video-segments/tree/main/skills/script-to-video-segments
```

保留 `references/`、`examples/` 和存在时的 `scripts/`、`agents/` 子目录。`SKILL.md` 是英文默认入口，`SKILL.zh-CN.md` 是对应中文版。英文入口同样要求按用户指定语言交付。

也可以从 [v0.1.0 发布页](https://github.com/Cynthiawongss/script-to-video-segments/releases/tag/v0.1.0) 下载英文或中文 Skill 安装包。两种版本选一种安装即可。

## 使用示例

```text
使用 $script-to-video-segments，把这个已确认剧本拆成视频生成片段，保留原台词，每段用同一时间轴安排镜头、动作、对白和声音。
```

## 验证

在仓库根目录执行：

```sh
python3 tools/build_examples.py
python3 -m unittest discover -s tests -v
```

[验证范围与限制](validation/README.md)包含浏览器检查方法。Python 检查器仅需 Python 3.10+ 标准库。

## 范围

交付的是制作计划，不是已生成的视频；声明状态通过检查不能保证成片的画面或声音连续。

封面用虚构角色的连续表演表达主题，不是附带案例的实际生成视频。
