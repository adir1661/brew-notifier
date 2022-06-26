import unittest
import json
from copy import deepcopy

from project.entities import CompanyCompetitor, Company, CRAWLING_STATUSES, ContentItem, Webinar, CompanyForWebinar
from project.notifier import notification_reducer


def main():
    with open('./db.json') as f:
        db = json.load(f)
        original_company1 = Company(**db['company1'])
        original_company2 = Company(**db['company2'])
        original_content_item1 = ContentItem(company=original_company2, **db['contentItem1'])
        original_webinar = Webinar(**db['webinar'])

    print('---------company test --------')
    company1 = deepcopy(original_company1)
    company1.crawling_status = CRAWLING_STATUSES.TEXT_UPLOADED
    notification_reducer(entity_obj=None, original_entity_obj=original_company1, entity_type="Company")
    notification_reducer(entity_obj=company1, original_entity_obj=None, entity_type="Company")
    notification_reducer(entity_obj=company1, original_entity_obj=original_company1, entity_type="Company")

    print('---------company competitor test --------')

    original_company_competitor = CompanyCompetitor(company=original_company1, competitor=original_company2)
    company_competitor = deepcopy(original_company_competitor)
    company_competitor.is_deleted = True
    notification_reducer(entity_obj=company_competitor, original_entity_obj=original_company_competitor,
                         entity_type='CompanyCompetitor')
    notification_reducer(entity_obj=None, original_entity_obj=original_company_competitor, entity_type='CompanyCompetitor')
    notification_reducer(entity_obj=company_competitor, original_entity_obj=None, entity_type='CompanyCompetitor')

    print('---------content item test --------')

    content_item1 = deepcopy(original_content_item1)
    content_item1.is_blacklisted = True
    notification_reducer(entity_obj=content_item1, original_entity_obj=None, entity_type='ContentItem')
    notification_reducer(entity_obj=None, original_entity_obj=original_content_item1, entity_type='ContentItem')
    notification_reducer(entity_obj=content_item1, original_entity_obj=original_content_item1, entity_type='ContentItem')

    print('---------webinar test --------')

    webinar = deepcopy(original_webinar)
    webinar.is_deleted = True
    notification_reducer(entity_obj=webinar, original_entity_obj=original_webinar, entity_type='Webinar')

    print('--------- company for webinar  test --------')

    original_company_for_webinar = CompanyForWebinar(company=original_company2, webinar=original_webinar, is_deleted=False,
                                                     is_blacklisted=False)
    company_for_webinar = deepcopy(original_company_for_webinar)
    company_for_webinar.is_deleted = True
    notification_reducer(entity_obj=company_for_webinar, original_entity_obj=original_company_for_webinar, entity_type='CompanyForWebinar')


if __name__ == '__main__':
    main()

