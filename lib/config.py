'''
The MIT License (MIT)
Copyright (c) 2014 Mats Liljegren
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''

import os
import sys
import textwrap
from configobj import ConfigObj, flatten_errors
from validate import Validator, VdtValueError

""" Local imports """
import loglib

log = loglib.getLogger(__name__)

def add_arguments(parser):
    default_config_file = os.path.join(os.path.expanduser('~'), '.git-reviewer')

    parser.add_argument('--config', default=default_config_file, metavar='FILE',
                    help=textwrap.dedent('''\
                        specify an alternative name for configuration FILE
                        default: %(default)s'''))

def read(arg):
    config_spec = '''
    [repository]
    url = string

        [[mailing-list]]
        url = string
        mailbox = string
        user.login = string
        user.password = string
        branch.master = string
    '''.splitlines()

    try:
        cfg = ConfigObj(arg.config, raise_errors = True, file_error = True, encoding = 'UTF8', configspec = config_spec)
       
    except (SyntaxError, IOError) as e:
        log.error(e)
        sys.exit(1)

    validator = Validator()
    validation = cfg.validate(validator, preserve_errors=True)
    validation_error = False
    for (section_list, key, error) in flatten_errors(cfg, validation):
        slist = ':'.join(section_list)
        if error == False:
            if key is None:
                log.error('[{}]: Mandatory section missing'.format(slist))
            else:
                log.error('[{}] {}: Mandatory key missing'.format(slist, key))
        elif key is not None:
            if isinstance(error, VdtValueError):
                log.error('[{}] {}={}: Failed validation: {}, valid value: {}'.format(', '.join(section_list), key, cfg[key], error, validation[key]))
            else:
                log.error('[{}] {}: Failed validation: {}'.format(', '.join(section_list), key, error))
        else:
            log.error('[{}]: Validation failed for unknown reason'.format(slist))
            
        validation_error = True

    if validation_error: sys.exit(1)

    return cfg

