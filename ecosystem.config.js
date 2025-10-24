module.exports = {
  apps: [
    {
      name: "PogBot",
      script: "./main.py",
      interpreter: "python3",
      instances: 1,        
      autorestart: true,
      watch: false,
    }
  ]
};
