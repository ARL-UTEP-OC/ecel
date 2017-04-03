class Default:
    def __init__(self, plugin_name):
        self.data = {
            'General': {
                'Plugin Name': {
                    'Value': plugin_name,
                    'Field Type': 'Label'
                },
                'Commands': {
                    'Value': '',
                    'Is Path Type': False,
                    'Field Type': 'Entry'
                },
                'Type': {
                    'Values': ['plugin', 'schedulable', 'manual', 'multi', 'custom'],
                    'Selected': 'plugin',
                    'Field Type': 'Option'
                },
                'Is Enabled': {
                    'Values': [True, False],
                    'Selected': True,
                    'Field Type': 'Option'
                },
                'Parser': {
                    'Value': 'plugins/' + plugin_name + '/parser.py',
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
