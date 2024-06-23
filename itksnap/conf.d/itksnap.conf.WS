[program:itksnap]
command=itksnap -w "%(ENV_WORKSPACE_PATH)s"
autorestart=false