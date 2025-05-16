import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL_QUESTIONS = 'https://esfcex.eb.mil.br/index.php/concursos-esfcex/provas-de-anos-anteriores'

DOWNLOAD_FOLDER = 'data_files'


def get_links_pdf_questions(year: int) -> list | None:
    '''Retornando uma lista com links para provas do ano passado como parâmetro'''
    try:
        response = requests.get(URL_QUESTIONS)
        
        if response.status_code != 200:
            raise Exception(f'Erro ao baixar os PDFs. Status Code: {response.status_code}')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        
        pdf_links = []
        
        for link in links:
            href = link['href']
            if f'{year}' in href:
                full_url = urljoin(URL_QUESTIONS, href)
                full_url = full_url.replace('.PDF', '.pdf')
                pdf_links.append(full_url)
            continue
        
        if not pdf_links:
            print('Nenhum PDF encontrado')
            return None
        
        return pdf_links
    except Exception as e:
        print(f'Erro ao baixar ou salvar: {e}')

def download_pdf_questions(pdf_links: list, name_of_competition: str, year: int):
    '''Baixando as provas em pdf do concurso e ano passados como parâmetro'''
    os.makedirs(f'{DOWNLOAD_FOLDER}/{name_of_competition}/{year}', exist_ok=True)
    
    for pdf_url in pdf_links:
        file_name = pdf_url.split('/')[-1]
        
        if '.pdf' in file_name:
            file_path = os.path.join(DOWNLOAD_FOLDER, name_of_competition, f'{year}', file_name)
            
            try:
                pdf_response = requests.get(pdf_url, stream=True)
            
                with open(file_path, 'wb') as file:
                    for chunk in pdf_response.iter_content(chunk_size=1024):
                        file.write(chunk)
                
                print(f'Prova {file_name} do ano {year} baixada com sucesso!\n')
            except Exception as e:
                print(f'Erro ao baixar os PDFs: {e}')
        else:
            print('Não é pdf')

if __name__ == '__main__':
    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    
    for year in years:
        result = get_links_pdf_questions(year)
        download_pdf_questions(result, 'esfcex', year)
    