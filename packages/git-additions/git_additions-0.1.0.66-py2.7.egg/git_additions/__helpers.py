import pathlib
import time


def find_toplevel(path, last=None):
    path = pathlib.Path(path).absolute()

    if path == last:
        return None
    if (path / '.git').is_dir():
        return path

    return find_toplevel(path.parent, last=path)


def duration(commit1, commit2):
    start = commit1.commit_time
    end = commit2.commit_time

    d = divmod(end - start, 86400)  # days
    h = divmod(d[1], 3600)  # hours
    m = divmod(h[1], 60)  # minutes
    s = m[1]  # seconds

    return d[0], h[0], m[0], s


def commit_date(commit):
    return time.ctime(commit.commit_time)


def normalize_duration(days, hours, minutes, seconds, total):
    minutes += int(seconds / 60)
    seconds = int(seconds % 60)

    hours += int(minutes / 60)
    minutes = int(minutes % 60)

    days += int(hours / 24)
    hours = int(hours % 24)

    if total == 'seconds':
        total_duration = (days * 24 * 60 * 60) + (hours * 60 * 60) + (minutes * 60) + seconds
    elif total == 'minutes':
        total_duration = (days * 24 * 60) + (hours * 60) + minutes + (seconds / 60)
    elif total == 'hours':
        total_duration = (days * 24) + hours + (minutes / 60) + (seconds / (60 * 60))
    elif total == 'days':
        total_duration = days + (hours / 24) + (minutes / (24 * 60)) + (seconds / (24 * 60 * 60))
    else:
        total_duration = None

    return days, hours, minutes, seconds, total_duration
