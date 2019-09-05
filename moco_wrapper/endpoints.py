"""List of API Enpoints the moco wrapper knows about."""

API_PATH = {
    "company_create":       "/companies",
    "company_update":       "/companies/{id}",
    "company_get":          "/companies/{id}",
    "company_getlist":      "/companies",
    "project_getlist":      "/projects",
    "project_get":          "/projects/{id}",
    "project_assigned":     "/projects/assigned",
    "project_create":       "/projects",
    "project_update":       "/projects/{id}",
    "project_archive":      "/projects/{id}/archive",
    "project_unarchive":    "/projects/{id}/unarchive",
    "project_report":       "/projects/{id}/report"
}