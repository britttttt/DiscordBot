module.exports = {
  apps: [
    {
      name: "PogBot",
      script: "main.py",
      interpreter: "/root/DiscordBot/.venv/bin/python",
      watch: false,
      env: {
        PATH: "/root/DiscordBot/.venv/bin:" + process.env.PATH,
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
};