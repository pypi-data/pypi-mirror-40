# Settings

# License {{{1
# Copyright (C) 2018 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

# Imports {{{1
from .collection import Collection
from .preferences import (
    BORG_SETTINGS,
    CONFIG_DIR,
    CONFIGS_SETTING,
    convert_name_to_option,
    DATE_FILE,
    DEFAULT_CONFIG_SETTING,
    INCLUDE_SETTING,
    INITIAL_SETTINGS_FILE_CONTENTS,
    INITIAL_ROOT_CONFIG_FILE_CONTENTS,
    INITIAL_HOME_CONFIG_FILE_CONTENTS,
    LOCK_FILE,
    LOG_FILE,
    PREV_LOG_FILE,
    PROGRAM_NAME,
    SETTINGS_FILE,
)
from .python import PythonFile
from .utilities import gethostname, getusername, render_path_list
from shlib import cd, getmod, mkdir, mv, rm, Run, to_path, render_command
from inform import (
    Error, codicil, conjoin, done, full_stop, get_informer, indent, is_str,
    narrate, output, warn,
)
from textwrap import dedent
from appdirs import user_config_dir
import arrow
import os


# Utilities {{{1
hostname = gethostname()
username = getusername()

# borg_options_args {{{2
borg_options_args = {
    'borg': 1,
    '--exclude': 1,
    '--encryption': 1,
}
for name, attrs in BORG_SETTINGS.items():
    if 'arg' in attrs and attrs['arg']:
        borg_options_args[convert_name_to_option(name)] = 1


