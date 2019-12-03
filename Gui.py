from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import ImageTk
import PIL
import auto_game
import threading
import sys
import os
import time
import re

root = Tk()
root.title("Auto_aknight")

width, height = 600, 500  # 窗口大小
mouse_coord = [0, 0]  # 初始化鼠标位置
# y居中显示
root.geometry('%dx%d+%d+%d' %
              (width, height, 0, (root.winfo_screenheight() - height) / 2))
# root.overrideredirect(True)
root.resizable(width=False, height=False)
root.config(bg='white')

icon = PIL.Image.open('images/material/icon.ico')
img_icon = ImageTk.PhotoImage(icon)
root.iconphoto(root,img_icon)

style = ttk.Style()
style.map('TButton', background=[('disabled', '#d9d9d9'), ('active', '#FFFFFF')], foreground=[
          ('disabled', '#a3a3a3')], relief=[('pressed', '!disabled', 'sunken')])
# 窗口部件
label = Label(root, text="auto_knight", bg='#FFAEB9', fg='white',
              font=("微软雅黑", 14), anchor=W, justify=LEFT)
label.pack(fill=X, side='top')

def go(n):
    auto_game.__running.set()  # 暂停信号
    text_insert('单任务循环开始\n')
    auto_game.chapter_run(int(n))
    text_insert('单任务循环完成\n')

# 左侧部件
left_frame = Frame(width=500, height=470, bg='#FFE4C4')
left_frame.pack(side='left')
left_top =Frame(left_frame,width=500, height=300, bg='#FFE4C4')
left_top.grid(column=0,row=0,pady=2,padx=26)
label_text = LabelFrame(
    left_top, text='任务列表', bg='#FFE4C4',width=280, height=300)
label_text.grid(column=0,row=0,padx=8)
misson_list = Listbox(label_text, width=32, height=15, bd=2, relief=FLAT,)
misson_list.pack()

label_text1 = LabelFrame(
    left_top, text='单任务模式', bg='#FFE4C4',width=180, height=290)
label_text1.grid(column=1,row=0,padx=18)
sp1 = ttk.Spinbox(label_text1, from_=0, to=99, increment=1, width=2)
sp1.grid(column=0, row=1,pady=20)
sp1.set(0)
def _start():
    times = int(sp1.get())
    if times > 0:
        go(times)
    else:
        messagebox.showinfo(message="请设定循环次数")
        root.lift()
button7=ttk.Button(label_text1, text='开始单任务循环',
           command=lambda: set_a_new_thread(_start))
button7.grid(column=0, row=2,padx=20,pady=50)
button7['state']='disabled'

label_text2 = LabelFrame(
    left_frame, text='调试窗口', bg='#FFE4C4',width=500, height=170)
label_text2.grid(column=0,row=1,pady=6,padx=30)
text2 = scrolledtext.ScrolledText(
    label_text2, width=59, height=10, bd=2, relief=FLAT, wrap=NONE)
text2.pack()
text2.config(state=DISABLED)  # 默认设定为不可gai

'''Y轴scroller，已被替代
scrollbar_y = Scrollbar(text2,command=text2.yview)
scrollbar_y.place(relx=1, rely=0,anchor=NE,relheight=1)
text2.configure(yscrollcommand=scrollbar_y.set)
''X轴scroller，直接增加了宽度
scrollbar_x = Scrollbar(text2,command=text2.xview,orient=HORIZONTAL,)
scrollbar_x.place(relx=0, rely=1,anchor=SW,relwidth=0.98)
text2.configure(xscrollcommand=scrollbar_x.set)
''text2自动滚动好像多此一举了
def modified(event):
    text2.see(END)  # tkinter.END if you use namespaces
text2.bind('<<Modified>>', modified)'''
global misson_sequence  # 初始化任务顺序
misson_sequence = 1


def text_insert(msg):
    text2['state'] = 'normal'
    text2.insert('end', msg)
    text2['state'] = 'disabled'
    text2.see(END)


