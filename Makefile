.PHONY: help
help: ## Display this help screen (not work in windows)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: up-dev
up-dev: ## create and start docker container in the development environment
	docker-compose -f docker-compose.yml -f docker-compose.development.yml up -d

.PHONY: up-prod
up-prod: ## create and start docker container in the production environment
	docker-compose -f docker-compose.yml -f docker-compose.production.yml up -d

.PHONY: build
build: ## build docker service (usage: make build options=[options])
	docker-compose build ${options}

.PHONY: makemigrations
makemigrations: ## make migration file
	docker-compose run --rm django python3 manage.py makemigrations

.PHONY: migrate
migrate: ## migrate database
	docker-compose run --rm django python3 manage.py migrate

.PHONY: create-superuser
create-superuser: ## create superuser (usage: make create-superuser username=[username] email=[email])
	docker-compose run --rm django python3 manage.py createsuperuser --username ${username} --email ${email}

.PHONY: restart-dev
restart-dev: ## restart docker container in the development environment
	docker-compose -f docker-compose.yml -f docker-compose.development.yml restart

.PHONY: restart-prod
restart-prod: ## restart docker container in the production environment
	docker-compose -f docker-compose.yml -f docker-compose.production.yml restart

.PHONY: collect-static
collect-static: ## collect django static files into STATIC_ROOT
	docker-compose exec django python3 manage.py collectstatic --noinput ${options}

.PHONY: django-log
django-log: ## show django logs
	docker-compose logs -f --tail=200 django

.PHONY: makemessages
makemessages: ## generate locale files from strings marked for translation
	docker-compose exec django python3 manage.py makemessages -l en --no-location

.PHONY: compilemessages
compilemessages: ## compile from *.po files to *.mo files
	docker-compose exec django python3 manage.py compilemessages

.PHONY: generate-ERD
generate-ERD: ## generate ERD figure from table_definition.er
	docker-compose exec django python3 manage_ERD/generate_ERD.py

.PHONY: run-dev
run-dev: ## run in the development environment (usage: make run-dev service=[service] command=[command])
	docker-compose -f docker-compose.yml -f docker-compose.development.yml run --rm ${service} ${command}

.PHONY: run-prod
run-prod: ## run in the production environment (usage: make run-prod service=[service] command=[command])
	docker-compose -f docker-compose.yml -f docker-compose.production.yml run --rm ${service} ${command}

.PHONY: yarn-all
yarn-all: ## run webpack build
	docker-compose run django yarn all ${arg}

.PHONY: webpack-watch
webpack-watch: ## run webpack build with watchmode
	docker-compose exec django yarn watch
