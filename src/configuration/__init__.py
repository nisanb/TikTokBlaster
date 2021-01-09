import os


class Paths:
    root_path = os.path.abspath(os.path.dirname(os.path.basename(__file__)))
    gauth_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "gauth.json"))
    output_path = None
    tmp_path = None


class GoogleConfigurations:
    datastore_requests_kind = "requests"


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Paths.gauth_path
