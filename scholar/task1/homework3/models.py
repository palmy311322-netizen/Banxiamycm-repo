class Student:
    def __init__(self,id='B18010101',name='Zhang San'):
        self.name=name
        self.id=id
        self.grade={}

    def add_subject(self,subject_name='Chinese',subject_grade=0.0):
        self.grade[subject_name]=subject_grade

    def average(self):
        if self.grade=={}:
            print('暂未录入成绩\n')
            return 0.0
        else:
            total=0.0
            for x in self.grade.values():
                total+=x
            return total/len(self.grade)

    def highest_subject(self):
        if self.grade=={}:
            print('暂未录入成绩\n')
            return 0.0
        else:
            max_grade=0.0
            for x in self.grade.values():
                if x>max_grade:
                    max_grade=x
            return max_grade

    def total(self):
        if self.grade=={}:
            print('暂未输入成绩\n')
            return 0.0
        else:
            total=0.0
            for x in self.grade.values():
                total+=x
            return total

    def __str__(self):
        return f"学生信息(姓名：{self.name}  学号：{self.id}  各科成绩：{self.grade})"

    class Classroom:
        def __init__(self):
            self.member={}
            self.num=0

        def add(self,student):
            self.member[student.id]=student
            self.num+=1
            return True

        def find_by_id(self,id):
            if id in self.member:
                return self.member[id]
            else:
                print('该学号不存在\n')
                return None

        def find_by_name(self,name):
            for student in self.member.values():
                if student.name==name:
                    return student
            return None

        def remove(self,student):
            del self.member[student.id]
            self.num-=1

        def update(self,id,name=None,grade=None):
            if id in self.member:
                student=self.member[id]
                if name is not None:
                    student.name=name
                if grade is not None:
                    student.grade=grade
                return True
            else:
                print('该学号不存在\n')
                return False

        def rank(self):
            member_grade=[]
            for student in self.member.values():
                member_grade.append((student,student.total()))
            return self.quick_sort(member_grade)

        def quick_sort(self,member_grade):
            if len(member_grade)<=1:
                return member_grade
            mid=member_grade[len(member_grade)//2]
            left=[]
            mid_list=[]
            right=[]
            for x in member_grade:
                if x[1]>mid[1]:
                    left.append(x)
                elif x[1]<mid[1]:
                    right.append(x)
                else:
                    mid_list.append(x)
            return self.quick_sort(left)+mid_list+self.quick_sort(right)

        def subject_stats(self,subject):
            stats=[]
            max_grade=0.0
            total_grade=0.0
            min_grade=100.0
            number=0
            for student in self.member.values():
                total_grade+=student.grade[subject]
                if student.grade[subject]>max_grade:
                    max_grade=student.grade[subject]
                if student.grade[subject]>=60.0:
                    number+=1
            average_grade=total_grade/len(self.member)
            stats.append(average_grade)
            stats.append(max_grade)
            stats.append(number/len(self.member))
            for student in self.member.values():
                if student.grade[subject]<min_grade:
                    min_grade=student.grade[subject]
            stats.append(min_grade)
            print(f"{subject}科平均分为：{stats[0]}  最高分为：{stats[1]}  最低分为：{stats[3]}  及格率为：{stats[2]}\n")


            