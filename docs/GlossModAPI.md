# API v3 使用说明

## 概述

API v3 提供对3DM Mod网站数据的访问，包括只读的数据查询接口和写入的内容发布接口。

## 授权

你只需要在 header 中添加 `Authorization: {APPKEY}` 即可使用 API。

## 基础信息

- **基础URL**: `/api/v3`
- **请求方法**: GET (查询接口), POST (发布接口)
- **响应格式**: JSON
- **缓存时间**: 
  - 默认缓存: 1天
  - 搜索和热门内容: 1小时
  - 不活跃内容: 30天
- **权限**: 只读查询 + 内容发布（需要 API Key）

## 响应格式

::: code-group
```json [成功响应]
{
  "success": true,
  "msg": "操作成功消息",
  "data": {
    // 实际数据
  }
}
```

```json [错误响应]
{
  "success": false,
  "msg": "错误消息",
  "data": null
}
```
:::

---

## API 接口

### 1. 游戏相关

#### 1.1 游戏列表

**GET** `/api/v3/games`

获取游戏列表,支持分页、搜索、类型筛选和排序。

**参数:**

| 参数名      | 类型   | 必填 | 默认值   | 说明                                                   |
| ----------- | ------ | ---- | -------- | ------------------------------------------------------ |
| `page`      | number | 否   | 1        | 页码                                                   |
| `pageSize`  | number | 否   | 20       | 每页数量，最大50                                       |
| `gameType`  | string | 否   | -        | 游戏类型筛选(如: 动作、冒险、射击等)                   |
| `search`    | string | 否   | -        | 搜索关键词(游戏名称、英文名称、描述)                   |
| `sortBy`    | string | 否   | allcount | 排序字段: `allcount`(总Mod数), `tcount`(最近30天Mod数) |
| `sortOrder` | string | 否   | desc     | 排序方向: `asc`(升序), `desc`(降序)                    |

**响应数据:**

```typescript
{
  data: Array<{
    id: number;              // 游戏ID
    game_name: string;       // 游戏名称
    game_ename: string;      // 游戏英文名称
    game_cover_imgUrl: string; // 游戏封面图
    game_path: string;       // 游戏路径
    game_desc: string;       // 游戏描述
    allcount: number;        // 总Mod数量
    tcount: number;          // 最近30天Mod数量
  }>;
  count: number;             // 总数
  page: number;              // 当前页码
  pageSize: number;          // 每页数量
  totalPages: number;        // 总页数
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/games?page=1&pageSize=20&gameType=动作&search=战争" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/games', {
  params: {
    page: 1,
    pageSize: 20,
    gameType: '动作',
    search: '战争'
  },
  headers: {
    Authorization: '{APPKEY}'
  }
});
```

```python [Python]
import requests

response = requests.get('https://mod.3dmgame.com/api/v3/games', 
  headers={'Authorization': '{APPKEY}'},
  params={
    'page': 1,
    'pageSize': 20,
    'gameType': '动作',
    'search': '战争'
  }
)
data = response.json()
```

```csharp [C#]
using System.Net.Http;
using System.Threading.Tasks;

var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");

var response = await client.GetAsync(
  "https://mod.3dmgame.com/api/v3/games?page=1&pageSize=20&gameType=动作&search=战争"
);
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
import java.net.http.*;
import java.net.URI;

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/games?page=1&pageSize=20&gameType=动作&search=战争"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
library(httr)

response <- GET(
  "https://mod.3dmgame.com/api/v3/games",
  add_headers(Authorization = "{APPKEY}"),
  query = list(
    page = 1,
    pageSize = 20,
    gameType = "动作",
    search = "战争"
  )
)
data <- content(response, "parsed")
```

```go [Go]
package main

import (
  "fmt"
  "io"
  "net/http"
)

func main() {
  url := "https://mod.3dmgame.com/api/v3/games?page=1&pageSize=20&gameType=动作&search=战争"
  req, _ := http.NewRequest("GET", url, nil)
  req.Header.Set("Authorization", "{APPKEY}")
  
  client := &http.Client{}
  resp, _ := client.Do(req)
  defer resp.Body.Close()
  
  body, _ := io.ReadAll(resp.Body)
  fmt.Println(string(body))
}
```
:::

---

#### 1.2 游戏详情

**GET** `/api/v3/games/{id}`

获取指定游戏的详细信息,包括Mod统计数据。

**参数:**

| 参数名 | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| `id`   | number | 是   | 游戏ID |

**响应数据:**

