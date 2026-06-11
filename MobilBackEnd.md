# Northstar Mobil Backend Dokümantasyonu

Bu doküman, Northstar mobil uygulamasının backend entegrasyonu, REST API adresleri ve mobil istemcilerle çalışan backend sistemlerinin sahip olması gereken genel tasarım prensiplerini açıklamaktadır.

---

## 1. REST API Adresleri

Mobil uygulama ortamlarında (iOS WKWebView / Android WebView) relative (görece) yollar çalışmadığı için, API isteklerinde mutlak (absolute) URL'ler kullanılır.

### Canlı Sunucu (Production)
Uygulamanın Vercel üzerinde barındırılan canlı API kök adresi:
* **API URL:** `https://northstar-nine-zeta.vercel.app/api/v1`
* **Dokümantasyon (Swagger):** `https://northstar-nine-zeta.vercel.app/api/docs`

### Yerel Geliştirme Sunucusu (Local Development)
Backend yerel ortamda uvicorn ile `0.0.0.0` hostu üzerinde çalıştırıldığında erişim yolları:
* **iOS Simulator (Mac Üzerinde):** `http://localhost:8000/api/v1` veya `http://127.0.0.1:8000/api/v1`
* **Fiziksel iPhone (Aynı Wi-Fi):** `http://<MAC-IP-ADRESINIZ>:8000/api/v1` (Örn: `http://192.168.1.100:8000/api/v1`)

---

## 2. Genel Mobil Backend Prensipleri

Mobil istemciler (native uygulamalar veya hibrit webview'ler) standart web tarayıcılarından farklı güvenlik ve ağ kısıtlamalarına tabidir. Mobil cihazlarla haberleşen bir backend tasarlanırken aşağıdaki prensipler uygulanmalıdır:

### A. CORS (Cross-Origin Resource Sharing) ve Origin Yönetimi
Hibrit mobil çerçeveler (Capacitor vb.) web kodunu yerel bir protokolden çalıştırır.
* **iOS Origin:** `capacitor://localhost`
* **Android Origin:** `http://localhost`

**Önemli CORS Kuralı:**
FastAPI (Starlette) gibi modern backend framework'lerinde, `allow_credentials=True` ayarlandığında, güvenlik gereği `allow_origins=["*"]` (wildcard) kullanımına izin verilmez. 
* JWT (Bearer Token) tabanlı kimlik doğrulama yapıldığında çerez (cookie) gönderilmediği için backend tarafında `allow_credentials=False` yapılmalı veya izin verilen mobil origin'ler açıkça tanımlanmalıdır.

### B. Güvenli İletişim (HTTPS) ve ATS Kısıtlamaları
* **HTTPS Zorunluluğu:** Apple'ın ATS (App Store Transport Security) protokolü ve Android'in Network Security yapılandırması, mobil uygulamaların HTTP üzerinden güvensiz veri alışverişi yapmasını varsayılan olarak engeller.
* Canlı yayına çıkacak tüm mobil backend'lerin geçerli bir SSL sertifikasına sahip olması ve isteklerin HTTPS protokolü üzerinden yapılması zorunludur.

### C. Stateless (Durumsuz) Kimlik Doğrulama (JWT)
* Mobil uygulamalar, tarayıcılardaki gibi oturum çerezlerini (sessions / cookies) yerel olarak yönetmekte zorlanabilir.
* Bu nedenle mobil backend tasarımlarında **JWT (JSON Web Token)** gibi token tabanlı stateless mekanizmalar tercih edilmelidir. İstemci token'ı güvenli yerel depolama alanında (`localStorage` veya `Keychain/SharedPreferences`) saklar ve backend isteklerinde `Authorization: Bearer <token>` başlığı ile iletir.

### D. Sıfır Güven (Zero-Trust) ve Veri Yalıtımı (Data Isolation)
* İstemciden gelen isteklere asla körü körüne güvenilmemelidir.
* Örneğin; bir egzersiz silme isteğinde (`/exercises/{id}`), backend sadece ID'yi silmekle kalmamalı, isteği yapan JWT token içerisinden çözülen `user_id` ile silinmek istenen verinin sahibini karşılaştırarak doğrulamalıdır. Northstar backend mimarisinde bu izolasyon her rotada zorunlu kılınmıştır.

### E. Dinamik IP / Sunucu Tespiti
* Mobil uygulamalar sürekli değişen ağlara (Wi-Fi, 4G/5G) bağlanır. 
* Backend ve frontend entegrasyonunda, API adresinin hardcoded (sabit kodlanmış) olması yerine, mobil uygulamanın çalışma anındaki ortama göre (yerel IP veya canlı Vercel sunucusu) dinamik olarak adres seçebilmesine imkan tanınmalıdır.
