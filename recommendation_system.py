import calculate
import librosa
import os
import sqlite3


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

    multilist = []  # [ID, diff]
    # Search for whole dataset
    for i in range(1000):
        cursor.execute(f"select * from music where ID={i}")
        data_from_music = cursor.fetchone()
        song_pitch = [data_from_music[x] for x in range(7, 12)]

        if not calculate.judge(user_pitch[0], user_pitch[4], data_from_music[7], data_from_music[11]):
            continue
        multilist.append([data_from_music[0], calculate.distance(user_pitch, song_pitch)])

    multilist.sort(key=lambda s: s[1])

    return_list = []
    for i in range(len(multilist)):
        cursor.execute(f"select * from music where ID={multilist[i][0]}")
        data = cursor.fetchone()
        return_list.append(dict([('Name', data[1]), ('Artist', data[2]), ('Album', data[3]), ('Cover', data[5]), ('URL', data[6]), ('Pitch', [librosa.midi_to_note(data[x]) for x in range(7, 12)])]))

    conn.close()  # close the file
    return return_list
