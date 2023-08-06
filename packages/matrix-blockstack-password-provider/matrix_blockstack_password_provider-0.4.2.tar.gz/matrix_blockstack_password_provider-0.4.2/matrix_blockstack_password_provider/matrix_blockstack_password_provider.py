# -*- coding: utf-8 -*-
#
# Blockstack Authentication module for Matrix synapse
# Copyright (C) 2018 Friedger Müffke
#
# Based on  Zjemm/Matrix-Synapse-mysql-password-provider
# Copyright (C) 2018 Eelke Smit
# https://sjemm.net
#
# Based on juju2143/matrix-synapse-smf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


from twisted.internet import defer
import blockstack_zones
import logging
import requests
import traceback
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("synapse.blockstackpwds")


class BlockstackPasswordProvider(object):
    __version__ = "0.4.2"

    def __init__(self, config, account_handler):
        self.account_handler = account_handler
        self.blockstack_node = config.blockstack_node

    @defer.inlineCallbacks
    def checkProfile(self, app, claims):
        # find status for the app domain via profile
        # currently there is no chat profile define
        # therefore, use chat.openintents.org for now.
        oichatBucket = claim["apps"]["https://chat.openintents.org"]
        r = requests.get(oichatBucket+"mxconf.json")

        is_user_app = false
        if r.status_code == requests.codes.ok:
            try:
                mxconf_response = r.json()
                if mxconf_response.get('userapps'):
                    for user_app in mxconf_response['userapps']:
                        if user_app == app:
                            is_user_app = true
            except Exception:
                pass
        defer.returnValue(is_user_app)

    @defer.inlineCallbacks
    def updateProfileFrom(self, claim, blockstack_id, id_address):
        try:
            store = yield self.account_handler.hs.get_profile_handler().store
            name = claim["name"]
            logger.info("User name set to %s", name)
            yield store.set_profile_displayname(id_address, name)
            avatar = claim["image"][0]["contentUrl"]
            logger.info("User avatar set to %s", avatar)
            yield store.set_profile_avatar_url(id_address, avatar)
        except Exception as err:
            logger.warn("failed to update profile (%s)", err)

    @defer.inlineCallbacks
    def check_password(self, user_id, password):
        logger.info("check password")
        if not password:
            logger.debug("no password provided")
            defer.returnValue(False)

        localpart = user_id.split(":", 1)[0][1:]
        id_address = localpart

        pwd_parts = password.split("|") 
        txid = pwd_parts[0]
        app = pwd_parts[1]
        blockstack_id = pwd_parts[2]

        r = requests.get(self.blockstack_node + '/v1/names/' + blockstack_id)
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid blockstack name")
            defer.returnValue(False)
        names_response = r.json()
        
        if (not blockstack_id == localpart) and (not names_response["address"].lower() == id_address):
            logger.debug("id address and localpart do not match")
            defer.returnValue(False)

        z = blockstack_zones.parse_zone_file(names_response["zonefile"])

        r = requests.get(z["uri"][0]["target"])
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid profile url")
            defer.returnValue(False)
        zone_file_response = r.json()
        claim = zone_file_response[0]["decodedToken"]["payload"]["claim"]

        challengeUrl = "http://auth.openintents.org/c/" + txid
        r = requests.get(challengeUrl)
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid txid")
            defer.returnValue(False)
        challenge_text = r.json()["challenge"]
        logger.info("Challenge for user %s: %s", user_id, challenge_text)

        responseUrl = claim["apps"][app] + "mxid.json"
        r = requests.get(responseUrl)
        if not r.status_code == requests.codes.ok:
            logger.debug("invalid mxid.json url")
            defer.returnValue(False)
        mxid_response = r.text
        logger.info("Response for user %s: %s", user_id, mxid_response)

        if mxid_response == challenge_text:
            if (yield self.account_handler.check_user_exists(user_id)):
                logger.info("User %s exists, logging in", localpart)
                self.updateProfileFrom(claim, blockstack_id, localpart)
                defer.returnValue(True)
            else:
                try:
                    user_id, access_token = (yield self.account_handler.register(localpart=localpart))
                    logger.info("User %s created, logging in", localpart)
                    self.updateProfileFrom(claim, blockstack_id, localpart)
                    defer.returnValue(True)
                except Exception as err:
                    logger.warning("User %s not created (%s)",
                                   localpart, err)
                    defer.returnValue(False)
        else:
            logger.warning("Wrong password for user %s", localpart)
            defer.returnValue(False)

    @staticmethod
    def parse_config(config):
        class _BlockstackConfig(object):
            pass
        blockstack_config = _BlockstackConfig()
        blockstack_config.enabled = config.get("enabled", False)
        blockstack_config.blockstack_node = config.get(
            "blockstack_node", "https://core.blockstack.org")
        return blockstack_config

    def cleanup(self):
        pass
