
def get_credential_class(use_proxy=False, tfa=False): 
    """Return a class representing a credential for the given service, 
    with an attribute repsenting the expected keys. """ 
    # If a proxy, such as Facebook Connect, is being used, we just 
    # # need the service name and the e-mail address. 
    if use_proxy:
        keys = ['service_name', 'email_address'] 
    else:
        # For the purposes of this example, all other services use 
        # username and password. 
        keys = ['username', 'password']
        # If two-factor auth is in play, then we need an authenticator 
        # token also. 
        if tfa:
            keys.append('tfa_token')

    # Return a class with a proper __init__ method which expects 
    # all expected keys.
    class Credential(object):
        expected_keys = set(keys)
        def __init__(self, **kwargs): 
        # Sanity check: Do our keys match
            if self.expected_keys != set(kwargs.keys()): 
                raise ValueError('Keys do not match.')
        # Write the keys to the credential object. 
            for k, v in kwargs.items():
                setattr(self, k, v) 
    return Credential


c = get_credential_class(False,True)
print(c.expected_keys)


