import http.server
import socketserver
import os
import socket

PORT = 8765
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_local_ip():
    """หา IP ในเครือข่ายของเครื่องนี้"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # ไม่ได้ส่งข้อมูลจริง แค่หา route
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

Handler = http.server.SimpleHTTPRequestHandler

# bind 0.0.0.0 = ฟังทุก network interface
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    ip = get_local_ip()
    print(f"✅ Local:   http://127.0.0.1:{PORT}/")
    print(f"🌐 Network: http://{ip}:{PORT}/")
    print("กด Ctrl+C เพื่อหยุด")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 หยุด server แล้ว")