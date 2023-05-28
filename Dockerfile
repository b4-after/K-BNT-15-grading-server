FROM public.ecr.aws/lambda/python:3.9 as builder

WORKDIR ${LAMBDA_TASK_ROOT}

COPY app/pyproject.toml app/poetry.lock ${LAMBDA_TASK_ROOT}/

RUN yum -y install gcc libmariadb-dev default-libmysqlclient-dev python-devel mysql-devel
RUN /var/lang/bin/python3.9 -m pip install --upgrade pip && pip install -U poetry && poetry export --only main --without-hashes --format=requirements.txt > requirements.txt && pip install -r requirements.txt -t .

COPY app/src ${LAMBDA_TASK_ROOT}/src

FROM public.ecr.aws/lambda/python:3.9

RUN yum -y install epel-release
RUN yum -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
RUN yum -y install gcc libmariadb-dev default-libmysqlclient-dev python-devel mysql-devel default-jdk ffmpeg ffmpeg-devel
COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

RUN export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))

WORKDIR ${LAMBDA_TASK_ROOT}/src
ENV PYTHONPATH="$PYTHONPATH:${LAMBDA_TASK_ROOT}"
ENV JAVA_HOME=${JAVA_HOME}

CMD ["main.lambda_handler"]
