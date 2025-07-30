import requests
import time

def test_server(port):
    """测试服务器连接"""
    urls = [
        f"http://localhost:{port}/test",
        f"http://127.0.0.1:{port}/test",
        f"http://10.21.83.207:{port}/test"
    ]
    
    for url in urls:
        try:
            print(f"测试连接: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ 成功连接到 {url}")
                print(f"响应: {response.json()}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"❌ 无法连接到 {url}: {e}")
    
    return False

if __name__ == "__main__":
    port = 123
    print(f"测试端口 {port} 的服务器连接...")
    
    if test_server(port):
        print("服务器运行正常！")
    else:
        print("无法连接到服务器，请检查:")
        print("1. 程序是否正在运行")
        print("2. 端口是否正确")
        print("3. 防火墙设置")
        print("4. 网络连接") 