.PHONY: setup-shared-modules test deploy

setup-shared-modules:
	rm -rf event-emitter-api/common
	rm -rf persistence-service/common
	rm -rf cdk/common
	cp -r common event-emitter-api/
	cp -r common persistence-service/
	cp -r common cdk/

test:
	pytest

deploy:
	cd cdk && cdk deploy

ci-cd: setup-shared-modules test deploy
