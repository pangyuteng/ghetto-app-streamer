#!/bin/bash
set -ex

RUN_FLUXBOX=${RUN_FLUXBOX:-yes}
RUN_XTERM=${RUN_XTERM:-yes}
RUN_ITKSNAP=${RUN_ITKSNAP:-yes}

case $RUN_FLUXBOX in
  false|no|n|0)
    rm -f /app/conf.d/fluxbox.conf
    ;;
esac

case $RUN_XTERM in
  false|no|n|0)
    rm -f /app/conf.d/xterm.conf
    ;;
esac

case $RUN_ITKSNAP in
  false|no|n|0)
    rm -f /app/conf.d/itksnap.conf
    ;;
esac


exec supervisord -c /app/supervisord.conf