# Settings class {{{1
class Settings:
    # Constructor {{{2
    def __init__(self, name=None, requires_exclusivity=True, options=()):
        self.requires_exclusivity = requires_exclusivity
        self.settings = {}
        self.options = options
        self.read(name)
        self.check()

    # read() {{{2
    def read(self, name=None, path=None):
        """Recursively read configuration files.

        name (str):
            Name of desired configuration. Passed only when reading the top level
            settings file. Default is the default configuration as specified in the
            settings file, or if that is not specified then the first configuration
            given is used.
        path (str):
            Full path to settings file. Should not be given for the top level
            settings file (SETTINGS_FILE in CONFIG_DIR).
        """

        if path:
            settings = PythonFile(path).run()
            parent = path.parent
            includes = Collection(settings.get(INCLUDE_SETTING))
        else:
            # this is generic settings file
            parent = to_path(CONFIG_DIR)
            if not parent.exists():
                # config dir does not exist, create and populate it
                parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                for name, contents in [
                    (SETTINGS_FILE, INITIAL_SETTINGS_FILE_CONTENTS),
                    ('root', INITIAL_ROOT_CONFIG_FILE_CONTENTS),
                    ('home', INITIAL_HOME_CONFIG_FILE_CONTENTS),
                ]:
                    path = parent / name
                    path.write_text(contents)
                output(
                    f'Configuration directory created: {parent!s}.',
                    'Includes example settings files. Edit them to suit your needs.',
                    'Search for and replace any fields delimited with << and >>.',
                    'Delete any configurations you do not need.',
                    'Generally you will use either home or root, but not both.',
                    sep = '\n'
                )
                done()

            path = PythonFile(parent, SETTINGS_FILE)
            settings_filename = path.path
            settings = path.run()

            configs = Collection(settings.get(CONFIGS_SETTING, ''))
            default = settings.get(DEFAULT_CONFIG_SETTING)
            if not name:
                name = default
            if name:
                if name not in configs:
                    raise Error(
                        'unknown configuration.',
                        culprit=(settings_filename, CONFIGS_SETTING, name)
                    )
                config = name
            else:
                if len(configs) > 1:
                    config = configs[0]
                else:
                    raise Error(
                        'no known configurations.',
                        culprit=(settings_filename, CONFIGS_SETTING)
                    )
            settings['config_name'] = config
            self.config_name = config
            includes = Collection(settings.get(INCLUDE_SETTING))
            includes = [config] + list(includes.values())

        if settings.get('passphrase'):
            if getmod(path) & 0o077:
                warn("file permissions are too loose.", culprit=path)
                codicil(f"Recommend running 'chmod 600 {path!s}'.")

        self.settings.update(settings)

        for include in includes:
            path = to_path(parent, include)
            self.read(path=path)

    # check() {{{2
    def check(self):
        # gather the string valued settings together (can be used by resolve)
        self.str_settings = {k:v for k, v in self.settings.items() if is_str(v)}

        # complain about required settings that are missing
        missing = []
        for each in 'repository archive src_dirs'.split():
            if not self.settings.get(each):
                missing.append(each)
        if missing:
            missing = conjoin(missing)
            warn(f'{missing}: no value given.')
            if 'src_dirs' in missing:
                self.settings['src_dirs'] = []

    # resolve {{{2
    def resolve(self, value):
        # escape any double braces
        try:
            value = value.replace('{{', r'\b').replace('}}', r'\e')
        except AttributeError:
            if isinstance(value, int):
                return str(value)
            return value

        try:
            resolved = value.format(
                host_name=hostname, user_name=username, prog_name=PROGRAM_NAME,
                **self.str_settings
            )
        except KeyError as e:
            raise Error('unknown setting.', culprit=e)
        if resolved != value:
            resolved = self.resolve(resolved)

        # restore escaped double braces with single braces
        return resolved.replace(r'\b', '{').replace(r'\e', '}')

    # handle errors {{{2
    def fail(self, *msg, comment=''):
        msg = full_stop(' '.join(str(m) for m in msg))
        try:
            if self.notify:
                Run(
                    ['mail', '-s', f'{PROGRAM_NAME} on {hostname}: {msg}'] + self.notify.split(),
                    stdin=dedent(f'''
                        {msg}
                        {comment}
                        config = {self.config_name}
                        source = {username}@{hostname}:{', '.join(str(d) for d in self.src_dirs)}
                        destination = {self.repository}
                    ''').lstrip(),
                    modes='soeW'
                )
        except Error as e:
            pass
        try:
            if self.notifier:
                Run(
                    self.notifier.format(
                        msg=msg, hostname=hostname,
                        user_name=username, prog_name=PROGRAM_NAME,
                    ),
                    modes='soeW'
                )
        except Error as e:
            pass
        except KeyError as e:
            warn('unknown key.', culprit=(self.settings_file, 'notifier', e))
        raise Error(msg)

    # get resolved value {{{2
    def value(self, name, default=''):
        """Gets fully resolved value of string setting."""
        return self.resolve(self.settings.get(name, default))

    # get resolved values {{{2
    def values(self, name):
        """Iterate though fully resolved values of a collection setting."""
        for value in Collection(self.settings.get(name)):
            yield self.resolve(value)

    def convert_to_options(self, names):
        def convert(name):
            return '--' + name.replace('_', '-')

        names = names.split() if is_str(names) else names
        args = []
        for name in setting_names:
            args.extend([convert(name), settings.value(name)])
        return args

    # borg_options() {{{2
    def borg_options(self, cmd, options):
        # handle special cases first {{{3
        if 'verbose' in options:
            if 'trial-run' in options:
                args = '--debug --dry-run'.split()
            else:
                args = '--debug'.split()
        else:
            if 'trial-run' in options:
                args = '--dry-run'.split()
            else:
                args = ''.split()

        if cmd == 'create':
            if 'verbose' in options:
                args.append('--list')
                if 'trial-run' not in options:
                    args.append('--stats')
            for path in render_path_list(self.values('excludes')):
                args.extend(['--exclude', path])

        if cmd == 'extract':
            if 'verbose' in options:
                args.append('--list')

        if cmd == 'init':
            if self.passphrase or self.avendesora_account:
                encryption = self.encryption if self.encryption else 'repokey'
                args.append(f'--encryption={encryption}')
                if encryption == 'none':
                    warn('passphrase given but not needed as encryption set to none.')
                if encryption in 'keyfile keyfile-blake2'.split():
                    warn(
                        "you should use 'borg export key' to export the",
                        "encryption key, and then keep that key in a safe",
                        "place.  If you loose the key you will loose access to",
                        "your back ups.",
                        wrap=True
                    )
            else:
                encryption = self.encryption if self.encryption else 'none'
                if encryption != 'none':
                    raise Error('passphrase not specified.')
                args.append(f'--encryption={encryption}')

        # add the borg command line options appropriate to this command {{{3
        for name, attrs in BORG_SETTINGS.items():
            if cmd in attrs['cmds'] or 'all' in attrs['cmds']:
                opt = convert_name_to_option(name)
                val = self.settings.get(name)
                if val:
                    if 'arg' in attrs and attrs['arg']:
                        args.extend([opt, str(val)])
                    else:
                        args.extend([opt])
        return args

    # publish_passcode() {{{2
    def publish_passcode(self):
        passcode = self.passphrase
        if not passcode and self.avendesora_account:
            narrate('running avendesora to access passphrase.')
            try:
                from avendesora import PasswordGenerator, PasswordError
                pw = PasswordGenerator()
                account = pw.get_account(self.value('avendesora_account'))
                passcode = str(account.get_value('passcode'))
            except ImportError:
                raise Error(
                    'Avendesora is not available',
                    'you must specify passphrase in settings.',
                    sep = ', '
                )
        if not passcode:
            narrate('no passphrase available, encryption disabled.')
            return {}

        narrate('passphrase is set.')
        return dict(BORG_PASSPHRASE = passcode)

    # run_borg() {{{2
    def run_borg(self, cmd, options=None):
        os.environ.update(self.publish_passcode())
        os.environ['BORG_DISPLAY_PASSPHRASE'] = 'no'
        if self.needs_ssh_agent:
            for ssh_var in 'SSH_AGENT_PID SSH_AUTH_SOCK'.split():
                if ssh_var not in os.environ:
                    warn(
                        'environment variable not found, is ssh-agent running?',
                        culprit=ssh_var
                    )
        narrating = options and ('verbose' in options or 'narrate' in options)
        narrate('running:\n{}'.format(indent(render_command(cmd, borg_options_args))))
        modes = 'soeW' if narrating else 'sOEW'
        return Run(cmd, modes=modes, env=os.environ, log=False)

    # destination() {{{2
    def destination(self, archive=None):
        repository = self.value('repository')
        if archive is True:
            archive = self.value('archive')
        if archive:
            return f'{repository}::{archive}'
        else:
            return repository

    # get attribute {{{2
    def __getattr__(self, name):
        return self.settings.get(name)

    # iterate through settings {{{2
    def __iter__(self):
        for key in sorted(self.settings.keys()):
            yield key, self.settings[key]

    # enter {{{2
    def __enter__(self):
        # resolve src directories
        self.src_dirs = [to_path(self.resolve(d)) for d in self.src_dirs]

        # resolve repository and archive
        self.repository = self.resolve(self.repository)
        self.archive = self.resolve(self.archive)

        # resolve other files and directories
        config_dir = self.resolve(CONFIG_DIR)
        self.config_dir = to_path(config_dir, config_dir)

        logfile = self.resolve(LOG_FILE)
        self.logfile = to_path(config_dir, logfile)

        if 'no-log' not in self.options:
            prev_logfile = self.resolve(PREV_LOG_FILE)
            self.prev_logfile = to_path(config_dir, prev_logfile)
            rm(self.prev_logfile)
            if self.logfile.exists():
                mv(self.logfile, self.prev_logfile)

        date_file = self.resolve(DATE_FILE)
        self.date_file = to_path(config_dir, date_file)

        # perform locking
        lockfile = self.lockfile = to_path(config_dir, self.resolve(LOCK_FILE))
        if self.requires_exclusivity:
            # check for existance of lockfile
            if lockfile.exists():
                raise Error(f'currently running (see {lockfile} for details).')

            # create lockfile
            now = arrow.now()
            pid = os.getpid()
            lockfile.write_text(dedent(f'''
                started = {now!s}
                pid = {pid}
            ''').lstrip())

        # open logfile
        if 'no-log' not in self.options:
            get_informer().set_logfile(self.logfile)

        return self

    # exit {{{2
    def __exit__(self, exc_type, exc_val, exc_tb):
        # delete lockfile
        if self.requires_exclusivity:
            self.lockfile.unlink()

