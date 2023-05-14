FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
COPY . /splitapp
WORKDIR /splitapp
RUN pip install -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5005"]
EXPOSE 5005