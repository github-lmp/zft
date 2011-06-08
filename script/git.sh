git status |grep modified: |awk -F" " '{print $3}'|xargs git add

