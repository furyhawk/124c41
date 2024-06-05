
deploy:
	@echo "Deploying..."
	poetry run mkdocs gh-deploy
	poetry run mkdocs build
	rsync -avuzP --delete ./site/ -e "ssh -p 9999" furyhawk@furyhawk.lol:/var/data/site
	@echo "Deployed!"