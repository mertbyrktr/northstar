# REST API Tasarımı

Northstar Gym Tracker uygulamasının REST API'si, modern, hızlı ve asenkron web uygulamaları geliştirmek için ideal olan **Python 3 ve FastAPI** kullanılarak tasarlanmıştır.

## 1. Mimari Seçimler
- **Web Framework:** FastAPI (Uvicorn ASGI sunucusu üzerinde koşar)
- **Veritabanı:** MongoDB Atlas (Cloud)
- **Veritabanı Sürücüsü:** `motor` (Asenkron PyMongo etkileşimi için)
- **Veri Validasyonu:** `pydantic` (Gelen istek gövdelerinin doğrulanması için modeller)

## 2. Kimlik Doğrulama ve Güvenlik
- API uç noktaları, endüstri standardı olan **JWT (JSON Web Token)** kullanılarak korunmaktadır.
- İstemci `POST /auth/login` isteği göndererek bir Access Token alır.
- Güvenli sayfalarda (Hedef ekleme, egzersiz silme vb.) isteklerin `Authorization` başlığında `Bearer <token>` olarak bu token'ın gönderilmesi mecburidir.
- Şifreler veritabanına düz metin olarak kaydedilmez. **Bcrypt** algoritması ile tuzlanarak hashlenir.

## 3. RESTful Prensipler
- API tasarımı katı REST standartlarına uyar:
  - Veri getirmek için `GET`, 
  - Veri oluşturmak için `POST`, 
  - Kısmi güncelleme veya tamamen değiştirme için `PUT/PATCH`, 
  - Veri silmek için `DELETE` metodları kullanılmıştır.
- Tüm `_id` değerleri dışarıya, frontend tarafında rahat kullanılabilmesi için standart 24 karakterlik String tabanlı `id` objelerine dönüştürülür.
