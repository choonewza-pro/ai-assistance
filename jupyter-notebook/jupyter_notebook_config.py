from jupyter_server.auth import passwd
from traitlets.config import get_config

# ตั้งค่าการใช้งาน Jupyter Notebook ด้วยรหัสผ่าน
c = get_config()
c.NotebookApp.password = passwd("Hrd12345")  # กำหนดรหัสผ่าน
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.allow_root = True
c.NotebookApp.token = ''  # ปิดการใช้ Token Authentication