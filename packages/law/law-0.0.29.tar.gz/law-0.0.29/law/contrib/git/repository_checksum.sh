#!/usr/bin/env bash

# Computes a checksum of a git repository considering
# 1. the current revision,
# 2. the current diff, and
# 3. the content of new files.

# Arguments:
# 1. the path to the repository

action() {
    # load polyfills
    local base="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    source "$base/../../polyfills.sh"

    # handle arguments
    local repo_path="$1"
    if [ -z "$repo_path" ]; then
        2>&1 echo "please provide the path to the repository to bundle"
        return "1"
    fi

    if [ ! -d "$repo_path" ]; then
        2>&1 echo "the provided path '$repo_path' is not a directory or does not exist"
        return "2"
    fi

    ( \
        cd "$repo_path" && \
        git rev-parse HEAD && \
        git diff && \
        ( git ls-files --others --exclude-standard | xargs cat ) \
    ) | shasum | cut -d " " -f 1
    local ret="$?"

    return "$ret"
}
action "$@"
