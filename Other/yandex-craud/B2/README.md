# Ответ на задание B2

```bash
git stash push -m "WIP: текущая работа"
git checkout main
# исправляем баг
git add .
git commit -m "Fix: исправление критического бага"
git checkout feature/junior-task
git stash pop
git commit --amend -m "Новое сообщение коммита"
```
