# AIO Datasets Main Repo

Repository: https://github.com/Purin1410/AIO_Datasets_MainRepo.git

## Git workflow để tránh conflict với `main`

### 1. Clone repo

```bash
git clone https://github.com/Purin1410/AIO_Datasets_MainRepo.git
cd AIO_Datasets_MainRepo
```

### 2. Luôn cập nhật `main` trước khi làm

Trước khi code hoặc tạo branch mới, luôn chạy:

```bash
git checkout main
git pull --rebase origin main
```

### 3. Không code trực tiếp trên `main`

Mỗi người tạo branch riêng cho phần mình phụ trách:

```bash
git checkout -b feature/check-xxx
```

Ví dụ:

```bash
git checkout -b feature/check-naming
git checkout -b feature/check-counts
git checkout -b feature/check-quality
```

### 4. Chỉ sửa file mình phụ trách

Ví dụ phụ trách `check_quality.py` thì chỉ sửa:

```text
modules/check_quality.py
```

Hạn chế sửa các file chung như:

```text
main.py
requirements.txt
README.md
```

Nếu cần sửa file chung, nên báo trước để tránh conflict.

### 5. Commit code

```bash
git status
git add modules/check_xxx.py
git commit -m "Implement check xxx"
```

Nên commit nhỏ, message rõ ràng.

### 6. Rebase với `main` trước khi push

Trước khi push branch lên GitHub, luôn cập nhật lại với `main`:

```bash
git checkout main
git pull --rebase origin main

git checkout feature/check-xxx
git rebase main
```

Nếu không có conflict thì push:

```bash
git push origin feature/check-xxx
```

Nếu branch đã từng push trước đó và vừa rebase, dùng:

```bash
git push --force-with-lease
```

Không dùng `git push --force` nếu không chắc chắn.

### 7. Nếu bị conflict khi rebase

Git sẽ báo file bị conflict. Mở file đó và sửa các đoạn có dạng:

```text
<<<<<<< HEAD
code hiện tại
=======
code từ branch khác
>>>>>>> branch-name
```

Sau khi sửa xong:

```bash
git add .
git rebase --continue
```

Nếu muốn hủy rebase:

```bash
git rebase --abort
```

### 8. Tạo Pull Request

Sau khi push branch:

1. Tạo Pull Request từ branch của mình vào `main`.
2. Ghi rõ mình đã làm phần nào.
3. Copy link Pull Request vào file Workplan.
4. Đợi mọi người cross-check và comment.

### 9. Nguyên tắc chính

- Mỗi người làm trên một branch riêng.
- Không sửa trực tiếp trên `main`.
- Chỉ sửa đúng file mình phụ trách.
- Luôn `pull --rebase` trước khi code và trước khi push.
- Luôn `rebase main` trước khi tạo Pull Request.
- Không tự ý sửa file chung nếu chưa thống nhất.
- Không dùng `git push --force`, ưu tiên `git push --force-with-lease`.