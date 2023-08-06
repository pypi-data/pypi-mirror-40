from .router import Router

def create_listener(box_class, router):
    from .listener import Listener

    class AppListener(Listener):
        pass

    AppListener.box_class = box_class
    AppListener.router = router

    return AppListener