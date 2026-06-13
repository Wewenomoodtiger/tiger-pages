---
project_name: Tiger 强身健体项目
create_date: 2026-06-13
---

# 强身健体项目

这是 Tiger 的健身训练项目，内容从之前的「锻炼」对话迁移到此。

## 项目结构

```
强身健体/
  跑步数据/        ← 跑步数据分析相关文件
     dashboard.html      仪表盘（可浏览器打开）
     跑步数据分析.xlsx    Excel 分析
     跑步数据报告.txt     数据分析报告
     runs_data.json      原始跑步记录
     extract_runs.py     从 Apple Health 提取数据的脚本
  训练计划/        ← 训练计划
     训练计划.txt         每周训练安排
  README.md              本文件
```

## 跑步数据概况

- 时间跨度: 2022-10-27 ~ 2026-06-09
- 有效跑步: 120 次
- 总距离: 830 km
- 平均配速: 6.7 min/km
- 已从 Apple Health 导出数据中提取

## 训练计划

目标：70kg / 17% 体脂
周期：4周
安排：周一推、周二 Zone 2 跑、周三拉、周四 Zone 2 跑、周五腿、周日长距离跑（可选）

## 使用方式

- **仪表盘**：用浏览器打开 `跑步数据/dashboard.html`
- **Excel 分析**：用 Excel 或 WPS 打开 `跑步数据/跑步数据分析.xlsx`
- **提取新数据**：将 Apple Health 的 `export.xml` 放到指定路径后，运行 `python extract_runs.py`