```typescript
{
  id: number;
  game_name: string;
  game_ename: string;
  game_cover_imgUrl: string;
  game_path: string;
  game_desc: string;
  game_type: string;
  allcount: number;        // 总Mod数量
  tcount: number;          // 最近30天Mod数量
  totalDownloads: number;  // 总下载量
  totalViews: number;      // 总浏览量
  // ... 其他游戏信息
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/games/123" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/games/123', {
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/games/123', 
  headers={'Authorization': '{APPKEY}'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync("https://mod.3dmgame.com/api/v3/games/123");
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/games/123"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/games/123",
  add_headers(Authorization = "{APPKEY}")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/games/123"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

### 2. Mod相关

#### 2.1 Mod列表

**GET** `/api/v3/mods`

获取Mod列表,支持多种筛选条件、排序和分页。

**参数:**

| 参数名         | 类型         | 必填 | 默认值 | 说明                                                             |
| -------------- | ------------ | ---- | ------ | ---------------------------------------------------------------- |
| `page`         | number       | 否   | 1      | 页码                                                             |
| `pageSize`     | number       | 否   | 20     | 每页数量，最大100                                                |
| `gameId`       | number/array | 否   | -      | 游戏ID筛选，支持单个或数组                                       |
| `gameType`     | number       | 否   | -      | Mod类型ID筛选(即 mods_type_id)                                   |
| `key`          | string/array | 否   | -      | 标签筛选，支持单个或数组                                         |
| `original`     | number       | 否   | -      | 创作类型: `1`=原创 `2`=二创 `3`=翻译 `4`=精华                    |
| `mods_publish` | number       | 否   | -      | 发布者用户ID                                                     |
| `time`         | number       | 否   | -      | 时间筛选: `1`=今天, `2`=最近一周, `3`=最近一个月, `4`=最近三个月 |
| `search`       | string       | 否   | -      | 搜索关键词(标题)                                                 |
| `order`        | number       | 否   | 0      | 排序方式(通过 UtilsModel.GetModOrder 处理)                       |
| `support_gmm`  | boolean      | 否   | false  | 是否支持管理器安装                                               |

**响应数据:**

```typescript
{
  data: Array<{
    id: number;
    mods_title: string;         // Mod标题
    mods_desc: string;          // Mod描述
    mods_author: string;        // Mod作者
    mods_version: string;       // Mod版本
    mods_image_url: string;     // Mod封面图
    game_id: number;            // 游戏ID
    game_name: string;          // 游戏名称
    game_imgUrl: string;        // 游戏图片
    mods_type_id: number;       // Mod类型ID
    mods_type_name: string;     // Mod类型名称
    mods_download_cnt: number;  // 下载数
    mods_click_cnt: number;     // 浏览数
    mods_mark_cnt: number;      // 收藏数
    mods_updateTime: Date;      // 更新时间
    mods_createTime: Date;      // 创建时间
    mods_isRecommend: boolean;  // 是否推荐
    // 用户信息
    user_nickName: string;      // 发布者昵称
    user_avatar: string;        // 发布者头像
    user_tag: string;           // 用户标签
    user_tag_colour: string;    // 标签颜色
  }>;
  games: Array<IGameInfo>;      // 搜索时关联的游戏列表
  count: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/mods?page=1&gameId=123&time=2&order=0" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/mods', {
  params: {
    page: 1,
    pageSize: 20,
    gameId: 123,
    time: 2,  // 最近一周
    order: 0
  },
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/mods',
  headers={'Authorization': '{APPKEY}'},
  params={
    'page': 1,
    'gameId': 123,
    'time': 2,
    'order': 0
  }
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync(
  "https://mod.3dmgame.com/api/v3/mods?page=1&gameId=123&time=2&order=0"
);
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/mods?page=1&gameId=123&time=2&order=0"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/mods",
  add_headers(Authorization = "{APPKEY}"),
  query = list(page = 1, gameId = 123, time = 2, order = 0)
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/mods?page=1&gameId=123&time=2&order=0"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

#### 2.2 Mod详情

**GET** `/api/v3/mods/{id}`

获取指定Mod的详细信息,包括用户信息和游戏信息。

**参数:**

| 参数名 | 类型   | 必填 | 说明   |
| ------ | ------ | ---- | ------ |
| `id`   | number | 是   | Mod ID |

**响应数据:**

```typescript
{
  id: number;
  mods_title: string;
  mods_desc: string;
  mods_content: string;       // Mod详细介绍
  mods_author: string;
  mods_version: string;
  mods_image_url: string;
  mods_resource: Array<{      // 资源文件列表
    id: number;
    mods_resource_name: string;
    mods_resource_desc: string;
    mods_resource_url: string;
    mods_resource_version: string;
    mods_resource_size: string;
    mods_resource_formart: string;
  }>;
  game_id: number;
  game_name: string;
  game_cover_imgUrl: string;
  game_path: string;
  mods_download_cnt: number;
  mods_click_cnt: number;
  mods_mark_cnt: number;
  // 用户信息
  user_nickName: string;
  user_avatar: string;
  user_Intr: string;
  user_tag: string;
  user_tag_colour: string;
  user_fan: number;
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/mods/456" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/mods/456', {
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/mods/456',
  headers={'Authorization': '{APPKEY}'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync("https://mod.3dmgame.com/api/v3/mods/456");
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/mods/456"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/mods/456",
  add_headers(Authorization = "{APPKEY}")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/mods/456"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

#### 2.3 发布Mod

**POST** `/api/v3/mods/publish`

发布或更新Mod。如果提供 `id` 则为更新操作,否则为新增操作。

**权限要求:** 需要有效的 API Key

**请求头:**

| 参数名          | 类型   | 必填 | 说明    |
| --------------- | ------ | ---- | ------- |
| `Authorization` | string | 是   | API Key |

**请求体参数:**

| 参数名          | 类型   | 必填   | 说明                            |
| --------------- | ------ | ------ | ------------------------------- |
| `id`            | number | 更新时 | Mod ID (更新时必填，新增时不填) |
| `mods_title`    | string | 是     | Mod标题                         |
| `game_id`       | number | 是     | 游戏ID                          |
| `mods_type_id`  | number | 是     | Mod类型ID                       |
| `mods_version`  | string | 是     | Mod版本                         |
| `mods_author`   | string | 是     | Mod作者                         |
| `mods_content`  | string | 是     | Mod详细介绍(至少10个字符)       |
| `mods_resource` | array  | 是     | 资源文件列表(至少包含一个资源)  |

**资源文件对象参数:**

| 参数名                         | 类型   | 必填 | 说明         |
| ------------------------------ | ------ | ---- | ------------ |
| `mods_resource_name`           | string | 是   | 资源名称     |
| `mods_resource_desc`           | string | 否   | 资源描述     |
| `mods_resource_url`            | string | 是   | 下载链接     |
| `mods_resource_version`        | string | 是   | 资源版本     |
| `mods_resource_size`           | string | 是   | 文件大小     |
| `mods_resource_sort`           | number | 否   | 排序         |
| `mods_resource_formart`        | string | 否   | 文件格式     |
| `mods_resource_latest_version` | string | 否   | 最新版本标识 |

**注意事项:**
- 新发布的Mod默认状态为 `-1` (审核中)
- `3DM Mod组` 用户发布的内容状态为 `3` (直接通过)
- 更新操作只能修改自己发布的Mod
- 系统会自动为资源文件分配唯一ID

**示例:**

::: code-group
```sh [curl]
curl -X POST "https://mod.3dmgame.com/api/v3/mods/publish" \
-H "Authorization: {APPKEY}" \
-H "Content-Type: application/json" \
-d '{
  "mod": {
    "mods_title": "超级武器包",
    "game_id": 123,
    "mods_type_id": 456,
    "mods_version": "1.0.0",
    "mods_author": "ModAuthor",
    "mods_content": "这是一个包含各种超级武器的Mod，为游戏增加更多战斗选择。",
    "mods_resource": [
      {
        "mods_resource_name": "主文件",
        "mods_resource_url": "https://example.com/download/main.zip",
        "mods_resource_version": "1.0.0",
        "mods_resource_size": "25.6MB"
      }
    ]
  }
}'
```

```typescript [TypeScript]
const response = await axios.post('/api/v3/mods/publish', {
  mod: {
    mods_title: '超级武器包',
    game_id: 123,
    mods_type_id: 456,
    mods_version: '1.0.0',
    mods_author: 'ModAuthor',
    mods_content: '这是一个包含各种超级武器的Mod，为游戏增加更多战斗选择。',
    mods_resource: [{
      mods_resource_name: '主文件',
      mods_resource_url: 'https://example.com/download/main.zip',
      mods_resource_version: '1.0.0',
      mods_resource_size: '25.6MB'
    }]
  }
}, {
  headers: {
    Authorization: '{APPKEY}',
    'Content-Type': 'application/json'
  }
});
```

```python [Python]
import json

