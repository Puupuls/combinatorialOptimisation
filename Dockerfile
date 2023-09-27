FROM mambaorg/micromamba:alpine
LABEL authors="Puupuls"

WORKDIR /co

COPY . /co

RUN micromamba install --yes --name base -f environment.yaml
RUN micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1


EXPOSE 5000
CMD micromamba run -n base python interface.py