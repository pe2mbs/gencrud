import webapp2.api as API
from webapp2.common.tracking.tracking import RecordTracking


API.recordTracking    = RecordTracking()