FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt
EXPOSE 8501  
ENTRYPOINT ["streamlit","run"]
CMD ["azure_ai_vector_search/app.py"]