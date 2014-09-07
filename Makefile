# The name of the project is used throughout the makefile to provide
# project-specific docker containers.
PROJNAME = beardo-control

# If running on Linux (and thus using docker directly) we set the user id to
# that of the current user. If running on Mac (and thus on top of boot2docker)
# we don't bother since Virtualbox takes care of ensuring any created files
# have the correct permissions.
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
	USER_ID = -u $(shell id -u $$USER)
else ifeq ($(UNAME), Darwin)
	USER_ID =
endif


help:
	@echo "build - Build docker container"
	@echo "storage - Create a storage-only container (we'll use its volumes elsewhere)"
	@echo "run - Run development server inside a Docker container"
	@echo "test - Run application's tests inside a docker container"

build:
	docker build -t="beardo/$(PROJNAME)" .

rebuild:
	touch assets/force_rebuild
	docker build -t="beardo/$(PROJNAME)" .

storage: build
	-docker run -t -i --name $(PROJNAME) beardo/$(PROJNAME) echo "Storage-only container."

run: storage
	@-docker kill $(PROJNAME)-run
	@-docker rm $(PROJNAME)-run
	docker run -t -i --rm --name $(PROJNAME)-run --volumes-from $(PROJNAME) -v $(CURDIR)/app:/app -p 0.0.0.0:8080:8080 -p 0.0.0.0:8000:8000 beardo/$(PROJNAME) make -C /app run

prospector: storage
	docker run -t -i --volumes-from $(PROJNAME) -v $(CURDIR)/app:/app -v $(CURDIR)/output:/output beardo/$(PROJNAME) make -C /app prospector

test: storage
	docker run -t -i --volumes-from $(PROJNAME) -v $(CURDIR)/app:/app -v $(CURDIR)/output:/output $(USER_ID) beardo/$(PROJNAME) make -C /app test

deploy: storage
	docker run -t -i --volumes-from $(PROJNAME) -v $(CURDIR)/app:/app beardo/$(PROJNAME) make -C /app deploy
