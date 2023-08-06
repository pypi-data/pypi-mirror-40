
from alerta.models.alarms import AlarmModel

SEVERITY_MAP = {
    'security': 0,
    'critical': 1,
    'major': 2,
    'minor': 3,
    'warning': 4,
    'normal': 5,
    'ok': 5,
    'cleared': 5,
    'indeterminate': 5,
    'informational': 6,
    'debug': 7,
    'trace': 8,
    'unknown': 9
}
DEFAULT_NORMAL_SEVERITY = 'normal'  # 'normal', 'ok', 'cleared'
DEFAULT_PREVIOUS_SEVERITY = 'indeterminate'
NORMAL_SEVERITY_LEVEL = 5

COLOR_MAP = {
    'severity': {
        'security': 'blue',
        'critical': 'red',
        'major': 'orange',
        'minor': 'yellow',
        'warning': 'dodgerblue',
        'indeterminate': 'lightblue',
        'cleared': '#00CC00',  # lime green
        'normal': '#00CC00',
        'ok': '#00CC00',
        'informational': '#00CC00',
        'debug': '#9D006D',  # purple
        'trace': '#7554BF',  # violet
        'unknown': 'silver'
    },
    'text': 'black',
    'highlight': 'skyblue '
}

OPEN = 'open'
ASSIGN = 'assign'
ACK = 'ack'
SHELVED = 'shelved'
BLACKOUT = 'blackout'
CLOSED = 'closed'
EXPIRED = 'expired'
UNKNOWN = 'unknown'
NOT_VALID = 'notValid'


MORE_SEVERE = 'moreSevere'
NO_CHANGE = 'noChange'
LESS_SEVERE = 'lessSevere'


ACTION_OPEN = 'open'
ACTION_ASSIGN = 'assign'
ACTION_ACK = 'ack'
ACTION_UNACK = 'unack'
ACTION_SHELVE = 'shelve'
ACTION_UNSHELVE = 'unshelve'
ACTION_CLOSE = 'close'

ACTION_ALL = [
    ACTION_OPEN,
    ACTION_ASSIGN,
    ACTION_ACK,
    ACTION_UNACK,
    ACTION_SHELVE,
    ACTION_UNSHELVE,
    ACTION_CLOSE
]


class StateMachine(AlarmModel):

    def register(self, app):
        from alerta.management.views import __version__
        self.name = 'Alerta %s' % __version__

        StateMachine.Severity = app.config['SEVERITY_MAP'] or SEVERITY_MAP
        StateMachine.Colors = app.config['COLOR_MAP'] or COLOR_MAP

        StateMachine.DEFAULT_STATUS = OPEN
        StateMachine.DEFAULT_NORMAL_SEVERITY = app.config['DEFAULT_NORMAL_SEVERITY'] or DEFAULT_NORMAL_SEVERITY
        StateMachine.DEFAULT_PREVIOUS_SEVERITY = app.config['DEFAULT_PREVIOUS_SEVERITY'] or DEFAULT_PREVIOUS_SEVERITY

    def trend(self, previous, current):
        assert previous in StateMachine.Severity, "'%s' is not a valid severity" % previous
        assert current in StateMachine.Severity, "'%s' is not a valid severity" % current

        if StateMachine.Severity[previous] > StateMachine.Severity[current]:
            return MORE_SEVERE
        elif StateMachine.Severity[previous] < StateMachine.Severity[current]:
            return LESS_SEVERE
        else:
            return NO_CHANGE

    def transition(self, previous_severity, current_severity, previous_status=None, current_status=None, action=None, **kwargs):

        assert current_severity in StateMachine.Severity, "'%s' is not a valid severity" % current_severity

        # if an unrecognised action is passed then assume state transition has been handled
        # by a take_action() plugin and return the current severity and status unchanged
        if action and action not in ACTION_ALL:
            return current_severity, current_status

        previous_status = previous_status or StateMachine.DEFAULT_STATUS
        state = current_status = current_status or StateMachine.DEFAULT_STATUS

        print('+' * 40)
        print('state {} prev sev={} curr sev={} prev status={} curr status={} action={} => '.format(
            state,
            previous_severity,
            current_severity,
            previous_status,
            current_status,
            action
        ), end='')

        if state == OPEN:
            if action == ACTION_ACK:
                print('{},{}'.format(current_severity, ACK))
                return current_severity, ACK
            if action == ACTION_SHELVE:
                print('{},{}'.format(current_severity, SHELVED))
                return current_severity, SHELVED
            if action == ACTION_CLOSE:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED

            if StateMachine.Severity[current_severity] == NORMAL_SEVERITY_LEVEL:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED
            if self.trend(previous_severity, current_severity) == MORE_SEVERE:
                print('{},{}'.format(current_severity, OPEN))
                return current_severity, OPEN
            else:
                print('{},{}'.format(current_severity, previous_status))
                return current_severity, previous_status

        if state == ASSIGN:
            pass

        if state == ACK:
            if action in [ACTION_UNACK, ACTION_OPEN]:
                print('{},{}'.format(current_severity, OPEN))
                return current_severity, OPEN
            if action == ACTION_SHELVE:
                print('{},{}'.format(current_severity, SHELVED))
                return current_severity, SHELVED
            if action == ACTION_CLOSE:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED

            if StateMachine.Severity[current_severity] == NORMAL_SEVERITY_LEVEL:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED
            if self.trend(previous_severity, current_severity) == MORE_SEVERE:
                print('{},{}'.format(current_severity, OPEN))
                return current_severity, OPEN
            else:
                print('{},{}'.format(current_severity, ACK))
                return current_severity, ACK

        if state == SHELVED:
            if action == ACTION_OPEN:
                print('{},{}'.format(current_severity, OPEN))
                return current_severity, OPEN
            if action == ACTION_ACK:
                print('{},{}'.format(current_severity, ACK))
                return current_severity, ACK
            if action == ACTION_UNSHELVE:
                print('{},{}'.format(current_severity, previous_status))
                return current_severity, previous_status
            if action == ACTION_CLOSE:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED

            if StateMachine.Severity[current_severity] == NORMAL_SEVERITY_LEVEL:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED
            else:
                print('{},{}'.format(current_severity, SHELVED))
                return current_severity, SHELVED

        if state == BLACKOUT:
            if action == ACTION_OPEN:
                print('{},{}'.format(current_severity, OPEN))
                return current_severity, OPEN
            if action == ACTION_ACK:
                print('{},{}'.format(current_severity, ACK))
                return current_severity, ACK
            if action == ACTION_CLOSE:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED

            if StateMachine.Severity[current_severity] == NORMAL_SEVERITY_LEVEL:
                print('{},{}'.format(StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED))
                return StateMachine.DEFAULT_NORMAL_SEVERITY, CLOSED

        if state == CLOSED:
            if action == ACTION_OPEN:
                print('{},{}'.format(previous_severity, OPEN))
                return previous_severity, OPEN

            if StateMachine.Severity[current_severity] != NORMAL_SEVERITY_LEVEL:
                print('{},{}'.format(previous_severity, OPEN))
                return previous_severity, OPEN

        if state == EXPIRED:
            if StateMachine.Severity[current_severity] != NORMAL_SEVERITY_LEVEL:
                print('{},{}'.format(current_severity, OPEN))
                return current_severity, OPEN

        print('{},{}'.format(current_severity, current_status))
        return current_severity, current_status

    @staticmethod
    def is_suppressed(alert):
        return alert.status == BLACKOUT
