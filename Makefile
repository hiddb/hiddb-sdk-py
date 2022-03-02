create-sdk:
	poetry update
	git clone git@github.com:hiddb/openapi.git openapi

update-sdk:
	poetry update
	rm -rf openapi
	git clone git@github.com:hiddb/openapi.git openapi

