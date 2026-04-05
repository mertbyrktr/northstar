# Northstar Web Front-End Dokümantasyonu

---
https://northstar-nine-zeta.vercel.app/
---

Bu doküman, Northstar uygulamasının web arayüzünün (Web Front-End) mimari yapısını, kullanılan teknolojileri ve mantıksal akışını açıklamaktadır.

## Kullanılan Teknolojiler
- **HTML5 & Vanilla Javascript:** Herhangi bir ağır framework (Vue, React vb.) kullanılmadan, doğrudan modern, saf JavaScript ile performanslı ve hafif bir *Single Page Application (SPA)* inşa edilmiştir.
- **CSS3 (Glassmorphism Presibi):** Modern ve premium bir "Dark Mode" teması uygulanıp ekranların arka planına `backdrop-filter` verilerek buzlu cam (Glassmorphism) estetiği yansıtılmıştır. Ek olarak dinamik CSS animasyonları bulunmaktadır.
- **Chart.js:** Grafik çizimleri (Vücut Ağırlık geçmişi ve Egzersiz Performansı gelişimi) için projeye CDN aracılığıyla entegre edilen popüler grafik analiz kütüphanesidir.

## Mimari ve Dosya Yapısı (frontend/)
1. **`index.html`**
   - Uygulamanın tek yapısal giriş noktası ve DOM kalıbıdır. 
   - SPA mantığı içindeki farklı görünümler (Kimlik Doğrulama, Dashboard, Goals, Profile, Tracker) standart HTML `<section>` etiketleriyle bölünmüş ve JavaScript üzerinden `hidden` sınıfının kontrolü ile gizlenip gösterilmektedir.
   
2. **`style.css`**
   - Tüm tasarım bileşenlerini yöneten global CSS dosyasıdır.
   - Modülerlik adına CSS Degişkenleri (Örn: `--glass-bg`, `--primary-glow`) yapısı kurulmuştur.
   
3. **`js/api.js`**
   - Uygulamanın Backend ile (FastAPI) konuşan ana köprüsüdür. `fetch()` fonksiyonunu modüler sınıflar vasıtasıyla sararak asenkron REST HTTP isteklerini standart hale getirir. 
   - *JWT Bearer Token* yöntemi `localStorage` üzerinden doğrudan bu dosyanın içerisinde işlenir ve istek başlıklarına aktarılır.
   
4. **`js/app.js`**
   - Temel iş mantığını ve uygulama akışını yönetir (Event Listener'lar, DOM Data Inject, Zaman Dönüşümleri (UTC -> Local), Grafik verilerinin transformasyonu ve Modal açılıp kapanma aksiyonları).

## Temel Özellikler
- **Kimlik Doğrulama**: Gerçek zamanlı üyelik ve token kalıcılığı. 
- **Tracker**: Seçilen antrenman bağlamında veriler parse edilerek maksimum ağırlık (PR) gelişimi dinamik line grafiğinde gösterilir.
- **Profil Yönetimi**: Backend destekli kısımlardan bilgiyi alıp frontend DOM elementlerinde anlık render alır.
- **Goals (Hedefler)**: Hedeflere özgü üstü çizme (completion) toggle aksiyonları görsel bir dinamiklikle eklenmiştir.
