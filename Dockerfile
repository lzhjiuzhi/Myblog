    FROM python:3.6

    RUN mkdir -p /blog
    WORKDIR /blog


    ADD . /blog
    RUN pip install gunicorn django psycopg2 markdown Pillow 	
    COPY . /blog
    EXPOSE  8080 80 8000 5000

    CMD ["gunicorn", "--chdir", "myblog", "--bind", ":8000", "myblog.wsgi:application"]
