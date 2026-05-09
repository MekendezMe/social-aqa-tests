from models.auth.responses import TokenResponse


def assert_token_response(token_response: TokenResponse):
    assert token_response.access_token
    assert token_response.refresh_token
    assert token_response.device_id
    assert token_response.access_token != token_response.refresh_token