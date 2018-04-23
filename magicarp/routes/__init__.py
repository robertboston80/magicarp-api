from magicarp import router

from . import common


routing = router.Router()

routing.register_version(None, [
    common.blueprint,
])
