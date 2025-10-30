ARG PYTHON_IMAGE_VERSION=3.12.2-alpine3.18

FROM python:$PYTHON_IMAGE_VERSION AS build
WORKDIR /wheels

RUN apk add --no-cache git gcc musl-dev libffi-dev
COPY requirements.txt .
RUN pip wheel -r requirements.txt

FROM python:$PYTHON_IMAGE_VERSION AS runtime
COPY --from=build /wheels /wheels

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PROJECT_DIR=/backend
ENV PYTHONPATH=$PROJECT_DIR/app
WORKDIR $PROJECT_DIR

RUN pip install --no-cache-dir /wheels/*.whl
RUN rm -rf /wheels

COPY . .

ENTRYPOINT ["python", "-m", "app"]