#!/usr/bin/env bash

COVER=true
SHORT_CIRCUIT=false
COLLECT_ONLY=false
VERBOSE=0
FAILED=false

while getopts ":vlcfxt:" opt; do
    case $opt in
        c)
            COVER=false
            ;;
        t)
            TEST_TO_RUN=$OPTARG
            ;;
        x)
            SHORT_CIRCUIT=true
            ;;
        l)
            COLLECT_ONLY=true
            ;;
        v)
            VERBOSE=2
            ;;
        f)
            FAILED=true
            ;;
        \?)
          echo "Invalid option: -$OPTARG" >&2
          exit 1
          ;;
        :)
          echo "Option -$OPTARG requires an argument." >&2
          exit 1
      ;;
    esac
done

ENV_VARIABLES="SETTINGS_MODULE=magicarp.settings.base TEST_VERBOSITY=$VERBOSE"

ENV_VARIABLES+=" COVERAGE_PROCESS_START=$PWD/.coverage_magicarp_rc"


number=$RANDOM

RUN_TEST="PYTHONPATH=$PYTHONPATH:$PWD $ENV_VARIABLES nosetests -s --nologcapture --with-id"

if [[ "$COVER" = true ]]; then
    RUN_TEST+=" --cover-package=magicarp --cover-html --cover-erase --cover-inclusive --with-coverage --cov-config=.coverage_magicarp_rc"
fi

if [[ "$SHORT_CIRCUIT" = true ]]; then
    RUN_TEST+=" -x"
fi

if [[ "$FAILED" = true ]]; then
    RUN_TEST+=" --failed"
fi

if [[ ! -z "$TEST_TO_RUN" ]]; then
    RUN_TEST+=" $TEST_TO_RUN"
fi

if [[ "$COLLECT_ONLY" = true ]]; then
    RUN_TEST+=" --collect-only"
fi

if [[ "$VERBOSE" = 2 ]]; then
    RUN_TEST+=" -v"
fi

eval $RUN_TEST

coverage combine  --rcfile=.coverage_magicarp_rc
coverage html --rcfile=.coverage_magicarp_rc
