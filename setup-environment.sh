#!/bin/bash

PYTHON="python3"

VENVPATH="${HOME}/.virtualenvs/${PWD##*/}"
if [ -d "$VENVPATH" ]; then
	echo "Pfad existiert schon"
else
	VENVRUN=$(which pyvenv || which virtualenv) || exit 1
	${VENVRUN} -p ${PYTHON} ${VENVPATH}
fi

source ${VENVPATH}/bin/activate
pip install -Ur requirements/local.txt
