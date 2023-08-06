from datetime import date, timedelta
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta


ADVENT = 'Advent'
CHRISTMAS_DAY = 'Christmas Day'
CHRISTMAS = 'Christmas Season'
EPIPHANY = 'Epiphany'
BAPTISM_OF_THE_LORD = 'Baptism of the Lord'
TRANSFIGURATION = 'Transfiguration Sunday'
ASH_WEDNESDAY = 'Ash Wednesday'
LENT = 'Lent'
MAUNDAY_THURSDAY = 'Maunday Thursday'
GOOD_FRIDAY = 'Good Friday'
HOLY_SATURDAY = 'Holy Saturday'
EASTER_SUNDAY = 'Easter Sunday'
EASTER = 'Easter Season'
PENTECOST = 'Pentecost'
TRINITY_SUNDAY = 'Trinity Sunday'
CHRIST_THE_KING = 'Christ the King'
ORDINARY_TIME = 'Ordinary Time'

WHITE = 'white'
PURPLE = 'purple'
RED = 'red'
GREEN = 'green'
BLACK = 'black'

COLOR_MAP = {
    ADVENT: PURPLE,
    CHRISTMAS_DAY: WHITE,
    CHRISTMAS: WHITE,
    EPIPHANY: WHITE,
    BAPTISM_OF_THE_LORD: WHITE,
    TRANSFIGURATION: WHITE,
    ASH_WEDNESDAY: PURPLE,
    LENT: PURPLE,
    MAUNDAY_THURSDAY: PURPLE,
    GOOD_FRIDAY: BLACK,
    HOLY_SATURDAY: BLACK,
    EASTER_SUNDAY: WHITE,
    EASTER: WHITE,
    PENTECOST: RED,
    TRINITY_SUNDAY: WHITE,
    CHRIST_THE_KING: WHITE,
    ORDINARY_TIME: GREEN
}


class Calendar:
    def __init__(self, year=None):
        if not year:
            year = date.today().year
        self.cal = {}

        e = easter(year)
        c = date(year=year, month=12, day=25)
        ep = date(year=year, month=1, day=6)
        nye = date(year=year, month=12, day=31)
        nyd = date(year=year, month=1, day=1)

        self._add(ADVENT,
                  c-timedelta(days=(21+c.weekday()+1)),
                  c-timedelta(days=1))
        self._add(CHRISTMAS_DAY, c)
        self._add(CHRISTMAS, c+timedelta(days=1), nye)
        self._add(CHRISTMAS, nyd, ep-timedelta(days=1))
        self._add(EPIPHANY, ep)
        self._add(BAPTISM_OF_THE_LORD,
                  ep+timedelta(days=1)+relativedelta(weekday=6))
        self._add(TRANSFIGURATION, e-timedelta(days=49))
        self._add(ASH_WEDNESDAY, e-timedelta(days=46))
        self._add(LENT, e-timedelta(days=45), e-timedelta(days=4))
        self._add(MAUNDAY_THURSDAY, e-timedelta(days=3))
        self._add(GOOD_FRIDAY, e-timedelta(days=2))
        self._add(HOLY_SATURDAY, e-timedelta(days=1))
        self._add(EASTER_SUNDAY, e)
        self._add(EASTER, e+timedelta(days=1), e+timedelta(days=48))
        self._add(PENTECOST, e+timedelta(days=49))
        self._add(TRINITY_SUNDAY, e+timedelta(days=56))
        self._add(CHRIST_THE_KING, c-timedelta(days=(28+c.weekday()+1)))

    def _add(self, name, start, end=None):
        if name not in self.cal:
            self.cal[name] = [{
                'start': start,
                'end': end if end else start
            }]
        else:
            self.cal[name].append({
                'start': start,
                'end': end if end else start
            })

    def lookup(self, d):
        for event in self.cal:
            for edate in self.cal[event]:
                if edate['start'] <= d <= edate['end']:
                    return (event, COLOR_MAP[event])
        return (ORDINARY_TIME, COLOR_MAP[ORDINARY_TIME])


def lookup(d):
    cal = Calendar(d.year)
    return cal.lookup(d)
