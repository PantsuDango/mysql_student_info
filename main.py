import pymysql
import tkinter as tk
import tkinter.messagebox
import sys
import multiprocessing
from preset import mysql_preset,user_write_preset
import pandas


def add(var,cur,db):

    if var.get() == 0:
        tk.messagebox.showwarning(title='error', message='请选择要操作的信息类型！')
    else:
        add_window = tk.Tk()
        add_window.title('新增信息')
        add_window.geometry('300x200')

        if var.get() == 1:
            tk.Label(add_window, text='专业：').place(x=20, y=110, anchor='nw')
            four_Entry = tk.Entry(add_window, width=25)
            four_Entry.place(x=80, y=110, anchor='nw')
            one,two,three = '学号','姓名','性别'
            table = 'students'
        elif var.get() == 2:
            one,two,three = '专业名称','学生数','课程数'
            table = 'majors'
        elif var.get() == 3:
            one,two,three = '课程号','课程名','开课专业'
            table = 'courses'
        elif var.get() == 4:
            one,two,three = '学号','课程号','分数'
            table = 'scores'
        
        tk.Label(add_window, text='%s：'%one).place(x=20, y=20, anchor='nw')
        one_Entry = tk.Entry(add_window, width=25)
        one_Entry.place(x=80, y=20, anchor='nw')

        tk.Label(add_window, text='%s：'%two).place(x=20, y=50, anchor='nw')
        two_Entry = tk.Entry(add_window, width=25)
        two_Entry.place(x=80, y=50, anchor='nw')
    
        tk.Label(add_window, text='%s：'%three).place(x=20, y=80, anchor='nw')
        three_Entry = tk.Entry(add_window, width=25)
        three_Entry.place(x=80, y=80, anchor='nw')
        
        def sure():

            one = one_Entry.get()
            two = two_Entry.get()
            three = three_Entry.get()
            if not one or not two or not three:
                tk.messagebox.showwarning(title='error', message='信息未填写完整！')
            else:
                if var.get() == 1:
                    four = four_Entry.get()
                    if not four:
                        tk.messagebox.showwarning(title='error', message='信息未填写完整！')
                    else:
                        try:
                            cur.execute("insert into %s values('%s','%s','%s','%s');"%(table,one,two,three,four))
                        except pymysql.err.ProgrammingError:
                            tk.messagebox.showwarning(title='error', message='带有特殊字符！')
                        except pymysql.err.OperationalError:
                            tk.messagebox.showwarning(title='error', message='当前用户权限不足！')
                        else:
                            db.commit()
                            tk.messagebox.showinfo(title='success', message='新增成功！')
                else:
                    if var.get() == 4:
                        three = three_Entry.get()
                        try:
                            if int(three) > 100 or int(three) < 0:
                                raise Exception
                        except Exception:
                            tk.messagebox.showwarning(title='error', message='无效的分数！')
                        else:
                            try:
                                cur.execute("insert into %s values('%s','%s','%s');"%(table,one,two,three))
                            except pymysql.err.ProgrammingError:
                                tk.messagebox.showwarning(title='error', message='带有特殊字符！')
                            except pymysql.err.OperationalError:
                                tk.messagebox.showwarning(title='error', message='当前用户权限不足！')
                            else:
                                db.commit()
                                tk.messagebox.showinfo(title='success', message='新增成功！')

                    else:
                        try:
                            cur.execute("insert into %s values('%s','%s','%s');"%(table,one,two,three))
                        except pymysql.err.ProgrammingError:
                            tk.messagebox.showwarning(title='error', message='带有特殊字符！')
                        except pymysql.err.OperationalError:
                                tk.messagebox.showwarning(title='error', message='当前用户权限不足！')
                        else:
                            db.commit()
                            tk.messagebox.showinfo(title='success', message='新增成功！')

        tk.Button(add_window, text="确认", width=7, height=1, command=sure).place(x=80,y=150,anchor='nw')
        tk.Button(add_window, text="取消", width=7, height=1, command=add_window.destroy).place(x=180,y=150,anchor='nw')

        add_window.mainloop()
        

def select(var,cur,lb):

    if var.get() == 0:
        tk.messagebox.showwarning(title='error', message='请选择要操作的信息类型！')
    else:
        lb.delete(0, tk.END)
        if var.get() == 1:
            table = 'students'
        elif var.get() == 2:
            table = 'majors'
        elif var.get() == 3:
            table = 'courses'
        elif var.get() == 4:
            table = 'scores'
        cur.execute('select * from %s;'%table)
        datas = cur.fetchall()
        for data in datas:
            string = '    '.join(data)
            lb.insert('end', string)


