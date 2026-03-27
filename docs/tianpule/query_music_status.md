# 纯音乐生成任务状态查询

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /base_url/open-apis/v1/instrumental/query:
    post:
      summary: 纯音乐生成任务状态查询
      deprecated: false
      description: 输入作品id，查询对应信息。
      tags:
        - API文档/纯音乐生成
      parameters:
        - name: Authorization
          in: header
          description: API密钥
          required: true
          example: Tempo-********************************-3w
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
                item_ids:
                  type: array
                  items:
                    type: string
                  description: 需要查询的任务itemId列表，最大10。
              required:
                - item_ids
              x-apifox-orders:
                - item_ids
            example:
              item_ids:
                - '123'
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
                              description: |-
                                状态 
                                running-生成中 
                                main_succeeded 主功能成功  
                                failed 主功能失败
                                succeeded 成功
                                part_failed   部分子功能失败
                            audio_hi_status:
                              type: string
                              description: |-
                                无损音频生成状态
                                waiting-等待中
                                running-生成中
                                sub_succeeded-成功
                                sub_failed-失败
                            model:
                              type: string
                              description: 生成的模型
                            title:
                              type: string
                              description: 歌曲名称
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
                    required:
                      - instrumentals
                    x-apifox-orders:
                      - instrumentals
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
                request_id: 1165b1fc-e56d-4b55-a5d9-dbae434cd47d
                data:
                  instrumentals:
                    - item_id: '123'
                      status: succeeded
                      audio_hi_status: sub_succeeded
                      model: TemPolor i3.5
                      title: Neon Pulse Groove
                      prompt: >-
                        Genre: Electronic Dance Music (EDM), House, Techno 
                        Style: Instrumental, Beat-driven, Club-oriented  Mood:
                        Energetic, Vibrant, Hypnotic  Tempo: Typically ranges
                        from 120 to 130 BPM (Beats Per Minute)  Structure:
                        Build-ups, Drops, Breakdowns  Instruments/Sounds:
                        Synthesizers, Drum Machines, Basslines, Hi-hats, Pads 
                        Purpose: Ideal for clubs, parties, workout sessions, or
                        background ambiance  Vibe: Uplifting, Groovy, Futuristic
                      duration: 266
                      created_at: 1747276813
                      finished_at: 1747277627
                      audio_url: https://****
                      audio_hi_url: https://****
                      style: electronic,house,techno
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: API文档/纯音乐生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296137441-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```