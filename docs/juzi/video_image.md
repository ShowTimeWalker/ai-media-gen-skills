# 全局公共参数

**全局Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**全局Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**全局Body参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**全局认证方式**

> 无需认证

# 状态码说明

| 状态码 | 中文描述 |
| --- | ---- |
| 暂无参数 |

# 橘子AI接口

> 创建人: 欧阳

> 更新人: 欧阳

> 创建时间: 2026-03-12 22:39:31

> 更新时间: 2026-03-12 23:33:22

```text
暂无描述
```

**目录Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**目录Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**目录Body参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| 暂无参数 |

**目录认证信息**

> 继承父级

**Query**

## 视频生成

> 创建人: 欧阳

> 更新人: 欧阳

> 创建时间: 2026-03-12 22:39:59

> 更新时间: 2026-03-22 21:43:33

```text
暂无描述
```

**接口状态**

> 已完成

**接口URL**

> http://juziaigc.com/open/api/video

**请求方式**

> POST

**Content-Type**

> form-data

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer 密钥 | string | 是 | - |

**请求Body参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| model | VEO 3.1 Fast 多参考版 | string | 是 | 模型 VEO 3.1 Fast 多参考版、Veo 3.1 Fast |
| prompt | 车子快速穿越到城堡里面玩漂移 | string | 是 | 提示词 |
| aspect_ratio | 9:16 | string | 是 | 比例 竖版9:16，横版16:9 |
| image_urls[0] | https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/f06aed0cb2ff8e1a131dd9ca6a56c781.png | array | 否 | 参考图数组如[https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/f06aed0cb2ff8e1a131dd9ca6a56c781.png,https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/0da76274207a04aae53423a753de15ab.png] |
| image_urls[1] | https://juziai.oss-cn-shenzhen.aliyuncs.com/uploads/20260301/0da76274207a04aae53423a753de15ab.png | array | 否 | - |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
	"code": 200,
	"msg": "success",
	"data": {
		"juzi_id": "30945f51-5bab-49ba-b851-4985b8295642"
	}
}
```

* 失败(404)

```javascript
暂无数据
```

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer 密钥 | string | 是 | - |

**Query**

## 视频进度

> 创建人: 欧阳

> 更新人: 欧阳

> 创建时间: 2026-03-13 00:15:37

> 更新时间: 2026-03-22 21:35:08

```text
暂无描述
```

**接口状态**

> 已完成

**接口URL**

> http://juziaigc.com/open/api/vNotify?juzi_id=30945f51-5bab-49ba-b851-4985b8295642

**请求方式**

> GET

**Content-Type**

> none

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer 密钥 | string | 是 | - |

**请求Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| juzi_id | 30945f51-5bab-49ba-b851-4985b8295642 | string | 是 | - |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
	"code": 200,
	"msg": "success",
	"data": {
		"status": "succeeded",
		"progress": 100,
		"juzi_url": "https://s.apipod.ai/videos/2026/03/12/e0edb00b-dca1-4758-9499-5d59783a5cb9.mp4",
		"complete_time": 1773334298
	}
}
```

* 失败(404)

```javascript
暂无数据
```

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer 密钥 | string | 是 | - |

**Query**

## 图片生成

> 创建人: 欧阳

> 更新人: 欧阳

> 创建时间: 2026-03-22 21:34:56

> 更新时间: 2026-03-22 22:13:12

```text
暂无描述
```

**接口状态**

> 开发中

**接口URL**

> http://juziaigc.com/open/api/images

**请求方式**

> POST

**Content-Type**

> form-data

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer mlh7k0pk8x1ht686r8j70zq25zl2rxtu | string | 是 | - |

**请求Body参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| model | nano-banana-2 | string | 是 | 支持模型
sora-image
gpt-image-1.5
nano-banana-fast |
| prompt | 性感不失大度的女人 | string | 是 | 提示词 |
| ratio | 16:9 | string | 否 | sora-image、gpt-image-1.5尺寸可选："auto"、"1:1"、"3:2"、"2:3"
其它模型尺寸可选  auto 1:1 16:9 9:16 4:3 3:4 3:2 2:3 5:4 4:5 21:9 |
| urls[0] | https://r2.grsai-resource.com/68879e99737d532.png | array | 否 | - |
| urls[1] | https://r2.grsai-resource.com/68879e99737d532.png | array | 否 | - |
| quality | 1K | string | 否 | nano-banana-2
nano-banana-2-cl(只支持1k，2k)
nano-banana-2-4k-cl(只支持4k)
nano-banana-pro
nano-banana-pro-vt
nano-banana-pro-cl
nano-banana-pro-vip(只支持1k，2k)
nano-banana-pro-4k-vip(只支持4k) |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
	"code": 200,
	"msg": "success",
	"data": {
		"juzi_id": "8-d6d7df5b-6759-4846-ae40-a935a0f582e0"
	}
}
```

* 失败(404)

```javascript
暂无数据
```

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer mlh7k0pk8x1ht686r8j70zq25zl2rxtu | string | 是 | - |

**Query**

## 图片进度

> 创建人: 欧阳

> 更新人: 欧阳

> 创建时间: 2026-03-22 22:01:04

> 更新时间: 2026-03-22 22:15:21

```text
暂无描述
```

**接口状态**

> 开发中

**接口URL**

> http://juziaigc.com/open/api/imgNotify?juzi_id=1-bc23381e-3232-4f60-8561-0dcb7525ab4d

**请求方式**

> GET

**Content-Type**

> none

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer mlh7k0pk8x1ht686r8j70zq25zl2rxtu | string | 是 | - |

**请求Query参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| juzi_id | 1-bc23381e-3232-4f60-8561-0dcb7525ab4d | string | 是 | - |

**认证方式**

> 继承父级

**响应示例**

* 成功(200)

```javascript
{
	"code": 200,
	"msg": "success",
	"data": {
		"sai_url": [
			{
				"url": "https://file1.aitohumanize.com/file/dc76bf01cfb34b9ba4f16a071257874c.png",
				"content": ""
			}
		],
		"width": 0,
		"height": 0,
		"status": "succeeded",
		"progress": 100,
		"complete_time": 100,
		"error": ""
	}
}
```

* 失败(404)

```javascript
暂无数据
```

**请求Header参数**

| 参数名 | 示例值 | 参数类型 | 是否必填 | 参数描述 |
| --- | --- | ---- | ---- | ---- |
| Authorization | Bearer xxx | string | 是 | - |

**Query**
