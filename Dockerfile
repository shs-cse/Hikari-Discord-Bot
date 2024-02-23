FROM continuumio/miniconda3:main
COPY . .
RUN conda install pandas
RUN pip install pygsheets
RUN pip install -U hikari[speedups]
RUN pip install hikari-crescent
# CMD [ "conda", "list"]
CMD ["python", "main.py"]