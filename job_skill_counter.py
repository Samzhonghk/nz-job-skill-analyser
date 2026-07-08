import re
import sys
from pathlib import Path
import argparse

def summurize_skill_counts(list_of_skill_counts: list[dict[str,str|int]])->dict[str, int]:
    result = {}
    for list in list_of_skill_counts:
        skill = list["skill"]
        count = list["count"]

        # result[skill] = 0

        # if skill not in result:
        #     result[skill] = count
        # else:
        #     result[skill] += count
        result[skill] = result.get(skill, 0) + count

    return result

def output_summary_to_csv(output_file: str, file_list: dict[str, int]):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Skill,count\n")
        for skill, count in file_list.items():
            file.write(f"{skill}, {count}\n")
    



def load_skills(file_path: str)-> list[str]:
    skills = []
    with open(file_path, "r", encoding = "utf-8") as files:
        for file in files:
            skill = file.strip()
            skills.append(skill)
    return skills

def parse_agr():
    parse = argparse.ArgumentParser(description="Analyze job description for skills.")
    parse.add_argument("input", help="Path to the job description file or folder containing job description files.")
    parse.add_argument(
        "--output",
        default=None,
        help="Path to the output CSV file. If not provided, defaults to 'skills.csv' for single file or 'skills_summary.csv' for multiple files.",
        
    )

    parse.add_argument(
        "--skills",
        default="skills.txt",
        help="Path to the skills file. Defaults to 'skills.txt'.",
    )
    return parse.parse_args()

def analyze_job_files(folder_path: str, skills: list[str]) -> None:
    result_list = []
    folder = Path(folder_path)
    for files in folder.glob('*.txt'):
        job_desc = files.read_text(encoding = 'utf-8')
        result = analyze_skill(job_desc, skills)
        for skill, count in result.items():
            # print(f'The skill "{skill}" appears {count} times in desc')
            result_list.append(
                    {
                        "file": files.name,
                        "skill": skill,
                        "count": count,
                    }
                )
    return result_list


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

def output_results_to_csv(output_file: str, skills: dict[str, int]):
    with open(output_file, "w", encoding = "utf-8", newline="") as file:
        file.write("Skill,Count\n")
        for skill, count in skills.items():
            file.write(f"{skill}, {count}\n")

def output_multi_files_to_csv(output_file: str, results: list[dict[str, int]])->None:
    with open(output_file, "w", encoding = "utf-8") as file:
        file.write("file,skill,count\n")
        for result in results:
            file.write(f"{result['file']}, {result['skill']}, {result['count']}\n")

def main() -> None:
    
    # if len(sys.argv) < 2:
    #     print("Please provide the path to the job description file as a command-line argument.")
    #     sys.exit(1)

    # input_path =  Path(sys.argv[1])
    arg = parse_agr()

    # skills = load_skills("skills.txt")
    skills = load_skills(arg.skills)

    
    arg_input = Path(arg.input)
    if arg_input.is_dir():
        output_file = arg.output or "skills_summary.csv"
        result = analyze_job_files(str(arg_input), skills)
        output_multi_files_to_csv(output_file, result)
        summary = summurize_skill_counts(result)
        output_summary_to_csv("skills_totals.csv", summary)
        print(f"Skill counts have been wriiten to {output_file}")
        print(f"Skill totals have been written to skills_totals.csv")
        # results = analyze_job_files(sys.argv[1], skills)
        # output_multi_files_to_csv("skills_summary.csv", results)
        # print("Skill counts have been written to skills_summary.csv")
        return
    
    

    # file_path = sys.argv[1]

    try:
        with open(arg_input, "r", encoding = "utf-8") as file:
            job_description = file.read()
    except FileNotFoundError:
        print(f"File not found: {arg_input}")
        sys.exit(1)

    

    skill_counts = analyze_skill(job_description, skills)
    output_results_to_csv("skills.csv", skill_counts)

# for skill, count in skill_counts.items():
#     print(f"The skills '{skill}' appears {count} in the job description.")

    for skill, count in skill_counts.items():
        if count > 0:
            print(f"The skill '{skill}' appears {count} times in the job description.")





    



if __name__ == "__main__":
    main()