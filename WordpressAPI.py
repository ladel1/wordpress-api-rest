import requests
import base64
import json
import os

ENDPOINT = '<URL>/wp-json/wp/v2'
API_KEY ="<api_key>"
USERNAME = '<username>'
class WordpressAPI:

    @staticmethod
    def add_article(title, content, category, image_path):
        # Obtenez l'ID de la catégorie en fonction de son nom
        category_id = WordpressAPI.get_category_id(category)

        # Créez le corps de la requête
        data = {
            'title': title,
            'content': content,
            'status': 'publish',
            'categories': [category_id]
        }

        # Envoyez la requête POST avec le corps et les en-têtes appropriés
        # Encodage des informations d'identification en base64
        credentials = base64.b64encode(f'{USERNAME}:{API_KEY}'.encode('utf-8')).decode('utf-8')
        
        # En-têtes de requête avec l'authentification de base
        headers = {
            'Authorization': 'Basic ' + credentials,
            'Content-Type': 'application/json'
        }

        image_id = WordpressAPI.add_featured_image(image_path, credentials)

        data['featured_media'] = image_id

        json_data = json.dumps(data)
        response = requests.post(ENDPOINT+'/posts', headers=headers, data=json_data)
        response.raise_for_status()

        print("Article added!")

    @staticmethod
    def get_category_id(category):
        print("Getting category id...")
        print(category)
        # En-têtes de requête avec l'authentification de base
        response = requests.get(ENDPOINT+'/categories?per_page=100')
        response.raise_for_status()

        categories = response.json()
        for cat in categories:
            if cat['name'] == category:
                return cat['id']

        raise Exception("Category don't found.")
    
    @staticmethod
    def add_featured_image(image_path, credentials):
        # Ouvrez le fichier de l'image en mode binaire
        with open(image_path, 'rb') as image_file:
            # Envoyez une requête POST pour télécharger l'image en tant que pièce jointe
            filename = os.path.basename(image_path)
            headers = {
                'Authorization': f'Basic {credentials}',
                'Content-Disposition': 'attachment; filename='+filename,
                'Content-Type': 'image/jpeg'
            }

            response = requests.post(ENDPOINT+f'/media', headers=headers, data=image_file)
            response.raise_for_status()

            # Obtenez l'ID de l'image téléchargée
            image_id = response.json().get('id')
            print("Image downloaded !")
            return image_id  
