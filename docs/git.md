# GIT

## README.md
- š Hi, Iām @furyhawk
- š Iām interested in AI
- š± Iām currently learning AI
- šļø Iām looking to collaborate on AI
- š« How to reach me ...

```sh
$ git config --global user.name "furyhawk"
$ git config --global user.email furyx@hotmail.com
```

## commit msg
```
<type>: <short summary>
  ā            ā
  ā            āāā«ø Summary in present tense. Not capitalized. No period at the end.
  ā
  āāā«ø Commit Type: build|cicd|docs|feat|fix|node|refactor|test
```

## Fetch/pull all branches
```sh
git branch -r | grep -v '\->' | sed "s,\x1B\[[0-9;]*[a-zA-Z],,g" | while read remote; do git branch --track "${remote#origin/}" "$remote"; done
git fetch --all
git pull --all
```