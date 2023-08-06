# spotify-cli-linux
A command line interface to [Spotify](https://www.spotify.com/) on Linux.

This project is inspired by the similar project called [shpotify](https://github.com/hnarayanan/shpotify), which does similar things, but on macOS.

View this project on PyPi at https://pypi.org/project/spotify-cli-linux/.

installation
------------

```
pip install spotify-cli-linux
```

to upgrade to the latest version, type:

```
pip install spotify-cli-linux --upgrade
```

usage
-----

run the following command from your terminal:

```
spotifycli
```

use one of the following parameters:

```
-h, --help        show this help message and exit
--version         shows version number
--status          shows song name and artist
--statusshort     shows status in a short way
--song            shows the song name
--songshort       shows the song name in a short way
--artist          shows artists name
--artistshort     shows artist name in a short way
--album           shows album name
--playbackstatus  shows playback status
--play            plays the song
--pause           pauses the song
--playpause       plays or pauses the song (toggles a state)
--next            plays the next song
--prev            plays the previous song
--volumeup        increases sound volume
--volumedown      decreases sound volume
```

solving problems
----------------

When you've seen the following error:

```
No module named dbus
```

Then try to install `python-dbus`! On Ubuntu you can do it as follows:

```
sudo apt-get install python-dbus
```

If you are using another distro, then try to install `python-dbus` with your package manager.

usage with tmux
---------------

If you want to use this script in your tmux panel, you can check [tmux-plugin-spotify](https://github.com/pwittchen/tmux-plugin-spotify).

code formatting
---------------

Source code should be formatted according to [PEP8](https://www.python.org/dev/peps/pep-0008/) style guides.

Install [autopep8](https://github.com/hhatto/autopep8) and [pycodestyle](https://github.com/PyCQA/pycodestyle) as follows:

```
pip install --upgrade autopep8
pip install --upgrade pycodestyle
```

Then run:

```
make format
```

to verify code formatting, type:

```
make check_format
```

docs
----

to update docs on `gh-pages`, type:

```
make docs
```

to run docs locally, type:
```
git checkout gh-pages
./serve.sh
```

and view page with docs at: 0.0.0.0:8000

releasing
---------

configure your `~/.pypirc` file as follows:

```
[distutils]
index-servers =
    pypi
[pypi]
username:yourusername
password:yourpassword
```

next, install [twine](https://github.com/pypa/twine):

```
pip install twine
```

then, update version in `spotifycli/version.py` and type:

```
make release
```
