#!/usr/bin/env bash

SUCCESS=1
RUNNING=0

check_colima_status() {
    if ! colima status >/dev/null 2>&1; then
        echo "Colima is not running. Starting Colima..."
        colima start
        RUNNING=1
    else
        echo "Colima is already running"
    fi
}

call_make() {
  if [ -f Makefile ]; then
    make $@
    SUCCESS=$?
  else
    echo "No Makefile found"
  fi
}


stop_colima() {
    if colima status >/dev/null 2>&1 && [ $RUNNING -eq 1 ]; then
        echo "Stopping Colima..."
        colima stop
    else
        echo "Colima is not running"
    fi
}

check_colima_status
call_make $@
stop_colima
echo "Build successful: $([ $SUCCESS -eq 0 ] && echo "TRUE" || echo "FALSE")"
exit $SUCCESS