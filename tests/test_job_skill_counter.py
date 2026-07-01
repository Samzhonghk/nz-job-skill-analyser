from job_skill_counter import count_skill, analyze_skill

def test_count_skill():
    job_description = "We use SQL and PostgreSQL."
    assert count_skill(job_description, "SQL") == 1

def test_count_skill_is_case_insensitive():
    job_description = "python Python PYTHON"
    assert count_skill(job_description, "python") == 3

def test_analyze_skill_returns_correct_counts():
    job_des = "There are python, SQL, cloud"

    skills = ["Python", "SQL", "Java"]
    
    result = analyze_skill(job_des, skills)
    assert result == {
        "Python": 1,
        "SQL": 1,
        "Java": 0
    }
