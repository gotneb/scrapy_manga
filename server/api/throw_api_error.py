from errors.api_error import ApiError


def throw_api_error(results: any):
    if results:
        message = results["error"]
    else:
        message = "unexpected error"

    raise ApiError(message)