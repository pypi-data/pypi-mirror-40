"""Helper methods to extract versions."""

from subprocess import check_output
import re

def __extract_sortable_tuple(semver_string):
    """Extract a tuple that can be sorted from a valid semver string (including those with + or - annotations)."""

    components = semver_string.replace("-", ".").replace("+", ".").split(".")

    return tuple([int(i) if i.isdigit() else i for i in components])


def extract_tags():
    """Extract tags from git using command line."""

    raw_tags = check_output(["git", "tag"], universal_newlines=True).strip()
    tags = raw_tags.split('\n')

    # Sort based on SemVer.

    return sorted(tags, key=__extract_sortable_tuple)


def extract_versions():
    """Get the versions from the CHANGELOG."""

    regex = re.compile("##.*")  # Match level 2 headers.
    versions = list()

    with open("CHANGELOG.md") as changelog_file:
        for line in changelog_file:
            result = regex.search(line)

            if result:
                versions.append(line[2:].strip())

    return versions
