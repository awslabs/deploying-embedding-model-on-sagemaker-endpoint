
CONTAINER_IMAGE := inference-server
CONTAINER_PRE_PATH := proserve
TAG := latest

.PHONY: flask-run
flask-run:
	python src/predictor.py

.PHONY: docker-run
docker-run: build
	-@docker stop ${CONTAINER_IMAGE}
	-@docker rm ${CONTAINER_IMAGE} || true
	docker run -p 5001:8080 -d --name ${CONTAINER_IMAGE} -e "MODEL_SERVER_WORKERS=1" ${CONTAINER_PRE_PATH}/${CONTAINER_IMAGE}:${TAG} serve

.PHONY: build
build:
	docker build  -t ${CONTAINER_PRE_PATH}/${CONTAINER_IMAGE}:${TAG} .

.PHONY: build_and_push
build_and_push: guard-image
	./script/build_and_push.sh ${image}

.PHONY: guard-%
guard-%:
	@#$(or ${$*}, $(error Argument '$*' is not set))

