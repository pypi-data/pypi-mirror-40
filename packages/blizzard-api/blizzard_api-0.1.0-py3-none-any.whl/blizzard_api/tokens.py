
"""
Blizzard API CLI - Token acquisition utilities.

Vaughn Kottler 01/07/19
"""

# third-party
import requests

def request_client_token(client_id, client_secret):
    """
    Query the battle.net OAuth 2.0 for a client access token.

    See: https://develop.battle.net/documentation/guides/using-oauth/client-credentials-flow

    :param client_id: String, 'Basic' Authentication user-id
    :param client_secret: String, 'Basic' Authentication password
    :returns: JSON result
    :raises: requests.exceptions.HTTPError
    """

    req = requests.post("https://us.battle.net/oauth/token",
                        data={"grant_type": "client_credentials"},
                        auth=(client_id, client_secret))

    # request succeeded, return to user
    if req.status_code == requests.codes.ok:
        return req.json()

    # request failed, raise exception
    req.raise_for_status()
    return None
