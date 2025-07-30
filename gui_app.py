import os
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import webbrowser
import re
from data_manager import GameDataManager
from web_app import app, set_global_db_manager

class GameDataGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("典狱长数据查询系统")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        self.server_root_dir = ""
        self.port = 8080
        self.db_manager = None
        self.server_thread = None
        self.server_running = False
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="典狱长数据查询系统", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 服务端根目录选择
        ttk.Label(main_frame, text="服务端根目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dir_var = tk.StringVar()
        dir_entry = ttk.Entry(main_frame, textvariable=self.dir_var, width=50)
        dir_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(main_frame, text="浏览", command=self.browse_directory).grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # 服务端名称显示
        ttk.Label(main_frame, text="服务端名称:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.server_name_var = tk.StringVar(value="服务端名称: 请先选择目录")
        server_name_label = ttk.Label(main_frame, textvariable=self.server_name_var, foreground="blue")
        server_name_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 端口设置
        ttk.Label(main_frame, text="端口号:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.port_var = tk.StringVar(value="8080")
        port_entry = ttk.Entry(main_frame, textvariable=self.port_var, width=10)
        port_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.init_button = ttk.Button(button_frame, text="初始化数据", command=self.initialize_data)
        self.init_button.pack(side=tk.LEFT, padx=5)
        
        self.start_button = ttk.Button(button_frame, text="启动服务器", command=self.start_server, state=tk.DISABLED)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止服务器", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.open_browser_button = ttk.Button(button_frame, text="打开浏览器", command=self.open_browser, state=tk.DISABLED)
        self.open_browser_button.pack(side=tk.LEFT, padx=5)
        
        # 典狱长封挂插件广告
        ad_frame = ttk.Frame(main_frame)
        ad_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ad_label = tk.Label(ad_frame, text="典狱长封挂插件", 
                           fg="blue", cursor="hand2", 
                           font=("Arial", 12, "underline"))
        ad_label.pack()
        ad_label.bind("<Button-1>", self.open_dyz_website)
        ad_label.bind("<Enter>", lambda e: ad_label.config(fg="red"))
        ad_label.bind("<Leave>", lambda e: ad_label.config(fg="blue"))
        
        # 状态显示
        ttk.Label(main_frame, text="状态:").grid(row=6, column=0, sticky=tk.W, pady=(20, 5))
        
        # 日志显示区域
        self.log_text = scrolledtext.ScrolledText(main_frame, height=20, width=80)
        self.log_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 配置网格权重
        main_frame.rowconfigure(7, weight=1)
    
    def browse_directory(self):
        directory = filedialog.askdirectory(title="选择服务端根目录")
        if directory:
            self.dir_var.set(directory)
            self.log_message(f"选择目录: {directory}")
            
            # 立即读取服务端名称
            try:
                config_file = os.path.join(directory, "Config.ini")
                if os.path.exists(config_file):
                    server_name = self.read_server_name(config_file)
                    self.server_name_var.set(f"服务端名称: {server_name}")
                    self.log_message(f"读取到服务端名称: {server_name}")
                else:
                    self.server_name_var.set("服务端名称: 未找到Config.ini文件")
                    self.log_message("未找到Config.ini文件")
            except Exception as e:
                self.server_name_var.set("服务端名称: 读取失败")
                self.log_message(f"读取服务端名称失败: {str(e)}")
    
    def read_server_name(self, config_file):
        """读取Config.ini中的服务端名称"""
        try:
            with open(config_file, 'r', encoding='gbk') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                return "DefaultServer"
        
        # 查找GameName
        match = re.search(r'GameName=([^\r\n]+)', content)
        if match:
            server_name = match.group(1).strip()
            return server_name
        else:
            return "DefaultServer"
    
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def initialize_data(self):
        if not self.dir_var.get():
            messagebox.showerror("错误", "请先选择服务端根目录")
            return
        
        self.server_root_dir = self.dir_var.get()
        
        try:
            self.port = int(self.port_var.get())
            if self.port < 1 or self.port > 65535:
                raise ValueError("端口号必须在1-65535之间")
        except ValueError as e:
            messagebox.showerror("错误", f"端口号无效: {e}")
            return
        
        self.init_button.config(state=tk.DISABLED)
        self.log_message("开始初始化数据...")
        
        # 在新线程中执行初始化
        def init_thread():
            try:
                self.db_manager = GameDataManager(self.server_root_dir, self.port)
                
                # 强制关闭端口上的进程
                self.log_message(f"正在检查端口 {self.port} 的占用情况...")
                if self.db_manager.kill_port_process(self.port):
                    self.log_message(f"已强制关闭占用端口 {self.port} 的进程")
                    time.sleep(1)  # 等待进程完全关闭
                
                # 检查端口
                try:
                    import socket
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('localhost', self.port))
                        s.close()
                        self.log_message(f"端口 {self.port} 可用")
                except OSError:
                    self.log_message(f"端口 {self.port} 仍被占用")
                    return
                
                # 初始化数据
                success, message = self.db_manager.initialize_data()
                if success:
                    self.log_message("数据初始化成功")
                    self.log_message(message)
                    self.start_button.config(state=tk.NORMAL)
                else:
                    self.log_message(f"数据初始化失败: {message}")
                    messagebox.showerror("错误", message)
                
            except Exception as e:
                self.log_message(f"初始化失败: {str(e)}")
                messagebox.showerror("错误", f"初始化失败: {str(e)}")
            finally:
                self.init_button.config(state=tk.NORMAL)
        
        threading.Thread(target=init_thread, daemon=True).start()
    
    def start_server(self):
        if not self.db_manager:
            messagebox.showerror("错误", "请先初始化数据")
            return
        
        if self.server_running:
            messagebox.showinfo("提示", "服务器已在运行")
            return
        
        # 重新读取端口号
        try:
            new_port = int(self.port_var.get())
            if new_port < 1 or new_port > 65535:
                raise ValueError("端口号必须在1-65535之间")
            self.port = new_port
        except ValueError as e:
            messagebox.showerror("错误", f"端口号无效: {e}")
            return
        
        # 强制关闭端口上的进程
        self.log_message(f"正在检查端口 {self.port} 的占用情况...")
        if self.db_manager.kill_port_process(self.port):
            self.log_message(f"已强制关闭占用端口 {self.port} 的进程")
            time.sleep(1)  # 等待进程完全关闭
        
        # 检查端口是否被占用
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', self.port))
                s.close()
                self.log_message(f"端口 {self.port} 可用")
        except OSError:
            messagebox.showerror("错误", f"端口 {self.port} 仍被占用，无法启动服务器")
            return
        
        self.server_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.open_browser_button.config(state=tk.NORMAL)
        
        # 设置全局数据库管理器
        set_global_db_manager(self.db_manager)
        
        local_ip = self.db_manager.get_local_ip()
        self.log_message(f"启动Web服务器在端口 {self.port}")
        self.log_message(f"请在浏览器中访问: http://{local_ip}:{self.port}")
        
        # 在新线程中启动Flask服务器
        def server_thread():
            try:
                self.log_message(f"正在启动Flask服务器，端口: {self.port}")
                app.run(host='0.0.0.0', port=self.port, debug=False, threaded=True)
            except Exception as e:
                self.log_message(f"服务器启动失败: {str(e)}")
                self.log_message(f"错误类型: {type(e).__name__}")
                self.server_running = False
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
                self.open_browser_button.config(state=tk.DISABLED)
        
        self.server_thread = threading.Thread(target=server_thread, daemon=True)
        self.server_thread.start()
    
    def stop_server(self):
        if not self.server_running:
            return
        
        self.server_running = False
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.open_browser_button.config(state=tk.DISABLED)
        
        self.log_message("正在停止服务器...")
        # Flask服务器会在主线程结束时自动停止
    
    def open_browser(self):
        if not self.server_running:
            messagebox.showerror("错误", "服务器未运行")
            return
        
        try:
            local_ip = self.db_manager.get_local_ip()
            webbrowser.open(f"http://{local_ip}:{self.port}")
            self.log_message("已打开浏览器")
        except Exception as e:
            self.log_message(f"打开浏览器失败: {str(e)}")
    
    def open_dyz_website(self, event=None):
        """打开典狱长封挂插件网站"""
        try:
            webbrowser.open("https://dyzplugin.win/")
            self.log_message("已打开典狱长封挂插件网站")
        except Exception as e:
            self.log_message(f"打开网站失败: {str(e)}")
    
    def on_closing(self):
        """程序关闭时的清理工作"""
        try:
            if self.server_running:
                self.log_message("正在关闭服务器...")
                self.server_running = False
            
            # 强制关闭端口上的进程
            if self.db_manager:
                self.log_message(f"正在清理端口 {self.port} 的进程...")
                self.db_manager.kill_port_process(self.port)
            
            self.log_message("程序正在退出...")
            time.sleep(0.5)  # 给一点时间让日志显示
            
        except Exception as e:
            print(f"清理时出错: {e}")
        finally:
            self.root.destroy()
    
    def run(self):
        self.root.mainloop() 