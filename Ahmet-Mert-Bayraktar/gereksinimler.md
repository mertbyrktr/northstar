1. **Kullanıcı Kaydı**
   - **API Metodu:** `POST /auth/register`
   - **Açıklama:** Sisteme yeni bir kullanıcı profili oluşturulmasını sağlar. Kullanıcının temel bilgilerini alarak kayıt işlemini gerçekleştirir.

2. **Kullanıcı Girişi**
   - **API Metodu:** `POST /auth/login`
   - **Açıklama:** Kaydedilmiş bir profile giriş yapılmasını sağlar. Kimlik doğrulama işlemlerini yürüterek kullanıcıya erişim yetkisi verir.

3. **Egzersiz Ekleme**
   - **API Metodu:** `POST /workouts/exercises`
   - **Açıklama:** Kullanıcının yaptığı antrenmana yeni bir egzersiz tanımı eklemesini sağlar. Antrenman içeriğini zenginleştirmek için kullanılır.

4. **Antrenman Listeleme**
   - **API Metodu:** `GET /workouts`
   - **Açıklama:** Kullanıcının geçmişte yaptığı tüm antrenmanları ekranda görüntüler. Tarih ve içerik bazlı liste sunar.

5. **Egzersiz Detaylarını Gör**
   - **API Metodu:** `GET /exercises/{id}`
   - **Açıklama:** Seçilen bir egzersizin set ve tekrar gibi detay bilgilerini getirir. Kullanıcının performans verilerini incelemesini sağlar.

6. **Profil Bilgisi Güncelleme**
   - **API Metodu:** `PUT /users/profile`
   - **Açıklama:** Kullanıcının boy, kilo gibi fiziksel bilgilerini değiştirmesine izin verir. Fiziksel gelişim takibi için verileri günceller.

7. **Antrenman Notu Düzenleme**
   - **API Metodu:** `PUT /workouts/{id}/notes`
   - **Açıklama:** Daha önce kaydedilmiş bir antrenman hakkındaki notların değiştirilmesini sağlar. Performans notlarını güncel tutar.

8. **Egzersiz Kaydını Silme**
   - **API Metodu:** `DELETE /exercises/{id}`
   - **Açıklama:** Yanlış girilen veya iptal edilen bir egzersiz verisinin sistemden kaldırılmasını sağlar.

9. **Hedef Ekleme**
   - **API Metodu:** `POST /goals`
   - **Açıklama:** Kullanıcının ulaşmak istediği bir fitness hedefini listeye eklemesini sağlar. Motivasyon ve takip amaçlıdır.

10. **Hedef Silme**
    - **API Metodu:** `DELETE /goals/{id}`
    - **Açıklama:** Kullanıcının ulaştığı veya vazgeçtiği bir fitness hedefini listeden kaldırır.

11. **Ağırlık Takibi**
    - **API Metodu:** `POST /metrics/weight`
    - **Açıklama:** Kullanıcının günlük veya haftalık kilo verilerini sisteme kaydetmesini sağlar. Gelişim grafiklerini besler.

12. **Yapay Zeka Destekli Antrenman Önerisi**
    - **API Metodu:** `POST /ai/recommendations`
    - **Açıklama:** (AI-Based) Kullanıcının geçmiş verilerini analiz ederek o gün yapması gereken en uygun antrenman programını oluşturur.