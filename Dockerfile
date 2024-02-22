FROM continuumio/miniconda3:main
COPY . .
RUN conda install pandas
# CMD [ "conda", "list"]
CMD ["python", "main.py"]