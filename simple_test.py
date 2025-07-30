import socket
import time

def test_port(host, port):
    """测试端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_http(host, port):
    """测试HTTP连接"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        
        # 发送HTTP GET请求
        request = f"GET /test HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())
        
        # 接收响应
        response = sock.recv(1024).decode()
        sock.close()
        
        return "200 OK" in response or "HTTP/1.1 200" in response
    except Exception as e:
        print(f"HTTP测试失败: {e}")
        return False

if __name__ == "__main__":
    port = 123
    hosts = ["localhost", "127.0.0.1", "10.21.83.207"]
    
    print(f"测试端口 {port} 的连接...")
    
    for host in hosts:
        print(f"\n测试 {host}:{port}")
        
        # 测试端口是否开放
        if test_port(host, port):
            print(f"✅ 端口 {port} 在 {host} 上开放")
            
            # 测试HTTP连接
            if test_http(host, port):
                print(f"✅ HTTP服务在 {host}:{port} 正常运行")
            else:
                print(f"❌ HTTP服务在 {host}:{port} 无响应")
        else:
            print(f"❌ 端口 {port} 在 {host} 上关闭")
    
    print("\n如果所有测试都失败，请检查:")
    print("1. 程序是否正在运行")
    print("2. 防火墙是否阻止了连接")
    print("3. 尝试使用不同的端口")
    print("4. 检查网络配置") 