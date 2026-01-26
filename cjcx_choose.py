from cjcx import *

if __name__ == "__main__":
    total_credits = sum(float(item['xf']) for item in grade_list)
    print(f"已修总学分：{total_credits}")
    print(f"总绩点：{gpa}")
    print("-" * 30)
    semester_options = sorted(list({(item['year'], item['xq']) for item in grade_list}), reverse=True)
    for i, option in enumerate(semester_options, start=1):
        print(f"{i}. {option[0]}年第{option[1]}学期")
    ch=int(input("选择你想要查询的学期："))
    selected_option = semester_options[ch - 1]
    print("-" * 30)

    def get_grades_by_semester(target_year, target_xq):
        filtered_grades = []
        for item in grade_list:
            if item['year'] == target_year and item['xq'] == target_xq:
                filtered_grades.append(item)
        return filtered_grades

    result = get_grades_by_semester(*selected_option)
    XFC = 0
    table_data = []
    for course in result:
        XFC = XFC + float(course['xf'])
        if course['fslx'] == "百分制":
            jd = 4 - 3 * (100 - float(course['kccj'])) ** 2 / 1600
            table_data.append([course['kcmc'], course['xf'], course['kccj'], f"{jd:.2f}"])
        else:
            table_data.append([course['kcmc'], course['xf'], course['kccj']])
    head = ["课程名称", "学分", "成绩", "绩点"]
    print(tabulate(table_data, headers=head, tablefmt="fancy_grid"))
    print(f"所选学期的总学分：{XFC}")
