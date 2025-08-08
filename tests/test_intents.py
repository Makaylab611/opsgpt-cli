
from opsgpt import parse_intent
def test_map_restart_db():
    assert parse_intent("restart the database") == "restart_database"
def test_map_failed_jobs():
    assert parse_intent("show failed jobs from last night") == "show_failed_jobs_last_night"
