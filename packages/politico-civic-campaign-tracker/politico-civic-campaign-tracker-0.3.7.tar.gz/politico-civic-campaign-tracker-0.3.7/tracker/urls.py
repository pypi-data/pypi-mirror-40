from django.urls import path, re_path

from .views import (
    CandidateAPI,
    CandidateRatingsAPI,
    EndorsementAPI,
    QuoteAPI,
    RatingsAPI,
    StoryAPI,
    TweetAPI,
    VideoAPI,
)
from .viewsets import (
    PersonList,
    PersonDetail,
    CandidateRatingCategoryList,
    CandidateRatingCategoryDetail,
)


urlpatterns = [
    path("api/people/", PersonList.as_view(), name="tracker_api_person-list"),
    re_path(
        r"^api/people/(?P<pk>.+)/$",
        PersonDetail.as_view(),
        name="tracker_api_person-detail",
    ),
    path(
        "api/categories/",
        CandidateRatingCategoryList.as_view(),
        name="tracker_api_rating-category-list",
    ),
    re_path(
        r"^api/categories/(?P<pk>.+)/$",
        CandidateRatingCategoryDetail.as_view(),
        name="tracker_api_rating-category-detail",
    ),
    path("api/candidates/", CandidateAPI.as_view()),
    path("api/candidate-ratings/", CandidateRatingsAPI.as_view()),
    path("api/endorsements/", EndorsementAPI.as_view()),
    path("api/quotes/", QuoteAPI.as_view()),
    path("api/ratings/", RatingsAPI.as_view()),
    path("api/stories/", StoryAPI.as_view()),
    path("api/tweets/", TweetAPI.as_view()),
    path("api/videos/", VideoAPI.as_view()),
]
