"""List of API Enpoints the moco wrapper knows about."""

API_PATH = {
    "presence_getlist":                 "/users/presences",
    "presence_get":                     "/users/presences/{id}",
    "presence_create":                  "/users/presences",
    "presence_update":                  "/users/presences/{id}",
    "presence_touch":                   "/users/presences/touch",
    "presence_delete":                  "/users/presences/{id}",
}
