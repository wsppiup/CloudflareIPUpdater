import requests

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

# 判断是否筛选成功
if selected_ips:
    # 打印筛选后的IP地址
    print("筛选后的IP地址：")
    for ip_info in selected_ips:
        print(f"IP地址: {ip_info['ip']}，延迟: {ip_info['delay']}ms，线路: {ip_info['line']}，节点: {ip_info['node']}，下载速度: {ip_info['downloadspeed']}，时间: {ip_info['time']}")

    # 删除之前的记录
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", headers=headers)
    records = response.json()["result"]
    for record in records:
        if record["name"] == domain:
            requests.delete(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record['id']}", headers=headers)
            print(f"删除旧记录成功：{record['id']}")

    # 更新新IP到Cloudflare DNS解析中
    for ip_info in selected_ips:
        ip = ip_info["ip"]
        payload = {
            "type": "A",
            "name": domain,
            "content": ip,
            "ttl": 60,
            "proxied": False
        }
        response = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records", headers=headers, json=payload)
        print(f"IP {ip} 更新成功")

    print("IP更新完成")
else:
    print("未找到符合条件的IP地址，请稍后重试")