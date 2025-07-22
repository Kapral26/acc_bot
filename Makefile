.DEFAULT_GOAL := help

run: ## Запустить приложение с помощью uvicorn с заданными аргументами или значениями по умолчанию
	uv run gunicorn main:app --worker-class uvicorn.workers.UvicornWorker -c gunicorn.conf.py

install: ## Установить зависимость с помощью poetry
	@echo "Установка зависимости $(LIBRARY)"
	uv add $(LIBRARY)

uninstall: ## Удалить зависимость с помощью poetry
	@echo "Удаление зависимости $(LIBRARY)"
	uv remove $(LIBRARY)

migrate-create: ## Создать новую миграцию
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply: ## Применить миграцию
	alembic upgrade head

help: ## Показать это сообщение о помощи
	@echo "Использование: make [команда]"
	@echo ""
	@echo "Команды:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
