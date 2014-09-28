git-reviewer
============

Tool for handling e-mail reviews

The purpose of this tool is to simplify review process for open source projects.
It will use an e-mail list for communication. It will support incoming patches by
git push or an e-mail sent to the mailing list. In the former case, the tool itself
will make sure the patches are posted on the mailing list.

The tool is currently written in Python, and while it is intended to be a command
line tool in the first hand, there are plans for providing a user interface as
well.
