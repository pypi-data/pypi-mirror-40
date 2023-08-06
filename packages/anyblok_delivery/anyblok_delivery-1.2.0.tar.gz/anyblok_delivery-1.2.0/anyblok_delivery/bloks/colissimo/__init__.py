# This file is a part of the AnyBlok / Delivery project
#
#    Copyright (C) 2018 Franck Bret <franckbret@gmail.com>
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.blok import Blok
from anyblok_delivery.release import version
from logging import getLogger
logger = getLogger(__name__)


class DeliveryColissimoBlok(Blok):
    """Delivery blok
    """
    version = version
    author = "Franck BRET"

    required = ['delivery']

    @classmethod
    def import_declaration_module(cls):
        from . import colissimo # noqa

    @classmethod
    def reload_declaration_module(cls, reload):
        from . import colissimo
        reload(colissimo)
