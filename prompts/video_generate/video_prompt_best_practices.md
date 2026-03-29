# AI 视频生成 Prompt 最佳实践

---

## 一、Prompt 标准结构

每个高质量的视频 Prompt 应包含以下 5 层描述：

| 层次 | 顺序 | 内容 | 必要性 |
|------|------|------|--------|
| **1. 风格声明** | 最先 | realistic / cinematic / 3D animation / time-lapse / stop-motion | 必须 |
| **2. 镜头语言** | 最先或第二 | 景别 + 运镜方式 | 必须 |
| **3. 主体描述** | 中段 | 外观、动作、状态 | 必须 |
| **4. 环境场景** | 中段 | 地点、周边元素、背景 | 推荐 |
| **5. 光影氛围** | 结尾 | 光线、色调、质感、电影属性 | 推荐 |

### 模板

```text
[风格声明] + [镜头语言] of [主体] [动作/状态] in/among [环境场景]. [光影氛围].
```

---

## 二、风格声明关键词

在 Prompt 开头明确声明视觉风格：

| 风格 | 关键词 | 适用场景 |
|------|--------|---------|
| **写实摄影** | `photorealistic`, `documentary style` | 真人、自然、街拍 |
| **电影感** | `cinematic`, `35mm film`, `anamorphic lens` | 叙事短片、广告 |
| **3D 动画** | `3D animation`, `Pixar-style`, `whimsical` | 卡通、奇幻、儿童内容 |
| **延时摄影** | `time-lapse`, `hyperlapse` | 城市、自然变化 |
| **航拍** | `drone shot`, `aerial view`, `bird's eye view` | 风景、建筑 |
| **手持纪实** | `handheld`, ` shaky cam`, `documentary footage` | 新闻、Vlog、紧张感 |
| **定格动画** | `stop-motion animation`, `claymation` | 创意短片 |

---

## 三、镜头语言参考

### 3.1 景别

| 景别 | 关键词 | 用途 |
|------|--------|------|
| 特写 | `extreme close-up` / `ECU` | 眼睛、细节、情绪 |
| 近景 | `close-up` / `CU` | 面部表情、物品细节 |
| 中景 | `medium shot` / `MS` | 半身人像、对话 |
| 全景 | `full shot` / `wide shot` | 全身人物、场景展示 |
| 远景 | `extreme wide shot` / `EWS` | 环境、大气氛围 |

### 3.2 运镜方式

| 运镜 | 关键词 | 效果 |
|------|--------|------|
| 跟随 | `tracking shot`, `following shot` | 跟随主体运动 |
| 环绕 | `orbiting shot`, `circling around` | 展示主体全貌 |
| 推进 | `push in`, `dolly in`, `zoom in` | 聚焦、强调 |
| 拉远 | `pull out`, `dolly out`, `zoom out` | 揭示环境 |
| 升降 | `crane shot`, `ascending/descending` | 场景转换 |
| 手持 | `handheld camera`, `POV shot` | 临场感、纪实感 |
| 航拍 | `drone shot`, `aerial tracking` | 大场景 |
| 静态 | `static camera`, `locked-off shot` | 延时、观察 |

### 3.3 景深控制

| 效果 | 关键词 |
|------|--------|
| 浅景深（背景虚化） | `shallow depth of field`, `bokeh`, `blurred background` |
| 深景深（全清晰） | `deep focus`, `everything in focus` |
| 移轴效果 | `tilt-shift` |

---

## 四、光影氛围词汇库

### 4.1 光线类型

```
golden hour          — 黄金时刻，暖金色柔光
blue hour            — 蓝调时刻，冷色柔光
backlight            — 逆光，轮廓光
sidelight            — 侧光，立体感强
overcast / diffused  — 阴天散射光，柔和均匀
neon / neon-lit      — 霓虹灯光，赛博朋克
volumetric lighting  — 体积光/丁达尔效应
rim light            — 边缘光，勾勒轮廓
practical lighting   — 场景光源（台灯、蜡烛等）
```

### 4.2 电影质感关键词

```
cinematic 35mm film          — 35mm 胶片质感
anamorphic lens              — 变形宽银幕镜头
lens flare                   — 镜头光晕
dreamy bokeh                 — 梦幻散景
high dynamic range / HDR     — 高动态范围
color graded                 — 调色后质感
film grain                   — 胶片颗粒感
soft focus                   — 柔焦
motion blur                  — 动态模糊
depth of field / DoF         — 景深效果
```