def connect():
    text_insert('正在尝试连接模拟器...大约需要10s...\n')
    button0_1['state'] = 'disabled'
    os.popen("adb kill-server", "r")
    time.sleep(1)
    f = os.popen("adb connect 127.0.0.1:7555", "r")
    console = f.read()
    f.close()
    text_insert(console)
    if console.find('unable') == -1:
        text_insert('连接成功\n')
        button0_2 = Button(right_frame, text="断开模拟器", command=lambda: set_a_new_thread(
            disconnect), padx=2, relief=GROOVE,bg='#BC8F8F')
        button0_2.place(relx=0.4, rely=0.04, anchor=N)
        button4['state'] = 'normal'
        button7['state'] = 'normal'

    else:
        text_insert('连接失败,请再次尝试\n')
        button0_1['state'] = 'normal'


def disconnect():
    # button0_2['state']='disabled'  noneed
    os.popen("adb kill-server", "r")
    text_insert('已停止adb server\n ')
    button0_1 = Button(right_frame, text="连接模拟器", command=lambda: set_a_new_thread(
        connect), padx=2, relief=GROOVE,bg='#8FBC8F')
    button0_1.place(relx=0.4, rely=0.04, anchor=N)


def _add_mission():

    def chapter_zx():
        zx = Toplevel()
        zx.geometry('1144x610+0+%d' % ((root.winfo_screenheight()-610)/2))
        zx.resizable(width=False, height=False)
        # zx.overrideredirect(1)
        im = PIL.Image.open('images/material/material.png')
        global img
        img = ImageTk.PhotoImage(im)
        mt = Canvas(zx, width=1200, height=610)
        mt.place(x=0, y=0)
        mt.create_image(0, 0, image=img, anchor=NW)
        lf = ttk.LabelFrame(mt, text='ready2add', width=150, height=200)
        lf.place(x=900, y=160)
        st = scrolledtext.ScrolledText(lf, width=20, height=15)
        st.place(x=0, y=0)
        st['state'] = 'disabled'

        b_plus = PIL.Image.open('images/material/plus.png')
        global img_b_plus
        img_b_plus = ImageTk.PhotoImage(b_plus)
        ready2add = {}

        chapter_name = {0: '4-9', 1: '3-2', 2: '4-8', 3: '3-1', 4: 'S4-1', 5: '3-4', 6: '4-4', 7: '3-8', 8: '4-2',
                        9: '4-7', 10: '4-5', 11: '4-10', 12: '5-3', 13: 'S4-6', 14: '2-10', 15: '3-3', 16: '4-6', 17: '5-8', 18: '5-10', 19: '2-4'}

        def ready(_name, times):
            global misson_sequence
            ready2add[misson_sequence] = '[' + \
                str(misson_sequence)+']'+chapter_name[_name]+' ^ '+str(times)
            st['state'] = 'normal'
            st.insert('end', ready2add[misson_sequence]+'\n')
            st['state'] = 'disabled'
            misson_sequence += 1

        spinbox = {}
        button_box = {}  # 字典批量生成19个spinbox和buttom
        xy = [[420, 47], [420, 104], [420, 162], [420, 282], [420, 338], [420, 396], [420, 454], [420, 511], [420, 569], [
            600, 104], [600, 282], [600, 396], [600, 511], [730, 569], [780, 47], [780, 162], [780, 220], [780, 282], [780, 396], [600, 220]]

        def get_spin(i): return ready(i, spinbox[i].get())
        button_box[0] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(0))
        button_box[1] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(1))
        button_box[2] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(2))
        button_box[3] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(3))
        button_box[4] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(4))
        button_box[5] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(5))
        button_box[6] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(6))
        button_box[7] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(7))
        button_box[8] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(8))
        button_box[9] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(9))
        button_box[10] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(10))
        button_box[11] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(11))
        button_box[12] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(12))
        button_box[13] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(13))
        button_box[14] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(14))
        button_box[15] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(15))
        button_box[16] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(16))
        button_box[17] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(17))
        button_box[18] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(18))
        button_box[19] = ttk.Button(
            mt, image=img_b_plus, command=lambda: get_spin(19))
        for i in range(0, 20):
            spinbox[i] = ttk.Spinbox(mt, from_=1, to=99, increment=1, width=2)
            eval('spinbox['+str(i)+'].set(1)')  # 初始化spinbox
            button_box[i].place(x=((xy[i][0])+40), y=(xy[i][1])-4)
            spinbox[i].place(x=xy[i][0], y=xy[i][1])

        def add_comfirm():
            if messagebox.askyesno(message='确定添加关卡吗？', icon='question', title='确认', parent=zx):
                for key in ready2add:
                    misson_list.insert(END, ready2add[key])
                zx.destroy()
                am.destroy()
                root.lift()

        def add_cancel():
            ready2add.clear()
            st['state'] = 'normal'
            st.delete('1.0', 'end')
            st['state'] = 'disabled'
            global misson_sequence
            misson_sequence = 1
            zx.destroy()

        def add_rescind():
            global misson_sequence
            if misson_sequence == 1:
                messagebox.showinfo(message="待添加列表为空")
            else:
                misson_sequence -= 1
                del ready2add[misson_sequence]
                st['state'] = 'normal'
                st.delete('end-2 lines', 'end')
                if misson_sequence != 1:
                    st.insert('end', '\n')
                st['state'] = 'disabled'
        ttk.Button(mt, text='撤销添加', command=add_rescind).place(x=900, y=370)
        ttk.Button(mt, text='√添加完成', command=add_comfirm).place(x=900, y=570)
        ttk.Button(mt, text='×取消并返回上页',
                   command=add_cancel).place(x=1000, y=570)

    def chapter_wz():
        wz = Toplevel()
        wz.geometry('300x370+0+%d' % ((root.winfo_screenheight()-370)/2))
        wz.resizable(width=False, height=False)
        b_plus = PIL.Image.open('images/material/plus.png')
        global img_b_plus
        img_b_plus = ImageTk.PhotoImage(b_plus)
        ready2add = {}
        chapter_name = {0: 'wz-ls-5', 1: 'wz-ca-3', 2: 'wz-ca-5',
                        3: 'wz-ce-5', 4: 'wz-ap-5', 5: 'wz-sk-3', 6: 'wz-sk-5'}

        def ready(_name, times):
            global misson_sequence
            ready2add[misson_sequence] = '[' + \
                str(misson_sequence)+']'+chapter_name[_name]+' ^ '+str(times)
            st['state'] = 'normal'
            st.insert('end', ready2add[misson_sequence]+'\n')
            st['state'] = 'disabled'
            misson_sequence += 1
        label_frame = {}
        spinbox = {}
        button_box = {}
        def get_spin(i): return ready(i, spinbox[i].get())

        label_frame[0] = ttk.LabelFrame(wz, width=150, height=10, text='狗粮本')
        ttk.Label(label_frame[0], text='狗粮5').grid(column=0, row=0)
        spinbox[0] = ttk.Spinbox(
            label_frame[0], from_=1, to=99, increment=1, width=2)
        button_box[0] = ttk.Button(
            label_frame[0], image=img_b_plus, command=lambda: get_spin(0))

        label_frame[1] = ttk.LabelFrame(wz, width=150, height=10, text='技能书本')
        ttk.Label(label_frame[1], text='二级书').grid(column=0, row=0)
        spinbox[1] = ttk.Spinbox(
            label_frame[1], from_=1, to=99, increment=1, width=2)
        button_box[1] = ttk.Button(
            label_frame[1], image=img_b_plus, command=lambda: get_spin(1))
        ttk.Label(label_frame[1], text='三级书').grid(column=0, row=1)
        spinbox[2] = ttk.Spinbox(
            label_frame[1], from_=1, to=99, increment=1, width=2)
        button_box[2] = ttk.Button(
            label_frame[1], image=img_b_plus, command=lambda: get_spin(2))

        label_frame[2] = ttk.LabelFrame(wz, width=150, height=10, text='龙门币本')
        ttk.Label(label_frame[2], text='龙门币5').grid(column=0, row=0)
        spinbox[3] = ttk.Spinbox(
            label_frame[2], from_=1, to=99, increment=1, width=2)
        button_box[3] = ttk.Button(
            label_frame[2], image=img_b_plus, command=lambda: get_spin(3))

        label_frame[3] = ttk.LabelFrame(wz, width=150, height=10, text='红票本')
        ttk.Label(label_frame[3], text='红票5').grid(column=0, row=0)
        spinbox[4] = ttk.Spinbox(
            label_frame[3], from_=1, to=99, increment=1, width=2)
        button_box[4] = ttk.Button(
            label_frame[3], image=img_b_plus, command=lambda: get_spin(4))

        label_frame[4] = ttk.LabelFrame(wz, width=150, height=10, text='碳本')
        ttk.Label(label_frame[4], text='二级碳').grid(column=0, row=0)
        spinbox[5] = ttk.Spinbox(
            label_frame[4], from_=1, to=99, increment=1, width=2)
        button_box[5] = ttk.Button(
            label_frame[4], image=img_b_plus, command=lambda: get_spin(5))
        ttk.Label(label_frame[4], text='三级碳').grid(column=0, row=1)
        spinbox[6] = ttk.Spinbox(
            label_frame[4], from_=1, to=99, increment=1, width=2)
        button_box[6] = ttk.Button(
            label_frame[4], image=img_b_plus, command=lambda: get_spin(6))

        label_frame[0].grid(column=0, row=0)
        label_frame[1].grid(column=0, row=1)
        label_frame[2].grid(column=0, row=2)
        label_frame[3].grid(column=0, row=3)
        label_frame[4].grid(column=0, row=4, rowspan=2)
        spinbox[0].grid(column=1, row=0)
        spinbox[1].grid(column=1, row=0)
        spinbox[2].grid(column=1, row=1)
        spinbox[3].grid(column=1, row=0)
        spinbox[4].grid(column=1, row=0)
        spinbox[5].grid(column=1, row=0)
        spinbox[6].grid(column=1, row=1)
        button_box[0].grid(column=2, row=0)
        button_box[1].grid(column=2, row=0)
        button_box[2].grid(column=2, row=1)
        button_box[3].grid(column=2, row=0)
        button_box[4].grid(column=2, row=0)
        button_box[5].grid(column=2, row=0)
        button_box[6].grid(column=2, row=1)
        spinbox[0].set(1)
        spinbox[1].set(1)
        spinbox[2].set(1)
        spinbox[3].set(1)
        spinbox[4].set(1)
        spinbox[5].set(1)
        spinbox[6].set(1)

        lf = ttk.LabelFrame(wz, text='ready2add', width=150, height=50)
        lf.grid(column=3, row=0, rowspan=3)
        st = scrolledtext.ScrolledText(lf, width=20, height=15)
        st.grid(column=0, row=0)

        def add_comfirm():
            if messagebox.askyesno(message='确定添加关卡吗？', icon='question', title='确认', parent=wz):
                for key in ready2add:
                    misson_list.insert(END, ready2add[key])
                wz.destroy()
                am.destroy()
                root.lift()

        def add_cancel():
            ready2add.clear()
            st['state'] = 'normal'
            st.delete('1.0', 'end')
            st['state'] = 'disabled'
            global misson_sequence

            misson_sequence = 1
            wz.destroy()

        def add_rescind():
            global misson_sequence
            if misson_sequence == 1:
                messagebox.showinfo(message="待添加列表为空")
            else:
                misson_sequence -= 1
                del ready2add[misson_sequence]
                st['state'] = 'normal'
                st.delete('end-2 lines', 'end')
                if misson_sequence != 1:
                    st.insert('end', '\n')
                st['state'] = 'disabled'
        ttk.Button(wz, text='撤销添加', command=add_rescind).grid(column=3, row=3)
        ttk.Button(wz, text='√添加完成', command=add_comfirm).grid(column=3, row=4)
        ttk.Button(wz, text='×取消并返回上页',
                   command=add_cancel).grid(column=3, row=5)

    def chapter_pr():
        pr = Toplevel()
        pr.geometry('470x180+0+%d' % ((root.winfo_screenheight()-180)/2))
        pr.resizable(width=False, height=False)
        b_plus = PIL.Image.open('images/material/plus.png')
        global img_b_plus
        img_b_plus = ImageTk.PhotoImage(b_plus)
        ready2add = {}
        chapter_name = {0: 'pr-a-1', 1: 'pr-a-2', 2: 'pr-b-1',
                        3: 'pr-b-2', 4: 'pr-c-1', 5: 'pr-c-2', 6: 'pr-d-1', 7: 'pr-d-2'}

        def ready(_name, times):
            global misson_sequence
            ready2add[misson_sequence] = '[' + \
                str(misson_sequence)+']'+chapter_name[_name]+' ^ '+str(times)
            st['state'] = 'normal'
            st.insert('end', ready2add[misson_sequence]+'\n')
            st['state'] = 'disabled'
            misson_sequence += 1
        label_frame = {}
        spinbox = {}
        button_box = {}
        def get_spin(i): return ready(i, spinbox[i].get())

        label_frame[0] = ttk.LabelFrame(pr, width=150, height=10, text='医疗重装')
        ttk.Label(label_frame[0], text='蓝色').grid(column=0, row=0)
        spinbox[0] = ttk.Spinbox(
            label_frame[0], from_=1, to=99, increment=1, width=2)
        button_box[0] = ttk.Button(
            label_frame[0], image=img_b_plus, command=lambda: get_spin(0))
        ttk.Label(label_frame[0], text='紫色').grid(column=0, row=1)
        spinbox[1] = ttk.Spinbox(
            label_frame[0], from_=1, to=99, increment=1, width=2)
        button_box[1] = ttk.Button(
            label_frame[0], image=img_b_plus, command=lambda: get_spin(1))

        label_frame[1] = ttk.LabelFrame(pr, width=150, height=10, text='术士狙击')
        ttk.Label(label_frame[1], text='蓝色').grid(column=0, row=0)
        spinbox[2] = ttk.Spinbox(
            label_frame[1], from_=1, to=99, increment=1, width=2)
        button_box[2] = ttk.Button(
            label_frame[1], image=img_b_plus, command=lambda: get_spin(2))
        ttk.Label(label_frame[1], text='紫色').grid(column=0, row=1)
        spinbox[3] = ttk.Spinbox(
            label_frame[1], from_=1, to=99, increment=1, width=2)
        button_box[3] = ttk.Button(
            label_frame[1], image=img_b_plus, command=lambda: get_spin(3))

        label_frame[2] = ttk.LabelFrame(pr, width=150, height=10, text='辅助先锋')
        ttk.Label(label_frame[2], text='蓝色').grid(column=0, row=0)
        spinbox[4] = ttk.Spinbox(
            label_frame[2], from_=1, to=99, increment=1, width=2)
        button_box[4] = ttk.Button(
            label_frame[2], image=img_b_plus, command=lambda: get_spin(4))
        ttk.Label(label_frame[2], text='紫色').grid(column=0, row=1)
        spinbox[5] = ttk.Spinbox(
            label_frame[2], from_=1, to=99, increment=1, width=2)
        button_box[5] = ttk.Button(
            label_frame[2], image=img_b_plus, command=lambda: get_spin(5))

        label_frame[3] = ttk.LabelFrame(pr, width=150, height=10, text='特种近卫')
        ttk.Label(label_frame[3], text='蓝色').grid(column=0, row=0)
        spinbox[6] = ttk.Spinbox(
            label_frame[3], from_=1, to=99, increment=1, width=2)
        button_box[6] = ttk.Button(
            label_frame[3], image=img_b_plus, command=lambda: get_spin(6))
        ttk.Label(label_frame[3], text='紫色').grid(column=0, row=1)
        spinbox[7] = ttk.Spinbox(
            label_frame[3], from_=1, to=99, increment=1, width=2)
        button_box[7] = ttk.Button(
            label_frame[3], image=img_b_plus, command=lambda: get_spin(7))

        label_frame[0].grid(column=0, row=0)
        label_frame[1].grid(column=0, row=1, rowspan=2)
        label_frame[2].grid(column=1, row=0)
        label_frame[3].grid(column=1, row=1, rowspan=2)
        spinbox[0].grid(column=1, row=0)
        spinbox[1].grid(column=1, row=1)
        spinbox[2].grid(column=1, row=0)
        spinbox[3].grid(column=1, row=1)
        spinbox[4].grid(column=1, row=0)
        spinbox[5].grid(column=1, row=1)
        spinbox[6].grid(column=1, row=0)
        spinbox[7].grid(column=1, row=1)
        button_box[0].grid(column=2, row=0)
        button_box[1].grid(column=2, row=1)
        button_box[2].grid(column=2, row=0)
        button_box[3].grid(column=2, row=1)
        button_box[4].grid(column=2, row=0)
        button_box[5].grid(column=2, row=1)
        button_box[6].grid(column=2, row=0)
        button_box[7].grid(column=2, row=1)
        spinbox[0].set(1)
        spinbox[1].set(1)
        spinbox[2].set(1)
        spinbox[3].set(1)
        spinbox[4].set(1)
        spinbox[5].set(1)
        spinbox[6].set(1)
        spinbox[7].set(1)

        lf = ttk.LabelFrame(pr, text='ready2add', width=150, height=50)
        lf.grid(column=3, row=0, rowspan=3)
        st = scrolledtext.ScrolledText(lf, width=20, height=10)
        st.grid(column=0, row=0)

        def add_comfirm():
            if messagebox.askyesno(message='确定添加关卡吗？', icon='question', title='确认', parent=pr):
                for key in ready2add:
                    misson_list.insert(END, ready2add[key])
                pr.destroy()
                am.destroy()
                root.lift()

        def add_cancel():
            ready2add.clear()
            st['state'] = 'normal'
            st.delete('1.0', 'end')
            st['state'] = 'disabled'
            global misson_sequence
            misson_sequence = 1
            pr.destroy()

        def add_rescind():
            global misson_sequence
            if misson_sequence == 1:
                messagebox.showinfo(message="待添加列表为空")
            else:
                misson_sequence -= 1
                del ready2add[misson_sequence]
                st['state'] = 'normal'
                st.delete('end-2 lines', 'end')
                if misson_sequence != 1:
                    st.insert('end', '\n')
                st['state'] = 'disabled'
        ttk.Button(pr, text='撤销添加', command=add_rescind).grid(column=4, row=0)
        ttk.Button(pr, text='√添加完成', command=add_comfirm).grid(column=4, row=1)
        ttk.Button(pr, text='×取消并返回上页',
                   command=add_cancel).grid(column=4, row=2)

    def chapter_jm():
        jm = Toplevel()
        jm.geometry('350x180+0+%d' % ((root.winfo_screenheight()-180)/2))
        jm.resizable(width=False, height=False)
        b_plus = PIL.Image.open('images/material/plus.png')
        global img_b_plus
        img_b_plus = ImageTk.PhotoImage(b_plus)
        ready2add = {}
        chapter_name = {0: 'jm-qc', 1: 'jm-wh', 2: 'jm-sq'}

        def ready(_name, times):
            global misson_sequence
            ready2add[misson_sequence] = '[' + \
                str(misson_sequence)+']'+chapter_name[_name]+' ^ '+str(times)
            st['state'] = 'normal'
            st.insert('end', ready2add[misson_sequence]+'\n')
            st['state'] = 'disabled'
            misson_sequence += 1
        label_frame = {}
        spinbox = {}
        button_box = {}
        def get_spin(i): return ready(i, spinbox[i].get())

        label_frame[0] = ttk.LabelFrame(jm, width=150, height=10, text='切城')
        spinbox[0] = ttk.Spinbox(
            label_frame[0], from_=1, to=99, increment=1, width=2)
        button_box[0] = ttk.Button(
            label_frame[0], image=img_b_plus, command=lambda: get_spin(0))

        label_frame[1] = ttk.LabelFrame(jm, width=150, height=10, text='龙门外环')
        spinbox[1] = ttk.Spinbox(
            label_frame[1], from_=1, to=99, increment=1, width=2)
        button_box[1] = ttk.Button(
            label_frame[1], image=img_b_plus, command=lambda: get_spin(1))

        label_frame[2] = ttk.LabelFrame(jm, width=150, height=10, text='龙门市区')
        spinbox[2] = ttk.Spinbox(
            label_frame[2], from_=1, to=99, increment=1, width=2)
        button_box[2] = ttk.Button(
            label_frame[2], image=img_b_plus, command=lambda: get_spin(2))

        label_frame[0].grid(column=0, row=0)
        label_frame[1].grid(column=0, row=1)
        label_frame[2].grid(column=0, row=2)

        spinbox[0].grid(column=0, row=0)
        spinbox[1].grid(column=0, row=0)
        spinbox[2].grid(column=0, row=0)

        button_box[0].grid(column=1, row=0)
        button_box[1].grid(column=1, row=0)
        button_box[2].grid(column=1, row=0)

        spinbox[0].set(1)
        spinbox[1].set(1)
        spinbox[2].set(1)

        lf = ttk.LabelFrame(jm, text='ready2add', width=150, height=50)
        lf.grid(column=1, row=0, rowspan=3)
        st = scrolledtext.ScrolledText(lf, width=20, height=10)
        st.grid(column=0, row=0)

        def add_comfirm():
            if messagebox.askyesno(message='确定添加关卡吗？', icon='question', title='确认', parent=jm):
                for key in ready2add:
                    misson_list.insert(END, ready2add[key])
                jm.destroy()
                am.destroy()
                root.lift()

        def add_cancel():
            ready2add.clear()
            st['state'] = 'normal'
            st.delete('1.0', 'end')
            st['state'] = 'disabled'
            global misson_sequence
            misson_sequence = 1
            jm.destroy()

        def add_rescind():
            global misson_sequence
            if misson_sequence == 1:
                messagebox.showinfo(message="待添加列表为空")
            else:
                misson_sequence -= 1
                del ready2add[misson_sequence]
                st['state'] = 'normal'
                st.delete('end-2 lines', 'end')
                if misson_sequence != 1:
                    st.insert('end', '\n')
                st['state'] = 'disabled'
        ttk.Button(jm, text='撤销添加', command=add_rescind).grid(column=2, row=0)
        ttk.Button(jm, text='√添加完成', command=add_comfirm).grid(column=2, row=1)
        ttk.Button(jm, text='×取消并返回上页',
                   command=add_cancel).grid(column=2, row=2)

    am = Toplevel()
    am.title('添加任务')
    am.geometry('595x90+0+%d' % (root.winfo_screenheight()/2))
    am.resizable(width=False, height=False)
    im1 = PIL.Image.open('images/material/button_zx.png')
    im2 = PIL.Image.open('images/material/button_wz.png')
    im3 = PIL.Image.open('images/material/button_xp.png')
    im4 = PIL.Image.open('images/material/button_jm.png')
    global img_zx, img_wz, img_xp, img_jm
    img_zx = ImageTk.PhotoImage(im1)
    img_wz = ImageTk.PhotoImage(im2)
    img_xp = ImageTk.PhotoImage(im3)
    img_jm = ImageTk.PhotoImage(im4)
    button1 = ttk.Button(am, image=img_zx, command=chapter_zx)
    button2 = ttk.Button(am, image=img_wz, command=chapter_wz)
    button3 = ttk.Button(am, image=img_xp, command=chapter_pr)
    button4 = ttk.Button(am, image=img_jm, command=chapter_jm)
    button1.grid(column=0, row=0)
    button2.grid(column=1, row=0)
    button3.grid(column=2, row=0)
    button4.grid(column=3, row=0)


