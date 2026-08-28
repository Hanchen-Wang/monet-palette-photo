[English](README.md) | [简体中文](README.zh-CN.md)

# Monet-Palette-Photo

通过莫奈式色彩、光线、笔触和边缘逻辑转换用户照片，同时保留主体身份与关键空间关系。

这是一个艺术指导 skill，而不是通用油画滤镜。照片始终是人物、物体、几何结构、光线与色彩关系的事实来源。

## 模式

| 模式 | 处理方式 |
|---|---|
| Full Impression | 重绘整张照片。 |
| Subject Monetization | 重绘主体，并弱化周围环境。 |
| Atmospheric Monetization | 保留摄影锚点，转换空气、水面、倒影或光线。 |
| Zine Hybrid | 将摄影锚点与莫奈化绘画区域结合。 |
| Distilled Monet | 根据原图语义和结构进行更自由的绘画重构。 |

强度从 `M1`（轻微）到 `M4`（抽象）。使用 `Sparse Social` 可以获得更简洁的形状、更低的视觉密度，以及更清晰的社交媒体缩略图效果。

## Zine Hybrid 策略

- `Integrated Field`：摄影锚点嵌入完整的绘画或简化环境中。
- `Cutout Isolation`：只保留一个摄影锚点和一个绘画载体，并让安静纸面占画面的 30–60%。

可选的 `Comparison Poster` 会把原图放在上方、生成作品放在下方，组合成暖色背景的 4:5 画报。

## 调用示例

```text
使用 Monet-Palette-Photo 的 Atmospheric Monetization · M2。
保留建筑的摄影质感，转换天空、远山和水面。
```

```text
使用 Zine Hybrid · M3 · Sparse Social · Integrated Field。
保留人物作为摄影锚点，其余场景进行绘画转换。
```

```text
使用 Zine Hybrid · M2 · Cutout Isolation，保留约 40% 安静纸面。
```

## 注意事项

- 默认不添加可见文字。
- 不会凭空加入原图不支持的莫奈标志性元素。
- 精确保留原始像素需要确定性蒙版或合成流程。仅使用生成式编辑时只能进行最佳努力保留，不能称为像素级精确保留。

完整工作流见 [SKILL.md](SKILL.md)，模式契约、schema、提示词和 QA 说明见 [references/](references/)。
