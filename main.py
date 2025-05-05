import customtkinter
import random
import string
import pyperclip
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os
import json

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# ملف الإعدادات
SETTINGS_FILE = "settings.json"
DEFAULT_LANGUAGE = "ar"
current_language = DEFAULT_LANGUAGE

# النصوص القابلة للتغيير حسب اللغة
TEXTS = {
    "en": {
        "app_title": "Encrypted Password Generator",
        "password_length": "Password Length:",
        "include_letters": "Include Letters",
        "include_numbers": "Include Numbers",
        "include_symbols": "Include Symbols",
        "generate_password": "Generate Password",
        "click_to_generate": "Click to generate password",
        "regenerate": "Regenerate",
        "copy": "Copy",
        "save_to_file": "Save to File",
        "save_encrypted": "Save Encrypted",
        "view_saved_passwords": "View Saved Passwords",
        "saved_passwords": "Saved Passwords",
        "username_prompt": "Enter username:",
        "save_file_title": "Save to File",
        "text_files": "Text files",
        "all_files": "All files",
        "save_success": "Password for {username} saved to file.",
        "save_error": "Error saving file:\n{e}",
        "username_required": "Please enter a username.",
        "save_encrypted_title": "Save Encrypted",
        "save_encrypted_success": "Password for {username} saved encrypted.",
        "save_encrypted_error": "Error saving file:\n{e}",
        "no_saved_passwords": "No encrypted passwords saved yet.",
        "no_encrypted_file": "No encrypted password database file yet.",
        "decrypt_error": "Error decrypting line:\n{e}",
        "read_file_error": "Error reading file:\n{e}",
        "copied_to_clipboard": "Password copied to clipboard.",
        "no_password_generated": "No password generated yet.",
        "error": "Error",
        "warning": "Warning",
        "settings": "Settings",
        "language": "Language",
        "language_en": "English",
        "language_ar": "Arabic"
    },
    "ar": {
        "app_title": "مولد كلمات المرور المشفر",
        "password_length": "طول كلمة المرور:",
        "include_letters": "تضمين حروف",
        "include_numbers": "تضمين أرقام",
        "include_symbols": "تضمين رموز",
        "generate_password": "إنشاء كلمة المرور",
        "click_to_generate": "انقر لإنشاء كلمة المرور",
        "regenerate": "تغيير",
        "copy": "نسخ",
        "save_to_file": "حفظ في ملف",
        "save_encrypted": "حفظ مشفر",
        "view_saved_passwords": "عرض كلمات المرور المحفوظة",
        "saved_passwords": "كلمات المرور المحفوظة",
        "username_prompt": "أدخل اسم المستخدم:",
        "save_file_title": "حفظ في ملف",
        "text_files": "ملفات نصية",
        "all_files": "كل الملفات",
        "save_success": "تم حفظ كلمة المرور لـ {username} في الملف.",
        "save_error": "حدث خطأ أثناء حفظ الملف:\n{e}",
        "username_required": "يرجى إدخال اسم المستخدم.",
        "save_encrypted_title": "حفظ مشفر",
        "save_encrypted_success": "تم حفظ كلمة المرور لـ {username} بشكل مشفر.",
        "save_encrypted_error": "حدث خطأ أثناء حفظ الملف:\n{e}",
        "no_saved_passwords": "لا توجد كلمات مرور محفوظة مشفرة حتى الآن.",
        "no_encrypted_file": "لا يوجد ملف لقاعدة بيانات كلمات المرور المشفرة حتى الآن.",
        "decrypt_error": "حدث خطأ أثناء فك تشفير سطر:\n{e}",
        "read_file_error": "حدث خطأ أثناء قراءة الملف:\n{e}",
        "copied_to_clipboard": "تم نسخ كلمة المرور إلى الحافظة.",
        "no_password_generated": "لم يتم إنشاء كلمة مرور بعد.",
        "error": "خطأ",
        "warning": "تنبيه",
        "settings": "إعدادات",
        "language": "اللغة",
        "language_en": "الإنجليزية",
        "language_ar": "العربية"
    }
}

