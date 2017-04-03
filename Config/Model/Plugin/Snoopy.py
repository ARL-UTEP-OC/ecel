import netifaces


class Snoopy:
    def __init__(self, plugin_name):
        self.data = {
            'General': {
                'Plugin Name': {
                    'Value': plugin_name,
                    'Field Type': 'Label'
                },
                'Snoopy Log Path': {
                    "Field Type": "Entry",
                    "Is Path Type": False,
                    "Value": "/var/log/auth.log"
                },
                'Type': {
                    'Values': ['plugin', 'schedulable', 'manual', 'multi', 'custom'],
                    'Selected': 'custom',
                    'Field Type': 'Option'
                },
                'Is Enabled': {
                    'Values': [True, False],
                    'Selected': True,
                    'Field Type': 'Option'
                },
                'Parser': {
                    'Value': 'plugins.parsers.snoopy.snoopy_parser,SnoopyParser',
                    'Is Path Type': True,
                    'Field Type': 'Entry'
                },
                'Auto Restart': {
                    'Values': [True, False],
                    'Selected': False,
                    'Field Type': 'Option'
                },
                'Auto Restart Time Interval': {
                    'Value': '30',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                }
            },
            'Archiving': {
                'File Format': {
                    'Values': ['zip', 'tar'],
                    'Selected': 'zip',
                    'Field Type': 'Option'
                },
                'Archive Time Interval': {
                    'Value': '30',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                }
            }
        }
