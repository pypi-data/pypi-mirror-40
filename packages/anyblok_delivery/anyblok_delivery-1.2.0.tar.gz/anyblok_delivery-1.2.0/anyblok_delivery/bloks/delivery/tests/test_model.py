# This file is a part of the AnyBlok / Delivery project
#
#    Copyright (C) 2018 Franck Bret <franckbret@gmail.com>
#    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok.tests.testcase import BlokTestCase
from os import urandom
from uuid import uuid1


class TestDeliveryModel(BlokTestCase):
    """ Test delivery model"""

    def create_sender_address(self):
        address = self.registry.Address.insert(
                first_name="Shipping",
                last_name="services",
                company_name="Acme",
                street1="1 company street",
                zip_code="00000", state="", city="There", country="FRA")
        return address

    def create_recipient_address(self):
        address = self.registry.Address.insert(
                first_name="Jon",
                last_name="Doe",
                street1="1 street",
                street2="crossroad",
                street3="♥",
                zip_code="99999",
                state="A region",
                city="Nowhere",
                country="FRA"
            )
        return address

    def test_credentials(self):
        cred = self.registry.Delivery.Carrier.Credential.insert(
                account_number="test", password="xxx")
        self.assertEqual(cred.account_number, 'test')
        self.assertEqual(cred.password, 'xxx')

    def test_addresses(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()

        self.assertNotEqual(
            sender_address,
            recipient_address
        )
        self.assertEqual(
            self.registry.Address.query().count(),
            2
        )

        self.assertEqual(
            self.registry.Address.query().filter_by(country="FRA").count(),
            2
        )

        self.assertEqual(
            self.registry.Address.query().filter_by(country="USA").count(),
            0
        )

    def create_carrier_service(self):
        ca = self.registry.Delivery.Carrier.insert(
            name="SomeOne", code="SOMEONE")

        ca_cred = self.registry.Delivery.Carrier.Credential.insert(
                    account_number="123",
                    password="password")
        service = self.registry.Delivery.Carrier.Service.insert(
                    name="Livraison à domicile", product_code="DOM",
                    carrier=ca, credential=ca_cred)
        return service

    def test_save_document_new(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        service = self.create_carrier_service()
        shipment = self.registry.Delivery.Shipment.insert(
                service=service, sender_address=sender_address,
                recipient_address=recipient_address)
        self.assertFalse(shipment.document)
        binary_file = urandom(100)
        content_type = 'application/pdf'
        shipment.save_document(binary_file, content_type)
        self.assertTrue(shipment.document)
        self.assertEqual(shipment.document.file, binary_file)
        self.assertEqual(shipment.document.contenttype, content_type)
        self.assertEqual(shipment.document.filesize, len(binary_file))
        self.assertTrue(shipment.document.hash)

    def test_save_document_already_exist(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        service = self.create_carrier_service()
        document = self.registry.Attachment.Document.Latest.insert(
            file=urandom(100)
        )
        shipment = self.registry.Delivery.Shipment.insert(
            service=service, sender_address=sender_address,
            recipient_address=recipient_address,
            document_uuid=document.uuid
        )
        self.assertTrue(shipment.document)
        old_version = document.version
        binary_file = urandom(100)
        content_type = 'application/pdf'
        shipment.save_document(binary_file, content_type)
        self.assertNotEqual(shipment.document.version, old_version)
        self.assertTrue(shipment.document)
        self.assertEqual(shipment.document.file, binary_file)
        self.assertEqual(shipment.document.contenttype, content_type)
        self.assertEqual(shipment.document.filesize, len(binary_file))
        self.assertTrue(shipment.document.hash)

    def test_save_document_unexisting_document(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        service = self.create_carrier_service()
        shipment = self.registry.Delivery.Shipment.insert(
            service=service, sender_address=sender_address,
            recipient_address=recipient_address,
            document_uuid=uuid1()
        )
        self.assertTrue(shipment.document_uuid)
        self.assertFalse(shipment.document)
        binary_file = urandom(100)
        content_type = 'application/pdf'
        shipment.save_document(binary_file, content_type)
        self.assertTrue(shipment.document)
        self.assertEqual(shipment.document.file, binary_file)
        self.assertEqual(shipment.document.contenttype, content_type)
        self.assertEqual(shipment.document.filesize, len(binary_file))
        self.assertTrue(shipment.document.hash)

    def test_service_create_label(self):
        service = self.create_carrier_service()
        with self.assertRaises(Exception):
            service.create_label()

    def test_service_get_labels_status(self):
        service = self.create_carrier_service()
        with self.assertRaises(Exception):
            service.get_label_status()

    def test_shipment_create_label(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        service = self.create_carrier_service()
        shipment = self.registry.Delivery.Shipment.insert(
                service=service, sender_address=sender_address,
                recipient_address=recipient_address)
        shipment.status = 'label'
        self.assertIsNone(shipment.create_label())

    def test_shipment_get_label_status(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        service = self.create_carrier_service()
        shipment = self.registry.Delivery.Shipment.insert(
                service=service, sender_address=sender_address,
                recipient_address=recipient_address)
        self.assertIsNone(shipment.get_label_status())

    def test_shipment_get_labels_status(self):
        sender_address = self.create_sender_address()
        recipient_address = self.create_recipient_address()
        service = self.create_carrier_service()
        self.registry.Delivery.Shipment.insert(
                service=service, sender_address=sender_address,
                recipient_address=recipient_address)
        self.assertIsNone(self.registry.Delivery.Shipment.get_labels_status())
