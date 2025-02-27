# ใช้ base image ของ jupyter/base-notebook
FROM jupyter/base-notebook

# ตั้งค่า environment variables
ENV JUPYTER_TOKEN=123456

# ติดตั้งแพ็คเกจเพิ่มเติมที่คุณต้องการ
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    scikit-learn 

# ตั้งค่าให้ Jupyter Notebook รันด้วยการตั้งค่าที่กำหนด
CMD ["start-notebook.sh", "--NotebookApp.allow_origin='*'", "--NotebookApp.ip='0.0.0.0'", "--NotebookApp.port=8888", "--NotebookApp.allow_remote_access=True"]