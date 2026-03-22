import os
from volcenginesdkarkruntime import Ark

client = Ark(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=os.getenv('ARK_API_KEY'),
)

response = client.responses.create(
    model="doubao-seed-2-0-lite-260215",
    input="hello", # Replace with your prompt
    # thinking={"type": "disabled"}, #  Manually disable deep thinking
)
print(response)