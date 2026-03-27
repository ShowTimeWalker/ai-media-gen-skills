# 歌词生成任务状态查询

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /base_url/open-apis/v1/lyrics/query:
    post:
      summary: 歌词生成任务状态查询
      deprecated: false
      description: 输入任务id，查询对应信息。
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
                              description: >-
                                状态 succeeded-生成完成 waiting-等待中  running-生成中
                                failed-失败
                            title:
                              type: string
                              description: 标题
                            lyric:
                              type: string
                              description: 歌词
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
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: API文档/歌词生成
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6360744/apis/api-296183395-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: https://api.tianpuyue.cn
    description: 正式环境
security: []

```