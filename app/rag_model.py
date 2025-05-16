import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ollama
import json
from sqlalchemy.orm import Session
from .logging_config import logger
from . import models, crud

# Configure Ollama client
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://ollama:11434')
ollama_client = ollama.Client(host=OLLAMA_HOST)

def scrape_fusemachines_jobs():
    """Scrape job listings from Fusemachines careers page."""
    options = Options()
    options.add_argument("--headless")  # Uncomment for headless mode
    # service = Service('/usr/local/bin/geckodriver')
    service = Service('/usr/local/bin/geckodriver', log_path='/app/logs/geckodriver.log')
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        driver.maximize_window()
        driver.get("https://fusemachines.com/")
        company_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='company']"))
        )
        company_button.click()
        careers_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/company/careers/']"))
        )
        careers_link.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "jazzhr"))
        )
        job_rows = driver.find_elements(By.XPATH, "//div[@id='jazzhr']//div[contains(@class, 'row py-3')]")
        jobs = []
        for row in job_rows:
            title = row.find_element(By.XPATH, ".//div[contains(@class, 'col-md-6')]//div[@class='bold-s']").text
            location = row.find_element(By.XPATH, ".//div[contains(@class, 'col-md-4')]//div[@class='c-dark-grey']").text
            jobs.append({"title": title, "location": location})
        logger.info(f"Scraped {len(jobs)} jobs")
        return jobs
    finally:
        driver.quit()

def generate_embedding(chunk: str) -> list:
    try:
        embedding = ollama_client.embed(model="hf.co/CompendiumLabs/bge-base-en-v1.5-gguf", input=chunk)['embeddings'][0]
        logger.info(f"Generated embedding for chunk: {chunk[:50]}...")
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding for chunk '{chunk[:50]}...': {e}")
        raise

def cosine_similarity(a: list, b: list) -> float:
    """Calculate cosine similarity between two vectors."""
    try:
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x ** 2 for x in a) ** 0.5
        norm_b = sum(x ** 2 for x in b) ** 0.5
        return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0
    except Exception as e:
        logger.error(f"Error calculating cosine similarity: {e}")
        raise

def retrieve_jobs(query: str, db: Session, top_n: int = 3) -> list:
    """Retrieve top N most relevant jobs based on query."""
    try:
        query_embedding = generate_embedding(query)
        similarities = []
        jobs = crud.get_jobs(db)
        for job in jobs:
            embedding = crud.get_embedding(db, job.id)
            if embedding:
                embedding_vector = json.loads(embedding.embedding_vector)
                similarity = cosine_similarity(query_embedding, embedding_vector)
                chunk = f"{job.title} in {job.location}"
                similarities.append((chunk, similarity))
        similarities.sort(key=lambda x: x[1], reverse=True)
        logger.info(f"Retrieved {len(similarities[:top_n])} jobs for query: {query}")
        return [{"chunk": chunk, "similarity": sim} for chunk, sim in similarities[:top_n]]
    except Exception as e:
        logger.error(f"Error retrieving jobs for query '{query}': {e}")
        raise

def generate_response(query: str, retrieved_jobs: list) -> str:
    try:
        instruction_prompt = f"""You are a helpful chatbot providing information about job openings at Fusemachines.
Use only the following job listings to answer the question. Don't make up any new information:
{'\n'.join([f' - {job["chunk"]}' for job in retrieved_jobs])}
"""
        stream = ollama_client.chat(
            model="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF",
            messages=[
                {'role': 'system', 'content': instruction_prompt},
                {'role': 'user', 'content': query},
            ],
            stream=True,
        )
        response = ''
        for chunk in stream:
            content = chunk['message']['content']
            response += content
        logger.info(f"Generated response for query: {query}")
        return response
    except Exception as e:
        logger.error(f"Error generating response for query '{query}': {e}")
        raise