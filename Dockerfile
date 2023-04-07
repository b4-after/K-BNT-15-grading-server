FROM public.ecr.aws/lambda/python:3.9

COPY app/ ${LAMBDA_TASK_ROOT}

RUN yum -y install gcc libmariadb-dev default-libmysqlclient-dev python-devel mysql-devel
RUN /var/lang/bin/python3.9 -m pip install --upgrade pip
RUN pip install -U poetry
RUN poetry export --only main --without-hashes --format=requirements.txt > requirements.txt
RUN pip install -r requirements.txt -t .

ENV PYTHONPATH="$PYTHONPATH:${LAMBDA_TASK_ROOT}"
WORKDIR ${LAMBDA_TASK_ROOT}/src
CMD ["main.lambda_handler"]
