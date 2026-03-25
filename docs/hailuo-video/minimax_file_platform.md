> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimaxi.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文件上传

> 使用本接口，在 MiniMax 开放平台，上传所需文件。



## OpenAPI

````yaml /api-reference/file/management/api/openapi.json POST /v1/files/upload
openapi: 3.1.0
info:
  title: MiniMax File Management API
  description: >-
    MiniMax file management API for uploading, retrieving, listing, and deleting
    files
  license:
    name: MIT
  version: 1.0.0
servers:
  - url: https://api.minimaxi.com
security:
  - bearerAuth: []
paths:
  /v1/files/upload:
    post:
      tags:
        - Files
      summary: Upload File
      operationId: uploadFile
      parameters:
        - name: Content-Type
          in: header
          required: true
          description: '请求体的媒介类型 `multipart/form-data` '
          schema:
            type: string
            enum:
              - multipart/form-data
            default: multipart/form-datan
      requestBody:
        description: ''
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - purpose
                - file
              properties:
                purpose:
                  type: string
                  description: |-
                    文件使用目的。取值及支持格式如下：

                    1. __voice_clone__: 快速复刻原始文件，（支持mp3、m4a、wav格式）
                    2. __prompt_audio__: 音色复刻的示例音频，（支持mp3、m4a、wav格式）
                    3. __t2a_async_input__: 异步长文本语音生成合成中，请求体中的文本文件（支持text、zip格式）
                  enum:
                    - voice_clone
                    - prompt_audio
                    - t2a_async_input
                  example: t2a_async_input
                file:
                  type: string
                  format: binary
                  description: 需要上传的文件。填写文件的路径地址
        required: true
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UploadFileResp'
components:
  schemas:
    UploadFileResp:
      type: object
      properties:
        file:
          $ref: '#/components/schemas/FileObject'
        base_resp:
          $ref: '#/components/schemas/UploadFileBaseResp'
      example:
        file:
          file_id: ${file_id}
          bytes: 5896337
          created_at: 1700469398
          filename: MiniMax Open Platform-Test bot.docx
          purpose: t2a_async_input
        base_resp:
          status_code: 0
          status_msg: success
    FileObject:
      type: object
      properties:
        file_id:
          type: integer
          format: int64
          description: 文件的唯一标识符
        bytes:
          type: integer
          format: int64
          description: 文件大小，以字节为单位
        created_at:
          type: integer
          format: int64
          description: 创建文件时的 Unix 时间戳，以秒为单位
        filename:
          type: string
          description: 文件的名称
        purpose:
          type: string
          description: 文件的使用目的
    UploadFileBaseResp:
      type: object
      properties:
        status_code:
          type: integer
          description: |-
            状态码如下：
            - 1000, 未知错误
            - 1001, 超时
            - 1002, 触发RPM限流
            - 1004, 鉴权失败
            - 1008, 余额不足
            - 1013, 服务内部错误
            - 1026, 输入内容错误
            - 1027, 输出内容错误
            - 1039, 触发TPM限流
            - 2013, 输入格式信息不正常

            更多内容可查看[错误码查询列表](/api-reference/errorcode)了解详情
        status_msg:
          type: string
          description: 状态详情
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |-
        `HTTP: Bearer Auth`
         - Security Scheme Type: http
         - HTTP Authorization Scheme: Bearer API_key，用于验证账户信息，可在 [账户管理>接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key) 中查看。

````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimaxi.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文件列出

> 使用本接口，列出不同分类下的文件。



## OpenAPI

````yaml /api-reference/file/management/api/openapi.json GET /v1/files/list
openapi: 3.1.0
info:
  title: MiniMax File Management API
  description: >-
    MiniMax file management API for uploading, retrieving, listing, and deleting
    files
  license:
    name: MIT
  version: 1.0.0
servers:
  - url: https://api.minimaxi.com
security:
  - bearerAuth: []
