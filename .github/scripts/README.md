# 主页自动化脚本

## 贡献贪吃蛇

`generate_snake.py` 从 GitHub GraphQL 读取账号的贡献日历，生成不含 JavaScript 的明暗两套 SVG。工作流使用现有 `GITHUB_TOKEN`，每天北京时间 08:17 更新 `output` 分支，也支持手动运行。

蛇身初始 4 节，累计每吃到 10 次贡献增加 1 节，最多 20 节；不足 10 次的余额跨日期累计。大贡献格子获得的多节长度会在后续步数中逐节长出，避免蛇身重叠。浅色和深色主题均采用贡献图的绿色。按实际贡献次数从少到多吃点，同次数优先选择能安全到达的近点。每轮结束短暂停顿，再恢复贡献格子和初始长度。

寻路先用 BFS 和基础环路生成保底路线，再对吃点之间及返回起点的路段寻找近路。近路可以脱离环路的单向顺序，但每次替换都重放整轮动画，确认后续转弯不会撞到蛇身、所有贡献按原顺序吃完、增长完成并能衔接下一轮，才接受替换；无法通过验证时保留原路线。优先绕开较高次数格子，必要时经过也暂不吃，直到轮到对应次数。路线不是全局最短旅行路线，吃点顺序严格按次数升序，蛇身不会自交。

长度参数位于 `simulate()` 和 `create_svg()`；根据路径长度调整每步时间，在常见贡献图上保持约 40 秒一轮，每步范围 25–90ms，循环结束停留 20 步。系统启用减少动态效果时显示静态初始状态。

验证行为和静态文件：

```bash
python3 -m unittest discover -s .github/scripts -p test_generate_snake.py -v
python3 .github/scripts/check_repository.py
```

本地预览可传入真实 GitHub `contributionCalendar` 结构的 JSON：

```bash
python3 .github/scripts/generate_snake.py --username wyNomad --calendar /path/to/calendar.json --output-dir /tmp/snake-preview
```

生产工作流不使用本地预览数据。获取日历失败时工作流失败并保留已发布的上一版动画。
