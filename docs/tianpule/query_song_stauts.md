# 歌曲生成任务状态查询

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /base_url/open-apis/v1/song/query:
    post:
      summary: 歌曲生成任务状态查询
      deprecated: false
      description: 输入作品id，查询对应信息。
      tags:
        - API文档/歌曲生成
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
                      songs:
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
                                 sub_failed-失败"
                            lyrics_sections_status:
                              type: string
                              description: |-
                                "歌词对齐生成状态
                                waiting-等待中
                                running-生成中
                                sub_succeeded-成功
                                 sub_failed-失败"
                            model:
                              type: string
                              description: 生成的模型
                            title:
                              type: string
                              description: 标题
                            style:
                              type: string
                              description: 风格
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
                            lyrics_sections:
                              type: array
                              items:
                                type: object
                                properties:
                                  start:
                                    type: number
                                    description: 行的开始时间，以秒为单位
                                  end:
                                    type: number
                                    description: 行的结束时间，以秒为单位。
                                  text:
                                    type: string
                                    description: 行中的歌词。
                                required:
                                  - start
                                  - end
                                  - text
                                x-apifox-orders:
                                  - start
                                  - end
                                  - text
                              description: 歌词对齐信息
                            lyrics:
                              type: string
                              description: 歌词信息
                          x-apifox-orders:
                            - item_id
                            - status
                            - audio_hi_status
                            - lyrics_sections_status
                            - model
                            - title
                            - style
                            - prompt
                            - duration
                            - created_at
                            - finished_at
                            - audio_url
                            - audio_hi_url
                            - lyrics_sections
                            - lyrics
                        description: 作品信息列表
                    required:
                      - songs
                    x-apifox-orders:
                      - songs
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
                request_id: 4b185c6f-ed37-4b7d-af15-691be79996fc
                data:
                  songs:
                    - item_id: '123'
                      status: succeeded
                      audio_hi_status: sub_succeeded
                      lyrics_sections_status: sub_succeeded
                      event: null
                      model: TemPolor v3
                      title: Owl's Moonlit Waltz
                      style: Pop
                      prompt: A Song About an Owl’s Moonlit Dance in Happy Style
                      duration: 96
                      created_at: 1747207597
                      finished_at: 1747207721
                      audio_url: https://*************
                      audio_hi_url: https://*****************
                      lyrics_sections:
                        - start: 0.76
                          end: 0.78
                          text: '[intro]'
                        - start: 0.9
                          end: 0.92
                          text: |-

                            [verse]
                        - start: 16.761
                          end: 19.75
                          text: Under silver beams it flies
                        - start: 20.361
                          end: 23.97
                          text: Graceful wings that paint the skies
                        - start: 24.502
                          end: 28.612
                          text: Whispers soft beneath the trees
                        - start: 28.662
                          end: 32.102
                          text: Night unfolds with gentle breeze
                        - start: 32.462
                          end: 32.482
                          text: |-

                            [chorus]
                        - start: 33.342
                          end: 36.97
                          text: Moonlight guides the silent flight
                        - start: 37.622
                          end: 41.123
                          text: Owls dance in pure delight
                        - start: 41.623
                          end: 45.57
                          text: Stars above with shining eyes
                        - start: 45.863
                          end: 49.343
                          text: Joy unfolds before sunrise
                        - start: 49.823
                          end: 49.843
                          text: |-

                            [chorus]
                        - start: 50.043
                          end: 53.21
                          text: Moonlight guides the silent flight
                        - start: 53.843
                          end: 57.48
                          text: Owls dance in pure delight
                        - start: 58.304
                          end: 61.004
                          text: Stars above with shining eyes
                        - start: 61.024
                          end: 61.964
                          text: Joy unfolds before sunrise
                        - start: 61.984
                          end: 62.004
                          text: |-

                            [verse]
                        - start: 62.024
                          end: 63.294
                          text: Echoes laugh through shadowed glade
                        - start: 63.344
                          end: 64.244
                          text: Every step a note is played
                        - start: 64.264
                          end: 65.244
                          text: Twilight wraps the forest deep
                        - start: 65.264
                          end: 66.644
                          text: Hearts awake from quiet sleep
                        - start: 66.684
                          end: 66.704
                          text: |-

                            [chorus]
                        - start: 66.744
                          end: 70.324
                          text: Moonlight guides the silent flight
                        - start: 71.045
                          end: 74.61
                          text: Owls dance in pure delight
                        - start: 75.025
                          end: 78.765
                          text: Stars above with shining eyes
                        - start: 79.305
                          end: 82.405
                          text: Joy unfolds before sunrise
                        - start: 92.366
                          end: 96.026
                          text: |-

                            [inst]
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: API文档/歌曲生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296153360-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```