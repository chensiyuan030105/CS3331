import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class Item:
    def __init__(self, name, description, contact_info):
        self.name = name
        self.description = description
        self.contact_info = contact_info

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'contact_info': self.contact_info
        }

class ItemManager:
    def __init__(self, filename='items.json'):
        self.filename = filename
        self.items = self.load_items()

    def load_items(self):
        try:
            with open(self.filename, 'r') as f:
                items_data = json.load(f)
                return [Item(**item) for item in items_data]
        except FileNotFoundError:
            return []

    def save_items(self):
        with open(self.filename, 'w') as f:
            json.dump([item.to_dict() for item in self.items], f)

    def add_item(self, name, description, contact_info):
        item = Item(name, description, contact_info)
        self.items.append(item)
        self.save_items()

    def delete_item(self, name):
        self.items = [item for item in self.items if item.name != name]
        self.save_items()

    def display_items(self):
        return "\n".join(f"名称: {item.name}, 描述: {item.description}, 联系人: {item.contact_info}" for item in self.items)

    def find_item(self, name):
        for item in self.items:
            if item.name == name:
                return f"找到物品 - 名称: {item.name}, 描述: {item.description}, 联系人: {item.contact_info}"
        return "没有找到该物品。"

class App:
    def __init__(self, root):
        self.manager = ItemManager()
        self.root = root
        self.root.title("物品复活软件")

        self.label = tk.Label(root, text="物品复活软件", font=("Arial", 16))
        self.label.pack(pady=10)

        self.add_button = tk.Button(root, text="添加物品", command=self.add_item)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="删除物品", command=self.delete_item)
        self.delete_button.pack(pady=5)

        self.display_button = tk.Button(root, text="显示物品列表", command=self.display_items)
        self.display_button.pack(pady=5)

        self.find_button = tk.Button(root, text="查找物品", command=self.find_item)
        self.find_button.pack(pady=5)

    def add_item(self):
        name = simpledialog.askstring("输入", "请输入物品名称:")
        description = simpledialog.askstring("输入", "请输入物品描述:")
        contact_info = simpledialog.askstring("输入", "请输入联系人信息:")
        if name and description and contact_info:
            self.manager.add_item(name, description, contact_info)
            messagebox.showinfo("成功", "物品添加成功！")
        else:
            messagebox.showwarning("警告", "请填写所有信息！")

    def delete_item(self):
        name = simpledialog.askstring("输入", "请输入要删除的物品名称:")
        if name:
            self.manager.delete_item(name)
            messagebox.showinfo("成功", "物品删除成功！")
        else:
            messagebox.showwarning("警告", "请输入物品名称！")

    def display_items(self):
        items = self.manager.display_items()
        if items:
            messagebox.showinfo("物品列表", items)
        else:
            messagebox.showinfo("物品列表", "没有可用的物品。")

    def find_item(self):
        name = simpledialog.askstring("输入", "请输入要查找的物品名称:")
        if name:
            result = self.manager.find_item(name)
            messagebox.showinfo("查找结果", result)
        else:
            messagebox.showwarning("警告", "请输入物品名称！")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
