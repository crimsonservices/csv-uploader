import csv
import requests
import json

# add your authentication token between quotes
authentication = ''

endpoint = 'https://api.crimsonhexagon.com/api/content/upload'

counter = 0

def parse():

    documents = []

    print('Opening file...')

    try:

    	# open CSV file
        with open('upload.csv', 'rb') as file:

        	# convert CSV file to a dictionary (key = column name, value = row value)
            reader = csv.DictReader(file, delimiter=',')

            print('Parsing file...')

            rowNumber = 1

            # for each row in CSV file do stuff...
            for row in reader:
                
           		# for each key in the CSV dictionary, strip whitespace and add to variable (also check for all caps [e.g. TITLE vs title])
                if row['title']: # make sure title exists
                    title = row.get('title').strip() or row.get('TITLE').strip() 
                
                if row['author']: # make sure author exists
                    author = row.get('author').strip().decode('utf-8') or row.get('AUTHOR').strip().decode('utf-8') # strip whitespace but also decode to deal with odd characters
                
                contents = row.get('contents').strip().decode('utf-8') or row.get('CONTENTS').strip().decode('utf-8')

                url = row.get('url') or row.get('URL')
                date = row.get('date') or row.get('DATE')
                content_type = row.get('type') or row.get('TYPE')
                language = row.get('language') or row.get('LANGUAGE')
                
                try:

                	# create a document from the CSV dictionary "row" variables we just created
                    payload = {
                        'title': title,
                        'date': date,
                        'author': author,
                        'url': url,
                        'contents': contents,
                        'language': language,
                        'type': content_type
                    }

                    # check if document includes country, state, and city string, if exists add to document payload
                    if 'country' and 'state' and 'city' in row:

                        if not row.get('country') or not row.get('state') or not row.get('city'):
                            print('Row {} missing geolocation.'.format(rowNumber))

                        geolocation = {
                            'id': '{}.{}.{}'.format(row.get('country'), row.get('state'), row.get('city'))
                        }

                        payload['geolocation'] = geolocation

                    # if no country,state,city then try for lat/long, if exists add to document payload
                    elif 'latitude' and 'longitude' in row:

                        if not row.get('latitude') or not row.get('longitude'):
                            print('Row {} missing geolocation.'.format(rowNumber))

                        if row['latitude'] and row['longitude']:

                            geolocation = {
                                'latitude': float(row.get('latitude')),
                                'longitude': float(row.get('longitude'))
                            }

                            payload['geolocation'] = geolocation

                    # if no country,state,city OR lat/long try zipcode, if exists add to document payload
                    elif 'zipcode' in row:

                        if not row.get('zipcode'):
                            print('Row {} missing geolocation.'.format(rowNumber))

                        geolocation = {
                            'zipcode': row.get('zipcode'),
                        }

                        payload['geolocation'] = geolocation

                    # get gender if it exists and add to document payload
                    if 'gender' in row:
                        if row['gender']:
                            gender = row.get('gender')
                        payload['gender'] = gender
                        if not row.get('gender'):
                            print('Row {} missing gender.'.format(rowNumber))

                    # get age if it exists and add to document payload
                    if 'age' in row:
                        if row['age']:
                            age = row.get('age')
                        payload['age'] = int(age)
                        if not row.get('age'):
                            print('Row {} missing age.'.format(rowNumber))


                    # add the document to the list of documents
                    documents.append(payload)

                    # if 1000 documents ready to upload, yield the documents to upload, erase the list of documents and continue on
                    if len(documents) == 1000:
                        yield documents
                        documents[:] = []

                    rowNumber = rowNumber + 1

                except Exception as e:
		    # count number of error documents, not used except for troubleshooting
                    global counter
                    counter += 1
                    pass


    except IOError:

        print('Error: File \'upload.csv\' not found')

    yield documents

def upload():

	# this is a generator, so it takes the yielded documents around line 120 and does things with them

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
