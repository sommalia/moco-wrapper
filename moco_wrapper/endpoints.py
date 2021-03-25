"""List of API Enpoints the moco wrapper knows about."""

API_PATH = {
    "employment_get":                   "/users/employments/{id}",
    "employment_getlist":               "/users/employments",
    "holiday_getlist":                  "/users/holidays",
    "holiday_get":                      "/users/holidays/{id}",
    "holiday_create":                   "/users/holidays",
    "holiday_update":                   "/users/holidays/{id}",
    "holiday_delete":                   "/users/holidays/{id}",
    "hourly_rate_get":                  "/account/hourly_rates",
    "presence_getlist":                 "/users/presences",
    "presence_get":                     "/users/presences/{id}",
    "presence_create":                  "/users/presences",
    "presence_update":                  "/users/presences/{id}",
    "presence_touch":                   "/users/presences/touch",
    "presence_delete":                  "/users/presences/{id}",
    "unit_get":                         "/units/{id}",
    "unit_getlist":                     "/units"
}
