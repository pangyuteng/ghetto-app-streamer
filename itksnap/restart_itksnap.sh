
pkill -f /opt/itksnap/lib/snap-4.2.0/ITK-SNAP
DISPLAY=:1 nohup /opt/itksnap/bin/itksnap -w /mnt/share/workspace.itksnap 1>/dev/null 2>/dev/null &
