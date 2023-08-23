from django.shortcuts import render, redirect
import random
import pymongo
import csv
import time
from .models import Candidate
import numpy as np
from django.http import HttpResponse
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome WebDriver with options
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

# Set the URL of the Indeed website
base_url = "https://in.indeed.com/jobs"
search_query = "python developer"
location = "Chennai"

def scrape_jobs(request):
    Job_data = []

    for page in range(0, 100, 10):  # You can adjust the range based on your requirement
        search_url = f'{base_url}?q={search_query}&l={location}&start={page}'
        driver.get(search_url)
        time.sleep(random.uniform(4.5, 5.9))

    
        jobs = driver.find_elements(By.XPATH, '//div[contains(@class, "css-1m4cuuf") and contains(@class, "e37uo190")]')


        for job in jobs:
            job.location_once_scrolled_into_view

            try:
                close=driver.find_element(By.XPATH,'//*[@id="mosaic-desktopserpjapopup"]/div[1]/button')
                close.click()
            except:
                pass

        
            try:
                job.click()
                time.sleep(random.uniform(3.6, 4.9))

                title = job.find_element(By.CSS_SELECTOR, 'h2').text.strip()

                company_element = driver.find_element(By.XPATH, '//span[@class = "companyName"]')
                company_name = company_element.text.split('\n')[0]

                loc = driver.find_element(By.XPATH, '//div[@class="companyLocation jobsearch-PreciseLocation-location has-icon"]').text.split(' - ')[0]

                try:
                    salary = driver.find_element(By.XPATH, '//div[@class="metadata salary-snippet-container"]/div[@class="attribute_snippet"]').text.strip()
                except:
                    salary = 'NaN'

                employement_element = driver.find_element(By.XPATH, '//div[@class="metadata"]/div[@data-testid="attribute_snippet_testid" and contains(text(), "Full-time")]').text.strip()
                employment_type = employement_element

                data = {
                    'Job_Title': title,
                    'Company': company_name,
                    'Location': loc,
                    'Salary': salary,
                    'employment_type': employment_type
                 }

                Job_data.append(data)
                print('[*] Saving')

            except Exception as e:
                print(f"An error occurred: {e}")

    # Write job data to a CSV file
    output_csv = 'Indeed_JobData.csv'
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Job_Title', 'Company', 'Location', 'Salary', 'employment_type']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(Job_data)

    driver.quit()

    return HttpResponse("Scraping completed and data saved.")

def search_candidates(request):
    candidates = Candidate.objects.all()
    return render(request, 'scraper_app/search_candidates.html', {'candidates': candidates})

def edit_candidate(request, candidate_id):
    candidate = Candidate.objects.get(pk=candidate_id)
    
    if request.method == 'POST':
        # Update candidate fields based on form data
        candidate.Job_Title = request.POST.get('Job_Title')
        candidate.Company = request.POST.get('Company')
        candidate.Location = request.POST.get('Location')
        candidate.Salary = request.POST.get('Salary')
        candidate.employment_type = request.POST.get('employment_type')
        candidate.save()
        return redirect('search_candidates')
    
    return render(request, 'craper_app/edit_candidate.html', {'candidate': candidate})

def delete_candidate(request, candidate_id):
    candidate = Candidate.objects.get(pk=candidate_id)
    
    if request.method == 'POST':
        candidate.delete()
        return redirect('search_candidates')
    
    return render(request, 'scraper_app/delete_candidate.html', {'candidate': candidate})

def calculate_average_salary(request):
    python_jobs = Candidate.objects.filter(Job_Title='python developer', Location='Chennai')
    salaries = [float(job.Salary.replace('$', '').replace(',', '')) for job in python_jobs if job.Salary != 'NaN']
    average_salary = np.mean(salaries)
    
    return render(request, 'scraper_app/average_salary.html', {'average_salary': average_salary})