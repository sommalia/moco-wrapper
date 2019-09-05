"""List of API Enpoints the moco wrapper knows about."""

API_PATH = {
    "company_create":           "/companies",
    "company_update":           "/companies/{id}",
    "company_get":              "/companies/{id}",
    "company_getlist":          "/companies",
    "project_getlist":          "/projects",
    "project_get":              "/projects/{id}",
    "project_assigned":         "/projects/assigned",
    "project_create":           "/projects",
    "project_update":           "/projects/{id}",
    "project_archive":          "/projects/{id}/archive",
    "project_unarchive":        "/projects/{id}/unarchive",
    "project_report":           "/projects/{id}/report",
    "project_contract_getlist": "/projects/{project_id}/contracts",
    "project_contract_get":     "/projects/{project_id}/contracts/{contract_id}",
    "project_contract_create":  "/projects/{project_id}/contracts",
    "project_contract_update":  "/projects/{project_id}/contracts/{contract_id}",
    "project_contract_delete":  "/projects/{project_id}/contracts/{contract_id}"
}