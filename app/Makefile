.PHONY: install
install:
	pip install -U poetry && poetry install

.PHONY: update
update:
	poetry update

.PHONY: lint
lint:
	poetry run pre-commit install && poetry run pre-commit run

.PHONY: event
event:
	poetry run sam local generate-event sqs receive-message > ../events/event.json

.PHONY: build
build:
	cd ../dockerfiles/ && docker-compose -p mocking-aws-s3 up -d --build

.PHONY: local-run
local-run:
	poetry run sam build -t ../template.yaml && \
	poetry run sam local invoke -t .aws-sam/build/template.yaml -e ../events/event.json --env-vars ../env.json --force-image-build
