import socket
import requests
import time

def test_port(port):
    """测试端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            s.close()
            return True
    except OSError:
        return False

def test_http_connection(port):
    """测试HTTP连接"""
    try:
        response = requests.get(f"http://localhost:{port}/test", timeout=5)
        return response.status_code == 200, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    ports_to_test = [7777, 8080, 8081, 8082]
    
    print("端口可用性测试:")
    print("=" * 50)
    
    for port in ports_to_test:
        print(f"\n测试端口 {port}:")
        
        # 测试端口是否被占用
        if test_port(port):
            print(f"  ✓ 端口 {port} 可用")
        else:
            print(f"  ✗ 端口 {port} 已被占用")
            continue
        
        # 测试HTTP连接
        success, result = test_http_connection(port)
        if success:
            print(f"  ✓ HTTP连接成功")
            print(f"    响应: {result}")
        else:
            print(f"  ✗ HTTP连接失败: {result}")
    
    print("\n" + "=" * 50)
    print("测试完成")

if __name__ == "__main__":
    main() 