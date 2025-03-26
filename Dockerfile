FROM artefact.skao.int/ska-build-python:0.1.1 as build

WORKDIR /src

COPY pyproject.toml poetry.lock* ./

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1

#no-root is required because in the build
#step we only want to install dependencies
#not the code under development
RUN poetry install --no-root

FROM artefact.skao.int/ska-python:0.1.2

WORKDIR /src

#Adding the virtualenv binaries
#to the PATH so there is no need
#to activate the venv
ENV VIRTUAL_ENV=/src/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=build ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./src/ska_oso_tmcsim ./ska_oso_tmcsim

#Add source code to the PYTHONPATH
#so python is able to find our package
#when we use it on imports
ENV PYTHONPATH=${PYTHONPATH}:/src/

CMD ["python3"]
