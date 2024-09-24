
deploy:
	@echo "Deploying..."
	poetry run mkdocs gh-deploy
	poetry run mkdocs build
	rsync -avuzP --delete ./site/ -e "ssh -p 9980" user@furyhawk.lol:/var/data/site
	@echo "Deployed!"