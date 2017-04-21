import csv
import requests
import json

# add token between quotes
authentication = ''

endpoint = 'https://api.crimsonhexagon.com/api/content/upload'

def parse():

    documents = []

    print('Opening file...')

    try:

        with open('upload.csv', 'rb') as file:

            reader = csv.DictReader(file, delimiter=',')

            print('Parsing file...')

            rowNumber = 1
            print reader

            for row in reader:

                if row['title']:
                    title = row.get('title').strip() or row.get('TITLE').strip()
                date = row.get('date') or row.get('DATE')
                if row['author']:
                    author = row.get('author') or row.get('AUTHOR')
                url = row.get('url') or row.get('URL')
                contents = row.get('contents').strip() or row.get('CONTENTS').strip()
                content_type = row.get('type') or row.get('TYPE')
                language = row.get('language') or row.get('LANGUAGE')

                payload = {
                    'title': title,
                    'date': date,
                    'author': author,
                    'url': url,
                    'contents': contents,
                    'language': language,
                    'type': content_type
                }

                if 'country' and 'state' and 'city' in row:

                    if not row.get('country') or not row.get('state') or not row.get('city'):
                        print('Row {} missing geolocation.'.format(rowNumber))

                    geolocation = {
                        'id': '{}.{}.{}'.format(row.get('country'), row.get('state'), row.get('city'))
                    }

                    payload['geolocation'] = geolocation

                elif 'latitude' and 'longitude' in row:

                    if not row.get('latitude') or not row.get('longitude'):
                        print('Row {} missing geolocation.'.format(rowNumber))

                    if row['latitude'] and row['longitude']:

                        geolocation = {
                            'latitude': float(row.get('latitude')),
                            'longitude': float(row.get('longitude'))
                        }

                        payload['geolocation'] = geolocation

                elif 'zipcode' in row:

                    if not row.get('zipcode'):
                        print('Row {} missing geolocation.'.format(rowNumber))

                    geolocation = {
                        'zipcode': row.get('zipcode'),
                    }

                    payload['geolocation'] = geolocation

                if 'gender' in row:
                    if row['gender']:
                        gender = row.get('gender')
                    payload['gender'] = gender
                    if not row.get('gender'):
                        print('Row {} missing gender.'.format(rowNumber))

                if 'age' in row:
                    if row['age']:
                        age = row.get('age')
                    payload['age'] = int(age)
                    if not row.get('age'):
                        print('Row {} missing age.'.format(rowNumber))

                documents.append(payload)
                print json.dumps(payload)

                # if 1000 documents ready to upload, yield the documents to upload, erase the list of documents and continue on
                if len(documents) == 1000:
                    yield documents
                    documents[:] = []

                rowNumber = rowNumber + 1

    except IOError:

        print('Error: File \'upload.csv\' not found')

    yield documents

def upload():

    for documents in parse():

        query_parameters = {
            'auth': authentication
        }

        payload = {
            'items': documents
        }

        response = requests.request("POST", endpoint, data=json.dumps(payload), params=query_parameters)
        print response.text

upload()
