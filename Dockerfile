FROM python:3.13-slim

RUN addgroup --gid 9999 code && \
    adduser --uid 9999 --ingroup code --gecos '' --disabled-password code

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir portal
COPY portal portal/.

USER code
EXPOSE 8000

CMD ["uvicorn", "portal:app", "--host", "0.0.0.0", "--port", "8000"]
