import tkinter as tk
from tkinter import messagebox
import functools


# 定义记录文件路径
file_path = "狼人杀发言记录.txt"
current_day = 1  # 当前天数
# 创建并初始化窗口
root = tk.Tk()
root.title("狼人杀发言记录")
root.geometry("800x600")

# 初始化身份字典
identity_dict = {c1: {c2: {"identity": "未选择身份"} for c2 in range(1, 13)} for c1 in range(1, 21)}  # 存储当前玩家的身份
# 初始化发言信息
context_dict = {c1: {c2: {"context": ""} for c2 in range(1, 13)} for c1 in range(1, 21)}  # 存储当前玩家的发言
# 初始化警徽流
badge_sequence = ""
# 检查并创建记录文件
def init_file():
    with open(file_path, "a", encoding="mbcs") as f:
        pass  # 创建文件，如果已存在则跳过

# 上一天按钮事件
def prev_day():
    global current_day
    if current_day > 1:
        current_day -= 1
        update_day_display()

# 下一天按钮事件
def next_day():
    global current_day
    if current_day < 20:
        current_day += 1
        update_day_display()


# 更新显示内容的函数
def update_day_display():
    day_label.config(text=f"第 {current_day} 天")

    # 获取当前天数的身份记录
    day_identity_data = identity_dict.get(current_day, {})
    # 发言记录
    day_context_data = context_dict.get(current_day, {})
    for player_number, data in day_identity_data.items():
        # 更新玩家的身份内容
        records1[player_number - 1].config(text=f"({data['identity']}){player_number}号:")
    # 更新玩家的发言内容
    for player_number1, data1 in day_context_data.items():
        records[player_number1 - 1].config(text=f"{data1['context']}")


# 记录发言内容到文件的函数
def save_record(player_number, content):
    global current_day


    record_text = f"玩家 {player_number} 在第{current_day} 发言: {content}(身份为{identity_dict[current_day][player_number]['identity']})"

    # 保存记录到文件
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(record_text + "\n")


    # 替换字典中玩家发言内容
    context_dict[current_day][player_number] = {"context": content}

    # 更新显示内容
    records[player_number - 1].config(text=content)
    records1[player_number - 1].config(text=f"({identity_dict[current_day][player_number]['identity']}){player_number}号:")

    # 显示记录成功提示
    messagebox.showinfo("记录成功", f"玩家 {player_number} 的发言已记录。")


