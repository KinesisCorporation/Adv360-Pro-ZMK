#!/usr/bin/env bash

SUCCESS=1
RUNNING=0
COLIMA_BUILD_SUCCESS=1
GIT_ADD_SUCCESS=1
GIT_COMMIT_SUCCESS=1
GIT_PUSH_SUCCESS=1

GIT_COMMIT_MESSAGE="feat: Quick fix"

if [ "$#" -eq 1 ]; then
  GIT_COMMIT_MESSAGE="$1"
fi

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
    COLIMA_BUILD_SUCCESS=$?
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
//Assumes no arguments passed to make
call_make
stop_colima

if [ $COLIMA_BUILD_SUCCESS -eq 0 ]; then
    git add .
    GIT_ADD_SUCCESS=$?
fi

if [ $GIT_ADD_SUCCESS -eq 0 ]; then
    git commit -m "$GIT_COMMIT_MESSAGE"
    GIT_COMMIT_SUCCESS=$?
fi

if [ $GIT_COMMIT_SUCCESS -eq 0 ]; then
    git push -u origin HEAD:V3.0
    GIT_PUSH_SUCCESS=$?
fi

if [ $GIT_PUSH_SUCCESS -eq 0 ]; then
    SUCCESS=0
fi

echo "Overall build successful: $([ $SUCCESS -eq 0 ] && echo "TRUE" || echo "FALSE")"
echo "Colima build successful: $([ $COLIMA_BUILD_SUCCESS -eq 0 ] && echo "TRUE" || echo "FALSE")"
echo "Git add successful: $([ $GIT_ADD_SUCCESS -eq 0 ] && echo "TRUE" || echo "FALSE")"
echo "Git commit successful: $([ $GIT_COMMIT_SUCCESS -eq 0 ] && echo "TRUE" || echo "FALSE")"
echo "Git push successful: $([ $GIT_PUSH_SUCCESS -eq 0 ] && echo "TRUE" || echo "FALSE")"

exit $SUCCESS