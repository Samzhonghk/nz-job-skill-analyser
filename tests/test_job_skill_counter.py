from job_skill_counter import count_skill, analyze_skill, output_results_to_csv, output_multi_files_to_csv, analyze_job_files, load_skills, summurize_skill_counts, output_summary_to_csv

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

def test_output_results_to_csv(tmp_path):
    skill_counts = {
        "python": 3,
        "SQL": 1,
    }



    output_file = tmp_path / "skills.csv"
    output_results_to_csv(output_file, skill_counts)
    assert output_file.read_text() == "Skill,Count\npython, 3\nSQL, 1\n"

def test_ouput_results_to_csv(tmp_path):
    job_file = tmp_path / "data_engineer.txt"
    job_file.write_text("Python, SQL, PostgreSQL", encoding = "utf-8")
    results = analyze_job_files(str(tmp_path), ["Python", "SQL", "PostgreSQL"])

    assert results == [
        {"file": "data_engineer.txt", "skill": "Python", "count": 1},
        {"file": "data_engineer.txt", "skill": "SQL", "count": 1},
        {"file": "data_engineer.txt", "skill": "PostgreSQL", "count": 1},
    ]

def test_load_files(tmp_path):
    skills_file = tmp_path/"skills.txt"
    skills_file.write_text("Python\nSQL\nPostgreSQL",encoding = "utf-8")
    skills = load_skills(str(skills_file))
    assert skills == ["Python", "SQL", "PostgreSQL"]

def test_summarize_skill_counts():
    skill_counts = [
        {"file": "a.txt", "skill": "Python", "count": 1},
        {"file": "b.txt", "skill": "Python", "count": 2},
        {"file": "a.txt", "skill": "SQL", "count": 1}
    ]

    result = summurize_skill_counts(skill_counts) 
    assert result == {
        "Python": 3,
        "SQL": 1
    }