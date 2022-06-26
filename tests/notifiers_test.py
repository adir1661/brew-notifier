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
from project.notifier import notification_reducer

default_logger = logging.getLogger("default")

notification_reducer_with_logs = partial(
    notification_reducer, options={"log_message": True}
)


@pytest.fixture()
def db():
    import os

    with open("./project/db.json") as f:
        db = json.load(f)
        original_company1 = Company(**db["company1"])
        original_company2 = Company(**db["company2"])
        original_content_item1 = ContentItem(
            company=original_company2, **db["contentItem1"]
        )
        original_webinar = Webinar(**db["webinar"])

        data = dict(
            original_company1=original_company1,
            original_company2=original_company2,
            original_content_item1=original_content_item1,
            original_webinar=original_webinar,
        )

        default_logger.info("loaded data")

        LocalDb = namedtuple("LocalDb", data)

        yield LocalDb(**data)

    default_logger.info("teardown")


class TestNotifier:
    def test_company(self, db):
        """test company notifier"""
        company1 = deepcopy(db.original_company1)
        company1.crawling_status = CRAWLING_STATUSES.TEXT_UPLOADED
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=None,
                original_entity_obj=db.original_company1,
                entity_type="Company",
            ),
            Company,
        )
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=company1, original_entity_obj=None, entity_type="Company"
            ),
            Company,
        )
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=company1,
                original_entity_obj=db.original_company1,
                entity_type="Company",
            ),
            Company,
        )

    def test_company_competitor(self, db):
        """test company competitor notifier"""

        original_company_competitor = CompanyCompetitor(
            company=db.original_company1, competitor=db.original_company2
        )
        company_competitor = deepcopy(original_company_competitor)
        company_competitor.is_deleted = True
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=company_competitor,
                original_entity_obj=original_company_competitor,
                entity_type="CompanyCompetitor",
            ),
            Company,
        )
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=None,
                original_entity_obj=original_company_competitor,
                entity_type="CompanyCompetitor",
            ),
            Company,
        )
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=company_competitor,
                original_entity_obj=None,
                entity_type="CompanyCompetitor",
            ),
            Company,
        )

    def test_content_item(self, db):
        """test content item competitor notifier"""

        content_item1 = deepcopy(db.original_content_item1)
        content_item1.is_blacklisted = True
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=content_item1,
                original_entity_obj=None,
                entity_type="ContentItem",
            ),
            Company,
        )
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=None,
                original_entity_obj=db.original_content_item1,
                entity_type="ContentItem",
            ),
            Company,
        )
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=content_item1,
                original_entity_obj=db.original_content_item1,
                entity_type="ContentItem",
            ),
            Company,
        )

    def test_webinar(self, db):
        """test webinar competitor notifier"""

        webinar = deepcopy(db.original_webinar)
        webinar.is_deleted = True
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=webinar,
                original_entity_obj=db.original_webinar,
                entity_type="Webinar",
            ),
            Webinar,
        )

    def test_company_for_webinar(self, db):
        """test company for webinar notifier"""

        default_logger.info("--------- company for webinar  test --------")

        original_company_for_webinar = CompanyForWebinar(
            company=db.original_company2,
            webinar=db.original_webinar,
            is_deleted=False,
            is_blacklisted=False,
        )
        company_for_webinar = deepcopy(original_company_for_webinar)
        company_for_webinar.is_deleted = True
        assert isinstance(
            notification_reducer_with_logs(
                entity_obj=company_for_webinar,
                original_entity_obj=original_company_for_webinar,
                entity_type="CompanyForWebinar",
            ),
            Webinar,
        )
