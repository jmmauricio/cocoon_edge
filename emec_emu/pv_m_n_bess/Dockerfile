FROM alvmunesp/conda-mkl:latest

WORKDIR /app

COPY . .

EXPOSE 8000:8000

RUN /root/anaconda3/bin/python3 pv_mn_builder.py

CMD ["/root/anaconda3/bin/python3", "emulator.py"]