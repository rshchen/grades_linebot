# 成績查詢系統使用說明
## 成績登錄系統公開板網址
* [成績登錄系統網址](https://samplescores.blesstw.com)
## 開發者使用說明
複製此專案後，
請在專案資料夾「StudentGradingSystem」之下（和主app:grade同一層）新增.env，
並在當中寫入
```
# .env
SECRET_KEY = '請替換為你的 Django 密鑰'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '請替換為你的 Google OAuth ID'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '請替換為你的 Google OAuth 密鑰'
EMAIL_HOST_USER = '請替換為你的發信 email'
EMAIL_HOST_PASSWORD = '請替換為你的 email 應用程式密碼'
LINE_CHANNEL_ACCESS_TOKEN = '請替換為你的 LINE Channel Access Token'
LINE_CHANNEL_SECRET = '請替換為你的 LINE Channel Secret'
```
當然還需處理Google Oauth, email host, line channel申請等項目問題，
並到setting.py的地方修改line hook對應的網址。


## 系統使用說明
試用人員請使用此帳號加密碼登入（此帳號無法以第三方方式登入）：
帳號：juihsiangchen3@gmail.com
密碼：ej03xu3m06
此帳號登入後會具有教師身份（葬送的芙莉蓮老師）與學生身份（費倫同學）（此帳號不具備管理員身份）
## 管理員使用說明
若您為開發者，可以經由以下步驟加入管理員身份：
### 1. 打開 Django Shell

首先，使用以下命令進入 Django Shell：

```bash
python manage.py shell
```

### 2. 導入你的 `Manager` 模型

在進入 Django Shell 後，導入你定義的 `Manager` 模型：

```python
from grades.models import Manager
```

### 3. 創建 `Manager` 實例並保存

接著，創建一個 `Manager` 實例，並將姓名和電子郵件地址設置為你提供的數據，然後保存這個實例到資料庫中：

```python
manager = Manager(name='Rui Xiang', email='sea810749@gmail.com')
manager.save()
```

### 4. 驗證資料是否已成功保存

為了確認數據是否正確保存，你可以查詢剛剛保存的管理員資料：

```python
Manager.objects.all()
```

這樣應該會返回包含你剛剛創建的 `Manager` 資料的查詢集。

如此一來，當您以管理員身份進入系統時，會看到這樣的畫面
![image](https://hackmd.io/_uploads/ryQc-22Zxx.png =70%x)

進入學生資料管理頁面，上傳學生資料csv檔案（檔案格式請參考「管理員匯入資料」 > 「學生資料.csv」）
![image](https://hackmd.io/_uploads/Sy3eGhnWll.png
 =70%x)
 
進入教師資料管理頁面，上傳教師資料csv檔案（檔案格式請參考「管理員匯入資料」 > 「教師資料.csv」）
![image](https://hackmd.io/_uploads/ByuEM33Zgg.png =70%x)





## 教師使用說明
1. 先請管理員開通教師權限。
2. 開通身份後可以按首頁中的教師按鈕以登入系統。
![image](https://hackmd.io/_uploads/BJvFQ23-gx.png =70%x)
3. 進入登入畫面，可以使用google第三方登入較為方便，就不需要再進行註冊了（試用人員無法以該帳號使用google第三方登入）。
![截圖 2025-03-27 下午1.45.32](https://hackmd.io/_uploads/ryiNLDM6kg.png =70%x)
4. 登入後點選左側創建課程。
![截圖 2025-03-27 下午1.47.16](https://hackmd.io/_uploads/S1lfyvPGTke.png =70%x)
5. 輸入課程名稱並提交。
![截圖 2025-03-27 下午1.50.56](https://hackmd.io/_uploads/HyMDvwfaJx.png =70%x)
6. 提交後會自動進入左側的「您的課程」頁面，之後可以直接在此頁面找到您所創建的課程。
![截圖 2025-03-27 下午1.51.49](https://hackmd.io/_uploads/rkaTPPzakg.png =70%x)
7. 點擊「編輯課程學生名單」按鈕。
![截圖 2025-03-27 下午1.51.49](https://hackmd.io/_uploads/ry04uwzakg.png =70%x)
8. 從下拉選單當中找到您的學生，勾選後按「更新學生成員」，如果學生是跑班也可以使用。（本來會直接顯示學生名單在頁面上，但不小心把這個功能改掉了，之後再改回來）
![截圖 2025-03-27 下午1.55.57](https://hackmd.io/_uploads/BJlBKDGa1e.png =70%x)
9. 回到您的課程後（可以拖曳方式改變課程順序），點選「顯示課程學生名單」可以確認學生名單。
![截圖 2025-03-27 下午1.51.49](https://hackmd.io/_uploads/HJd5FvGT1e.png =70%x)
10. 點選「管理課程成績」按鈕
![截圖 2025-03-27 下午1.51.49](https://hackmd.io/_uploads/ry1BqPzaye.png =70%x)
11. 輸入要新增的成績項目和類別，點擊「新增成績項目」按鈕。
![截圖 2025-03-27 下午2.08.24](https://hackmd.io/_uploads/BkN9iDGaJl.png =70%x)
12. 成績匯入方面，本系統提供excel匯入，或是直接輸入。
13. 直接輸入成績：請點擊「管理項目成績」按鈕。
![截圖 2025-03-27 下午2.11.35](https://hackmd.io/_uploads/H1nnTPzT1g.png =70%x)
14. 直接複製excel一整行（沒有分數的要空一行）的成績到網頁中間的框框當中，並點擊「保存成績」按鈕，立刻會顯示學生成績，若要修改成績再利用下方的表格修改成績。
![截圖 2025-03-27 下午2.22.22](https://hackmd.io/_uploads/rJt11ufTJx.png =70%x)
15. 使用excel匯入成績：請先點擊「匯出成績到excel」按鈕，利用匯出後的檔案格式，填入您的該項目成績，之後再利用下方的「選擇檔案」和「匯入成績」按鈕上傳檔案。
![截圖 2025-03-27 下午2.28.16](https://hackmd.io/_uploads/HJbNx_za1e.png =70%x)

## 學生使用說明
1. 請學生加入linebot，這裡有試用者可使用的linebot
<img src="https://qr-official.line.me/gs/M_653lxgat_GW.png?oat_content=qr" width="50%">
2. 請點擊右下的「身份驗證」按鈕
![IMG_4251](https://hackmd.io/_uploads/BkPjbuGTyx.png =40%x)
3. 請輸入學校信箱（試用者請輸入juihsiangchen3@gmail.com）。
4. 系統會傳送驗證碼到學校信箱，若沒收到，請確認
(1)信箱填寫正確
(2)是否被當成垃圾信件。（試用者會直接綁定系統）
5. 輸入正確驗證碼後即可使用本查詢系統查詢個人成績。





