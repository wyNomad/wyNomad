# 主页自动化脚本

## 贡献贪吃蛇

`generate_snake.py` 从 GitHub GraphQL 读取账号的贡献日历，生成不含 JavaScript 的明暗两套 SVG。工作流使用现有 `GITHUB_TOKEN`，每天北京时间 08:17 更新 `output` 分支，也支持手动运行。

蛇身初始 4 节，每吃掉一个有贡献的日期格子增加 1 节，最多 20 节；空格不增加长度。同一天的贡献数量决定格子颜色，不换算为新增蛇身节数。路线逐列巡游并沿外边框返回，避免增长后的蛇身穿过自身。每轮结束短暂停顿，再恢复贡献格子和初始长度。

长度参数位于 `simulate()` 和 `create_svg()`；动画每步 90ms，循环结束停留 20 步。系统启用减少动态效果时显示静态初始状态。

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
