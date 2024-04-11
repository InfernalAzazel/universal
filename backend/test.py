import httpx

proxies = {
    "http://": "http://127.0.0.1:7890",
    "https://": "http://127.0.0.1:7890",
}


url = 'https://raw.githubusercontent.com/hairyf/naive-ui-pro-components/main/docs/docs/intro.md'

# 发送同步GET请求
try:
    response = httpx.get(url, timeout=30000, proxies=proxies)
    response.raise_for_status()  # 如果请求返回了4xx或5xx响应码，将抛出异常

    # 打印响应内容
    print(response.text)

except httpx.HTTPStatusError as e:
    print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
except httpx.RequestError as e:
    print(f"An error occurred while requesting {e.request.url!r}.")