# REST API Endpointleri

Bu doküman, canlı olarak çalışan Northstar uygulamasının sağladığı tüm 13 servis ucunu (endpoint) listeler. Her çağrı `/api/v1` ön eki ile başlar (Örnek: `http://localhost:8000/api/v1/auth/login`).

## A. Authentication (Kimlik Doğrulama)
- **POST /auth/register** : Sisteme yeni kullanıcı kaydeder.
- **POST /auth/login** : Email ve şifre kabul ederek `access_token` JWT değeri döndürür. (OAuth2 form data kullanır).

## B. Users (Kullanıcı Profil)
*Not: Bu noktadan itibaren listelenen tüm istekler Authorization Bearer Token gerektirir.*
- **PUT /users/profile** : Kullanıcının boy, kilo, vb. metriklerini günceller. İstek gövdesinden ID atılmaz, token üzerinden tanınır.

## C. Workouts & Exercises (Antrenmanlar)
- **GET /workouts** : Oturum açmış kullanıcının tüm geçmiş antrenmanlarını listeler.
- **POST /workouts/exercises** : `workout_id` parametresi ile o antrenmana yeni bir egzersiz ekler. Yoksa antrenmanı da yaratır.
- **GET /exercises/{id}** : Yalnızca belirtilen exercise ID'sine sahip egzersizin iç detaylarını getirir.
- **DELETE /exercises/{id}** : Egzersizi kalıcı olarak siler ve ilgili antrenman ID'sinden düşer.
- **PUT /workouts/{id}/notes** : Belirli bir antrenmanın alt notlarını (Nasıl geçtiği vb.) günceller.
- **DELETE /workouts/{id}** : Bir antrenmanı VE o antrenmana bağlanmış tüm egzersizleri toplu bir şelide kalıcı olarak siler!

## D. Goals & Metrics (Hedefler ve Fiziksel Metrikler)
- **POST /goals** : Kullanıcı hesabı için yeni bir fiziksel hedef oluşturur.
- **DELETE /goals/{id}** : Ulaşılmış veya vazgeçilmiş bir hedefi sistemden kaldırır.
- **POST /metrics/weight** : Periyodik ağırlık veya fiziksel ölçü kayıtlarını zaman damgasıyla (timestamp) veritabanına işler.

## E. Artificial Intelligence (Yapay Zeka)
- **POST /ai/recommendations** : Mevcut egzersiz geçmişini kullanarak mantıklı bir mock JSON antreman programı döndürür. İleride OpenAI entegrasyonu ile aktifleşecektir.
