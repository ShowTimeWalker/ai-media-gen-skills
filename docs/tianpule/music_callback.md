# 纯音乐生成回调接口

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/instrumental/callback:
    post:
      summary: 纯音乐生成回调接口
      deprecated: false
      description: >
        您需要自行开发一个回调接口，可以在https://webhook.site/
        配置一个回调进行测试。天谱乐在音乐生成后会回调你的接口进行任务状态通知，处理成功需返回：success。音乐一次生成会有三次回调，第一次mp3音频回调，第二次wav音频回调，第三次歌词数据回调。支持流式生成的模型会多一次回调，流式播放的url有效期10分钟。请确保你的接口可以正常通过公网访问，实现回调接口可以第一时间接受通知是我们最推荐的实现的方案，你也可以在任务提交一段时间后通过状态查询接口去兜底查询状态，查询接口有限流，请不要调用过于频繁。
      tags:
        - API文档/纯音乐生成
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                instrumentals:
                  type: array
                  items:
                    type: object
                    properties:
                      item_id:
                        type: string
                        description: 作品id
                      status:
                        type: string
                        description: >-
                          "状态 

                          running 任务中间状态，音乐生成中

                          main_succeeded 任务中间状态,mp3生成完毕 

                          failed 任务最终状态，mp3生成失败，任务失败，本次不计费

                          succeeded 任务最终状态，任务成功，意味着所有功能全部成功

                          part_failed  
                          任务最终状态，任务成功但是部分子功能失败，比如时间戳歌词生成失败，无损音乐生成失败"
                      audio_hi_status:
                        type: string
                        description: |-
                          "无损音频生成状态
                          waiting-等待中
                          running-生成中
                          sub_succeeded-成功
                          sub_failed-失败，audio_hi_status 对应wav_complete 回调事件"
                      model:
                        type: string
                        description: 生成的模型
                      title:
                        type: string
                        description: 标题
                      prompt:
                        type: string
                        description: 音乐描述
                      duration:
                        type: integer
                        description: 时长-秒
                      created_at:
                        type: integer
                        description: 任务创建的时间戳（以秒为单位）
                      finished_at:
                        type: integer
                        description: 任务完成的时间戳（以秒为单位），主功能完成的时间
                      audio_url:
                        type: string
                        description: 作品音频Url mp3  （有效期3天）
                      audio_hi_url:
                        type: string
                        description: 无损音频 wav  （有效期3天）
                      style:
                        type: string
                        description: 风格
                      event:
                        type: string
                        description: >-
                          回调事件  1、audio_complete  音乐生成完毕，这个事件最先收到，后续的事件顺序不固定 
                          2、wav_complete  无损音频生成完毕 3、lrcsections_complete
                          歌词时间戳生成完毕 4、audio_chunk 流式播放url生成完毕，支持流式播放的模型会有此回调
                    x-apifox-orders:
                      - item_id
                      - status
                      - audio_hi_status
                      - model
                      - title
                      - prompt
                      - duration
                      - created_at
                      - finished_at
                      - audio_url
                      - audio_hi_url
                      - style
                      - event
                  description: 作品信息列表
              required:
                - instrumentals
              x-apifox-orders:
                - instrumentals
            examples:
              '1':
                value:
                  instrumentals:
                    - audio_url: https://****
                      audio_hi_status: sub_succeeded
                      audio_hi_url: https://****
                      created_at: 1747278096
                      duration: 262
                      event: wav_complete
                      finished_at: 1747278158
                      item_id: '123'
                      model: TemPolor i3.5
                      prompt: >-
                        Genre: Electronic Dance Music (EDM), House, Techno 
                        Style: Instrumental, Beat-driven, Club-oriented  Mood:
                        Energetic, Vibrant, Hypnotic  Tempo: Typically ranges
                        from 120 to 130 BPM (Beats Per Minute)  Structure:
                        Build-ups, Drops, Breakdowns  Instruments/Sounds:
                        Synthesizers, Drum Machines, Basslines, Hi-hats, Pads 
                        Purpose: Ideal for clubs, parties, workout sessions, or
                        background ambiance  Vibe: Uplifting, Groovy, Futuristic
                      status: succeeded
                      style: electronic,house,techno
                      title: Neon Pulse Drive
              '2':
                value:
                  instrumentals:
                    - item_id: '22'
                      status: ut irure
                      audio_hi_status: sint sit
                      model: ad amet labore
                      title: 仍然对一共哼哦好些向下慢长椅缺乏
                      prompt: nostrud id sint
                      duration: 72
                      created_at: 1737062449961
                      finished_at: 86
                      audio_url: https://long-bran.info/
                      audio_hi_url: https://ironclad-disadvantage.org/
                      style: elit ad sint exercitation
                      event: incididunt exercitation sed
                summary: 示例 2
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
      x-apifox-folder: API文档/纯音乐生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296320241-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```