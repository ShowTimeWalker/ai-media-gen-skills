# 音乐生成

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /base_url/open-apis/v1/song/generate:
    post:
      summary: 音乐生成
      deprecated: false
      description: |
        支持用户自定义上传音乐描述和歌词，然后生成歌曲。
      tags:
        - API文档/歌曲生成
      parameters:
        - name: Authorization
          in: header
          description: ''
          required: true
          example: your-api-key
          schema:
            type: string
        - name: Content-Type
          in: header
          description: ''
          required: true
          example: application/json
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                prompt:
                  type: string
                  description: 通过输入提示词控制音乐的生成。参考示例
                model:
                  type: string
                  description: 要使用的模型。例如TemPolor v4.5
                callback_url:
                  type: string
                  description: 任务生成成功后的回调地址，需要合作方自行开发，任务完成后调用通知。
                lyrics:
                  type: string
                  description: 若上传为空，会自动调用歌词生成模型
                  nullable: true
                voice_id:
                  type: string
                  description: 输入官方歌手id即可指定歌手，使用对应声音生成歌曲
                  nullable: true
              required:
                - callback_url
                - prompt
                - model
              x-apifox-orders:
                - prompt
                - lyrics
                - model
                - voice_id
                - callback_url
            example:
              prompt: >-
                中文流行抒情歌曲，中慢速节奏（70–85
                BPM），钢琴与柔和合成器开场，副歌加入弦乐与鼓组增强情绪。旋律有记忆点，副歌朗朗上口。
              lyrics: |-
                [verse]
                夜色慢慢盖住城市的光
                人群散场 像没说完的谎
                手机亮着 却没人来访
                我把名字写进黑暗中央

                [pre-chorus]
                如果时间真的能倒流
                我会不会 选择不同的路口
                那些没说出口的以后
                还在心里 反复生锈

                [chorus]
                我在夜里 学会不再回头
                把你的影子交给风带走
                就算孤单 把我整夜围绕
                至少这次 我为自己停留

                [verse]
                窗外的雨敲着旧节奏
                像你离开那天的前奏
                回忆太重 压得我颤抖
                却也提醒我 还真实地活着

                [pre-chorus]
                如果世界真的听得懂
                我想让痛 快一点结束
                但当黎明慢慢靠拢
                我发现伤口 正在愈合中

                [chorus]
                我在夜里 学会不再回头
                把你的影子交给风带走
                就算孤单 把我整夜围绕
                至少这次 我为自己停留

                [bridge]
                也许爱 本来就没有答案
                只是陪伴 一段就够勇敢
                就算结局 没能并肩到最后
                我也感谢 曾经拥有

                [chorus]
                我在夜里 终于不再回头
                让所有遗憾慢慢沉没
                当世界再次亮起的时候
                我会带着自己 继续向前走

                [outro]
                天亮以后
                我还是我
              model: TemPolor v4.5
              callback_url: https://**************/callback
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: integer
                    description: 响应状态码
                  message:
                    type: string
                    description: 响应结果说明
                  request_id:
                    type: string
                    description: 本次请求的唯一ID、可用于联系客服排查问题等
                  data:
                    type: object
                    properties:
                      item_ids:
                        type: array
                        items:
                          type: string
                        description: 提交任务生成的作品id列表
                    required:
                      - item_ids
                    x-apifox-orders:
                      - item_ids
                    description: 具体的返回结果
                required:
                  - status
                  - message
                  - request_id
                  - data
                x-apifox-orders:
                  - status
                  - message
                  - request_id
                  - data
              example:
                status: 200000
                message: success
                request_id: b072a68c-4c1b-41be-bdd1-0a0309754de7
                data:
                  item_ids:
                    - '123'
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: API文档/歌曲生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296153313-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```