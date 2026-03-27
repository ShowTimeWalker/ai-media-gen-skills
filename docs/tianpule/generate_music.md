# 纯音乐生成

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /base_url/open-apis/v1/instrumental/generate:
    post:
      summary: 纯音乐生成
      deprecated: false
      description: 输入关键词，生成纯音乐，支持通过prompt精准控制时长。
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
                prompt:
                  type: string
                  description: |-
                    通过输入提示词控制纯音乐的生成，可支持输入节奏、调性、和弦、时长等，实现精确控制。
                    #例：
                    #节奏：BPM 85
                    #调性：Cmajor
                    #和弦：C,Am,F,G
                    #时长: 100秒
                model:
                  type: string
                  description: 要使用的模型。
                callback_url:
                  type: string
                  description: 任务生成成功后的回调地址，需要合作方自行开发，任务完成后调用通知。
              required:
                - callback_url
                - prompt
                - model
              x-apifox-orders:
                - prompt
                - model
                - callback_url
            example:
              prompt: >-
                Genre: Electronic Dance Music (EDM), House, Techno  Style:
                Instrumental, Beat-driven, Club-oriented  Mood: Energetic,
                Vibrant, Hypnotic 
              model: TemPolor i3.5
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
      x-apifox-folder: API文档/纯音乐生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296107004-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```