### 4.3 氛围描述

```
magical and romantic    — 奇幻浪漫
serene yet exhilarating — 宁静又令人振奋
tranquil and dynamic    — 宁静而富有动感
moody and atmospheric   — 情绪化氛围感
gritty and raw          — 粗粝真实
ethereal and dreamy     — 空灵梦幻
warm and inviting       — 温暖舒适
cold and isolating      — 冷寂孤独
```

---

## 五、运动与动态词汇

### 5.1 主体运动

| 场景 | 推荐词汇 |
|------|---------|
| 人物 | `walking gracefully`, `pacing slowly`, `turning to face`, `leaning against` |
| 动物 | `gliding`, `swimming fluidly`, `hopping playfully`, `running swiftly` |
| 车辆 | `speeding along`, `cornering with ease`, `kicking up dust` |
| 物体 | `floating gently`, `drifting gracefully`, `ascending and descending` |
| 自然 | `waves crashing`, `leaves swaying`, `clouds drifting`, `sunlight filtering` |

### 5.2 镜头运动节奏

```
fluidly       — 流畅地
smoothly      — 平滑地
gently        — 缓慢轻柔
rapidly       — 快速地
dynamically   — 动态地
gracefully    — 优雅地
steadily      — 稳定地
```

---

## 六、叙事技巧：让 Prompt 讲故事

单纯描述画面 vs 加入叙事张力，生成效果差距巨大。

### 6.1 对比

| 等级 | 写法 | 示例 |
|------|------|------|
| **差** | 静态罗列 | "A fish swims in coral reefs" |
| **中** | 增加细节 | "A vibrant tropical fish swimming gracefully among colorful coral reefs" |
| **好** | 加入叙事 | "An octopus is unaware of a king crab crawling towards it from behind a rock, claws raised and ready to attack" |
| **最好** | 叙事 + 情绪弧线 | "A gray-haired man deep in thought pondering the history of the universe... at the end he offers a subtle closed-mouth smile as if he found the answer to the mystery of life" |

### 6.2 叙事句式模板

```
# 冲突型
[主体A] is [状态], unaware of [威胁/惊喜] [正在靠近/发生]...

# 对比型
[Bright/Vivid subject] contrasting sharply against [dark/bleak environment]...

# 情绪弧线型
[主体] is [初始状态]... as [事件发生]... [最终状态/表情变化]

# 发现型
[主体] [探索动作]... stops to [交互]... looks up in awe at [震撼场景]
```

---

## 七、完整 Prompt 模板

### 7.1 自然风景模板

```text
A [drone/tracking/wide] shot of [主体] in [环境场景].
The [主体特征] [动作/状态].
[环境细节 - 天气/植被/地形/水面].
[光线描述].
[氛围关键词], [电影质感关键词].
```

### 7.2 人物肖像模板

```text
[Extreme close-up / Medium shot] of [人物描述] in [场景].
[服装/配饰描述].
[动作/表情/内心状态].
[背景环境描述].
[光线描述], [景深描述].
[电影质感/胶片属性].
```

### 7.3 动物/自然模板

```text
A [景别] of [动物] [动作] in [环境].
[动物外观细节].
[互动/叙事元素].
[环境细节].
[光线/水面/氛围].
[运镜方式], [画质关键词].
```

### 7.4 城市街景模板

```text
A [handheld/static/tracking] shot of [场景描述].
[主体动作/状态].
[环境细节 - 建筑/街道/人物].
[光线/天气].
[氛围/情绪].
[运镜转换], [景别转换].
```

### 7.5 3D 动画模板

```text
3D animation of [角色描述]. The character, [特征补充],
[动作/交互]. The [环境] is alive with [奇幻元素].
[角色与环境互动].
[色彩/光影氛围].
```

### 7.6 延时/速度感模板

```text
A dynamic time-lapse [tracking from / showing] [视角/场景].
The camera captures [移动元素] [运动方式].
[固定元素 - 窗框/地面/天空].
[速度/运动感描述].
[整体氛围], [景别].
```

---

## 八、完整示例

### 示例 1：水下微距（自然生态）

