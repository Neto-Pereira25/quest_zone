r pdf_url in pdf_links:
        file_name = pdf_url.split('/')[-1]
        
        if '.pdf' in file_name:
            file_path = os.path.join(DOWNLOAD_FOLDER, name_of_competition, f'{year}', file_name)
            
            try:
                pdf_response = requests.get(pdf_url, stream=True)
            
                with open(file_path, 'wb') as file:
                    for chunk in pdf_response.iter_content(chunk_size=1024):
                        file.write(chunk)
                
                print(f'{file_name} baixado com sucesso!\n')
            except Exception as e:
                p