# -*- coding: utf-8 -*-

from django.core.management import get_commands, load_command_class
from django.core.management.base import handle_default_options

from telnetsrv.green import TelnetHandler, command


commands = {}
for name, app in get_commands().items():
    if not app.startswith('django') and app not in ['djcelery', 'south', 'telnet']:
        try:
            cmd = load_command_class(app, name)
            args = []
            if cmd.option_list:
                for opt in cmd.option_list:
                    args.append(opt)
            else:
                args = [cmd.args]
            commands[name] = {
                'name': name,
                'help': cmd.help,
                'args': args,
                'cmd': cmd
            }
        except (AttributeError, ImportError):
            pass


class DjangoCommandHandler(TelnetHandler):
    """ Django commands handler """

    WELCOME = ""
    PROMPT = '> '

    @command(commands.keys(), hidden=True)
    def command_echo(self, params):
        keys = commands.keys()
        cmd = self.raw_input
        cmd = next(k for k in keys if cmd.startswith(k))
        if cmd:
            argv = ['telnetsrv', cmd] + params
            cmd = commands[cmd]['cmd']
            try:
                parser = cmd.create_parser(argv[0], argv[1])
                options, args = parser.parse_args(argv[2:])
                handle_default_options(options)
                try:
                    cmd.execute(stdout=self, *args, **options.__dict__)
                except Exception as e:
                    self.writeerror(str(e))
                self.write("\n")
            except Exception, e:
                self.writeerror(str(e))
        else:
            self.writeerror("Command error: <<%s>>" % "".join(params))

    def writeerror(self, text):
        '''Write errors in red'''
        TelnetHandler.writeerror(self, "\x1b[91m%s\x1b[0m" % text)

    @command('commands')
    def commands(self, params):
        """ Django commands list
            commands [command name]
        """

        if params:
            cmd = params[0].lower()
            doc = "%s\n" % cmd
            for arg in commands[cmd]['args']:
                doc += "\n\t %s" % (str(arg))
            doc += "\n***********************************"
            self.writeline(doc)
        else:
            self.writeline("Django commands\n")

        keys = self.COMMANDS.keys()
        keys.sort()
        for cmd in keys:
            cmd = cmd.lower()
            if cmd in commands:
                try:
                    self.writeline(u"{name} {help_text}".format(
                        name=cmd,
                        help_text=commands[cmd]['help'],
                    ))
                except (UnicodeEncodeError, UnicodeDecodeError):
                    self.writeline(u"{name} {help_text}".format(
                        name=cmd,
                        help_text='',
                    ))
