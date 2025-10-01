# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.borrow_records = []

    def add_book(self, book_id, title, author, copies):
        if any(book["book_id"] == book_id for book in self.books):
            print(f"図書ID「{book_id}」の本は既に存在します。")
            return
        self.books.append({
            "book_id": book_id,
            "title": title,
            "author": author,
            "copies": copies,
            "available_copies": copies
        })
        print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")

    def list_books(self):
        if not self.books:
            print("現在、登録されている図書はありません。")
            return
        print("--- 図書一覧 ---")
        for book in self.books:
            print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")

    def search_book(self, book_id):
        book = next((b for b in self.books if b["book_id"] == book_id), None)
        if book:
            print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")
        else:
            print(f"図書ID「{book_id}」の本は存在しません。")

    def add_member(self, member_id, name):
        if any(member["member_id"] == member_id for member in self.members):
            print(f"会員ID「{member_id}」の会員は既に存在します。")
            return
        self.members.append({"member_id": member_id, "name": name})
        print(f"会員「{name}」（ID: {member_id}）を追加しました。")

    def list_members(self):
        if not self.members:
            print("現在、登録されている会員はいません。")
            return
        print("--- 会員一覧 ---")
        for member in self.members:
            print(f"ID: {member['member_id']}, 名前: {member['name']}")

    def borrow_book(self, book_id, member_id):
        book = next((b for b in self.books if b["book_id"] == book_id), None)
        if not book:
            print(f"図書ID「{book_id}」の本は存在しません。")
            return
        member = next((m for m in self.members if m["member_id"] == member_id), None)
        if not member:
            print(f"会員ID「{member_id}」の会員は存在しません。")
            return
        if book["available_copies"] <= 0:
            print(f"図書「{book['title']}」は現在貸出可能な冊数がありません。")
            return
        record_count = sum(1 for r in self.borrow_records if r["member_id"] == member_id and not r["returned"])
        if record_count >= 5:
            print(f"貸出可能数は5冊までです。")
            return
        borrow_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        self.borrow_records.append({
            "book_id": book_id,
            "member_id": member_id,
            "borrow_date": borrow_date,
            "due_date": due_date,
            "returned": False
        })
        print(f"図書「{book['title']}」を会員「{member['name']}」に貸し出しました。\n返却期限: {due_date}")
        book["available_copies"] -= 1

    def list_borrowed_books(self):
        print("--- 貸出中の図書一覧 ---")
        borrow_list = [r for r in self.borrow_records if not r["returned"]]
        if not borrow_list:
            print("現在、貸出中の図書はありません。")
            return
        for record in borrow_list:
            book = next((b for b in self.books if b["book_id"] == record["book_id"]), None)
            member = next((m for m in self.members if m["member_id"] == record["member_id"]), None)
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}")

    def return_book(self, book_id, member_id):
        record = next((r for r in self.borrow_records if r["book_id"] == book_id and r["member_id"] == member_id and not r["returned"]), None)
        if not record:
            print(f"図書ID「{book_id}」本を会員ID「{member_id}」の会員は借りていません。")
            return
        record["returned"] = True
        book = next((b for b in self.books if b["book_id"] == book_id), None)
        if book:
            book["available_copies"] += 1
            print(f"図書「{book['title']}」が返却されました。")
        else:
            print(f"図書ID「{book_id}」の本は存在しません。")

    def calculate_fines(self):
        print("--- 延滞料金一覧 ---")
        today = datetime.now()
        borrow_list = [r for r in self.borrow_records if not r["returned"]]
        if not borrow_list:
            print("現在、貸出中の図書はありません。")
            return
        for record in borrow_list:
            book = next((b for b in self.books if b["book_id"] == record["book_id"]), None)
            member = next((m for m in self.members if m["member_id"] == record["member_id"]), None)
            due_date = datetime.strptime(record["due_date"], "%Y-%m-%d")
            overdue_days = max((today - due_date).days, 0)
            fine = overdue_days * 100
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 延滞料金: {fine}円")

    def show_member_history(self, member_id):
        member = next((m for m in self.members if m["member_id"] == member_id), None)
        if not member:
            print(f"会員ID「{member_id}」の会員は存在しません。")
            return
        print(f"--- 会員「{member['name']}」（ID: {member_id}）の貸出履歴 ---")
        history = [r for r in self.borrow_records if r["member_id"] == member_id]
        if not history:
            print("この会員の貸出履歴はありません。")
            return
        for record in history:
            book = next((b for b in self.books if b["book_id"] == record["book_id"]), None)
            status = "返却済み" if record["returned"] else "貸出中"
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}, 状態: {status}")

def main():
    library = Library()
    while True:
        print("図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 終了")
        print("11: 会員の貸出履歴を表示")

        try:
            choice = int(input("操作を選択してください（1-11）: "))
        except ValueError as e:
            print(f"入力エラー: {e}")
            continue
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")
            continue

        if choice == 1:
            book_id = input("図書IDを入力してください: ")
            title = input("タイトルを入力してください: ")
            author = input("著者名を入力してください: ")
            copies = int(input("冊数を入力してください: "))
            library.add_book(book_id, title, author, copies)

        elif choice == 2:
            library.list_books()

        elif choice == 3:
            book_id = input("検索する図書IDを入力してください: ")
            library.search_book(book_id)

        elif choice == 4:
            member_id = input("会員IDを入力してください: ")
            name = input("名前を入力してください: ")
            library.add_member(member_id, name)

        elif choice == 5:
            library.list_members()

        elif choice == 6:
            book_id = input("貸し出す図書IDを入力してください: ")
            member_id = input("会員IDを入力してください: ")
            library.borrow_book(book_id, member_id)

        elif choice == 7:
            library.list_borrowed_books()

        elif choice == 8:
            book_id = input("返却する図書IDを入力してください: ")
            member_id = input("会員IDを入力してください: ")
            library.return_book(book_id, member_id)

        elif choice == 9:
            library.calculate_fines()

        elif choice == 10:
            print("図書館管理システムを終了します。")
            break

        elif choice == 11:
            member_id = input("履歴を表示する会員IDを入力してください: ")
            library.show_member_history(member_id)
        else:
            print("無効な選択です。1-11の数字を入力してください。")

main()