def add_mission():
    _add_mission()


def cancel_mission():
    misson_list.delete('end')
    global misson_sequence
    if misson_sequence == 1:
        messagebox.showinfo(message="任务列表为空")
    else:
        misson_sequence -= 1


def clean_mission():
    misson_list.delete(0, 'end')
    global misson_sequence
    misson_sequence = 1


def get_name(i):
    name = misson_list.get(i-1)
    matchObj = re.match(r'(.*)](.*?) .*', name, re.M | re.I)
    get = str(matchObj.group(2))
    get = get.replace('-', '_')
    print(get)
    return get


def get_times(i):
    name = misson_list.get(i-1)
    matchObj = re.match(r'(.*)\s\^\s(.*)', name, re.M | re.I)
    print(matchObj.group(2))
    return int(matchObj.group(2))


def start_missions():
    text_insert('多任务模式开始\n')
    # auto_game.run_state = 'ready'
    auto_game.__running.set()  # 暂停信号
    num = misson_list.size()+1
    # print(num)
    for i in range(1, num):
        text_insert('现在是第%d个任务\n' % i)
        _name = get_name(i)
        time.sleep(1)
        auto_game.screenshot()
        if auto_game.Image_to_position('chapter_' + _name) == False:
            if (i == 1):
                text_insert('不在目标关卡界面，检测是否在首页\n')
                auto_game.find_back()
            elif (_name != get_name(i-1)):
                text_insert('与上个任务目标不同，回到首页\n')
                auto_game.find_back()
            # auto_game.run_state = 'running'
            auto_game.chapter_selet(_name)
        else:
            auto_game.click(auto_game.center[0], auto_game.center[1])
        auto_game.chapter_run(get_times(i))

    text_insert('全部任务完成\n')
    # auto_game.run_state = 'standby'