def modify(var,cur,db,lb):

    if var.get() == 0:
        tk.messagebox.showwarning(title='error', message='请选择要操作的信息类型！')
    else:
        if var.get() != 4:
            tk.messagebox.showwarning(title='error', message='仅支持修改分数！')
        else:
            try:
                data = lb.get(lb.curselection()[0]).split('    ')
            except IndexError:
                tk.messagebox.showwarning(title='error', message='请选择要修改的对象！')
            else:
                student_id = data[0]
                course_id = data[1]
                score = data[2]
            
                modify_window = tk.Tk()
                modify_window.title('修改成绩')
                modify_window.geometry('250x220')

                tk.Label(modify_window, text='学   号：%s'%student_id).place(x=20, y=20, anchor='nw')
                tk.Label(modify_window, text='课程号：%s'%course_id).place(x=20, y=50, anchor='nw')
                tk.Label(modify_window, text='分   数：%s'%score).place(x=20, y=80, anchor='nw')
                tk.Label(modify_window, text='修改为：').place(x=20, y=110, anchor='nw')
                modify_Entry = tk.Entry(modify_window, width=15)
                modify_Entry.place(x=70, y=110, anchor='nw')

                def modify_score():

                    score = modify_Entry.get()
                    try:
                        if int(score) > 100 or int(score) < 0:
                            raise Exception
                    except Exception:
                        tk.messagebox.showwarning(title='error', message='无效的分数！')
                    else:
                        try:
                            cur.execute('update scores set 分数="%s" where 学号="%s" and 课程号="%s";'%(score,student_id,course_id))
                        except pymysql.err.ProgrammingError:
                            tk.messagebox.showwarning(title='error', message='带有特殊字符！')
                        except pymysql.err.OperationalError:
                            tk.messagebox.showwarning(title='error', message='当前用户权限不足！')
                        else:
                            db.commit()
                            tk.messagebox.showinfo(title='success', message='修改成功！')
                            modify_window.destroy()

                tk.Button(modify_window, text="确认", width=7, height=1, command=modify_score).place(x=20,y=150,anchor='nw')
                tk.Button(modify_window, text="取消", width=7, height=1, command=modify_window.destroy).place(x=120,y=150,anchor='nw')

                modify_window.mainloop()


def delete(var,cur,db,lb):

    if var.get() == 0:
        tk.messagebox.showwarning(title='error', message='请选择要操作的信息类型！')
    else:
        if var.get() == 1:
            table = 'students'
            condition = '学号'
        elif var.get() == 2:
            table = 'majors'
            condition = '专业名称'
        elif var.get() == 3:
            table = 'courses'
            condition = '课程号'
        elif var.get() == 4:
            table = 'scores'
            condition = '学号'

        value = lb.get(lb.curselection()[0]).split('    ')[0]
        try:
            cur.execute('delete from %s where %s="%s";'%(table,condition,value))
        except pymysql.err.OperationalError:
            tk.messagebox.showwarning(title='error', message='当前用户权限不足！')
        else:
            db.commit()
            tk.messagebox.showinfo(title='success', message='删除成功！')


def output_file(var,cur,lb):

    if var.get() == 0:
        tk.messagebox.showwarning(title='error', message='请选择要操作的信息类型！')
    else:
        
        if var.get() == 1:
            table = 'students'
            cur.execute('select * from %s;'%table)
            datas = cur.fetchall()
            
            data1 = []
            data2 = []
            data3 = []
            data4 = []
            for data in datas:
                data1.append(data[0])
                data2.append(data[1])
                data3.append(data[2])
                data4.append(data[3])
            file = pandas.DataFrame({'学号':data1, '姓名':data2, '性别': data3, '专业': data4})
        
        elif var.get() == 2:
            table = 'majors'
            cur.execute('select * from %s;'%table)
            datas = cur.fetchall()
            
            data1 = []
            data2 = []
            data3 = []
            for data in datas:
                data1.append(data[0])
                data2.append(data[1])
                data3.append(data[2])
            file = pandas.DataFrame({'专业名称':data1, '学生数':data2, '课程数': data3})

        elif var.get() == 3:
            table = 'courses'
            cur.execute('select * from %s;'%table)
            datas = cur.fetchall()
            
            data1 = []
            data2 = []
            data3 = []
            for data in datas:
                data1.append(data[0])
                data2.append(data[1])
                data3.append(data[2])
            file = pandas.DataFrame({'课程号':data1, '课程名':data2, '开课专业': data3})
            
        
        elif var.get() == 4:
            table = 'scores'
            cur.execute('select * from %s;'%table)
            datas = cur.fetchall()
            
            data1 = []
            data2 = []
            data3 = []
            for data in datas:
                data1.append(data[0])
                data2.append(data[1])
                data3.append(data[2])
            file = pandas.DataFrame({'学号':data1, '课程号':data2, '分数': data3})

        file.to_excel('%s.xlsx'%table, index=False)
        tk.messagebox.showwarning(title='error', message='导出成功！')


