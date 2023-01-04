import functools

import calculate
import librosa
import os
import sqlite3


def _cmp(x, y):  # [ID, diff, [low_pass, high_pass]]
    if not x[2][0] and y[2][0]:
        return 1
    elif x[2][0] and not y[2][0]:
        return -1

    if not x[2][1] and y[2][1]:
        return 1
    elif x[2][1] and not y[2][1]:
        return -1

    if x[1] < y[1]:
        return -1
    elif x[1] > y[1]:
        return 1

    return 0


def recommendation(user_pitch: list, db: str = "./MusicDay.db") -> list:
    """
    This function provides the full recommendation songs using user's pitch.
    Parameters
    ----------
    user_pitch: list
        The list containing the five reference pitches of the tester [low, avg. low, avg., avg high, high]
    db: str
        The location of the SQLite database.
    Returns
    -------
    out: list
        The list contains all recommendations in order.
        The first dictionary is the most recommend song.
        The structure of dictionary is {Name: str, Artist: str, Album: str, Cover: str, URL: str, Pitch: list}.
        The Cover shows the path of the cover image.
        The URL shows the original download source.
        The Pitch shows the list of the five reference pitches of the song [low, avg. low, avg., avg high, high].
        The Judge Result shows if the tester can handle the song. The list contains two booleans [low pass, high pass].
    Raises
    ------
    FileNotFoundError
        If the given path of the database is not exist.
    """
    if not os.path.isfile(db):
        raise FileNotFoundError(f"Error, the database path {db} is not exist. Abort.")

    # Opens a connection to the SQLite database file database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    multilist = []  # [ID, diff, judge result]
    # Search for whole dataset
    for i in range(1000):
        cursor.execute(f"select * from music where ID={i}")
        data_from_music = cursor.fetchone()
        song_pitch = [data_from_music[x] for x in range(7, 12)]

        judge_result = calculate.judge(user_pitch[0], user_pitch[4], data_from_music[7], data_from_music[11])  # Return boolean of list.
        multilist.append([data_from_music[0], calculate.distance(user_pitch, song_pitch), judge_result])

    multilist = sorted(multilist, key=functools.cmp_to_key(_cmp))

    return_list = []
    for i in range(len(multilist)):
        cursor.execute(f"select * from music where ID={multilist[i][0]}")
        data = cursor.fetchone()
        return_list.append(dict([('Name', data[1]), ('Artist', data[2]), ('Album', data[3]), ('Cover', data[5]), ('URL', data[6]), ('Pitch', [librosa.midi_to_note(data[x]) for x in range(7, 12)]), ('Judge Result', multilist[i][2])]))

    conn.close()  # close the file
    return return_list