# 打开记录窗口的函数
def open_record_window(player_number):
    record_window = tk.Toplevel(root)
    record_window.title(f"记录玩家 {player_number} 的发言")
    record_window.geometry("350x400")

    # 创建一个标签显示当前玩家的身份，初始为“未选择身份”
    identity_label = tk.Label(record_window, text=f"身份: {identity_dict[current_day][player_number]['identity']}")
    identity_label.pack(pady=10)

    def record_content():
        content = content_entry.get()  # 获取输入框内容
        save_record(player_number, content)  # 记录内容
        record_window.destroy()

    # 警徽流
    def open_badge_window():
        badge_window = tk.Toplevel(record_window)
        badge_window.title("选择警徽流顺序")
        badge_window.geometry("300x350")  # 调整为较大的窗口

        sequence = []

        def add_to_sequence(num):
            sequence.append(num)
            sequence_label.config(text="警徽流: " + " -> ".join(map(str, sequence)) + '   ')

        # 创建1到12号的按钮
        for num in range(1, 13):
            btn = tk.Button(badge_window, text=str(num), width=5,
                            command=functools.partial(add_to_sequence, num))
            btn.grid(row=(num - 1) // 4, column=(num - 1) % 4, padx=5, pady=5)

        sequence_label = tk.Label(badge_window, text="警徽流: ")
        sequence_label.grid(row=4, columnspan=4, pady=10)

        # 完成按钮，点击后将结果显示在内容输入框中
        def finish_badge_sequence():
            badge_sequence = "警徽流: " + " -> ".join(map(str, sequence))
            content_entry.insert('end', badge_sequence)  # 插入警徽流内容
            badge_window.destroy()

        finish_button = tk.Button(badge_window, text="完成", command=finish_badge_sequence)
        finish_button.grid(row=5, columnspan=4, pady=10)

    # 自称身份
    def open_identity_window():
        identity_window = tk.Toplevel(record_window)
        identity_window.title("选择自称身份")
        identity_window.geometry("300x500")

        selected_identity = tk.StringVar()  # 使用 StringVar 保存身份

        def change_button_color(button, identity):
            # 将当前按钮背景色恢复，更新为新的背景色
            for btn in identity_buttons:
                if btn != button:
                    btn.config(bg="SystemButtonFace")  # 恢复默认背景色
            button.config(bg="grey")  # 更改当前按钮的背景色为深色

            selected_identity.set(identity)  # 更新选择的身份

        identities = ["女巫", "猎人", "平民", "预言家", "守卫", "愚者", "狼人", "狼王"]
        identity_buttons = []  # 用于保存身份按钮

        for identity in identities:
            btn = tk.Button(identity_window, text=identity, width=10)
            btn.config(command=functools.partial(change_button_color, btn, identity))
            btn.pack(pady=5)
            identity_buttons.append(btn)

        # 其他选项
        tk.Label(identity_window, text="其他:").pack(pady=10)
        other_entry = tk.Entry(identity_window)
        other_entry.pack(pady=5)

        def finish_identity_selection():
            # 获取选择的身份和输入框内容
            selected_identity_value = selected_identity.get() or "未选择身份"
            other_input = other_entry.get()

            # 更新身份字典
            identity_dict[current_day][player_number]['identity'] = selected_identity_value  # 更新身份变量

            # 更新二级窗口中的身份标签
            identity_label.config(text=f"身份: {identity_dict[current_day][player_number]['identity']}")
            identity_window.destroy()  # 关闭身份窗口

        # 完成按钮
        finish_button = tk.Button(identity_window, text="完成", command=finish_identity_selection)
        finish_button.pack(pady=10)

    # 听感好/差
    def open_hearing_window(hearing_type):
        # 将反馈内容更新到主窗口的内容输入框
        content_entry.insert('end', hearing_type)  # 插入选定的反馈内容

    # 快捷记录按钮
    tk.Button(record_window, text="警徽流", command=open_badge_window).pack(pady=10)
    tk.Button(record_window, text="自称身份", command=open_identity_window).pack(pady=10)
    tk.Button(record_window, text="听感好", command=functools.partial(open_hearing_window, "听感好  ")).pack(pady=10)
    tk.Button(record_window, text="听感差", command=functools.partial(open_hearing_window, "听感差  ")).pack(pady=10)

    # 自定义记录内容输入框
    tk.Label(record_window, text="内容:").pack(pady=10)
    content_entry = tk.Entry(record_window, width=20)
    content_entry.insert(0, context_dict[current_day][player_number]['context'])  # 插入当前玩家的发言内容
    content_entry.pack()

    # 自定义记录按钮
    tk.Button(
        record_window,
        text="保存内容",
        command=record_content
    ).pack(pady=10)


# 初始化文件
init_file()

# 创建玩家按钮和记录标签
records = []
records1 = []
for i in range(1, 13):
    frame = tk.Frame(root)
    frame.pack(fill=tk.X, pady=5)
    # 在号码左边添加括号并显示身份内容（默认“未记录身份”）
    label = tk.Label(frame, text=f"({identity_dict[current_day][i]['identity']}){i}号:")
    label.pack(side=tk.LEFT)
    records1.append(label)
    # 记录标签，显示玩家发言内容（初始为“”）
    record_label = tk.Label(frame, text="", width=30, anchor="w")
    record_label.pack(side=tk.LEFT)
    records.append(record_label)

    # 记录按钮，点击后打开记录窗口(记录按钮始终随着窗口大小变化而变化)
    button = tk.Button(frame, text="记录", command=functools.partial(open_record_window, i))
    button.pack(side=tk.RIGHT, padx=10)

# 在主界面中加入"上一天"和"下一天"按钮
prev_button = tk.Button(root, text="上一天", command=prev_day)
prev_button.pack(side=tk.LEFT, padx=10)

next_button = tk.Button(root, text="下一天", command=next_day)
next_button.pack(side=tk.RIGHT, padx=10)

# 显示当前第几天的标签
day_label = tk.Label(root, text=f"第 {current_day} 天")
day_label.pack(pady=10)

# 运行更新函数来显示第1天的记录
update_day_display()

# 运行 Tkinter 主循环
root.mainloop()
