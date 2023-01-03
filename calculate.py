def judge(tester_lowest: int, tester_highest: int, song_lowest: int, song_highest: int) -> bool:
    """
    To determine the lowest and highest pitches of the given song is beyond that of the tester.

    Parameters
    ----------
    tester_lowest: int
        The midi integer represent the lowest pitch of the tester.

    tester_highest: int
        The midi integer represent the highest pitch of the tester.

    song_lowest: int
        The midi integer represent the lowest pitch of the song.

    song_highest: int
        The midi integer represent the highest pitch of the song.

    Returns
    -------
    out: bool
        The function returns True if the tester can handle the song. Otherwise, return False.
    """
    if song_lowest < tester_lowest or song_highest > tester_highest:
        return False  # 判斷歌曲最高/低音是否超過Tester的音域，是return 0,or return 1
    else:
        return True


def distance(tester: list, song: list) -> int:
    """
    Calculate the sum of the 1-norm of the five reference pitches.

    Parameters
    ----------
    tester: list
        The list containing the five reference pitches of the tester [low, avg. low, avg., avg high, high]

    song: list
        The list containing the five reference pitches of the song [low, avg. low, avg., avg high, high]

    Returns
    -------
    out: int
        The function returns the sum of the 1-norm of the five reference pitches.

    Raises
    ------
    IndexError
        If the lengths of given tester and song lists are not same.
    """
    if len(tester) != len(song):
        raise IndexError(f"The length of {tester} and {song} are not same. Abort.")
    diff = [abs(x - y) for x, y in zip(tester, song)]
    return sum(diff)
