ARG CAR_OCI_REGISTRY_HOST=artefact.skao.int

FROM artefact.skao.int/ska-tango-images-pytango-builder:9.4.3 AS buildenv
FROM artefact.skao.int/ska-tango-images-pytango-runtime:9.4.3 AS runtime

USER root

RUN poetry export --format requirements.txt --output poetry-requirements.txt --without-hashes && \
    pip install -r poetry-requirements.txt && \
    rm poetry-requirements.txt && \
    pip install .

USER tango

# Important! This ARG has to come AFTER the FROM statements, not before. If you put the
# ARG statement above FROM then PIP_INDEX_URL is set to a blank value and we default to
# the pypi host set in pip.conf.
ARG CAR_PYPI_REPOSITORY_URL=https://artefact.skao.int/repository/pypi-internal
ENV PIP_INDEX_URL ${CAR_PYPI_REPOSITORY_URL}/simple

ENV PATH="/home/tango/.local/bin:${PATH}"

CMD ["python3"]
