from django.urls import re_path

# from landing.views.adm_callforpapers import callPaperView
from landing.views.adm_committee_category import committeeCategoryView
from landing.views.adm_schedule_conference import scheduleConferenceView
# from landing.views.adm_guideline_type import guidelineTypeView
# from landing.views.adm_important_date import importantDateView
# from landing.views.adm_principalcarrousel import carrouselImageView
# from landing.views.adm_sponsor_category import sponsorCategoryView
# from landing.views.adm_summary import summaryView
# from landing.views.adm_summary_image import summaryImageView
from landing.views.adm_topic_categories import topicCategoryView
from landing.views.view_conference import conferenceView
# from landing.views.view_notificacions import personNotificacionView
from landing.views.view_feesconference import conferenceFeesView

landing_urls = (
    {
        "nombre": "Topic categories",
        "url": 'topic_categories/',
        "vista": topicCategoryView,
    },
    {
        "nombre": "Committee category",
        "url": 'committee_category/',
        "vista": committeeCategoryView,
    },
    {
        "nombre": "Conference",
        "url": 'conference/',
        "vista": conferenceView,
    },
    {
        "nombre": "Conference Fees",
        "url": 'conference_fees/',
        "vista": conferenceFeesView,
    },
    {
        "nombre": "Conference Schedules",
        "url": 'conference_schedule/',
        "vista": scheduleConferenceView,
    },

)

urlpatterns = []

for u in landing_urls:
    urlpatterns.append(re_path(r'^{}$'.format(u["url"]), u["vista"]))
