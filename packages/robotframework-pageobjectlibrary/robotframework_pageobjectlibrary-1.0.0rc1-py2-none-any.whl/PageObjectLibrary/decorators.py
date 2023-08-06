def capture_screenshot_on_failure(func):
    """A decorator that takes a screenshot if the decorated function raises an error"""
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
        except:
            self.se2lib.capture_page_screenshot()
            raise
