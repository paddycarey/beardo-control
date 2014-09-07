help:
	@echo "clean - remove build artifacts"
	@echo "deploy - deploy the app to the development environment"
	@echo "run - run the local development server for testing/debugging purposes"
	@echo "test - run all of the app's tests and print a coverage report"

clean:
	# remove build artifacts from tree
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -empty -type d -delete
	@-rm -f .coverage
	@-rm -f /output/coverage.xml
	@-rm -f /output/nosetests.xml

deploy:
	# deploy application to the default environment
	appcfg.py update . --oauth2 --oauth2_credential_file=~/.appengine_storage/.appcfg_oauth2 --noauth_local_webserver

run: clean
	# run the appengine development server
	dev_appserver.py .                            \
		--host 0.0.0.0                            \
		--admin_host 0.0.0.0                      \
		--datastore_consistency_policy consistent \
		--storage_path /.appengine_storage/       \
		--skip_sdk_update_check

prospector: clean
	# run prospector
	@python ./run-prospector.py

test: clean
	# run tests with a coverage report
	@python ./run-tests.py
