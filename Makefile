create-sdk:
	poetry update
	git clone git@github.com:hiddb/openapi.git openapi
	poetry run openapi-python-client generate --path openapi/openapi.yaml

update-sdk:
	poetry update
	rm -rf openapi
	git clone git@github.com:hiddb/openapi.git openapi
	poetry run openapi-python-client generate --path openapi/openapi.yaml

