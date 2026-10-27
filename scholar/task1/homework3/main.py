from models import Student
from storage import load_data,save_data

def main():
    classroom=load_data()
    while True:
        print('这是HOMEWORK2-学生成绩管理系统')
        print('1. 添加学生')
        print('2. 录入成绩')
        print('3. 按学号查找学生')
        print('4. 按姓名查找学生')
        print('5. 删除学生')
        print('6. 修改学生信息')
        print('7. 按总分排名')
        print('8. 科目成绩统计')
        print('0. 退出系统')
        try:
            choice=input('请输入选项编号：')
            if choice=='1':
                sid=input('请输入学号：')
                sname=input('请输入姓名：')
                student=Student(sid,sname)
                classroom.add(student)
                print(f'已添加学生：{student}\n')

            elif choice=='2':
                sid=input('请输入学号：')
                student=classroom.find_by_id(sid)
                if student is None:
                    continue
                subject=input('请输入科目名：')
                try:
                    grade=float(input('请输入成绩：'))
                except ValueError:
                    print('成绩必须为数字，请重新输入\n')
                    continue
                student.add_subject(subject,grade)
                print(f'已录入 {student.name} 的 {subject} 成绩：{grade}\n')

            elif choice=='3':
                sid=input('请输入学号：')
                student=classroom.find_by_id(sid)
                if student is not None:
                    print(f'{student}\n')

            elif choice=='4':
                sname=input('请输入姓名：')
                student=classroom.find_by_name(sname)
                if student is not None:
                    print(f'{student}\n')
                else:
                    print('未找到该姓名的学生\n')

            elif choice=='5':
                sid=input('请输入要删除的学生学号：')
                try:
                    student=classroom.member[sid]
                    classroom.remove(student)
                    print(f'已删除学号为 {sid} 的学生\n')
                except KeyError:
                    print('该学号不存在，删除失败\n')

            elif choice=='6':
                sid=input('请输入要修改的学生学号：')
                student=classroom.find_by_id(sid)
                if student is None:
                    continue
                print(f'当前信息：{student}')
                new_name=input('请输入新姓名（直接回车跳过）：')
                if new_name!='':
                    classroom.update(sid,name=new_name)
                new_grade_input=input('是否修改成绩？(y/n)：')
                if new_grade_input=='y':
                    subject=input('请输入科目名：')
                    try:
                        grade=float(input('请输入新成绩：'))
                    except ValueError:
                        print('成绩必须为数字，修改取消\n')
                        continue
                    student.add_subject(subject,grade)
                print(f'修改后：{student}\n')

            elif choice=='7':
                if classroom.num==0:
                    print('班级暂无学生\n')
                    continue
                ranked=classroom.rank()
                print('===== 总分排名 =====')
                for i,(student,total) in enumerate(ranked,1):
                    print(f'第{i}名：{student.name}({student.id}) 总分：{total}')
                print()

            elif choice=='8':
                subject=input('请输入要统计的科目名：')
                try:
                    classroom.subject_stats(subject)
                except KeyError:
                    print(f'没有学生录入 {subject} 科目成绩\n')

            elif choice=='0':
                save_data(classroom)
                print('即将退出系统，再见！')
                break

            else:
                print('无效选项，请重新输入\n')

        except Exception as e:
            print(f'操作异常：{e}，请重新输入\n')

if __name__=='__main__':
    main()
