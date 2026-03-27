# 歌词生成

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /base_url/open-apis/v1/lyrics/generate:
    post:
      summary: 歌词生成
      deprecated: false
      description: 输入关键词，生成歌词。
      tags:
        - API文档/歌词生成
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
          example: application/json; charset=utf-8
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
                  description: 歌词生成的提示文本
                callback_url:
                  type: string
                  description: 任务生成成功后的回调地址，需要合作方自行开发，任务完成后调用通知。
                song_model:
                  type: string
                  description: |-
                    上传适配的歌曲模型名称,参考歌曲模型列表
                    - TemPolor v3
                    - TemPolor v3.5
                    - TemPolor v4.0
                  nullable: true
              required:
                - callback_url
                - prompt
              x-apifox-orders:
                - prompt
                - song_model
                - callback_url
            example:
              prompt: >-
                Genre: Electronic Dance Music (EDM), House, Techno  Style:
                Instrumental, Beat-driven, Club-oriented  Mood: Energetic,
                Vibrant, Hypnotic 
              song_model: TemPolor v3.5
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
      x-apifox-folder: API文档/歌词生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296174772-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```