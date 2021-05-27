import logging

import azure.functions as func
from unalix import clear_url, unshort_url

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    dirty_url = req.params.get('url')
    if not dirty_url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            dirty_url = req_body.get('url')

#    logging.info(f'URL rcvd: {dirty_url}')
    if dirty_url:
        full_url = unshort_url(dirty_url)
#        logging.info(f'URL expanded: {full_url}')
        clean_url = clear_url(full_url)
#        logging.info(f'URL clean: {clean_url}')
        return func.HttpResponse(f"Original URL: {dirty_url}\nURL with tracking information removed \n{clean_url}")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a 'url' in the query string or in the request body to clean the input dirty_url.",
            status_code=200
        )

