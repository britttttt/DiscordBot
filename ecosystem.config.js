module.exports = {
  apps: [
    {
      name: "PogBot",
      script: "/root/DiscordBot/main.py",
      interpreter: "/usr/bin/python3",   
      watch: false,
      autorestart: true,
      env: {
   
      },
    },
  ],
};
