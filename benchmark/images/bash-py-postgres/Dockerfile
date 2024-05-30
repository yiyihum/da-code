FROM python:3.9

WORKDIR /workspace

# 将 init.sh 复制到工作目录
COPY init.sh .

# 执行 init.sh
RUN chmod +x init.sh && ./init.sh

# 设置容器启动时执行的命令
CMD ["/bin/bash"]

