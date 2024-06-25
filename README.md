
# RESTAPI Blog

REST API for a personal blog that allows adding different images and tags for each post. Using FastAPI and PostgreSQL

 <img src="https://drive.google.com/uc?id=1nTRpwv9CuMM0Sp1gmw2HO9dID-p28Krq" style="width:50%; height:auto; margin:auto; display:block; />

## Tech


<div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

</div>

## API Reference

#### Get Random Tag

```http
  GET /tags/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. Random Tag |

#### Get ALL Tags

```http
  GET /tags/all
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. All Tags |

#### Post Tag

```http
  POST /tags/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. New Tag |

##### Request Body Example

{
  "id_tag": 0,
  "title": "string",
  "status": "string"
}

#### Get Tag By iD

```http
  Get /tags/{id_tag}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_tag` | `Integer` | UID Tag |

#### Delete Tag By iD

```http
    Delete /tags/{id_tag}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_tag` | `Integer` | UID Tag |

#### Put Tag By iD

```http
    PUT /tags/{id_tag}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_tag` | `Integer` | UID Tag |

#### Request Body Example
{
  "id_tag": 0,
  "title": "string",
  "status": "string"
}

#### Get Random Image

```http
  GET /images/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. Random Image |

#### Get ALL Tags

```http
  GET /images/all
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. All Stored Images |

#### Post Image

```http
  POST /images/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. New Tag |

##### Request Body Example

{
  "id_image": 0,
  "url": "string",
  "caption": "string"
}

#### Get Image By iD

```http
  Get /images/{id_images}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_image` | `Integer` | UID Image |

#### Delete Image By iD

```http
    Delete /images/{id_image}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_image` | `Integer` | UID Image |

#### Put Image By iD

```http
    PUT /images/{id_image}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_image` | `Integer` | UID Image |

#### Request Body Example
{
  "id_image": 0,
  "url": "string",
  "caption": "string"
}

#### Get Random Post

```http
  GET /posts/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. Random Posts |

#### Get ALL Posts

```http
  GET /posts/all
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. All Stored Posts |

#### Post POst

```http
  POST /posts/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. New Tag |

##### Request Body Example

{
  "id_post": 0,
  "title": "string",
  "body": "string",
  "status": "ACT",
  "has_image": false,
  "publishing_date": "2024-06-25T12:09:19.264Z"
}

#### Get post By iD

```http
  Get /posts/{id_post}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_post` | `Integer` | UID Post |

#### Delete Post By iD

```http
    Delete /posts/{id_post}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_post` | `Integer` | UID Post |

#### Put Post By iD

```http
    PUT /posts/{id_post}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id_post` | `Integer` | UID Post |

#### Request Body Example

{
  "id_post": 0,
  "title": "string",
  "body": "string",
  "status": "ACT",
  "has_image": false,
  "publishing_date": "2024-06-25T12:11:18.622Z"
}

#### Get Heatlh

```http
  GET /health/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. String |

```http
  GET /
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `none` | `none` | **Returns**. "HELLO WORLD" |