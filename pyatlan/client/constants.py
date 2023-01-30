from pyatlan.utils import ADMIN_URI, API, HTTPMethod, HTTPStatus

ROLE_API = ADMIN_URI + "roles"

# Role APIs
GET_ROLES = API(ROLE_API, HTTPMethod.GET, HTTPStatus.OK)
