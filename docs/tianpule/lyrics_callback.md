# 歌词生成回调接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/lyrics/callback:
    post:
      summary: 歌词生成回调接口
      deprecated: false
      description: >
        您需要自行开发一个回调接口，天谱乐在歌词生成后会回调你的接口进行任务状态通知，处理成功需返回字符串：success，如果没有返回success，天谱乐平台会有重试机制。请确保你的接口可以正常通过公网访问，实现回调接口可以第一时间接受通知是我们最推荐的实现的方案，你也可以在任务提交一段时间后通过状态查询接口去兜底查询状态，查询接口有限流，请不要调用过于频繁。
      tags:
        - API文档/歌词生成
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                lyrics:
                  type: array
                  items:
                    type: object
                    properties:
                      item_id:
                        type: string
                        description: 作品id
                      status:
                        type: string
                        description: 状态 succeeded-生成完成 waiting-等待中  running-生成中 failed-失败
                      title:
                        type: string
                        description: 标题
                      lyric:
                        type: string
                    x-apifox-orders:
                      - item_id
                      - status
                      - title
                      - lyric
                  description: 作品信息列表
              required:
                - lyrics
              x-apifox-orders:
                - lyrics
            example:
              lyrics:
                - item_id: '123'
                  status: succeeded
                  title: 月光诉语
                  lyric: |-
                    [Intro]

                    [Verse]
                    月光穿过了重重云层轻轻洒落在你的发梢
                    夜晚的街道没有归人只有我和影子漫长寂寞
                    思绪像风一样游走不定每一刻都在等待醒悟
                    星空下藏着我们未说的话安静得让人心动

                    [Verse]
                    街角的灯光映照着回忆像一场未完的电影
                    月亮挂在天边像眼睛看尽孤独与梦想的交替
                    风吹过记忆的街道那温柔的触感仍在心底
                    时间悄无声息地走过把一切留给夜色阑珊

                    [Inst]

                    [Chorus]
                    月亮是夜的诗句柔柔地诉说无声的誓言
                    孤独的光辉映照着远方梦里的模样清晰
                    在这沉默的时刻我悄悄把思念放飞天空
                    让它随星光飘散融入那无边的黑夜

                    [Chorus]
                    转身看那苍穹依旧静静守护我们的秘密
                    月色流淌是温柔的指引穿越深深的暗夜
                    我和你之间没有距离只有心跳交织的时光
                    让这份感动在风中轻轻地回荡

                    [Inst]
      responses:
        '200':
          description: ''
          content:
            '*/*':
              schema:
                result: success
                type: string
              example: success
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: API文档/歌词生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296320243-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```