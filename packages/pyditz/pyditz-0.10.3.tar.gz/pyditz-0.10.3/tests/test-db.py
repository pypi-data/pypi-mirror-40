# -*- coding: utf-8 -*-

"""
Database tests.
"""

import shutil
from filecmp import dircmp
from nose.tools import raises

from ditz.database import DitzDB, DitzError
from ditz.display import *
from ditz.flags import *

desc = u"""
A description cöntaining Unicode
"""


def test_create(name="database"):
    "Test database creation"

    try:
        shutil.rmtree(name)
    except OSError:
        pass

    db = DitzDB("MyProject", path=name, usecache=True, autosave=True)
    print(db)

    db.add_component("default")
    db.add_release('0.1')
    db.add_release('0.2')

    issue = db.add_issue("A title with Unicodé", desc)
    db.add_reference(issue, "file.txt")

    issue = db.add_issue("Critical fix", desc, comment="Really urgent")

    db.set_release(issue, '0.1')
    db.set_release(issue, '0.2')
    db.set_release(issue, None)

    db.add_comment(issue, "Will you make up yöur mind?")

    db.set_status(issue, IN_PROGRESS, comment="Let's do it!")
    db.set_status(issue, PAUSED, comment="Er.. let's think about it")
    db.set_status(issue, CLOSED, WONTFIX, comment="Nah, let's not bother")

    for issue in db:
        print(issue)

    for issuename in db.issue_names:
        print(issuename)

    db.write()

    issue = db.add_issue("Another issue")
    db.write()

    db.drop_issue(issue)
    db.write()

    newdb = DitzDB.read(name, usecache=True)
    assert len(newdb.issues) == 2

    newdb = DitzDB.read(name, usecache=False)
    assert len(newdb.issues) == 2


@raises(DitzError)
def test_nosuchcomp():
    "Test nonexistent component"

    db = DitzDB("MyProject")
    db.add_issue("Issue 1", component='fred')


def test_claim():
    "Test issue claiming"

    db = DitzDB("MyProject")
    issue = db.add_issue("Issue")

    db.claim_issue(issue, claimer="Fred", comment="You're my issue now!")
    assert issue.claimer == "Fred"

    db.claim_issue(issue, claimer="Brian", force=True)
    assert issue.claimer == "Brian"

    db.unclaim_issue(issue, claimer="Fred", force=True)
    assert issue.claimer == None


@raises(DitzError)
def test_claim_fail():
    "Test issue claiming failure"

    db = DitzDB("MyProject")
    issue = db.add_issue("Issue")
    db.claim_issue(issue, claimer="Fred")
    db.claim_issue(issue, claimer="Brian")


@raises(DitzError)
def test_unclaim_fail():
    "Test issue unclaiming failure"

    db = DitzDB("MyProject")
    issue = db.add_issue("Issue")
    db.claim_issue(issue, claimer="Fred")
    db.unclaim_issue(issue, claimer="Brian")


def test_release():
    "Test valid release"

    db = DitzDB("MyProject")
    db.add_release("0.1")
    db.add_issue("Issue 1", release='0.1', status=CLOSED)
    db.release_release("0.1")


@raises(DitzError)
def test_norelease():
    "Test nonexistent release"

    db = DitzDB("MyProject")
    db.add_component("default")
    db.add_issue("Issue 1", release='1.0')


@raises(DitzError)
def test_duprelease():
    "Test duplicate releases"

    db = DitzDB("MyProject")
    db.add_release("0.2")
    db.add_release("0.2")


@raises(DitzError)
def test_invalidrelease_1():
    "Test invalid release (no issues)"

    db = DitzDB("MyProject")
    db.add_release("0.1")
    db.release_release("0.1")


@raises(DitzError)
def test_invalidrelease_2():
    "Test invalid release (issue not closed)"

    db = DitzDB("MyProject")
    db.add_release("0.1")
    db.add_issue("Issue 1", release='0.1')
    db.release_release("0.1")


@raises(DitzError)
def test_invalidrelease_3():
    "Test invalid release (no such release)"

    db = DitzDB("MyProject")
    db.release_release("0.1")


@raises(DitzError)
def test_invalidrelease_4():
    "Test invalid release (already released)"

    db = DitzDB("MyProject")
    db.add_release("0.1")
    db.add_issue("Issue 1", release='0.1', status=CLOSED)
    db.release_release("0.1")
    db.release_release("0.1")


@raises(DitzError)
def test_dupcomponent():
    "Test duplicate components"

    db = DitzDB("MyProject")
    db.add_component("doc")
    db.add_component("doc")


def test_show_todo():
    "Test show todo"

    db = DitzDB("MyProject")
    db.add_release("0.1")
    show_todo(db)
    show_todo(db, "0.1")
    show_todo(db, None, True)


def test_show_changelog():
    "Test show changelog"

    db = DitzDB("MyProject")
    db.add_release("0.1")
    db.add_issue("Issue 1", release='0.1', status=CLOSED)
    db.add_issue("Issue 2", release='0.1', status=CLOSED, type=FEATURE)
    show_changelog(db, "0.1")
    db.release_release("0.1")
    show_changelog(db, "0.1")


def test_archive():
    "Test archiving of releases"

    archive = "example-archive"

    try:
        shutil.rmtree(archive)
    except OSError:
        pass

    db = DitzDB("MyProject")
    db.add_release("0.1")
    db.add_issue("Issue 1", release='0.1', status=CLOSED)
    db.release_release("0.1")
    db.archive_release("0.1", archive)


def test_copy(name="example"):
    "Test database copying and roundtripping"

    db = DitzDB.read(name)
    db.write(name + "-copy")

    def check_files(dcmp):
        for name in dcmp.diff_files:
            if name != '.ditz-cache':
                raise Exception("file '%s' differs" % name)

        for sub_dcmp in list(dcmp.subdirs.values()):
            check_files(sub_dcmp)

    dcmp = dircmp(name, name + "-copy")
    check_files(dcmp)


def test_convert():
    "Test conversion between names and IDs in strings"

    db = DitzDB("MyProject")
    issue = db.add_issue("A bug")

    text = db.convert_to_id("This is issue ID myproject-1")
    assert text == "This is issue ID {issue %s}" % issue.id

    text = db.convert_to_name("This is issue name {issue %s}" % issue.id)
    assert text == "This is issue name myproject-1"

    name = db.issue_name(issue)
    assert name == "myproject-1"

    otherissue = db.get_issue(name)
    assert otherissue == issue
