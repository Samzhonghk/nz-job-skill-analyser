import re

with open("sample_job.txt", "r", encoding = "utf-8") as file:
    job_description = file.read()

skills = ["Python", "SQL", "Java", "Docker", "AWS", "PostgreSQL"]


def count_skill(job_description: str, skill: str)-> int:
    pattern = rf"\b{re.escape(skill)}\b"
    matches = re.findall(pattern, job_description, flags=re.IGNORECASE)
    return len(matches)
    # return job_description.lower().count(skill.lower())

def analyze_skill(job_description: str, skills:list[str])-> dict[str, int]:
    result = {}
    for skill in skills:
       result[skill]= count_skill(job_description, skill)
    return result


    
skill_counts = analyze_skill(job_description, skills)

# for skill, count in skill_counts.items():
#     print(f"The skills '{skill}' appears {count} in the job description.")

for skill, count in skill_counts.items():
    if count > 0:
        print(f"The skill '{skill}' appears {count} times in the job description.")