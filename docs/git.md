# GIT

## README.md
- 👋 Hi, I’m @furyhawk
- 👀 I’m interested in AI
- 🌱 I’m currently learning AI
- 💞️ I’m looking to collaborate on AI
- 📫 How to reach me ...

[https://github.com/furyhawk](https://github.com/furyhawk)

```sh
$ git config --global user.name "furyhawk"
$ git config --global user.email furyx@hotmail.com
```

## commit msg
```
<type>: <short summary>
  │            │
  │            └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|cicd|docs|feat|fix|node|refactor|test
```

## Fetch/pull all branches
```sh
git branch -r | grep -v '\->' | sed "s,\x1B\[[0-9;]*[a-zA-Z],,g" | while read remote; do git branch --track "${remote#origin/}" "$remote"; done
git fetch --all
git pull --all
```

## How can I enable github notifications?

install and authenticate with the github cli:
```sh
pacman -S github-cli
gh auth login
```

ubuntu:
```sh
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh -y
```