## AI-PPT

### API
- [通义千问](https://www.aliyun.com/product/bailian)
- [UNSPLASH](https://unsplash.com/developers)

### 现阶段功能

- 调用阿里通义千问API获取PPT文本内容
- 调用UNSPLASH的API获取高质量图片
  - 模式一：随机选择图片
  - 模式二：用户通过图形界面选择图片（undone）
- 通过python-pptx生成简陋的slide
- 图形化界面选择资源文件（内容文件，prompt文件）

### 待优化

- 加入图片后排版混乱
- 现阶段的图片生成主题是写死在程序里的，未来可以让大模型生成图片关键词，每张slide生成不同主题的图
- 调用UNSPLASH时会遇到网络问题
- 图片源单一，未来可加入AI生成的图片
