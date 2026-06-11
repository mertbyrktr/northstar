# Ahmet Mert Bayraktar - Mobil Frontend Görevleri

## Tamamlanan Özellikler ve Geliştirmeler

**1. Proje Altyapısı ve Capacitor Entegrasyonu:**
- [x] `frontend/` dizini altında `package.json` oluşturularak npm altyapısı kuruldu.
- [x] Capacitor core, CLI ve iOS kütüphaneleri (`@capacitor/core`, `@capacitor/cli`, `@capacitor/ios`) projeye kuruldu.
- [x] Projenin adı `"Northstar"`, paket ID'si `"com.northstar.gymtracker"` olacak şekilde `capacitor.config.json` oluşturuldu.

**2. Derleme (Build) Süreci:**
- [x] `node_modules/` klasörünün iOS native uygulamasına kopyalanıp paket boyutunu şişirmesini engellemek için `build.js` derleme scripti yazıldı.
- [x] Sadece gerekli web varlıklarının (`index.html`, `style.css`, `js/`) `dist/` klasörüne kopyalanması sağlandı.
- [x] `.gitignore` dosyası güncellenerek `node_modules/`, `dist/` ve `ios/` klasörleri git dışı bırakıldı.

**3. iOS Native Entegrasyonu (Xcode & CocoaPods):**
- [x] Mac işletim sistemi üzerinde eksik olan CocoaPods aracı Homebrew (`brew install cocoapods`) ile kuruldu.
- [x] `npx cap add ios` ile Xcode projesi oluşturuldu.
- [x] `npx cap sync ios` ve `npx cap open ios` ile web varlıkları başarıyla senkronize edilerek Xcode workspace projesi açıldı.

**4. Ekran Çentiği (Notch) ve Safe Area Uyumluluğu:**
- [x] `index.html` içerisindeki viewport etiketine `viewport-fit=cover` parametresi eklenerek webview içerisinde Safe Area CSS değişkenlerinin (`env()`) çalışması sağlandı.
- [x] Çentikli ekranlarda (örn. iPhone 13) sekmelerin çentik altında kalarak tıklanamaz duruma gelmesini önlemek amacıyla üst menüye (`.navbar`) dinamik üst boşluk (padding) uygulandı:
  ```css
  padding-top: calc(1.5rem + env(safe-area-inset-top, 0px));
  ```

**5. Sayfa Boyutu ve Kayma (Zoom / Horizontal Overflow) Düzeltmeleri:**
- [x] Çift tıklamada veya yön değişiminde (yatay/dikey) webview'in kendi kendine zoom yaparak ekran düzenini bozmasını engellemek için `maximum-scale=1.0, user-scalable=no` ve `touch-action: manipulation;` kuralları eklendi.
- [x] Arka plan balonlarının (`.blob`) ekran dışına taşarak yatayda gereksiz kaydırma alanları oluşturması, balonlar `fixed` konumlu ve `overflow: hidden` özellikli bir `.bg-wrapper` içine alınarak düzeltildi.
- [x] Mobil portre modunda yan yana sığmayan menü butonlarının (`.nav-links`) ana sayfayı yatayda kaydırması engellendi; menü butonları kendi içerisinde kaydırılabilir (`overflow-x: auto`) mobil sekmeli bar tasarımına dönüştürüldü.

**6. Çalışma Ortamı ve Dinamik API URL Tespiti:**
- [x] Tarayıcı, yerel simülatör ve fiziksel mobil cihazları ayırt edebilen API URL tespiti kuruldu.
- [x] Mobil uygulama içindeyken yerel testler için `localStorage.getItem('northstar_api_url')` değeri kullanılarak uygulamanın kodunu değiştirmeden canlı veya yerel backend sunucuları arasında geçiş yapabilmesi sağlandı.
