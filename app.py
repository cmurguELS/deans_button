from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Function to fetch metrics data from SciVal API for a single author ID
def fetch_metrics(author_id):
    api_key = '7f59af901d2d86f78a1fd60c1bf9426a'  # Replace 'YOUR_API_KEY' with your actual API key
    base_url = 'https://api.elsevier.com/analytics/scival/author/metrics'
    headers = {'X-ELS-APIKey': api_key}
    params = {
        'metricTypes': 'ScholarlyOutput,CitationCount,CitationsPerPublication,FieldWeightedCitationImpact,PublicationsInTopJournalPercentiles',
        'authors': author_id,
        'yearRange': '5yrs',
        'includeSelfCitations': 'true',
        'byYear': 'true',
        'includedDocs': 'AllPublicationTypes',
        'journalImpactType': 'CiteScore',
        'showAsFieldWeighted': 'false',
        'indexType': 'hIndex'
    }
    response = requests.get(base_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_data')
def fetch_data():
    author_ids = request.args.get('author_ids')
    if author_ids:
        author_ids_list = author_ids.split(',')
        data = {}  # Initialize an empty dictionary to store metrics data for each author
        for author_id in author_ids_list:
            metrics_data = fetch_metrics(author_id)
            if metrics_data:
                data[author_id] = metrics_data
            else:
                # Handle case where metrics data couldn't be fetched for an author
                data[author_id] = {'error': 'Metrics data not available'}
        return render_template('data.html', data=data)
    else:
        return 'No author IDs provided'

if __name__ == '__main__':
    app.run(debug=True)
