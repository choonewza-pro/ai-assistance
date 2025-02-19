FROM jupyter/base-notebook

# กำหนด username และ password
ENV JUPYTER_PASSWORD=Hrd12345

# ติดตั้ง jupyterlab และ notebook
RUN pip install --no-cache-dir jupyterlab notebook

# คัดลอกไฟล์ config เข้าไปใน container
COPY jupyter_notebook_config.py ~/.jupyter/

# เปิด port 8888
EXPOSE 8888

# รัน Jupyter Notebook
CMD ["start-notebook.sh", "--NotebookApp.token=''"]