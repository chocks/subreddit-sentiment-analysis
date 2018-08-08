
import traceback

# ADD config path here:
CONFIG_FILE_PATH = '/home/'


class Config:
    def __init__(self, file_path=None):
        self.config_file = file_path + '.reddit-config' if file_path else CONFIG_FILE_PATH + '.reddit-config'
        self.client_id = None
        self.client_secret = None

        try:
            with open(self.config_file) as config_file_handle:
                for config_property in config_file_handle:
                    configs = config_property.split('=')

                    if configs[0] == 'CLIENT_ID':
                        self.client_id = configs[1].rstrip('\n')
                    elif configs[0] == 'CLIENT_SECRET':
                        self.client_secret = configs[1].rstrip('\n')
        except:
            print 'Cannot load config file'
            traceback.print_exc()

    def get_client_id(self):
        return self.client_id

    def get_client_secret(self):
        return self.client_secret
