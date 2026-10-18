<div align="center">

<img src="assets/header.svg" width="100%" alt="wyNomad — AI Infra / Robotics / Computer Vision" />

<img src="https://readme-typing-svg.demolab.com?font=Noto+Sans+SC&amp;weight=500&amp;size=22&amp;duration=3200&amp;pause=1800&amp;color=818CF8&amp;center=true&amp;vCenter=true&amp;width=760&amp;height=60&amp;lines=%E9%83%BD%E6%98%AF%E9%A3%8E%E6%99%AF%EF%BC%8C%E5%B9%B8%E4%BC%9A%E3%80%82;All+is+scenery.+A+pleasure+to+meet+you." width="100%" alt="都是风景，幸会。 / All is scenery. A pleasure to meet you." />

**Hi, I'm wyi 👋**

一名在代码与实践中探索的学生，以 AI Infra 为主要方向，持续探索 Robotics 与计算机视觉。

<a href="https://github.com/wyNomad?tab=repositories"><img src="https://img.shields.io/badge/Explore_my_projects-6366F1?style=flat-square&amp;logo=github&amp;logoColor=white" alt="Explore my projects" /></a>
<a href="#-开源贡献--open-source-contributions"><img src="https://img.shields.io/badge/Open_source_contributions-0EA5E9?style=flat-square&amp;logo=opensourceinitiative&amp;logoColor=white" alt="Open source contributions" /></a>

</div>

### 🐍 贡献足迹 · Contribution Snake

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wyNomad/wyNomad/output/github-contribution-grid-snake-dark.svg?v=4" />
  <img src="https://raw.githubusercontent.com/wyNomad/wyNomad/output/github-contribution-grid-snake.svg?v=4" width="100%" alt="Green contribution snake eating lower counts first and gaining one segment per four contributions, capped at 20" />
</picture>
</div>

### 🛠️ 技术栈 · Tech Stack

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://skillicons.dev/icons?i=python%2Ccpp%2Cc%2Cpytorch%2Copencv%2Cros%2Clinux%2Cgit&amp;theme=dark&amp;perline=8" />
  <img src="https://skillicons.dev/icons?i=python%2Ccpp%2Cc%2Cpytorch%2Copencv%2Cros%2Clinux%2Cgit&amp;theme=light&amp;perline=8" alt="Python, C++, C, PyTorch, OpenCV, ROS, Linux, Git" />
</picture>
</div>

### 🧭 正在探索 · Currently Exploring

<img src="assets/focus.svg" width="100%" alt="探索方向，按优先级排列：01 AI Infra — 推理框架、算子、CI/CD；02 Robotics — ROS 2、RL、VLA、深度学习；03 Computer Vision — 深度学习、视觉感知。" />

### 🚀 项目与贡献 · Projects & Contributions

| 方向 | 项目 | 内容 |
| :--- | :--- | :--- |
| ⚙️ AI Infra · 开源贡献 | [Torch-FL](https://github.com/flagos-ai/Torch-FL) · [FlagScale](https://github.com/flagos-ai/FlagScale) | 多平台 CI、构建与测试流水线、按改动路由与测试报告 |
| ⚙️ AI Infra · 推理优化 | [vLLM / FlagOS · Iluvatar 实验](https://github.com/wyNomad/vllm-plugin-FL/tree/perf/iluvatar-native2d-context-routing/experiments/iluvatar) | 基于上游的 attention 推理优化，包含插件实现、性能剖析与实验验证 |
| 🤖 机器人 | [农业巡检机器人](https://github.com/wyNomad/agricultural-inspection-robot) · [香橙派侧](https://github.com/wyNomad/agricultural-inspection-orangepi) | ROS 2 双主控项目，保留早期 / 中期源码，最终版本暂未公开 |
| 🤖 机器人视觉 | [RoboMaster 自瞄](https://github.com/wyNomad/robomaster-auto-aim) | 相机采集、YOLO 装甲板检测、PnP 与云台串口，完整闭环仍在开发 |
| 👁️ 计算机视觉 | [柑橘病害检测](https://github.com/wyNomad/citrus-disease-detection) | YOLO11 数据准备、微调与图片检测实验 |
| 🧠 知识管理 | [MindOS](https://github.com/wyNomad/MindOS) | 基于 MindOS 维护的个人知识库：项目笔记、学习记录与可复用工作流 |

### 🔗 开源贡献 · Open-source Contributions

参与 Torch-FL 与 FlagScale 的多平台 CI、构建测试与训练环境适配，以下为已合入上游的代表工作。

| 工作 | 上游记录 | 状态 |
| :--- | :--- | :--- |
| 昇腾 CANN / ACLNN、海光 DCU、平头哥 PPU 的构建与集成测试 | [Torch-FL #71](https://github.com/flagos-ai/Torch-FL/pull/71) · [#81](https://github.com/flagos-ai/Torch-FL/pull/81) · [#91](https://github.com/flagos-ai/Torch-FL/pull/91) | 已合入 · 共同作者 |
| 按代码改动选择测试平台，支持受信任 Fork 按需运行 CI | [Torch-FL #521](https://github.com/flagos-ai/Torch-FL/pull/521) | 已合入 |
| 收集各平台 pytest 结果并上报 FlagCICD | [Torch-FL #542](https://github.com/flagos-ai/Torch-FL/pull/542) | 已合入 |
| 昆仑芯 P800 训练环境、CI 与 Qwen3 训练测试支持 | [FlagScale #1282](https://github.com/flagos-ai/FlagScale/pull/1282) | 已合入 · 共同作者 |
| 清理独立流水线迁移后的通用集成任务，统一配置与调用接口 | [个人提交](https://github.com/flagos-ai/Torch-FL/commit/1353c33ca7c1ac35ddbd21e0f9833db605d1a5ee) · [协作 PR #505](https://github.com/flagos-ai/Torch-FL/pull/505) | 已合入 · 共同作者 |

协作开发仓库：[Torch-FL](https://github.com/BrianPei/PyTorch-Plugin-FL/branches) · [FlagScale](https://github.com/BrianPei/FlagScale/branches) · [我发起的 Torch-FL PR](https://github.com/flagos-ai/Torch-FL/pulls?q=is%3Apr+author%3AwyNomad)

### 📊 数据一览 · GitHub Stats

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=wyNomad&amp;theme=github_dark" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username=wyNomad&amp;theme=github" width="32%" alt="GitHub statistics for wyNomad" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=wyNomad&amp;theme=github_dark" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=wyNomad&amp;theme=github" width="32%" alt="Languages used in public repositories" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=wyNomad&amp;theme=github_dark" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=wyNomad&amp;theme=github" width="32%" alt="Most committed languages" />
</picture>
</div>

<sub>公开活动自动统计；语言图反映仓库与提交分布。具体工作与协作贡献见上方记录。</sub>

<div align="center">

<br />
<sub>保持好奇，持续构建。 · Stay curious. Keep building.</sub>

<img src="assets/footer.svg" width="100%" alt="Blue and violet waves" />

</div>
