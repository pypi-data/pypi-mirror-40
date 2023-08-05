
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import OgliError
from .controllers.base import Base

# configuration defaults
CONFIG = init_defaults('ogli')
CONFIG['ogli']['foo'] = 'bar'


class Ogli(App):
    """ogli primary application."""

    class Meta:
        label = 'ogli'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base
        ]


class OgliTest(TestApp,Ogli):
    """A sub-class of Ogli that is better suited for testing."""

    class Meta:
        label = 'ogli'


def main():
    with Ogli() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except OgliError as e:
            print('OgliError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
