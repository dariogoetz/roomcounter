from typing import Optional
from fastapi import Depends
from fastapi.templating import Jinja2Templates

# from roomcounter.core import config
from roomcounter.models.user import PermissionType
from roomcounter.schemas.user import AuthenticatedUser
from roomcounter.api.dependencies import optional_user

# settings = config.settings()

templates = Jinja2Templates(directory="roomcounter/templates")


# dependencies
def default_template_context(
        user: Optional[AuthenticatedUser] = Depends(optional_user)):
    """Generate default template context required for base template, such as whether the user
    is logged in, whether he is the admin, etc.
    """
    tplcontext = dict()
    tplcontext['global_username'] = ""
    if user is not None:
        tplcontext['global_username'] = user.username
    tplcontext['global_logged_in'] = user is not None

    # annotate some roles
    permissions = user.permissions if user else []
    tplcontext['global_is_admin'] = PermissionType.admin in permissions
    # tplcontext['websocket_url'] = json.dumps(settings.websocket_url)
    return tplcontext