def pause_mission():
    auto_game.__running.clear()
    text_insert('任务暂停\n')
    button5_2 = Button(right_frame, text="恢复任务",
                       command=restart_mission, padx=9, relief=GROOVE, bg='green')
    button5_2.place(relx=0.4, rely=0.54, anchor=N)


def restart_mission():
    auto_game.__running.set()
    text_insert('结束暂停\n')
    button5_2 = Button(right_frame, text="暂停任务",
                       command=pause_mission, padx=9, relief=GROOVE, bg='red')
    button5_2.place(relx=0.4, rely=0.54, anchor=N)




def single_mode():
    a_mission = Toplevel()
    a_mission.geometry('350x180+0+%d' % ((root.winfo_screenheight()-180)/2))
    a_mission.resizable(width=False, height=False)
    Label(a_mission, text='单任务模式需要手动选好要刷的图', font=("微软雅黑", 11),
          anchor=W, justify=LEFT).grid(column=0, row=0, columnspan=2)
    Label(a_mission, text='开始任务后自动帮你刷这个图n次', font=("微软雅黑", 11),
          anchor=W, justify=LEFT).grid(column=0, row=1, columnspan=2)
    


# 右侧部件
right_frame = Frame(width=100, height=470, bg='#FFE4C4')
right_frame.pack(side='right')
button0_1 = Button(right_frame, text="连接模拟器", command=lambda: set_a_new_thread(
    connect), padx=2, relief=GROOVE,bg='#8FBC8F')
