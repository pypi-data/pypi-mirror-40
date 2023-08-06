import requests

class Device():

    def __init__(self, main_domain, device_host, domain, device_user, device_password, redirect_user, redirect_password):
        self.main_domain = main_domain
        self.device_host = device_host
        self.domain = domain
        self.device_user = device_user
        self.device_password = device_password
        self.redirect_user = redirect_user
        self.redirect_password = redirect_password
        
    def activate(self):

        response = requests.post('http://{0}:81/rest/activate'.format(self.device_host),
                                 data={'main_domain': self.main_domain,
                                       'redirect_email': self.redirect_user,
                                       'redirect_password': self.redirect_password,
                                       'user_domain': self.domain,
                                       'device_username': self.device_user,
                                       'device_password': self.device_password})
        return response
