TEST_CONTAINER="drf-bulk-destroy-container"
IMAGE_NAME="drf-bulk-destroy-local"

build:
	docker build -t ${IMAGE_NAME} .

run:
	docker run --rm -it -v ${PWD}/src:/usr/src/app -p 8000:8000 --name ${TEST_CONTAINER} ${IMAGE_NAME}

exec:
	docker exec -it ${TEST_CONTAINER} bash

bash:
	docker run --rm -it -v ${PWD}/src:/usr/src/app --name ${TEST_CONTAINER} ${IMAGE_NAME} bash

clean:
	find . -name __pycache__ -exec rm -rf {} \;