```text
A vibrant tropical fish swimming gracefully among colorful coral reefs
in a clear, turquoise ocean. The fish has bright blue and yellow scales
with a small, distinctive orange spot on its side, its fins moving fluidly.
The coral reefs are alive with a variety of marine life, including small
schools of colorful fish and sea turtles gliding by. The water is crystal
clear, allowing for a view of the sandy ocean floor below. The reef itself
is adorned with a mix of hard and soft corals in shades of red, orange,
and green. A close-up shot with dynamic movement.
```

**结构拆解**：
- 风格：写实自然（隐含）
- 镜头：`close-up shot with dynamic movement`
- 主体：热带鱼（蓝黄鳞片+橙色斑点）
- 环境：珊瑚礁 + 小鱼群 + 海龟 + 沙底
- 光影：`crystal clear water`
- 动态：`swimming gracefully`, `fins moving fluidly`

### 示例 2：人物肖像（电影叙事）

```text
An extreme close-up of a gray-haired man with a beard in his 60s,
he is deep in thought pondering the history of the universe as he
sits at a cafe in Paris, his eyes focus on people offscreen as they
walk as he sits mostly motionless, he is dressed in a wool coat suit
coat with a button-down shirt, he wears a brown beret and glasses
and has a very professorial appearance, and at the end he offers a
subtle closed-mouth smile as if he found the answer to the mystery
of life, the lighting is very cinematic with the golden light and
the Parisian streets and city in the background, depth of field,
cinematic 35mm film.
```

**结构拆解**：
- 风格：`cinematic 35mm film`
- 镜头：`extreme close-up` + `depth of field`
- 主体：60岁灰发大胡子老人（贝雷帽、眼镜、羊毛外套）
- 环境：巴黎咖啡馆 + 街道
- 叙事：沉思 → 观察行人 → 微笑（情绪弧线）
- 光影：`golden light`, `cinematic`

### 示例 3：航拍风景（旅行大片）

```text
A drone camera circles around a beautiful historic church built on
a rocky outcropping along the Amalfi Coast, the view showcases
historic and magnificent architectural details and tiered pathways
and patios, waves are seen crashing against the rocks below as the
view overlooks the horizon of the coastal waters and hilly landscapes
of the Amalfi Coast Italy, several distant people are seen walking
and enjoying vistas on patios of the dramatic ocean views, the warm
glow of the afternoon sun creates a magical and romantic feeling to
the scene, stunningly captured with beautiful photography.
```

**结构拆解**：
- 风格：`beautiful photography`（写实摄影）
- 镜头：`drone camera circles around`
- 主体：阿马尔菲海岸历史教堂
- 环境：岩石海岸 + 台阶 + 露台 + 远处人物
- 光影：`warm glow of the afternoon sun`
- 氛围：`magical and romantic feeling`

---

## 九、Prompt 优化检查清单

写完 Prompt 后，逐项检查：

- [ ] **开头是否声明了风格？**（realistic / cinematic / 3D animation / time-lapse）
- [ ] **镜头语言是否明确？**（景别 + 运镜方式）
- [ ] **主体是否有具体的视觉描述？**（外观、颜色、材质）
- [ ] **是否有动作/运动描述？**（避免静态呆板）
- [ ] **环境描述是否足够丰富？**（至少 2-3 个环境元素）
- [ ] **是否有光影/氛围关键词？**（至少 1 个光线词 + 1 个质感词）
- [ ] **是否包含微型叙事或情绪变化？**（强烈推荐）
- [ ] **长度是否在 120-150 词之间？**（最佳区间）
- [ ] **是否避免了抽象概念？**（AI 无法渲染"悲伤"，只能渲染"低头垂泪"）

---

## 十、常见问题与规避

| 问题 | 错误写法 | 正确写法 |
|------|---------|---------|
| 太抽象 | "a sad scene" | "a person with tears streaming down their face, looking down" |
| 缺少运镜 | "a car on a road" | "a tracking shot following behind a car speeding along a dirt road" |
| 没有风格 | 混合写实和动画元素 | 开头明确 `3D animation` 或 `photorealistic` |
| 镜头冲突 | "extreme close-up" 同时 "showing the vast environment" | 二选一，或用镜头转换描述 |
| 负面描述过多 | "no blur, no distortion, not dark..." | 用正面描述替代："sharp focus, clean lines, well-lit" |
| 时序混乱 | 在一个 Prompt 中描述多个不连续场景 | 每个 Prompt 只描述一个连续镜头 |
