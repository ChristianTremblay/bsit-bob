#!/bin/bash

#     --volume $(pwd):/data \

docker run -it --rm \
    --user $(id -u ${USER}):$(id -g ${USER}) \
    --volume /etc/passwd:/etc/passwd:ro \
    --mount src="$(pwd)",target=/data,type=bind \
    validate:latest \
    python3 test_validation.py $@
