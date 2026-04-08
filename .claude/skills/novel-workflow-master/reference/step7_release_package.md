# 阶段七：定稿与发布包

## 目标

把阶段一至六产物整理为可发布版本与作者工作版本，便于连载发布和后续维护。

## 输入

- `framework.md`
- `blueprint.md`
- `story/story.md`
- `chapters/draft/chXX.md`
- `editing/consistency_report.md`
- `editing/retcon_tasks.md`（若已处理则同步状态）

## 输出

- `release/release_version.md`
- `release/author_working_version.md`
- `release/synopsis.md`
- `release/characters.md`
- `release/worldbook.md`
- `release/toc.md`

## 文件说明

- `release_version.md`：面向发布平台的整洁版（不含内部注释）
- `author_working_version.md`：含章节元信息与修订痕迹
- `synopsis.md`：长简介 + 短简介 + 卖点语
- `characters.md`：角色速查（身份、动机、关系、关键事件）
- `worldbook.md`：世界观与规则速查
- `toc.md`：卷-章目录及一句话摘要

## 收尾检查

1. 章节编号连续
2. 卷名与目录一致
3. 发布版不含内部标注
4. 关键伏笔在目录摘要中可追踪

## 完成提示模板

```markdown
小说工作流已完成，发布包已生成。

你现在可以：
1. 直接用于发布（`release/release_version.md`）
2. 继续做精修（`release/author_working_version.md`）
3. 回到任意阶段局部重生成
```
