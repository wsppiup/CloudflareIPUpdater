import requests
import threading

# Cloudflare API参数
api_token = ""  # Cloudflare API Token
zone_id = ""  # Cloudflare Zone ID
domain = ""  # 您的二级域名

# 定义需要筛选的线路和筛选IP的个数
line = "CU"  # 可以根据需要修改的线路电信CT移动CM联通CU
num_ips_to_select = 2  # 修改此处以更改筛选IP的个数

# 请求优选IP接口
url = "https://api.345673.xyz/get_data"
payload = {
    "key": "o1zrmHAF"
}
response = requests.post(url, json=payload)
data = response.json()

# 筛选延时最低的指定个数线路IP
selected_ips = sorted([ip_info for ip_info in data["info"][line] if ip_info["line"] == line], key=lambda x: float(x["delay"].replace("ms", "")))[:num_ips_to_select]

# 获取原有的DNS记录
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}
response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", headers=headers)
records = response.json()["result"]

# 删除原有的DNS记录
for record in records:
    if record["name"] == domain:
        requests.delete(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}", headers=headers)
        print(f"删除旧记录成功：{record['id']}")

# 更新DNS解析的函数
def update_dns(ip):
    payload = {
        "type": "A",
        "name": domain,
        "content": ip,
        "ttl": 60,
        "proxied": False
    }
    response = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", headers=headers, json=payload)
    print(f"IP {ip} 更新成功")

# 并行更新IP到Cloudflare DNS解析中
threads = []
for ip_info in selected_ips:
    ip = ip_info["ip"]
    thread = threading.Thread(target=update_dns, args=(ip,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("IP更新完成")