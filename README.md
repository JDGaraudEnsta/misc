# misc

# mon pense bete IN104

## git

Cette [cheatsheet](http://files.zeroturnaround.com/pdf/zt_git_cheat_sheet.pdf) est très claire.

Créer un dépot :

    git init
    emacs README.md
    git status   # on le fait jamais assez souvent !
    git add README.md
    git commit -m "c'est un debut"
    git push

    git status


### git graphique

Récupérer tkdiff chez JDG :

    # a ajouter au ~/.bashrc
    export PATH=/home/g/garaud/bin:$PATH
    # puis en prevision de la suite des TP:
    export PATH=~/bin:~/.local/bin:$PATH

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

(lire ça)[https://guides.github.com/features/mastering-markdown/]

