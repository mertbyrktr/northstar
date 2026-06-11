# Northstar Mobil Frontend Dokümantasyonu

Bu doküman, Northstar web arayüzünün Capacitor aracılığıyla iOS platformuna (ve genel mobil cihazlara) dönüştürülmesi sürecinde uygulanan mobil frontend tasarım ve geliştirme prensiplerini açıklamaktadır.

---

## 1. Temel Mobil Frontend Prensipleri

Web uygulamaları mobil cihazlarda (webview) çalıştırılırken, masaüstü tarayıcılardan farklı ekran yapıları ve kısıtlamalarla karşılaşır. Projemizde uyguladığımız temel mobil uyumluluk prensipleri şunlardır:

### A. Safe Area (Güvenli Alan) ve Çentik (Notch) Yönetimi
Yeni nesil mobil cihazlarda ekranın üst kısmında çentik (notch), alt kısmında ise ana ekran çizgisi (home indicator) yer alır. Web içeriğinin bu alanların altında kalarak tıklanamaz hale gelmesini önlemek için:
1. **Viewport Yapılandırması:** `index.html` içindeki meta viewport etiketine mutlaka `viewport-fit=cover` parametresi eklenmelidir. Bu parametre, webview'in tüm ekranı kaplamasını sağlar ve tarayıcıya güvenli alan sınırlarını bildirir.
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
   ```
2. **CSS Güvenli Alan Değişkenleri:** CSS tarafında, ekranın en üstündeki yapışkan (sticky) veya sabit (fixed) elemanların (örneğin `.navbar`) çentik ile çakışmaması için `env(safe-area-inset-top)` değişkeni kullanılarak dinamik dolgu eklenmelidir:
   ```css
   padding-top: calc(1.5rem + env(safe-area-inset-top, 0px));
   ```

### B. Dinamik Çalışma Ortamı ve API URL Tespiti
Mobil uygulamanın yerel geliştirme aşamalarında canlı sunucu yerine kendi Mac'inizdeki yerel sunucuya (`localhost:8000`) bağlanması gerekebilir.
* **Protokol ve Port Kontrolü:** `window.Capacitor` yüklenmeden önce bile uygulamanın mobil webview'de olduğunu anlamak için URL protokolü (`capacitor:`) veya port numarasının boş olması (`window.location.port === ''`) kontrol edilir.
* **localStorage Overrides:** Mobil uygulama içindeyken API adresini değiştirebilmek amacıyla, `localStorage` üzerinde bir override anahtarı (`northstar_api_url`) aranır. Bu sayede uygulamanın tekrar derlenmesine gerek kalmadan geliştirici konsolu üzerinden canlı/yerel geçişleri yapılabilir.

### C. Derleme (Build) ve Paket Optimizasyonu
Capacitor, web klasöründeki dosyaları doğrudan mobil uygulamanın içine gömer.
* **Gereksiz Dosyaların Temizlenmesi:** Projede kullanılan geliştirme bağımlılıklarının (`node_modules/`, `package.json`, yapılandırma dosyaları vb.) mobil pakete girerek uygulamanın boyutunu megabaytlarca şişirmesini önlemek için bir derleme (build) scripti kullanılır.
* **Temiz Dağıtım Klasörü (`dist`):** `npm run build` komutu çalıştırılarak sadece uygulamanın çalışması için gerekli olan statik kaynaklar (`index.html`, `style.css`, `js/`) `dist/` klasörüne kopyalanır ve Capacitor sadece bu klasörü (`webDir: "dist"`) mobil projeyle eşitler.

### D. Dokunma Alanları (Touch Targets) ve Mobil UX
* **Buton ve Menü Boyutları:** Mobil cihazlarda kullanıcıların parmakla rahatça etkileşime girebilmesi için tıklanabilir tüm öğelerin dokunma alanları (touch targets) en az **44x44 piksel** boyutunda olacak şekilde ayarlanmalıdır. Sekmeler ve navigasyon butonlarındaki `padding` değerleri bu kurala göre optimize edilmiştir.
* **Scroll Davranışı:** Mobil cihazlarda kaydırma hissinin akıcı olması için uzun listelerde ivmeli kaydırma (momentum scrolling) özellikleri kontrol edilmelidir.

### E. Ağ Hataları ve Konsol Logları Yönetimi
* **Failed to Fetch Durumları:** Mobil cihazlar internet bağlantısını kaybedebilir veya sunucu kapalı olabilir. API istekleri başarısız olduğunda oluşan `TypeError: Failed to Fetch` hataları yakalanarak kullanıcıya boş ekran yerine anlamlı uyarılar gösterilmelidir.
* **Hata Nesnelerinin Stringify Edilmesi:** JavaScript'te `Error` nesnesinin özellikleri varsayılan olarak non-enumerable (sıralanamaz) olduğu için `JSON.stringify(error)` yapıldığında boş bir obje (`{}`) döner. Konsolda hatayı doğru görebilmek için hata nesnesinin doğrudan kendisi loglanmalı veya `error.message` özelliği yazdırılmalıdır.

### F. Farklı Ekran Boyutları ve Yatay Mod (Landscape) Uyumluluğu
Mobil cihazlar dik (portrait) veya yatay (landscape) konumda kullanılabilir; ayrıca farklı ekran en-boy oranlarına (tabletler, katlanabilir telefonlar, SE modelleri) sahiptir.
* **Esnek ve Grid Tabanlı Düzenler:** Arayüz bileşenlerinde piksel bazlı sabit genişlikler yerine CSS Flexbox ve CSS Grid (`grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))`) tercih edilmiştir. Bu sayede ekran genişlediğinde antrenman kartları otomatik olarak yan yana dizilir, küçük ekranlarda ise alt alta hizalanarak taşmaları önler.
* **Yatay Mod (Landscape Mode) Algılaması:** Cihaz yan yatırıldığında çentik sola veya sağa geçer. Bu durumda içeriğin çentik altında ezilmemesi için yan kenar boşlukları (`5%` veya `env(safe-area-inset-left)`) dinamik olarak sol ve sağ taraflara uygulanır. 
* **Grafiklerin (Charts) Ölçeklenmesi:** Chart.js grafikleri (`progressChart`, `volumeChart`, `weightChart`), yatay ve dikey mod geçişlerinde en-boy oranını koruyacak (`responsive: true` ve `maintainAspectRatio: false` ile sarılmış container) şekilde yapılandırılmıştır. Böylece cihaz yatay moda geçtiğinde grafikler ekranı kaplayarak daha geniş bir analiz alanı sunar.
* **Görsel Ölçekleme (Zoom) Engellemesi:** Çift tıklamada veya yatay-dikey yön değişimlerinde webview'in otomatik yakınlaştırma yapmasını ve sayfa boyutunun bozularak kaymasını önlemek için `viewport` etiketine `maximum-scale=1.0, user-scalable=no` özellikleri eklenmiş ve CSS `body` seçicisine `touch-action: manipulation;` kuralı getirilmiştir. Bu sayede çift tıklama ve rotasyon kaynaklı kaymalar engellenmiştir.
* **Yatay Taşma (Horizontal Overflow) ve Kaydırma Çözümleri:** Sayfanın sağa doğru gereksiz kaymasını ve boş beyaz alanlar çıkmasını önlemek için üç kademeli çözüm uygulanmıştır:
  1. `html` ve `body` elemanlarına genişlik sınırlamaları (`width: 100%`, `max-width: 100%`, `overflow-x: hidden`) eklenmiştir.
  2. Ekran dışına taşan dekoratif arka plan balonları (`.blob`), `position: fixed` ve `overflow: hidden` özellikli bağımsız bir `.bg-wrapper` kapsayıcısı içine alınarak sayfa genişliğini etkilemesi engellenmiştir.
  3. Mobil portre modunda yan yana sığmayan menü butonları (`.nav-links`), ana ekranı yatayda kaydırmak yerine kendi içinde taşarak yana kaydırılabilir (`overflow-x: auto`, `-webkit-overflow-scrolling: touch`) hale getirilmiş ve scrollbar gizlenmiştir.



