# Cloudflare IP更新脚本

这个Python脚本用于从指定网站的API接口获取优选IP地址，并更新到Cloudflare DNS解析中。以下是一些简单的说明：

## 功能
- 从指定网站的API接口获取优选IP地址
- 筛选延时最低的指定线路和IP个数
- 更新选定的IP地址到Cloudflare DNS解析中

## 系统要求
- Python 3.x
- 适用于 Windows、Mac、Linux 等操作系统

## 依赖
- requests 库：用于发送HTTP请求和处理API响应

## 使用说明
1. 安装Python 3.x：请确保已安装Python 3.x，可以从官方网站 [Python官网](https://www.python.org/downloads/) 下载安装程序。
2. 安装 requests 库：在命令行中运行以下命令安装 requests 库：
pip install requests

3. 获取API Token、Zone ID和域名：在脚本中填入您的Cloudflare API Token、Zone ID和域名。
4. 选择运营商线路：在脚本中修改 `line` 变量来选择电信（CT）、移动（CM）或联通（CU）线路。
5. 运行脚本：在命令行中运行脚本，即可获取优选IP地址并更新到Cloudflare DNS解析中。

## 注意事项
- 脚本使用了 [https://345673.xyz/get_data](https://345673.xyz/get_data) 提供的API接口，使用免费的key。如需稳定使用，请到该网站购买key。
- 请谨慎操作，确保填写正确的API Token、Zone ID和域名，以免造成不必要的问题。

如有任何问题或疑问，请随时联系我。
