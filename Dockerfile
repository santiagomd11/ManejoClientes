FROM python:3.9

EXPOSE 5001

WORKDIR /manejoClientes

COPY . /manejoClientes/

RUN pip install pipenv && pipenv install

ENV PYTHONPATH /manejoClientes

ENTRYPOINT ["pipenv", "run", "python", "./src/main.py"]