response = requests.post('https://mod.3dmgame.com/api/v3/mods/publish',
  headers={
    'Authorization': '{APPKEY}',
    'Content-Type': 'application/json'
  },
  json={
    'mod': {
      'mods_title': '超级武器包',
      'game_id': 123,
      'mods_type_id': 456,
      'mods_version': '1.0.0',
      'mods_author': 'ModAuthor',
      'mods_content': '这是一个包含各种超级武器的Mod，为游戏增加更多战斗选择。',
      'mods_resource': [{
        'mods_resource_name': '主文件',
        'mods_resource_url': 'https://example.com/download/main.zip',
        'mods_resource_version': '1.0.0',
        'mods_resource_size': '25.6MB'
      }]
    }
  }
)
data = response.json()
```

```csharp [C#]
using System.Net.Http;
using System.Text;
using System.Text.Json;

var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");

var data = new {
  mod = new {
    mods_title = "超级武器包",
    game_id = 123,
    mods_type_id = 456,
    mods_version = "1.0.0",
    mods_author = "ModAuthor",
    mods_content = "这是一个包含各种超级武器的Mod，为游戏增加更多战斗选择。",
    mods_resource = new[] {
      new {
        mods_resource_name = "主文件",
        mods_resource_url = "https://example.com/download/main.zip",
        mods_resource_version = "1.0.0",
        mods_resource_size = "25.6MB"
      }
    }
  }
};

var json = JsonSerializer.Serialize(data);
var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync("https://mod.3dmgame.com/api/v3/mods/publish", content);
```

```java [Java]
import java.net.http.*;
import java.net.URI;

String jsonBody = """
{
  "mod": {
    "mods_title": "超级武器包",
    "game_id": 123,
    "mods_type_id": 456,
    "mods_version": "1.0.0",
    "mods_author": "ModAuthor",
    "mods_content": "这是一个包含各种超级武器的Mod，为游戏增加更多战斗选择。",
    "mods_resource": [{
      "mods_resource_name": "主文件",
      "mods_resource_url": "https://example.com/download/main.zip",
      "mods_resource_version": "1.0.0",
      "mods_resource_size": "25.6MB"
    }]
  }
}
""";

HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/mods/publish"))
  .header("Authorization", "{APPKEY}")
  .header("Content-Type", "application/json")
  .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
  .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
library(httr)
library(jsonlite)

body <- list(
  mod = list(
    mods_title = "超级武器包",
    game_id = 123,
    mods_type_id = 456,
    mods_version = "1.0.0",
    mods_author = "ModAuthor",
    mods_content = "这是一个包含各种超级武器的Mod，为游戏增加更多战斗选择。",
    mods_resource = list(
      list(
        mods_resource_name = "主文件",
        mods_resource_url = "https://example.com/download/main.zip",
        mods_resource_version = "1.0.0",
        mods_resource_size = "25.6MB"
      )
    )
  )
)

response <- POST(
  "https://mod.3dmgame.com/api/v3/mods/publish",
  add_headers(Authorization = "{APPKEY}"),
  body = body,
  encode = "json"
)
data <- content(response, "parsed")
```

```go [Go]
package main

import (
  "bytes"
  "encoding/json"
  "net/http"
)

func main() {
  data := map[string]interface{}{
    "mod": map[string]interface{}{
      "mods_title": "超级武器包",
      "game_id": 123,
      "mods_type_id": 456,
      "mods_version": "1.0.0",
      "mods_author": "ModAuthor",
      "mods_content": "这是一个包含各种超级武器的Mod，为游戏增加更多战斗选择。",
      "mods_resource": []map[string]interface{}{
        {
          "mods_resource_name": "主文件",
          "mods_resource_url": "https://example.com/download/main.zip",
          "mods_resource_version": "1.0.0",
          "mods_resource_size": "25.6MB",
        },
      },
    },
  }
  
  jsonData, _ := json.Marshal(data)
  req, _ := http.NewRequest("POST", "https://mod.3dmgame.com/api/v3/mods/publish", bytes.NewBuffer(jsonData))
  req.Header.Set("Authorization", "{APPKEY}")
  req.Header.Set("Content-Type", "application/json")
  
  client := &http.Client{}
  resp, _ := client.Do(req)
  defer resp.Body.Close()
}
```
:::

---

#### 2.4 检查Mod更新

**POST** `/api/v3/mods/checkUpdate`

批量检查Mod的版本信息。

**请求体参数:**

| 参数名  | 类型  | 必填 | 说明       |
| ------- | ----- | ---- | ---------- |
| `modId` | array | 是   | Mod ID数组 |

**响应数据:**

```typescript
{
  modId: number[];
  data: Array<{
    id: number;
    mods_version: string;
  }>;
}
```

**示例:**

::: code-group
```typescript [TypeScript]
const response = await axios.post('/api/v3/mods/checkUpdate', {
  modId: [123, 456, 789]
});
```

```python [Python]
response = requests.post('https://mod.3dmgame.com/api/v3/mods/checkUpdate',
  json={'modId': [123, 456, 789]}
)
data = response.json()
```

```csharp [C#]
var data = new { modId = new[] { 123, 456, 789 } };
var json = JsonSerializer.Serialize(data);
var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync("https://mod.3dmgame.com/api/v3/mods/checkUpdate", content);
```

```java [Java]
String jsonBody = "{\"modId\": [123, 456, 789]}";
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/mods/checkUpdate"))
  .header("Content-Type", "application/json")
  .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- POST(
  "https://mod.3dmgame.com/api/v3/mods/checkUpdate",
  body = list(modId = c(123, 456, 789)),
  encode = "json"
)
data <- content(response, "parsed")
```

```go [Go]
data := map[string]interface{}{"modId": []int{123, 456, 789}}
jsonData, _ := json.Marshal(data)
req, _ := http.NewRequest("POST", "https://mod.3dmgame.com/api/v3/mods/checkUpdate", bytes.NewBuffer(jsonData))
req.Header.Set("Content-Type", "application/json")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()
```
:::

---

### 3. Minecraft相关

#### 3.1 Minecraft Mod列表

**GET** `/api/v3/minecraft`

获取Minecraft Mod列表，支持模组类型、时间范围等多种筛选。

**参数:**

| 参数名      | 类型   | 必填 | 默认值     | 说明                                                                      |
| ----------- | ------ | ---- | ---------- | ------------------------------------------------------------------------- |
| `page`      | number | 否   | 1          | 页码                                                                      |
| `pageSize`  | number | 否   | 20         | 每页数量，最大100                                                         |
| `modules`   | string | 否   | -          | 模组类型筛选                                                              |
| `types`     | object | 否   | -          | 类型筛选对象，格式: `{categoryKey: [value1, value2]}`                     |
| `startTime` | string | 否   | -          | 开始时间 (ISO格式)                                                        |
| `endTime`   | string | 否   | -          | 结束时间 (ISO格式)                                                        |
| `search`    | string | 否   | -          | 搜索关键词(名称、别名、描述、作者)                                        |
| `sortBy`    | string | 否   | updateTime | 排序字段: `updateTime`, `createTime`, `downloadCnt`, `viewCnt`, `likeCnt` |
| `sortOrder` | string | 否   | desc       | 排序方向: `asc`, `desc`                                                   |

**响应数据:**

```typescript
{
  data: Array<{
    id: number;
    name: string;
    aliases: string;
    description: string;
    author: string;
    cover: string;
    modules: string;
    types: object;
    downloadCnt: number;
    viewCnt: number;
    likeCnt: number;
    updateTime: Date;
    createTime: Date;
  }>;
  count: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/minecraft?page=1&modules=fabric&search=优化" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/minecraft', {
  params: {
    page: 1,
    modules: 'fabric',
    search: '优化'
  },
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/minecraft',
  headers={'Authorization': '{APPKEY}'},
  params={'page': 1, 'modules': 'fabric', 'search': '优化'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync(
  "https://mod.3dmgame.com/api/v3/minecraft?page=1&modules=fabric&search=优化"
);
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/minecraft?page=1&modules=fabric&search=优化"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/minecraft",
  add_headers(Authorization = "{APPKEY}"),
  query = list(page = 1, modules = "fabric", search = "优化")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/minecraft?page=1&modules=fabric&search=优化"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

#### 3.2 Minecraft Mod详情

**GET** `/api/v3/minecraft/{id}`

获取指定Minecraft Mod的详细信息。

**参数:**

| 参数名 | 类型   | 必填 | 说明             |
| ------ | ------ | ---- | ---------------- |
| `id`   | number | 是   | Minecraft Mod ID |

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/minecraft/123" \
-H "Authorization: {APPKEY}"
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/minecraft/123',
  headers={'Authorization': '{APPKEY}'}
)
data = response.json()
```

```csharp [C#]
var response = await client.GetAsync("https://mod.3dmgame.com/api/v3/minecraft/123");
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/minecraft/123"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/minecraft/123",
  add_headers(Authorization = "{APPKEY}")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/minecraft/123"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

#### 3.3 发布Minecraft Mod

**POST** `/api/v3/minecraft/publish`

发布或更新Minecraft Mod。

**权限要求:** 需要有效的 API Key

**请求体参数:**

| 参数名        | 类型   | 必填   | 说明                       |
| ------------- | ------ | ------ | -------------------------- |
| `id`          | number | 更新时 | Mod ID (更新时必填)        |
| `name`        | string | 是     | Mod名称                    |
| `aliases`     | string | 否     | 别名                       |
| `description` | string | 是     | 描述                       |
| `author`      | string | 是     | 作者                       |
| `cover`       | string | 否     | 封面图URL                  |
| `modules`     | string | 是     | 模组类型                   |
| `types`       | object | 否     | 类型分类                   |
| `files`       | array  | 是     | 文件列表(至少包含一个文件) |

**文件对象参数:**

| 参数名        | 类型   | 必填 | 说明     |
| ------------- | ------ | ---- | -------- |
| `modVersion`  | string | 是   | Mod版本  |
| `fileName`    | string | 是   | 文件名   |
| `fileLink`    | string | 是   | 下载链接 |
| `fileSize`    | string | 是   | 文件大小 |
| `fileVersion` | string | 是   | 文件版本 |
| `order`       | number | 否   | 排序     |

**示例:**

::: code-group
```typescript [TypeScript]
const response = await axios.post('/api/v3/minecraft/publish', {
  data: {
    name: 'OptiFine',
    description: 'Minecraft 优化模组',
    author: 'sp614x',
    modules: 'forge',
    files: [{
      modVersion: '1.20.1',
      fileName: 'OptiFine_1.20.1_HD_U_I6.jar',
      fileLink: 'https://example.com/download/optifine.jar',
      fileSize: '5.2MB',
      fileVersion: 'HD_U_I6'
    }]
  }
}, {
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.post('https://mod.3dmgame.com/api/v3/minecraft/publish',
  headers={'Authorization': '{APPKEY}'},
  json={
    'data': {
      'name': 'OptiFine',
      'description': 'Minecraft 优化模组',
      'author': 'sp614x',
      'modules': 'forge',
      'files': [{
        'modVersion': '1.20.1',
        'fileName': 'OptiFine_1.20.1_HD_U_I6.jar',
        'fileLink': 'https://example.com/download/optifine.jar',
        'fileSize': '5.2MB',
        'fileVersion': 'HD_U_I6'
      }]
    }
  }
)
data = response.json()
```

```csharp [C#]
var data = new {
  data = new {
    name = "OptiFine",
    description = "Minecraft 优化模组",
    author = "sp614x",
    modules = "forge",
    files = new[] {
      new {
        modVersion = "1.20.1",
        fileName = "OptiFine_1.20.1_HD_U_I6.jar",
        fileLink = "https://example.com/download/optifine.jar",
        fileSize = "5.2MB",
        fileVersion = "HD_U_I6"
      }
    }
  }
};

var json = JsonSerializer.Serialize(data);
var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync("https://mod.3dmgame.com/api/v3/minecraft/publish", content);
```

```java [Java]
String jsonBody = """
{
  "data": {
    "name": "OptiFine",
    "description": "Minecraft 优化模组",
    "author": "sp614x",
    "modules": "forge",
    "files": [{
      "modVersion": "1.20.1",
      "fileName": "OptiFine_1.20.1_HD_U_I6.jar",
      "fileLink": "https://example.com/download/optifine.jar",
      "fileSize": "5.2MB",
      "fileVersion": "HD_U_I6"
    }]
  }
}
""";

HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/minecraft/publish"))
  .header("Authorization", "{APPKEY}")
  .header("Content-Type", "application/json")
  .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
  .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
body <- list(
  data = list(
    name = "OptiFine",
    description = "Minecraft 优化模组",
    author = "sp614x",
    modules = "forge",
    files = list(
      list(
        modVersion = "1.20.1",
        fileName = "OptiFine_1.20.1_HD_U_I6.jar",
        fileLink = "https://example.com/download/optifine.jar",
        fileSize = "5.2MB",
        fileVersion = "HD_U_I6"
      )
    )
  )
)

response <- POST(
  "https://mod.3dmgame.com/api/v3/minecraft/publish",
  add_headers(Authorization = "{APPKEY}"),
  body = body,
  encode = "json"
)
data <- content(response, "parsed")
```

```go [Go]
data := map[string]interface{}{
  "data": map[string]interface{}{
    "name": "OptiFine",
    "description": "Minecraft 优化模组",
    "author": "sp614x",
    "modules": "forge",
    "files": []map[string]interface{}{
      {
        "modVersion": "1.20.1",
        "fileName": "OptiFine_1.20.1_HD_U_I6.jar",
        "fileLink": "https://example.com/download/optifine.jar",
        "fileSize": "5.2MB",
        "fileVersion": "HD_U_I6",
      },
    },
  },
}

jsonData, _ := json.Marshal(data)
req, _ := http.NewRequest("POST", "https://mod.3dmgame.com/api/v3/minecraft/publish", bytes.NewBuffer(jsonData))
req.Header.Set("Authorization", "{APPKEY}")
req.Header.Set("Content-Type", "application/json")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()
```
:::

---

### 4. Wiki相关

#### 4.1 Wiki列表

**GET** `/api/v3/wikis`

获取Wiki列表，支持标签筛选和搜索。

**参数:**

| 参数名      | 类型   | 必填 | 默认值     | 说明                                          |
| ----------- | ------ | ---- | ---------- | --------------------------------------------- |
| `page`      | number | 否   | 1          | 页码                                          |
| `pageSize`  | number | 否   | 20         | 每页数量，最大50                              |
| `tags`      | array  | 否   | -          | 标签筛选，支持数组                            |
| `search`    | string | 否   | -          | 搜索关键词(标题、描述)                        |
| `sortBy`    | string | 否   | updateTime | 排序字段: `updateTime`, `clickCnt`, `likeCnt` |
| `sortOrder` | string | 否   | desc       | 排序方向: `asc`, `desc`                       |

**响应数据:**

```typescript
{
  data: Array<{
    id: number;
    title: string;
    describe: string;
    tags: string[];
    clickCnt: number;
    likeCnt: number;
    updateTime: Date;
    // 用户信息
    user_nickName: string;
    user_avatar: string;
    user_tag: string;
    user_tag_colour: string;
  }>;
  count: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/wikis?page=1&tags=攻略&search=新手" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/wikis', {
  params: {
    page: 1,
    tags: ['攻略'],
    search: '新手'
  },
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/wikis',
  headers={'Authorization': '{APPKEY}'},
  params={'page': 1, 'tags': ['攻略'], 'search': '新手'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync(
  "https://mod.3dmgame.com/api/v3/wikis?page=1&tags=攻略&search=新手"
);
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/wikis?page=1&tags=攻略&search=新手"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/wikis",
  add_headers(Authorization = "{APPKEY}"),
  query = list(page = 1, tags = "攻略", search = "新手")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/wikis?page=1&tags=攻略&search=新手"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

#### 4.2 Wiki详情

**GET** `/api/v3/wikis/{id}`

获取指定Wiki的详细信息，包含完整内容和用户信息。

**参数:**

| 参数名 | 类型   | 必填 | 说明    |
| ------ | ------ | ---- | ------- |
| `id`   | number | 是   | Wiki ID |

**响应数据包含完整的 content 字段**

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/wikis/789" \
-H "Authorization: {APPKEY}"
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/wikis/789',
  headers={'Authorization': '{APPKEY}'}
)
data = response.json()
```

```csharp [C#]
var response = await client.GetAsync("https://mod.3dmgame.com/api/v3/wikis/789");
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/wikis/789"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/wikis/789",
  add_headers(Authorization = "{APPKEY}")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/wikis/789"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

### 5. 阅读内容相关

#### 5.1 阅读列表

**GET** `/api/v3/reads`

获取阅读内容列表，支持类型、标签筛选。

**参数:**

| 参数名      | 类型   | 必填 | 默认值          | 说明                                                                              |
| ----------- | ------ | ---- | --------------- | --------------------------------------------------------------------------------- |
| `page`      | number | 否   | 1               | 页码                                                                              |
| `pageSize`  | number | 否   | 20              | 每页数量，最大50                                                                  |
| `readType`  | string | 否   | -               | 阅读类型筛选                                                                      |
| `tags`      | array  | 否   | -               | 标签筛选，支持数组                                                                |
| `search`    | string | 否   | -               | 搜索关键词(标题、描述、作者)                                                      |
| `sortBy`    | string | 否   | read_updateTime | 排序字段: `read_updateTime`, `read_createTime`, `read_click_cnt`, `read_mark_cnt` |
| `sortOrder` | string | 否   | desc            | 排序方向: `asc`, `desc`                                                           |

**响应数据:**

```typescript
{
  data: Array<{
    id: number;
    read_title: string;
    read_desc: string;
    read_author: string;
    read_type: string;
    read_tag: string[];
    read_click_cnt: number;
    read_mark_cnt: number;
    read_updateTime: Date;
    read_createTime: Date;
    // 用户信息
    user_nickName: string;
    user_avatar: string;
    user_tag: string;
    user_tag_colour: string;
  }>;
  count: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/reads?page=1&readType=评测&sortBy=read_click_cnt" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/reads', {
  params: {
    page: 1,
    readType: '评测',
    sortBy: 'read_click_cnt'
  },
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/reads',
  headers={'Authorization': '{APPKEY}'},
  params={'page': 1, 'readType': '评测', 'sortBy': 'read_click_cnt'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync(
  "https://mod.3dmgame.com/api/v3/reads?page=1&readType=评测&sortBy=read_click_cnt"
);
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/reads?page=1&readType=评测&sortBy=read_click_cnt"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/reads",
  add_headers(Authorization = "{APPKEY}"),
  query = list(page = 1, readType = "评测", sortBy = "read_click_cnt")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/reads?page=1&readType=评测&sortBy=read_click_cnt"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

#### 5.2 阅读详情

**GET** `/api/v3/reads/{id}`

获取指定阅读内容的详细信息，包含完整内容和用户信息。

**参数:**

| 参数名 | 类型   | 必填 | 说明       |
| ------ | ------ | ---- | ---------- |
| `id`   | number | 是   | 阅读内容ID |

**响应数据包含完整的 read_content 字段**

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/reads/101" \
-H "Authorization: {APPKEY}"
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/reads/101',
  headers={'Authorization': '{APPKEY}'}
)
data = response.json()
```

```csharp [C#]
var response = await client.GetAsync("https://mod.3dmgame.com/api/v3/reads/101");
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/reads/101"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/reads/101",
  add_headers(Authorization = "{APPKEY}")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/reads/101"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

### 6. 搜索功能

#### 6.1 全局搜索

**GET** `/api/v3/search`

跨多个内容类型进行搜索。

**参数:**

| 参数名     | 类型   | 必填 | 默认值 | 说明                                                            |
| ---------- | ------ | ---- | ------ | --------------------------------------------------------------- |
| `q`        | string | 是   | -      | 搜索关键词                                                      |
| `type`     | string | 否   | all    | 搜索类型: `all`, `games`, `mods`, `wikis`, `reads`, `minecraft` |
| `page`     | number | 否   | 1      | 页码(仅在指定type时有效)                                        |
| `pageSize` | number | 否   | 20     | 每页数量，最大50(仅在指定type时有效)                            |

**响应数据:**

- 当 `type=all` 时，返回各类型的前5条结果
- 当指定具体 `type` 时，返回该类型的分页结果

```typescript
// type=all
{
  results: {
    games: Array<游戏信息>;
    mods: Array<Mod信息>;
    wikis: Array<Wiki信息>;
    reads: Array<阅读内容>;
    minecraft: Array<Minecraft Mod>;
  };
  query: string;
  type: 'all';
}

// 指定type
{
  data: Array<指定类型数据>;
  count: number;
  page: number;
  pageSize: number;
  totalPages: number;
  type: string;
}
```

**示例:**

::: code-group
```sh [curl - 全局搜索]
curl -X GET "https://mod.3dmgame.com/api/v3/search?q=武器" \
-H "Authorization: {APPKEY}"
```

```sh [curl - 指定类型]
curl -X GET "https://mod.3dmgame.com/api/v3/search?q=武器&type=mods&page=1" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
// 全局搜索
const response1 = await axios.get('/api/v3/search', {
  params: { q: '武器' },
  headers: { Authorization: '{APPKEY}' }
});

// 指定类型搜索
const response2 = await axios.get('/api/v3/search', {
  params: { q: '武器', type: 'mods', page: 1 },
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
# 全局搜索
response1 = requests.get('https://mod.3dmgame.com/api/v3/search',
  headers={'Authorization': '{APPKEY}'},
  params={'q': '武器'}
)

# 指定类型搜索
response2 = requests.get('https://mod.3dmgame.com/api/v3/search',
  headers={'Authorization': '{APPKEY}'},
  params={'q': '武器', 'type': 'mods', 'page': 1}
)
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");

// 全局搜索
var response1 = await client.GetAsync("https://mod.3dmgame.com/api/v3/search?q=武器");

// 指定类型搜索
var response2 = await client.GetAsync("https://mod.3dmgame.com/api/v3/search?q=武器&type=mods&page=1");
```

```java [Java]
HttpClient client = HttpClient.newHttpClient();

// 全局搜索
HttpRequest request1 = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/search?q=武器"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response1 = client.send(request1, HttpResponse.BodyHandlers.ofString());

// 指定类型搜索
HttpRequest request2 = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/search?q=武器&type=mods&page=1"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response2 = client.send(request2, HttpResponse.BodyHandlers.ofString());
```

```r [R]
# 全局搜索
response1 <- GET(
  "https://mod.3dmgame.com/api/v3/search",
  add_headers(Authorization = "{APPKEY}"),
  query = list(q = "武器")
)

# 指定类型搜索
response2 <- GET(
  "https://mod.3dmgame.com/api/v3/search",
  add_headers(Authorization = "{APPKEY}"),
  query = list(q = "武器", type = "mods", page = 1)
)
```

```go [Go]
client := &http.Client{}

// 全局搜索
url1 := "https://mod.3dmgame.com/api/v3/search?q=武器"
req1, _ := http.NewRequest("GET", url1, nil)
req1.Header.Set("Authorization", "{APPKEY}")
resp1, _ := client.Do(req1)
defer resp1.Body.Close()

// 指定类型搜索
url2 := "https://mod.3dmgame.com/api/v3/search?q=武器&type=mods&page=1"
req2, _ := http.NewRequest("GET", url2, nil)
req2.Header.Set("Authorization", "{APPKEY}")
resp2, _ := client.Do(req2)
defer resp2.Body.Close()
```
:::

---

### 7. 热门内容

#### 7.1 获取热门内容

**GET** `/api/v3/hot`

获取各类型的热门内容。

**参数:**

| 参数名   | 类型   | 必填 | 默认值 | 说明                                                               |
| -------- | ------ | ---- | ------ | ------------------------------------------------------------------ |
| `type`   | string | 否   | all    | 内容类型: `all`, `games`, `mods`, `wikis`, `reads`, `minecraft`    |
| `limit`  | number | 否   | 10     | 返回数量，最大50                                                   |
| `period` | string | 否   | week   | 时间范围: `day`(今天), `week`(本周), `month`(本月), 不传则全部时间 |

**响应数据:**

```typescript
{
  // type=all时返回所有类型
  games?: Array<{
    id: number;
    game_name: string;
    modCount: number;
    totalDownloads: number;
    totalViews: number;
  }>;
  mods?: Array<Mod信息>;
  wikis?: Array<Wiki信息>;
  reads?: Array<阅读内容>;
  minecraft?: Array<Minecraft Mod>;
  
  period: string;
  limit: number;
  type: string;
  generatedAt: string;
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/hot?type=mods&limit=20&period=week" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/hot', {
  params: {
    type: 'mods',
    limit: 20,
    period: 'week'
  },
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/hot',
  headers={'Authorization': '{APPKEY}'},
  params={'type': 'mods', 'limit': 20, 'period': 'week'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync(
  "https://mod.3dmgame.com/api/v3/hot?type=mods&limit=20&period=week"
);
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/hot?type=mods&limit=20&period=week"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/hot",
  add_headers(Authorization = "{APPKEY}"),
  query = list(type = "mods", limit = 20, period = "week")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/hot?type=mods&limit=20&period=week"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

### 8. 统计信息

#### 8.1 获取统计数据

**GET** `/api/v3/stats`

获取平台整体统计信息，无需参数。

**响应数据:**

```typescript
{
  summary: {
    totalGames: number;
    totalMods: number;
    totalWikis: number;
    totalReads: number;
    totalMinecraftMods: number;
    totalContent: number;
  };
  games: {
    total: number;
  };
  mods: {
    total: number;
    totalDownloads: number;
    totalViews: number;
    totalFavorites: number;
    recentCount: number;  // 最近30天新增
  };
  wikis: {
    total: number;
    totalViews: number;
    totalLikes: number;
  };
  reads: {
    total: number;
    totalViews: number;
    totalFavorites: number;
  };
  minecraft: {
    total: number;
    totalDownloads: number;
    totalViews: number;
    totalLikes: number;
  };
  lastUpdated: string;
}
```

**示例:**

::: code-group
```sh [curl]
curl -X GET "https://mod.3dmgame.com/api/v3/stats" \
-H "Authorization: {APPKEY}"
```

```typescript [TypeScript]
const response = await axios.get('/api/v3/stats', {
  headers: { Authorization: '{APPKEY}' }
});
```

```python [Python]
response = requests.get('https://mod.3dmgame.com/api/v3/stats',
  headers={'Authorization': '{APPKEY}'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
client.DefaultRequestHeaders.Add("Authorization", "{APPKEY}");
var response = await client.GetAsync("https://mod.3dmgame.com/api/v3/stats");
var data = await response.Content.ReadAsStringAsync();
```

```java [Java]
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/stats"))
  .header("Authorization", "{APPKEY}")
  .GET()
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- GET(
  "https://mod.3dmgame.com/api/v3/stats",
  add_headers(Authorization = "{APPKEY}")
)
data <- content(response, "parsed")
```

```go [Go]
url := "https://mod.3dmgame.com/api/v3/stats"
req, _ := http.NewRequest("GET", url, nil)
req.Header.Set("Authorization", "{APPKEY}")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

### 9. 用户认证

#### 9.1 用户登录

**POST** `/api/v3/user/login`

使用3DM账号登录验证。

**请求体参数:**

| 参数名     | 类型   | 必填 | 说明   |
| ---------- | ------ | ---- | ------ |
| `username` | string | 是   | 用户名 |
| `password` | string | 是   | 密码   |

**响应数据:**

```typescript
{
  user: {
    user_nickName: string;
    user_avatar: string;
    user_tag: string;
    user_tag_colour: string;
    user_fan: number;
    user_Intr: string;
  }
}
```

**示例:**

::: code-group
```typescript [TypeScript]
const response = await axios.post('/api/v3/user/login', {
  username: 'myusername',
  password: 'mypassword'
});
```

```python [Python]
response = requests.post('https://mod.3dmgame.com/api/v3/user/login',
  json={'username': 'myusername', 'password': 'mypassword'}
)
data = response.json()
```

```csharp [C#]
var client = new HttpClient();
var data = new { username = "myusername", password = "mypassword" };
var json = JsonSerializer.Serialize(data);
var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync("https://mod.3dmgame.com/api/v3/user/login", content);
var result = await response.Content.ReadAsStringAsync();
```

```java [Java]
String jsonBody = "{\"username\": \"myusername\", \"password\": \"mypassword\"}";
HttpRequest request = HttpRequest.newBuilder()
  .uri(URI.create("https://mod.3dmgame.com/api/v3/user/login"))
  .header("Content-Type", "application/json")
  .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
  .build();
HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

```r [R]
response <- POST(
  "https://mod.3dmgame.com/api/v3/user/login",
  body = list(username = "myusername", password = "mypassword"),
  encode = "json"
)
data <- content(response, "parsed")
```

```go [Go]
data := map[string]string{"username": "myusername", "password": "mypassword"}
jsonData, _ := json.Marshal(data)
req, _ := http.NewRequest("POST", "https://mod.3dmgame.com/api/v3/user/login", bytes.NewBuffer(jsonData))
req.Header.Set("Content-Type", "application/json")

client := &http.Client{}
resp, _ := client.Do(req)
defer resp.Body.Close()

body, _ := io.ReadAll(resp.Body)
```
:::

---

## 错误代码说明

| HTTP状态码 | 说明                |
| ---------- | ------------------- |
| 200        | 请求成功            |
| 400        | 请求参数错误        |
| 401        | 未授权或API Key无效 |
| 403        | 权限不足            |
| 404        | 资源不存在          |
| 500        | 服务器内部错误      |

---

## 最佳实践

### 1. 缓存策略

- API 响应已经包含缓存机制，建议客户端也实现适当的缓存
- 搜索和热门内容缓存时间较短(1小时)，需要更频繁的刷新
- 详情页面缓存1天，列表页根据活跃度缓存

### 2. 分页建议

- 建议 `pageSize` 不超过 50(游戏)或 100(Mods)
- 大量数据请使用分页而不是一次性获取全部

### 3. 搜索优化

- 使用 `/api/v3/search` 进行全局搜索时，先用 `type=all` 预览各类型结果
- 然后根据用户选择使用具体 type 获取详细结果

### 4. 发布内容注意事项

- 发布前确保已获取有效的 API Key
- 新发布的内容默认需要审核
- 更新操作只能修改自己发布的内容
- 资源文件必须提供有效的下载链接

### 5. API Key 管理

- 妥善保管 API Key，不要在客户端代码中硬编码
- 建议使用环境变量或配置文件管理
- 定期更换 API Key 以确保安全

---

## 更新日志

### v3.1.0 (2025-10-09)

- ✅ 完整的游戏、Mod、Wiki、阅读内容 API
- ✅ Minecraft 专区 API
- ✅ 全局搜索功能
- ✅ 热门内容聚合
- ✅ 平台统计信息
- ✅ 内容发布和更新接口
- ✅ 用户认证接口
- ✅ 智能缓存机制
- ✅ 批量查询支持

---

## 联系方式

如有问题或建议，请联系:
- 网站: https://mod.3dmgame.com
- 邮箱: mod@3dmgame.com



---

**文档版本**: v3.1.0 
**最后更新**: 2025-10-09  
**API 基础路径**: `/api/v3`