def operation_interface(db,cur,user):

    window = tk.Tk()
    window.title('学生成绩管理系统---登录用户：%s'%user)
    window.geometry('480x400')

    frame1 = tk.Frame(window).pack()
    var = tk.IntVar()
    var.set(0)
    tk.Radiobutton(frame1, text='学生信息', variable=var, value=1,).place(x=50, y=20, anchor='nw')
    tk.Radiobutton(frame1, text='专业信息', variable=var, value=2,).place(x=150, y=20, anchor='nw')
    tk.Radiobutton(frame1, text='课程信息', variable=var, value=3,).place(x=250, y=20, anchor='nw')
    tk.Radiobutton(frame1, text='成绩信息', variable=var, value=4,).place(x=350, y=20, anchor='nw')
    
    # 创建listbox        
    lb=tk.Listbox(window)        
    lb.place(x=50, y=50, width=375, height=250)
    # 创建listbox的滚动条
    scrollbar1 = tk.Scrollbar(lb, command=lb.yview)
    scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
    lb.config(yscrollcommand=scrollbar1.set)

    tk.Button(window, text="查询", width=7, height=1, command=lambda:select(var,cur,lb)).place(x=50, y=315, anchor='nw')
    tk.Button(window, text="新增", width=7, height=1, command=lambda:add(var,cur,db)).place(x=130, y=315, anchor='nw')
    tk.Button(window, text="修改", width=7, height=1, command=lambda:modify(var,cur,db,lb)).place(x=210, y=315, anchor='nw')
    tk.Button(window, text="删除", width=7, height=1, command=lambda:delete(var,cur,db,lb)).place(x=290, y=315, anchor='nw')
    tk.Button(window, text="导出", width=7, height=1, command=lambda:output_file(var,cur,lb)).place(x=370, y=315, anchor='nw')

    window.mainloop()


def log_in(user_Entry,password_Entry,window):

    user = user_Entry.get()
    password = password_Entry.get()
    if not user:
        tk.messagebox.showerror(title='error', message='请输入用户名！')
    elif not password:
        tk.messagebox.showerror(title='error', message='请输入密码！')
    else:
        data = pandas.read_excel('系统用户注册信息.xlsx', sheet_name=0)
        user_names = data['登录名'].values.tolist()
        users = [str(user_name) for user_name in user_names]
        user_passwords = data['密码'].values.tolist()
        passwords = [str(user_password) for user_password in user_passwords]
        
        global failure
        if user not in users:
            tk.messagebox.showerror(title='error', message='用户名不存在！')
            failure += 1
        elif password not in passwords:
            tk.messagebox.showerror(title='error', message='密码错误！')
            failure += 1
        else:
            try:
                db = pymysql.connect(host='localhost', user=user, password=password, charset='UTF8MB4')
            except pymysql.err.OperationalError:
                tk.messagebox.showerror(title='error', message='密码错误！')
                failure += 1
            else:
                cur = db.cursor()
                cur.execute('use Student_info;')
                window.destroy()
                operation_interface(db,cur,user)

        if failure == 3:
            tk.messagebox.showerror(title='error', message='超出错误上限，程序结束！')
            sys.exit()


