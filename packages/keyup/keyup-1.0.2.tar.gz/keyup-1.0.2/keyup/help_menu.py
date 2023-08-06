"""

Help Menu
    Help menu object containing body of help content.
    For printing with formatting

"""

from keyup.statics import PACKAGE, CONFIG_SCRIPT
from keyup.colors import Colors


PKG_ACCENT = Colors.ORANGE
PARAM_ACCENT = Colors.WHITE


synopsis_cmd = (
    Colors.RESET + PKG_ACCENT + PACKAGE +
    PARAM_ACCENT + ' --profile ' + Colors.RESET + ' [PROFILE] ' +
    PARAM_ACCENT + '--operation ' + Colors.RESET + '[OPERATION]'
    )

url_doc = Colors.URL + 'http://keyup.readthedocs.io' + Colors.RESET
url_sc = Colors.URL + 'https://bitbucket.org/blakeca00/keyup' + Colors.RESET

menu_body = Colors.BOLD + """
  DESCRIPTION""" + Colors.RESET + """
            Automated Access Key Rotation for Amazon Web Services

            Documentation:  """ + url_doc + """
            Source Code:  """ + url_sc + """
    """ + Colors.BOLD + """
  SYNOPSIS""" + Colors.RESET + """

              """ + synopsis_cmd + """

                            -p, --profile    <value>
                            -o, --operation  <value>
                           [-u, --user-name  <value> ]
                           [-a, --auto    ]
                           [-c, --configure ]
                           [-V, --version ]
                           [-d, --debug   ]
                           [-h, --help    ]
    """ + Colors.BOLD + """
  OPTIONS
        -p, --profile""" + Colors.RESET + """ (string) : Profile name of an IAM user from local
            awscli config for which you want to rotate access keys
    """ + Colors.BOLD + """
        -o, --operation""" + Colors.RESET + """ (string): Operation conducted on the access key
        of the IAM user noted by the PROFILE value.

                Valid Operations: {list (default), update}

                    - list       : List keys and key metadata (DEFAULT)
                    - up         : Create and install new keys, delete
                                   deprecated keyset
    """ + Colors.BOLD + """
        -u, --user-name""" + Colors.RESET + """ (string):  the IAM username for which you cond-
            duct key  operations using  the enabled  permissions of the
            profile username provided with the --profile option
    """ + Colors.BOLD + """
        -a, --auto""" + Colors.RESET + """:  Suppress output to stdout when """ + PACKAGE + """ triggered via
            a scheduler such as cron or by other automated means to rot-
            ate keys on a periodic schedule.
    """ + Colors.BOLD + """
        -c, --configure""" + Colors.RESET + """:  Configure parameters to custom values. If the
            local configuration file does not exist, option writes a new
            local configuration file to disk. If file exists, overwrites
            existing configuration with updated values.

              Configure runtime options:  |  Display local config file:
                                          |
                $ """ + PKG_ACCENT + PACKAGE + PARAM_ACCENT + ' --configure' + Colors.RESET + """       |       $ """ + PKG_ACCENT + CONFIG_SCRIPT + PARAM_ACCENT + """
    """ + Colors.BOLD + """
        -d, --debug""" + Colors.RESET + """ :  When True, do  not write  to local awscli config
            file(s).  Instead, write to a temporary location for testing
            the intgrity of the credentials  file format that is written
            to disk.
    """ + Colors.BOLD + """
        -V, --version""" + Colors.RESET + """ : Print package version
    """ + Colors.BOLD + """
        -h, --help""" + Colors.RESET + """ : Show this help message and exit

    """