paths:
  /v1/files/list:
    get:
      tags:
        - Files
      summary: List Files
      operationId: listFiles
      parameters:
        - name: purpose
          in: query
          required: true
          description: |-
            列出文件分类。取值及支持格式如下：

            1. __voice_clone__: 快速复刻原始文件
            2. __prompt_audio__: 音色复刻的示例音频
            3. __t2a_async__: 异步长文本语音生成合成中音频
          schema:
            type: string
            enum:
              - voice_clone
              - prompt_audio
              - t2a_async_input
            example: t2a_async_input
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ListFileResp'
components:
  schemas:
    ListFileResp:
      type: object
      properties:
        files:
          type: array
          items:
            $ref: '#/components/schemas/FileObject'
          description: List of files
        base_resp:
          $ref: '#/components/schemas/ListRetrieveDeleteFileBaseResp'
      example:
        files:
          - file_id: ${file_id}
            bytes: 5896337
            created_at: 1699964873
            filename: 297990555456011.tar
            purpose: t2a_async_input
          - file_id: ${file_id}
            bytes: 5896337
            created_at: 1700469398
            filename: 297990555456911.tar
            purpose: t2a_async_input
        base_resp:
          status_code: 0
          status_msg: success
    FileObject:
      type: object
      properties:
        file_id:
          type: integer
          format: int64
          description: 文件的唯一标识符
        bytes:
          type: integer
          format: int64
          description: 文件大小，以字节为单位
        created_at:
          type: integer
          format: int64
          description: 创建文件时的 Unix 时间戳，以秒为单位
        filename:
          type: string
          description: 文件的名称
        purpose:
          type: string
          description: 文件的使用目的
    ListRetrieveDeleteFileBaseResp:
      type: object
      properties:
        status_code:
          type: integer
          description: |-
            状态码如下：
            - 1000, 未知错误
            - 1001, 超时
            - 1002, 触发RPM限流
            - 1004, 鉴权失败
            - 1008, 余额不足
            - 1013, 服务内部错误
            - 1026, 输入内容错误
            - 1027, 输出内容错误
            - 1039, 触发TPM限流
            - 2013, 输入格式信息不正常

            更多内容可查看[错误码查询列表](/api-reference/errorcode)了解详情
        status_msg:
          type: string
          description: 状态详情
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |-
        `HTTP: Bearer Auth`
         - Security Scheme Type: http
         - HTTP Authorization Scheme: Bearer API_key，用于验证账户信息，可在 [账户管理>接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key) 中查看。

````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimaxi.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文件检索

> 使用本接口，检索 MiniMax 开放平台上的文件。



## OpenAPI

````yaml /api-reference/file/management/api/openapi.json GET /v1/files/retrieve
openapi: 3.1.0
info:
  title: MiniMax File Management API
  description: >-
    MiniMax file management API for uploading, retrieving, listing, and deleting
    files
  license:
    name: MIT
  version: 1.0.0
servers:
  - url: https://api.minimaxi.com
security:
  - bearerAuth: []
paths:
  /v1/files/retrieve:
    get:
      tags:
        - Files
      summary: Retrieve File
      operationId: retrieveFile
      parameters:
        - name: file_id
          in: query
          required: true
          description: |-
            文件的唯一标识符
            本接口支持：

            - 视频生成中，查询视频任务状态接口获得的file_id
            - 异步语音合成中，查询语音生成任务状态接口获得的file_id
          schema:
            type: integer
            format: int64
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/RetrieveFileResp'
components:
  schemas:
    RetrieveFileResp:
      type: object
      properties:
        file:
          $ref: '#/components/schemas/FileObject'
        base_resp:
          $ref: '#/components/schemas/ListRetrieveDeleteFileBaseResp'
      example:
        file:
          file_id: ${file_id}
          bytes: 5896337
          created_at: 1700469398
          filename: output_aigc.mp4
          purpose: video_generation
          download_url: www.downloadurl.com
        base_resp:
          status_code: 0
          status_msg: success
    FileObject:
      type: object
      properties:
        file_id:
          type: integer
          format: int64
          description: 文件的唯一标识符
        bytes:
          type: integer
          format: int64
          description: 文件大小，以字节为单位
        created_at:
          type: integer
          format: int64
          description: 创建文件时的 Unix 时间戳，以秒为单位
        filename:
          type: string
          description: 文件的名称
        purpose:
          type: string
          description: 文件的使用目的
    ListRetrieveDeleteFileBaseResp:
      type: object
      properties:
        status_code:
          type: integer
          description: |-
            状态码如下：
            - 1000, 未知错误
            - 1001, 超时
            - 1002, 触发RPM限流
            - 1004, 鉴权失败
            - 1008, 余额不足
            - 1013, 服务内部错误
            - 1026, 输入内容错误
            - 1027, 输出内容错误
            - 1039, 触发TPM限流
            - 2013, 输入格式信息不正常

            更多内容可查看[错误码查询列表](/api-reference/errorcode)了解详情
        status_msg:
          type: string
          description: 状态详情
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |-
        `HTTP: Bearer Auth`
         - Security Scheme Type: http
         - HTTP Authorization Scheme: Bearer API_key，用于验证账户信息，可在 [账户管理>接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key) 中查看。