def get_text(key):
    return TEXTS[current_language].get(key, TEXTS[DEFAULT_LANGUAGE][key])

def load_settings():
    global current_language
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            current_language = settings.get("language", DEFAULT_LANGUAGE)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def save_settings():
    settings = {"language": current_language}
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

class PasswordGeneratorApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        load_settings()
        self.title(get_text("app_title"))
        self.geometry("650x590+450+150")
        self.resizable(False, False)

        self.font_large = customtkinter.CTkFont(family="Arial", size=20, weight="bold")
        self.font_medium = customtkinter.CTkFont(family="Arial", size=16)
        self.font_medium_bold = customtkinter.CTkFont(family="Arial", size=16, weight="bold")

        # إنشاء Fernet object
        self.key_file = "encryption.key"
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
        with open(self.key_file, "rb") as key_file:
            key = key_file.read()
        self.f = Fernet(key)
        self.database_file = "passwords_db_encrypted.dat"

        # إطار الإعدادات الرئيسي
        self.settings_frame = customtkinter.CTkFrame(self, corner_radius=15, fg_color="#2c3e50")
        self.settings_frame.pack(pady=20, padx=20, fill="x", expand=False)

        # زر الإعدادات داخل الإطار
        self.settings_button = customtkinter.CTkButton(
            self.settings_frame,
            text="⚙",
            command=self.open_settings_window,
            fg_color="transparent",
            hover_color="#3a5f7a",
            width=35,
            height=35,
            corner_radius=17,
            font=("Arial", 18)
        )
        self.settings_button.place(relx=0.98, rely=0.05, anchor="ne")

        # عناصر التحكم في توليد كلمة المرور
        self.length_label = customtkinter.CTkLabel(
            self.settings_frame,
            text=get_text("password_length"),
            font=self.font_medium,
            text_color="white"
        )
        self.length_label.pack(pady=(10, 5), padx=10, anchor="w")

        self.length_entry = customtkinter.CTkEntry(
            self.settings_frame,
            width=50,
            font=self.font_medium,
            justify="center"
        )
        self.length_entry.insert(0, "12")
        self.length_entry.pack(pady=(0, 10), padx=10, anchor="w")

        self.include_letters = customtkinter.CTkCheckBox(
            self.settings_frame,
            text=get_text("include_letters"),
            font=self.font_medium
        )
        self.include_letters.select()
        self.include_letters.pack(pady=(5, 5), padx=10, anchor="w")

        self.include_numbers = customtkinter.CTkCheckBox(
            self.settings_frame,
            text=get_text("include_numbers"),
            font=self.font_medium
        )
        self.include_numbers.select()
        self.include_numbers.pack(pady=(5, 5), padx=10, anchor="w")

        self.include_symbols = customtkinter.CTkCheckBox(
            self.settings_frame,
            text=get_text("include_symbols"),
            font=self.font_medium
        )
        self.include_symbols.select()
        self.include_symbols.pack(pady=(5, 10), padx=10, anchor="w")

        self.generate_button = customtkinter.CTkButton(
            self.settings_frame,
            text=get_text("generate_password"),
            font=self.font_medium,
            command=self.generate_password,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.generate_button.pack(pady=15, padx=10, fill="x")

        # إطار عرض كلمة المرور
        self.password_frame = customtkinter.CTkFrame(self, corner_radius=15, fg_color="#34495e")
        self.password_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.password_frame.columnconfigure(0, weight=1)
        self.password_frame.columnconfigure(1, weight=1)
        self.password_frame.columnconfigure(2, weight=1)
        self.password_frame.columnconfigure(3, weight=1)

        self.password_label_text = customtkinter.StringVar(value=get_text("click_to_generate"))
        self.password_label = customtkinter.CTkLabel(
            self.password_frame,
            textvariable=self.password_label_text,
            font=self.font_large,
            text_color="white"
        )
        self.password_label.grid(row=0, column=0, columnspan=4, pady=20, padx=10, sticky="ew")

        self.regenerate_button = customtkinter.CTkButton(
            self.password_frame,
            text=get_text("regenerate"),
            font=self.font_medium,
            command=self.generate_password,
            fg_color="#e67e22",
            hover_color="#d35400"
        )
        self.regenerate_button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.copy_button = customtkinter.CTkButton(
            self.password_frame,
            text=get_text("copy"),
            font=self.font_medium,
            command=self.copy_password,
            fg_color="#27ae60",
            hover_color="#219653"
        )
        self.copy_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        self.save_file_button = customtkinter.CTkButton(
            self.password_frame,
            text=get_text("save_to_file"),
            font=self.font_medium,
            command=self.save_password_to_file_inline,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        self.save_file_button.grid(row=1, column=2, pady=10, padx=10, sticky="ew")

        self.save_db_button = customtkinter.CTkButton(
            self.password_frame,
            text=get_text("save_encrypted"),
            font=self.font_medium,
            command=self.ask_and_save_encrypted_inline,
            fg_color="#f39c12",
            hover_color="#e67e22"
        )
        self.save_db_button.grid(row=1, column=3, pady=10, padx=10, sticky="ew")

        # زر عرض كلمات المرور المحفوظة
        self.view_passwords_button = customtkinter.CTkButton(
            self,
            text=get_text("view_saved_passwords"),
            font=self.font_medium,
            command=self.show_saved_passwords_gui,
            fg_color="#3a539b",
            hover_color="#2c3e50"
        )
        self.view_passwords_button.pack(pady=15, padx=20, fill="x")

        self.current_password = ""
        self.settings_window = None
        self.update_texts()

    def update_texts(self):
        self.title(get_text("app_title"))
        self.length_label.configure(text=get_text("password_length"))
        self.include_letters.configure(text=get_text("include_letters"))
        self.include_numbers.configure(text=get_text("include_numbers"))
        self.include_symbols.configure(text=get_text("include_symbols"))
        self.generate_button.configure(text=get_text("generate_password"))
        self.password_label_text.set(get_text("click_to_generate"))
        self.regenerate_button.configure(text=get_text("regenerate"))
        self.copy_button.configure(text=get_text("copy"))
        self.save_file_button.configure(text=get_text("save_to_file"))
        self.save_db_button.configure(text=get_text("save_encrypted"))
        self.view_passwords_button.configure(text=get_text("view_saved_passwords"))
        if self.settings_window:
            self.settings_window.title(get_text("settings"))

    def open_settings_window(self):
        if self.settings_window:
            self.settings_window.destroy()
        
        self.settings_window = customtkinter.CTkToplevel(self)
        self.settings_window.title(get_text("settings"))
        self.settings_window.geometry("300x150+550+250")
        self.settings_window.resizable(False, False)
        self.settings_window.grab_set()
        
        languages = {"English": "en", "العربية": "ar"}
        self.language_option_menu = customtkinter.CTkOptionMenu(
            self.settings_window,
            values=list(languages.keys()),
            command=self.change_language
        )
        
        for key, value in languages.items():
            if value == current_language:
                self.language_option_menu.set(key)
                break
                
        self.language_option_menu.pack(padx=20, pady=20)
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings_window)

    def close_settings_window(self):
        if self.settings_window:
            self.settings_window.grab_release()
            self.settings_window.destroy()
        self.settings_window = None

    def change_language(self, selected_language):
        global current_language
        languages = {"English": "en", "العربية": "ar"}
        current_language = languages[selected_language]
        self.update_texts()
        save_settings()

    def generate_password(self):
        try:
            length = int(self.length_entry.get())
        except ValueError:
            messagebox.showerror(get_text("error"), get_text("password_length"))
            return

        letters = string.ascii_letters if self.include_letters.get() else ""
        numbers = string.digits if self.include_numbers.get() else ""
        symbols = string.punctuation if self.include_symbols.get() else ""

        characters = letters + numbers + symbols

        if not characters:
            messagebox.showerror(get_text("error"), get_text("username_required"))
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_label_text.set(password)
        self.current_password = password

    def copy_password(self):
        if self.current_password:
            pyperclip.copy(self.current_password)
            messagebox.showinfo(get_text("copied_to_clipboard"), get_text("copied_to_clipboard"))
        else:
            messagebox.showinfo(get_text("warning"), get_text("no_password_generated"))

    def save_password_to_file_inline(self):
        if not self.current_password:
            messagebox.showinfo(get_text("warning"), get_text("no_password_generated"))
            return

        dialog = customtkinter.CTkInputDialog(
            text=get_text("username_prompt"),
            title=get_text("save_file_title"),
            font=self.font_medium_bold
        )
        username = dialog.get_input()

        if username:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[(get_text("text_files"), "*.txt"), (get_text("all_files"), "*.*")],
                initialfile=f"{username}_password.txt"
            )
            if filepath:
                try:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(f"{get_text('username_prompt')} {username}\n")
                        f.write(f"{get_text('password_length')} {self.current_password}\n")
                    messagebox.showinfo("Success", get_text("save_success").format(username=username))
                except Exception as e:
                    messagebox.showerror(get_text("error"), get_text("save_error").format(e=e))

    def ask_and_save_encrypted_inline(self):
        if not self.current_password:
            messagebox.showinfo(get_text("warning"), get_text("no_password_generated"))
            return

        dialog = customtkinter.CTkInputDialog(
            text=get_text("username_prompt"),
            title=get_text("save_encrypted_title"),
            font=self.font_medium_bold
        )
        username = dialog.get_input()

        if username:
            try:
                data = f"{username}:{self.current_password}".encode()
                encrypted_data = self.f.encrypt(data)
                with open(self.database_file, "ab") as f:
                    f.write(encrypted_data + b"\n")
                messagebox.showinfo("Success", get_text("save_encrypted_success").format(username=username))
            except Exception as e:
                messagebox.showerror(get_text("error"), get_text("save_encrypted_error").format(e=e))

    def show_saved_passwords_gui(self):
        try:
            saved_passwords = []
            if os.path.exists(self.database_file):
                with open(self.database_file, "rb") as f:
                    for line in f:
                        try:
                            decrypted = self.f.decrypt(line.strip()).decode()
                            username, password = decrypted.split(":", 1)
                            saved_passwords.append((username, password))
                        except Exception as e:
                            messagebox.showerror(get_text("error"), get_text("decrypt_error").format(e=e))

                if saved_passwords:
                    view_window = customtkinter.CTkToplevel(self)
                    view_window.title(get_text("saved_passwords"))
                    view_window.geometry("600x400+500+200")

                    scroll_frame = customtkinter.CTkScrollableFrame(view_window)
                    scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

                    for username, password in saved_passwords:
                        entry_frame = customtkinter.CTkFrame(scroll_frame)
                        entry_frame.pack(fill="x", pady=5, padx=5)

                        info_frame = customtkinter.CTkFrame(entry_frame, fg_color="transparent")
                        info_frame.pack(side="left", fill="x", expand=True)

                        customtkinter.CTkLabel(
                            info_frame,
                            text=f"{username}",
                            font=self.font_medium_bold
                        ).pack(anchor="w")

                        customtkinter.CTkLabel(
                            info_frame,
                            text=f"{password}",
                            font=self.font_medium
                        ).pack(anchor="w")

                        copy_btn = customtkinter.CTkButton(
                            entry_frame,
                            text=get_text("copy"),
                            width=80,
                            command=lambda p=password: self.copy_saved_password(p)
                        )
                        copy_btn.pack(side="right", padx=10)

                else:
                    messagebox.showinfo(get_text("warning"), get_text("no_saved_passwords"))
            else:
                messagebox.showinfo(get_text("warning"), get_text("no_encrypted_file"))
        except Exception as e:
            messagebox.showerror(get_text("error"), get_text("read_file_error").format(e=e))

    def copy_saved_password(self, password):
        pyperclip.copy(password)
        messagebox.showinfo(get_text("copied_to_clipboard"), get_text("copied_to_clipboard"))

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
    save_settings()