FROM registry.access.redhat.com/ubi9/python-312

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER 1001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
