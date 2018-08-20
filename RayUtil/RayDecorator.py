
def retry_buddy(retry_times=6, default_ret=None):
    def retry(original_function):
        def retry_function(*args, **kwargs):
            retry = 0
            while retry < retry_times:
                try:
                    ret = original_function(*args, **kwargs)
                    return ret
                except Exception:
                    retry += 1
            return default_ret
        return retry_function
    return retry
