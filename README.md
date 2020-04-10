# misc

# mon pense bete IN104

## git

Cette [cheatsheet](http://files.zeroturnaround.com/pdf/zt_git_cheat_sheet.pdf) est très claire.

Créer un dépot :

    git init
    emacs README.md
    git status   # on le fait jamais assez souvent !
    git diff     # tkdiff ou meld si on les a configures
    git add README.md
    git commit -m "c'est un debut"
    git log
    git push

    git status


### git alias et diff-graphique

Récupérer tkdiff (ou meld, ou kdiff, ...).

Ajouter les lignes suivantes au fichier `~/.gitconfig` :

```
[color]
	ui = true
[alias]
lg  = log --graph --abbrev-commit --decorate --date=relative --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(bold yellow)%d%C(reset) %C(white)%s%C(reset) ' --all
lg1 = log --graph --abbrev-commit --decorate --date=relative --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(bold yellow)%d%C(reset)' --all
lg2 = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(bold yellow)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)' --all
co = checkout
tkdiff = difftool -t tkdiff -y
meld   = difftool -t meld -y

[core]
    filemode = false
    editor = vi
```

### pour tout le reste...

Stack Overflow est une mine d'or. 


## vi

Editeur de texte.
Le minimum a retenir :

    :q   # pour quitter sans sauver
    :w   # (w)rite
    :wq  # sauve et quitte
    i    # passe en mode edition
    ESC  # revient en mode "command"



## python3

Pour utiliser des modules qui sont dans un répertoire non usuel:

    export PYTHONPATH=/ce/super/repertoire:$PYTHONPATH


## markdown

Lire [mastering markdown](https://guides.github.com/features/mastering-markdown/)

essais de syntaxe: 

TODO list:

- [ ] un item non coché
- [x] un item coché

TODO list sans tiret (c'est ok sur certains flavors de markdown) :

[ ] un autre item non coché
[x] un autre item coché

Tableau : 

| col 1  | col 2 |  col 3 |
| - | - |- |
| rouge | jaune
| bleu  | vert | orange
| carmin | azur


Tableau sans header [source](https://stackoverflow.com/questions/17536216/create-a-table-without-a-header-in-markdown)

| | | |
| - | - |- |
| rouge | jaune
| bleu  | vert | orange
| carmin | azur


## modèle de développement

git n'est qu'un outil, il ne vous dit pas comment travailler (dans quelle branche faire ses devs et commits).

Pour tout projet il est important de se donner des guides de développement. 

Cette page https://nvie.com/posts/a-successful-git-branching-model/ donne un exemple intéressant (devenu un classique) de comment arranger ses branches git.

Le tutoriel https://guides.github.com/introduction/flow/ montre une autre façon de faire (qui repose sur les facilités apportées par github).

Quand on travaille seul ou à deux, on peut s'en sortir en ne travaillant sur `master`. 
