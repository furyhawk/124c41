
deploy:
	@echo "Deploying..."
	poetry run mkdocs gh-deploy
	poetry run mkdocs build
	rsync -avuzP --delete ./site/ -e "ssh" user@192.168.50.220:/var/data/site
	@echo "Deployed!"