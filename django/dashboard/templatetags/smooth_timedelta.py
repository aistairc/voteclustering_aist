from django import template

register = template.Library()


@register.filter()
def smooth_timedelta(timedelta):
    """Convert a datetime.timedelta object into Days, Hours, Minutes, Seconds."""
    secs = timedelta.total_seconds()
    delta_str = ""

    hrs = secs // 3600
    delta_str += "{:02d}:".format(int(hrs))
    secs = secs - hrs*3600

    mins = secs // 60
    delta_str += "{:02d}:".format(int(mins))
    secs = secs - mins*60

    delta_str += "{:02d}".format(int(secs))
    return delta_str
