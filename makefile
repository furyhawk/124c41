
deploy:
	@echo "Deploying..."
	poetry run mkdocs gh-deploy
	poetry run mkdocs build
	rsync -avuz --delete ./site/ -e "ssh -p 9999" furyhawk@furyhawk.lol:/home/furyhawk/cloudy/site
	@echo "Deployed!"