button0_1.place(relx=0.4, rely=0.04, anchor=N)

button1 = Button(right_frame, text="增加任务",
                 command=add_mission, padx=9, relief=GROOVE)
button1.place(relx=0.4, rely=0.14, anchor=N)
button2 = Button(right_frame, text="删除最后项",
                 command=cancel_mission, padx=3, relief=GROOVE)
button2.place(relx=0.4, rely=0.24, anchor=N)
button3 = Button(right_frame, text="清空任务",
                 command=clean_mission, padx=9, relief=GROOVE)
button3.place(relx=0.4, rely=0.34, anchor=N)
button4 = Button(right_frame, text="开始任务", command=lambda: set_a_new_thread(
    start_missions), padx=9, relief=GROOVE, bg='#AFEEEE')
button4.place(relx=0.4, rely=0.44, anchor=N)
button4['state'] = 'disabled'
button5_1 = Button(right_frame, text="暂停任务",
                   command=pause_mission, padx=9, relief=GROOVE, bg='red')
button5_1.place(relx=0.4, rely=0.54, anchor=N)
button6 = Button(label_text1, text="模式说明", command=single_mode,
                 padx=3, relief=GROOVE, bg='#87CEFA')
button6.grid(column=0,row=0,pady=20)

right_frame_1 = Frame(right_frame, width=80, height=100,
                      )
