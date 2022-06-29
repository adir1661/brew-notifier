import logging
import json
from collections import namedtuple
from copy import deepcopy
from functools import partial
import pytest

from project.entities import (
    CompanyCompetitor,
    Company,
    CRAWLING_STATUSES,
    ContentItem,
    Webinar,
    CompanyForWebinar,
)
from notifier.notifier import notification_reducer

default_logger = logging.getLogger("default")

notification_reducer_with_logs = partial(
    notification_reducer, options={"log_message": True}
)


@pytest.fixture()
def db():
    with open("./project/db.json") as f:
        data_to_test = json.load(f)
        original_company1 = Company(**data_to_test["company1"])
        original_company2 = Company(**data_to_test["company2"])
        original_content_item1 = ContentItem(
            company=original_company2, **data_to_test["contentItem1"]
        )
        original_webinar = Webinar(**data_to_test["webinar"])

        original_company_competitor = CompanyCompetitor(
            company=original_company1, competitor=original_company2
        )

        company_competitor = deepcopy(original_company_competitor)
        company_competitor.is_deleted = True

        data = dict(
            original_company1=original_company1,
            original_company2=original_company2,
            original_content_item1=original_content_item1,
            original_webinar=original_webinar,
            original_company_competitor=original_company_competitor,
            company_competitor=company_competitor,
        )
        LocalDb = namedtuple("LocalDb", data)

        yield LocalDb(**data)


class TestNotifier:
    def test_company_created(self, db):
        """test company notifier"""

        assert notification_reducer_with_logs(
            entity_obj=None,
            original_entity_obj=db.original_company1,
            entity_type="Company",
        )

    def test_company_deleted(self, db):
        """test company notifier"""
        assert notification_reducer_with_logs(
            entity_obj=db.original_company1,
            original_entity_obj=None,
            entity_type="Company",
        )

    def test_company_crawling_status(self, db):
        """test company notifier"""

        company1 = deepcopy(db.original_company1)
        company1.crawling_status = CRAWLING_STATUSES.TEXT_UPLOADED

        assert notification_reducer_with_logs(
            entity_obj=company1,
            original_entity_obj=db.original_company1,
            entity_type="Company",
        )

    def test_company_competitor_is_deleted_field(self, db):
        """test company competitor notifier is deleted field changed."""

        assert notification_reducer_with_logs(
            entity_obj=db.company_competitor,
            original_entity_obj=db.original_company_competitor,
            entity_type="CompanyCompetitor",
        )

    def test_company_competitor_created(self, db):
        """test company competitor notifier created"""
        assert notification_reducer_with_logs(
            entity_obj=None,
            original_entity_obj=db.original_company_competitor,
            entity_type="CompanyCompetitor",
        )

    def test_company_competitor_deleted(self, db):
        """test company competitor notifier deleted"""
        assert notification_reducer_with_logs(
            entity_obj=db.company_competitor,
            original_entity_obj=None,
            entity_type="CompanyCompetitor",
        )

    def test_content_item_deleted(self, db):
        """test content item competitor notifier deleted"""

        assert notification_reducer_with_logs(
            entity_obj=db.original_content_item1,
            original_entity_obj=None,
            entity_type="ContentItem",
        )

    def test_content_item_created(self, db):
        """test content item competitor notifier"""
        assert notification_reducer_with_logs(
            entity_obj=None,
            original_entity_obj=db.original_content_item1,
            entity_type="ContentItem",
        )

    def test_content_item_is_blacklisted(self, db):
        """test content item competitor notifier is_blacklisted changed"""

        content_item1 = deepcopy(db.original_content_item1)
        content_item1.is_blacklisted = True

        assert notification_reducer_with_logs(
            entity_obj=content_item1,
            original_entity_obj=db.original_content_item1,
            entity_type="ContentItem",
        )

    def test_webinar_is_deleted_field(self, db):
        """test webinar competitor notifier is_deleted changed"""

        webinar = deepcopy(db.original_webinar)
        webinar.is_deleted = True
        assert notification_reducer_with_logs(
            entity_obj=webinar,
            original_entity_obj=db.original_webinar,
            entity_type="Webinar",
        )

    def test_company_for_webinar(self, db):
        """test company for webinar notifier is_deleted field changed"""

        original_company_for_webinar = CompanyForWebinar(
            company=db.original_company2,
            webinar=db.original_webinar,
            is_deleted=False,
            is_blacklisted=False,
        )

        company_for_webinar = deepcopy(original_company_for_webinar)
        company_for_webinar.is_deleted = True

        assert notification_reducer_with_logs(
            entity_obj=company_for_webinar,
            original_entity_obj=original_company_for_webinar,
            entity_type="CompanyForWebinar",
        )
