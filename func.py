import logging
from parliament import Context
from unalix import clear_url, unshort_url

def main(context: Context):
    """
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """
    logging.info('function processed a request.')

    req = context.request
    dirty_url = None
    if req.args:
        dirty_url = req.args.get('url')
        if not dirty_url:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                dirty_url = req_body.get('url')

    if dirty_url:
        full_url = unshort_url(dirty_url)
        clean_url = clear_url(full_url)
        retval = f"Original URL: {dirty_url}\nURL with tracking information removed \n{clean_url}"
        code = 200
    else:
        retval = ("This HTTP triggered function executed successfully. " +
                    "Pass a 'url' in the query string or in the request body to clean " +
                    "the input dirty_url.")
        code = 400

    return { "message": retval}, code
