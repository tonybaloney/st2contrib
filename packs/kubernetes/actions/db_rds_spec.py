import re
import uuid
import sys

from st2actions.runners.pythonrunner import Action


class DatabaseRdsSpec(Action):
    def run(self, payload, config):
        # take the payload name and replace any non-alphanumerical characters with "-"
        # to create a name for the database
        try:
            db_name = re.sub('[^0-9a-zA-Z]+', '-', payload['name']) + "-" + payload['namespace']
        except:
            sys.exit()
        # Lets get a username generated
        try:
            user_name = self._user_name(uid=payload['uid'])
        except:
            self.logger.info("No name or namespace in payload")
            sys.exit()

        l = dict(self.config['rds'])
        pw = self._id_generator()

        newpayload = {
            'db_name': db_name,
            'user_name': user_name,
            'pw': pw
        }

        # Parse through config.yaml for rds:. If rds.key exists in labels.keys(),
        # use label.value otherwise use default value from config.yaml
        # then add to newpayload dict.
        for i in l.keys():
            if i in payload['labels'].keys():
                key = i
                value = payload['labels'][i]
                newpayload[key] = value
            else:
                key = i
                valuealt = l[i]
                newpayload[key] = valuealt

        return newpayload

    def _user_name(self, uid):
        short_uid = uid[0:7]
        return "db_" + short_uid

    def _id_generator(self):
        return uuid.uuid4().hex