module.exports = {
  apps: [
    {
      name: "PogBot",
      script: "main.py",
      interpreter: "/root/DiscordBot/.venv/bin/python3",
      watch: false,
      env: {
        NODE_ENV: "production"
      }
    }
  ]
}
