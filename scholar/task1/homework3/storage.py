import pickle

def load_data():
    try:
        with open('students.pkl','rb') as f:
            classroom=pickle.load(f)
        print('已成功载入存档数据\n')
    except FileNotFoundError:
        from models import Student
        classroom=Student.Classroom()
        print('未找到存档，已创建新班级\n')
    return classroom

def save_data(classroom):
    with open('students.pkl','wb') as f:
        pickle.dump(classroom,f)
    print('数据已保存\n')
