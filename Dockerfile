FROM continuumio/miniconda3:main
COPY . .
RUN conda install pandas
RUN pip install pygsheets
# RUN conda install marta-sd::pygsheets
# CMD [ "conda", "list"]
CMD ["python", "main.py"]