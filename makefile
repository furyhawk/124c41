
deploy:
	@echo "Deploying..."
	uv run mkdocs gh-deploy
	uv run mkdocs build
	rsync -avuzP --delete ./site/ -e "ssh" user@192.168.50.220:/var/data/site
	@echo "Deployed!"