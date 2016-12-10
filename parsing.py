import os, re
import requests
from bs4 import BeautifulSoup


START_URL = 'https://otvet.mail.ru'
QUESTIONS_DIR = 'questions'
N_QUESTIONS = 5000


def make_question_url(question_id):
    url = "{}/question/{}".format(START_URL, question_id)
    return url


def get_question(id):
    url = make_question_url(id) 
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    text = soup.h1.text.strip()
    return text

def save_question(text, id):
    with open('{}/{}.txt'.format(QUESTIONS_DIR, id), 'w') as f:
        f.write(text)
        
def get_save_question(id):
    try:
        text = get_question(id)
        save_question(text, id)
    except:
        text = None
    return text



def qet_question_filenames():
    question_files = list(filter(lambda f: f.endswith('.txt'), os.listdir(QUESTIONS_DIR)))
    print('files in /{}/: {}'.format(QUESTIONS_DIR, len(question_files)))
    return question_files

def get_question_ids(question_files):
    question_ids = [int(re.sub('\.txt', '', f)) for f in question_files]
    question_ids.sort()
    return question_ids

def get_start_end():
    q_filenames = qet_question_filenames()
    q_ids = get_question_ids(q_filenames) 
    min_id = min(q_ids)

    end   = min_id
    if end <= N_QUESTIONS: 
        start = 0
    else:            
        start = min_id - N_QUESTIONS
    return start, end



def main():
    start, end = get_start_end()
    
    print('=' * 20)
    print('Starting: #{}'.format(start))
    
    for id in range(start, end):
        if id % 500 == 0:
            print('{} ({}%)'.format(id, round((id - start) * 100/(end - start), 1)))
        get_save_question(id + 1)
    
    print('Finishing: #{}'.format(end))

if __name__ == '__main__':
    main()