def set_user(lb, user_Entry, password_Entry, password_Entry_again, register_window):

    user = user_Entry.get()
    password = password_Entry.get()
    password_again = password_Entry_again.get()
    if not user:
        tk.messagebox.showerror(title='error', message='用户名不能为空！')
    elif not password or not password_again:
        tk.messagebox.showerror(title='error', message='密码不能为空！')
    else:
        try:
            user_type = lb.curselection()[0]
        except IndexError:
            tk.messagebox.showwarning(title='error', message='请选择用户类型！')
        else:
            data = pandas.read_excel('系统用户注册信息.xlsx', sheet_name=0)
            user_names = data['登录名'].values.tolist()
            users = [str(user_name) for user_name in user_names]
    
            if password != password_again:
                tk.messagebox.showwarning(title='error', message='两次输入的密码不一致！')
            elif user in users:
                tk.messagebox.showerror(title='error', message='用户名已存在！')
            else:
                db = pymysql.connect(host='localhost', user='root', password='121031', charset='UTF8MB4')
                cur = db.cursor()
                cur.execute('create user "{}"@"localhost" identified by "{}";'.format(user,password))
                if user_type == 0:
                    cur.execute("grant select on Student_info.* to '{}'@'localhost';".format(user))
                    user_type = '学生'
                elif user_type == 1:
                    cur.execute("grant insert on Student_info.scores to '{}'@'localhost';".format(user))
                    cur.execute("grant update on Student_info.scores to '{}'@'localhost';".format(user))
                    user_type = '老师'
                elif user_type == 2:
                    cur.execute("grant all privileges on Student_info.* to '{}'@'localhost';".format(user))
                    user_type = '管理员'
                db.commit()
                cur.close()
                db.close()

                user_types = data['用户类型'].values.tolist()
                types = [str(user_type) for user_type in user_types]
                user_passwords = data['密码'].values.tolist()
                passwords = [str(user_password) for user_password in user_passwords]
                users.append(user)
                types.append(user_type)
                passwords.append(password)
                file = pandas.DataFrame({'登录名':users, '用户类型':types, '密码':passwords})
                title = ['登录名', '用户类型', '密码']
                file.to_excel('系统用户注册信息.xlsx', index=False ,columns=title)

                tk.messagebox.showinfo(title='success', message='账号创建成功！')
                register_window.destroy()


def register():

    register_window = tk.Tk()
    register_window.title('学生成绩管理系统---注册新用户')
    register_window.geometry('300x400')

    tk.Label(register_window, text='用户名：').place(x=25, y=80, anchor='nw')
    user_Entry = tk.Entry(register_window, width=25)
    user_Entry.place(x=80, y=80, anchor='nw')

    tk.Label(register_window, text='密   码：').place(x=25, y=110, anchor='nw')
    password_Entry = tk.Entry(register_window, width=25, show='*')
    password_Entry.place(x=80, y=110, anchor='nw')
    
    tk.Label(register_window, text='密码确认：').place(x=15, y=140, anchor='nw')
    password_Entry_again = tk.Entry(register_window, width=25, show='*')
    password_Entry_again.place(x=80, y=140, anchor='nw')
     
    tk.Label(register_window, text='用户类型：').place(x=15, y=170, anchor='nw')
    lb=tk.Listbox(register_window)        
    lb.place(x=80, y=170, width=100, height=57)
    lb.insert('end', ' 学生')
    lb.insert('end', ' 老师')
    lb.insert('end', ' 管理员')

    tk.Button(register_window, text="确认", width=7, height=1, command=lambda:set_user(lb, user_Entry, password_Entry, password_Entry_again, register_window)).place(x=80, y=250, anchor='nw')
    tk.Button(register_window, text="取消", width=7, height=1, command=register_window.destroy).place(x=180, y=250, anchor='nw')

    register_window.mainloop()


def interface():

    window = tk.Tk()
    window.title('学生成绩管理系统')
    window.geometry('300x400')

    tk.Label(window, text='用户名：').place(x=25, y=80, anchor='nw')
    user_Entry = tk.Entry(window, width=25)
    user_Entry.place(x=80, y=80, anchor='nw')

    tk.Label(window, text='密   码：').place(x=25, y=110, anchor='nw')
    password_Entry = tk.Entry(window, width=25, show='*')
    password_Entry.place(x=80, y=110, anchor='nw')

    tk.Button(window, text="登录", width=7, height=1, command=lambda:log_in(user_Entry,password_Entry, window)).place(x=120, y=150, anchor='nw')
    tk.Button(window, text="注册", width=7, height=1, command=register).place(x=120, y=200, anchor='nw')
    tk.Button(window, text="退出", width=7, height=1, command=sys.exit).place(x=120, y=250, anchor='nw')
        
    window.mainloop()


def main():

    interface()


if __name__ == '__main__':

    failure = 0
    multiprocessing.Process(target=user_write_preset).start()
    multiprocessing.Process(target=mysql_preset).start()
    main()