right_frame_1.place(relx=0.41, rely=0.90, anchor=S)
icon_96 = PIL.Image.open('images/material/icon_1.png')
img_icon_96 = ImageTk.PhotoImage(icon_96)
icon_c=Canvas(right_frame_1,width=80, height=80)
icon_c.pack()
icon_c.create_image(0,0,image=img_icon_96,anchor=NW)

# 新建线程


def set_a_new_thread(fun_name, _args=()):
    th = threading.Thread(target=fun_name, args=_args)
    th.setDaemon(True)  # 守护线程
    th.start()


# root.winfo_x()获取当前窗口位置x
# def windows_move(event):
#     time.sleep(0.01)
#     root.geometry('%dx%d+%d+%d' % (width, height, (root.winfo_x()+(event.x -
#                                                                    mouse_coord[0])/2), (root.winfo_y()+(event.y-mouse_coord[1])/2)))
#     root.update()

# 获取当前鼠标位置


# def get_mouse(event):
#     global mouse_coord
#     mouse_coord = [event.x, event.y]
#     print(mouse_coord)

# frame.bind("<Motion>",callback),使用bind获取点击事件


# def monitor():
#     while True:
#         label.bind("<Button-1>", get_mouse)
#         label.bind("<B1-Motion>", windows_move)
#         label.update()


# set_a_new_thread(monitor)
root.update()

root.mainloop()
