# NORTHSTAR GYM TRACKER

![Product image](Product.png)

Northstar is an app for tracking your gym activites, your best PR's and getting an AI overview of your latest activity.
This project uses **FastAPI, Async MongoDB (Motor)** for a highly concurrent backend, alongside a natively-built **Vanilla JavaScript** Web front-end utilizing a modern, "Glassmorphism" aesthetic with integrated **Chart.js** visuals.

---

## Proje Linkleri

REST API Adresi: https://northstar-nine-zeta.vercel.app/api/docs

Web Front-End Adresi: https://northstar-nine-zeta.vercel.app/

---

**Proje Kategorisi:** 
Kişisel gelişim takip uygulaması

---

## Backend Özellikleri (FastAPI)
- **Kimlik Doğrulama:** JWT (JSON Web Tokens) tabanlı güvenli giriş ve kayıt sistemi (OAuth2PasswordBearer).
- **CRUD Operasyonları:** Antrenman, Egzersiz, Hedef ve Kilo takibi verilerinin veritabanında asenkron motorlar (Motor) ile güvenli rotalar üzerinden işlenmesi.
- **İleri Seviye Uç Noktalar (Endpoints):** Profil bilgilerini okuma/güncelleme, API aracılığıyla geçmiş verilerin alınması, tam/kısmi güncellemeler (hedef toggling vb.).
- **Data Isolation:** Tüm veritabanı sorguları JWT ile çözülen dinamik kullanıcı kimliğine (user_id) dayalı olacak şekilde tamamen yalıtılmış olup, zero-trust prensibi uygulanmıştır.

---

## Proje Ekibi

**Grup Adı:** 
Northstar

**Ekip Üyeleri:** 
- Ahmet Mert Bayraktar

---

## Dokümantasyon

Proje dokümantasyonuna aşağıdaki linklerden erişebilirsiniz:

1. [Gereksinim Analizi](Gereksinim-Analizi.md)
2. [REST API Tasarımı](API-Tasarimi.md)
3. [REST API](Rest-API.md)
4. [Web Front-End](WebFrontEnd.md)
5. [Mobil Front-End](MobilFrontEnd.md)
6. [Mobil Backend](MobilBackEnd.md)
7. [Video Sunum](Sunum.md)

---

