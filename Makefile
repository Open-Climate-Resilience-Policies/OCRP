DOCKER_IMAGE := ocrap-jekyll

.PHONY: build-docker serve-docker

build-docker:
	docker build -t $(DOCKER_IMAGE) .

serve-docker: build-docker
	docker run --rm -p 4000:4000 -v $(PWD):/srv/jekyll $(DOCKER_IMAGE) jekyll serve --watch --force_polling --host 0.0.0.0
