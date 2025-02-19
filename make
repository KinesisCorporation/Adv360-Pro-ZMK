#!/bin/env bash
make() {
  if [ -f Makefile ]; then
    make $@
  else
    echo "No Makefile found"
  fi
}