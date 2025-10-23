# Discord Bot Update Workflow (PM2)

---

## 1. SSH into Your Server

```bash
ssh root@your_server_ip
cd ~/DiscordBot
source .venv/bin/activate
```


## 2. Pull the Latest Code
If using Git:
```
git pull origin main
```
Replace main with your branch name if different.


## 3. Update Dependencies
```
    pip install -r requirements.txt
```

## 4. Restart the Bot Using PM2
```
    pm2 restart PogBot --update-env
```
For zero downtime updates (especially with multiple processes):

```
    pm2 reload PogBot
```
Check logs to confirm:
```
    pm2 logs PogBot
```


## 5. Save PM2 Process List
If you made changes to the PM2 setup:
```
    pm2 save
```