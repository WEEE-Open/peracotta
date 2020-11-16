FROM ubuntu:latest
COPY . /root/peracotta
WORKDIR /root/peracotta
RUN rm -rf tmp copy_this_to_tarallo.json
RUN apt update
RUN apt full-upgrade -y
RUN apt install -y python3-pip
RUN ./install_dependencies_all.sh
RUN pip3 install -r requirements.txt
ENTRYPOINT ["/root/peracotta/main.sh"]
# build with:
# docker build -t peracotta .
# run with:
# ./main_docker.sh