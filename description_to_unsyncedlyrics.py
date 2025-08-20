# -*- coding: utf-8 -*-
# 2025/08/16
# Code mostly "inspired" by the already included tagging extension
# Dependencies:
# * python-mutagen

import logging
import gpodder
from mutagen.id3 import ID3, USLT, ID3NoHeaderError

logger = logging.getLogger(__name__)

_ = gpodder.gettext
__title__ = _("Copy description to unsyncedlyrics")
__description__ = _('Copies the podcast description if it exists to the "unsyncedlyrics" tag.')
__authors__ = "axberu <no@thank.you>"
__category__ = "post-download"


class gPodderExtension:
    def __init__(self, container):
        self.container = container

    def on_episode_downloaded(self, episode):
        desc = episode._text_description
        # desc = f"{episode._text_description}".replace('\\n','\n') # for some rason f-strings only escape \n on prints
        if not desc:
            logger.info("LYRDESC: No description for the episode")
            return

        logger.debug(f"LYRDESC: Got description")

        filename = episode.local_filename(create=False, check_only=True)
        if not filename:
            logger.warning("LYRDESC: Filename not found")
            return

        logger.debug(f"LYRDESC: Opening {filename} as mutagen ID3")
        try:
            audio = ID3(filename)
        except ID3NoHeaderError:
            audio = ID3()

        logger.debug(f"LYRDESC: Adding USLT tag with description")
        audio.delall("USLT")
        audio.add(USLT(text=desc, lang="eng", desc=""))

        logger.debug("LYRDESC: Saving file")
        audio.save(filename)
