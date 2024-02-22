FROM continuumio/miniconda3:main
COPY . .
RUN conda install pandas
RUN pip install pyjson5
# CMD [ "conda", "list"]
CMD ["python", "main.py"]