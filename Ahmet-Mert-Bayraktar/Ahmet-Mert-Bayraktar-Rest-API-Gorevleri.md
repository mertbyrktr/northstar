# Ahmet Mert Bayraktar - REST API Görevleri

## Tamamlanan Özellikler ve Geliştirmeler

**1. Çekirdek Altyapı:**
- [x] Python, FastAPI, Uvicorn kütüphaneleriyle projenin ayağa kaldırılması.
- [x] MongoDB Atlas (Mongoose/Motor Asenkron) bulut veritabanı entegrasyonu.
- [x] Postman test koleksiyonu (`.postman/`) ve Swagger `openapi.json` çıktılarının hazırlanması.
- [x] Çevresel değişken yönetimi (`.env` dosyası).

**2. Güvenlik:**
- [x] PyJWT kullanılarak tam teşekküllü Bearer token mekanizması oluşturuldu. 
- [x] `user_id` istek gövdelerinden atılıp, tokenlardan çekilerek Multi-Tenant data sızıntısı önlendi.
- [x] Kullanıcı şifreleri veritabanına düz format yerine `bcrypt` şifrelenerek kayıt edildi. (Passlib çakışma sorunları native kodlama ile düzeltildi).

**3. İş Mantığı Uç Noktaları (13 Toplam):**
- [x] Authentication Modülü (Register, Login)
- [x] Workout & Exercises Modülü (Yaratma, Getirme, Güncelleme ve Silme)
- [x] Antrenman Silme (Cascade silme de eklendi: Bir antrenman silinirse altındaki tüm egzersizler MongoDB'den aynı saniyede toplu silinir).
- [x] Profil güncelleme, Hedef belirleme ve Kilo(Metrics) takibi modülleri.
- [x] Mock AI Öneri Endpoint'i altyapısı.

**Ek Görev / Tespitler:**
- Tüm RESTful prensipler başarıyla uyarlandı.
- Form data hatası veren eksik kütüphaneler (`python-multipart`) eklendi.
- Geçersiz ObjectId parse durumunda oluşabilecek `500 Server Error` tarzı çökmeler, güvenli bir format denetimiyle (`400 Bad Request`) olarak düzeltildi.
