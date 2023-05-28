FROM public.ecr.aws/lambda/python:3.9 as builder

WORKDIR ${LAMBDA_TASK_ROOT}

COPY app/pyproject.toml app/poetry.lock ${LAMBDA_TASK_ROOT}/

RUN yum -y install gcc libmariadb-dev default-libmysqlclient-dev python-devel mysql-devel default-jdk
RUN /var/lang/bin/python3.9 -m pip install --upgrade pip && pip install -U poetry && poetry export --only main --without-hashes --format=requirements.txt > requirements.txt && pip install -r requirements.txt -t .

COPY app/src ${LAMBDA_TASK_ROOT}/src

FROM public.ecr.aws/lambda/python:3.9

RUN yum -y install gcc libmariadb-dev default-libmysqlclient-dev python-devel mysql-devel default-jdk
COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}/src
ENV PYTHONPATH="$PYTHONPATH:${LAMBDA_TASK_ROOT}"

CMD ["main.lambda_handler"]