````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimaxi.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文件下载

> 使用本接口，下载模型生成的文件。



## OpenAPI

````yaml /api-reference/file/management/api/openapi.json GET /v1/files/retrieve_content
openapi: 3.1.0
info:
  title: MiniMax File Management API
  description: >-
    MiniMax file management API for uploading, retrieving, listing, and deleting
    files
  license:
    name: MIT
  version: 1.0.0
servers:
  - url: https://api.minimaxi.com
security:
  - bearerAuth: []
paths:
  /v1/files/retrieve_content:
    get:
      tags:
        - Files
      summary: Retrieve File Content
      operationId: retrieveFileContent
      parameters:
        - name: file_id
          in: query
          required: true
          description: 需要下载的文件ID
          schema:
            type: integer
            format: int64
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: string
                format: binary
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |-
        `HTTP: Bearer Auth`
         - Security Scheme Type: http
         - HTTP Authorization Scheme: Bearer API_key，用于验证账户信息，可在 [账户管理>接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key) 中查看。

````

> ## Documentation Index
> Fetch the complete documentation index at: https://platform.minimaxi.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文件删除

> 使用本接口，删除 MiniMax 开放平台上的相关文件。



## OpenAPI

````yaml /api-reference/file/management/api/openapi.json POST /v1/files/delete
openapi: 3.1.0
info:
  title: MiniMax File Management API
  description: >-
    MiniMax file management API for uploading, retrieving, listing, and deleting
    files
  license:
    name: MIT
  version: 1.0.0
servers:
  - url: https://api.minimaxi.com
security:
  - bearerAuth: []
paths:
  /v1/files/delete:
    post:
      tags:
        - Files
      summary: Delete File
      operationId: deleteFile
      parameters:
        - name: Content-Type
          in: header
          required: true
          description: '请求体的媒介类型 `multipart/form-data` '
          schema:
            type: string
            enum:
              - multipart/form-data
            default: multipart/form-datan
      requestBody:
        description: ''
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/DeleteFileReq'
        required: true
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DeleteFileResp'
components:
  schemas:
    DeleteFileReq:
      type: object
      required:
        - file_id
        - purpose
      properties:
        file_id:
          type: integer
          format: int64
          description: 文件的唯一标识符
        purpose:
          type: string
          description: |-
            文件使用目的。取值及支持格式如下：
            1. voice_clone
            2. prompt_audio
            3. t2a_async
            4. t2a_async_input
            5. video_generation
          enum:
            - voice_clone
            - prompt_audio
            - t2a_async
            - t2a_async_input
            - video_generation
      example:
        file_id: ${file_id}
        purpose: t2a_async_input
    DeleteFileResp:
      type: object
      properties:
        file_id:
          type: integer
          format: int64
          description: The unique identifier for the file.
        base_resp:
          $ref: '#/components/schemas/ListRetrieveDeleteFileBaseResp'
      example:
        file_id: ${file_id}
        base_resp:
          status_code: 0
          status_msg: success
    ListRetrieveDeleteFileBaseResp:
      type: object
      properties:
        status_code:
          type: integer
          description: |-
            状态码如下：
            - 1000, 未知错误
            - 1001, 超时
            - 1002, 触发RPM限流
            - 1004, 鉴权失败
            - 1008, 余额不足
            - 1013, 服务内部错误
            - 1026, 输入内容错误
            - 1027, 输出内容错误
            - 1039, 触发TPM限流
            - 2013, 输入格式信息不正常

            更多内容可查看[错误码查询列表](/api-reference/errorcode)了解详情
        status_msg:
          type: string
          description: 状态详情
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |-
        `HTTP: Bearer Auth`
         - Security Scheme Type: http
         - HTTP Authorization Scheme: Bearer API_key，用于验证账户信息，可在 [账户管理>接口密钥](https://platform.minimaxi.com/user-center/basic-information/interface-key) 中查看。

````