[program:itksnap]
command=/opt/itksnap/bin/itksnap -w "%(ENV_WORKSPACE_PATH)s"
autorestart=false