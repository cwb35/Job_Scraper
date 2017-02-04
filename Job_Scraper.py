# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 19:22:19 2017

@author: Colin
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from string import Template
import sys
import argparse
import re

def scrape_jobs(job_title, terms, location, radius, num_jobs):
    
    url = "https://www.indeed.com/jobs?"
    search = Template("as_and=$job&radius=$r&l=$loc&fromage=any&limit=$num&psf=advsrch")
    response = requests.get(url+search.substitute(job=job_title,
                                           r=radius, loc=location, num=num_jobs))
    soup = BeautifulSoup(response.text,"lxml")
    
    job_info = []
    for i, div in enumerate(soup.find_all('div', {'class':' row result'})):


        loc, company, date, title, link = 0, 0, 0, 0, 0

        for span in div.find_all('span', {'class': 'location'}):
            loc = span.text
        for span in div.find_all('span', {'class': 'company'}):
            company = span.text
        for span in div.find_all('span', {'class', 'date'}):
            date = span.text
        for header in div.find_all("h2"):
            title = header.text
            link = "https://www.indeed.com" + header.find("a").get('href')

        job_info.append((title.strip(), company.strip(), loc.strip(), date.strip(), link))
        
    return pd.DataFrame(job_info, columns=['Job_Title', 'Company', 'Location', 
                                           'Date_Posted', 'Link'])
    
def extract_text(list_links, v=False):
    
    job_text = []
    replace_punc = re.compile(r"[,.;@#?!&$]+")
    for link in list_links:

        if v: print("Getting html from:", link)
        try:
            response = requests.get(link)
            soup = BeautifulSoup(response.text,"lxml")
        except:
            if v: print("Failed to get html from: ", link)
            job_text.append("FAILED")
            continue

        if v: print("got html from: ", link)

        text = ""
        for p in soup.find_all("p"):
            text += "\n" + p.text.lower()
        for li in soup.find_all('li'):
            text += "\n" + li.text.lower()

        job_text.append(re.sub(replace_punc, ' ', text.strip()))
        
    return job_text
    
def count_terms(list_text, terms):
    """
    Counts # times each term inside terms appears in each string in list_text.
    
    Parameters
    ----------
        list_text - <list> Text that's being searched
        terms - <list> Keywords that are being counted
        
    Returns
    -------
        doc_count - <list of dicts> Each dict represents the count of terms in
                    that text
    """
    
    doc_count = []
    for text in list_text:
        keyword_dict = {term:text.count(term.lower()) for term in terms}
        doc_count.append(keyword_dict)
        
    return doc_count
    
def get_lines(list_text, terms):
    
    list_dicts = []
    for text in list_text:
        line_dict = {term:[] for term in terms}
        if type(text) == str:
            for line in text.replace('\r','\n').split('\n'):
                for term in terms:
                    if term.lower() in line:
                        line_dict[term].append(line)
        list_dicts.append(line_dict)
        
    return list_dicts

def main():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('program', metavar='PROG', type=str)
    parser.add_argument('job_title', metavar='job', type=str)
    parser.add_argument('location', metavar='loc', type=str)
    parser.add_argument('radius', metavar='R', type=int)
    parser.add_argument('num_jobs', metavar='N', type=int)
    parser.add_argument('-terms', metavar='T', type=str, nargs='+')
    parser.add_argument('-output', metavar='out', type=str)
    parser.add_argument('-keeplines', metavar='keep', type=bool)
    
    arg_dict = vars(parser.parse_args(sys.argv))
    
    if arg_dict['output']!=None:
        output = arg_dict['output']
    else:
        string = arg_dict['job_title'] + " " + arg_dict['location']
        output = "_".join(string.split())+"_Job_Report.csv"
        
    if arg_dict['terms']!=None:
        terms = arg_dict['terms']
    else:
        terms = None
        
    if arg_dict['keeplines']!=None:
        keeplines = True
    else:
        keeplines = False
        
    params = {
        'job_title':arg_dict['job_title'].replace(' ', '+'),
        'location':arg_dict['location'].replace(' ', '+'),
        'radius':arg_dict['radius'],
        'num_jobs':arg_dict['num_jobs'],
        'terms':terms    
    }
    df = scrape_jobs(**params)
    
    df['Text'] = extract_text(df.Link)
    df = df[df.Text != 'FAILED']

    doc_count = count_terms(df.Text, terms)
    
    for term in terms:
        df[term] = [x[term] for x in doc_count]

    df.to_csv(output, index=False, encoding='utf8')

if __name__ == "__main__":
    main()
    
