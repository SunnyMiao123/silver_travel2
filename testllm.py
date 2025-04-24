import os
from openai import OpenAI

client = OpenAI(
    # 从环境变量中读取您的方舟API Key
    api_key="f6d78d84-e1c1-47ae-b325-a7c01d1dd9d9", 
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    )
completion = client.chat.completions.create(
    # 将推理接入点 <Model>替换为 Model ID
    model="doubao-1-5-pro-32k-250115",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)
print(completion.choices[0].message)