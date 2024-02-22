FROM continuumio/miniconda3:main
COPY . .
CMD [ "which", "python" ]