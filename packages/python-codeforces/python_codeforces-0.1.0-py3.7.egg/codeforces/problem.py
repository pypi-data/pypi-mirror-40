import os
import urllib.request
import urllib.error
from bs4 import BeautifulSoup

CODEFORCES_URL = "https://codeforces.com"


def get_testcase(contest_id, index, lang='en'):
    """
    Get all testcases for a problem.

    Parameters
    ----------
    contest_id: int
        Id of the contest, containing the problem.
    index: str
        Usually a letter of a letter, followed by a digit, that represent a
        problem index in a contest.

    Returns
    -------
    testcases: iter
        An iteratable of testcases in the form (input, output)
    """

    problem_url = os.path.join(
        CODEFORCES_URL,
        "contest/%d/problem/%s?lang=%s" % (contest_id, index, lang)
    )

    with urllib.request.urlopen(problem_url) as res:
        soup = BeautifulSoup(res.read(), 'html.parser')

    i = [i.pre.string[1:] for i in soup.find_all("div", class_="input")]
    o = [i.pre.string[1:] for i in soup.find_all("div", class_="output")]

    self.testcases = zip(i, o)
