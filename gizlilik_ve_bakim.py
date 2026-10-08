# -*- coding: utf-8 -*-
"""
mobilcv.net - Gizlilik politikası + bakım scripti
Deponun KÖK klasöründe çalıştırın:   python gizlilik_ve_bakim.py
(Blog botu her çalıştığında da otomatik çalıştırılabilir; tekrar çalıştırmak zararsızdır.)

Yaptıkları:
 1) 10 dilde gizlilik politikası sayfası oluşturur:
      gizlilik-politikasi.html, en/privacy-policy.html, de/privacy-policy.html ... zh/privacy-policy.html
 2) Tüm sayfaların alt kısmına (footer) o dildeki gizlilik politikası linkini ekler.
 3) İletişim formlarını (iletisim.html, en/contact.html) çalışır hale getirir (Formspree).
    "Bu form şu an sadece görseldir" yazan ikinci, çalışmayan formu kaldırır.
 4) Makalelerdeki çalışmayan "Abone Ol" (bülten) kutusunu kaldırır.
 5) Gizlilik sayfalarını sitemap.xml'e ekler.
"""
import re
from datetime import date
from pathlib import Path

NET = "https://mobilcv.net"
COM = "https://www.mobilcv.com"
FORMSPREE = "https://formspree.io/f/movkoozp"
CONTACT = "info@mobilcv.com"
UPDATED = date(2026, 10, 8)

# Dil -> (sayfa yolu, link etiketi, ana site etiketi, blog etiketi, başlık, son güncelleme etiketi, tarih formatı)
LANGS = {
    "tr": dict(path="gizlilik-politikasi.html", label="Gizlilik Politikası", home="Ana Site", blog="Blog",
               updated="Son güncelleme", date="8 Ekim 2026", rtl=False, com=f"{COM}/", net=f"{NET}/"),
    "en": dict(path="en/privacy-policy.html", label="Privacy Policy", home="Homepage", blog="Blog",
               updated="Last updated", date="8 October 2026", rtl=False),
    "de": dict(path="de/privacy-policy.html", label="Datenschutzerklärung", home="Startseite", blog="Blog",
               updated="Zuletzt aktualisiert", date="8. Oktober 2026", rtl=False),
    "fr": dict(path="fr/privacy-policy.html", label="Politique de confidentialité", home="Accueil", blog="Blog",
               updated="Dernière mise à jour", date="8 octobre 2026", rtl=False),
    "es": dict(path="es/privacy-policy.html", label="Política de privacidad", home="Inicio", blog="Blog",
               updated="Última actualización", date="8 de octubre de 2026", rtl=False),
    "it": dict(path="it/privacy-policy.html", label="Informativa sulla privacy", home="Home", blog="Blog",
               updated="Ultimo aggiornamento", date="8 ottobre 2026", rtl=False),
    "pt": dict(path="pt/privacy-policy.html", label="Política de privacidade", home="Início", blog="Blog",
               updated="Última atualização", date="8 de outubro de 2026", rtl=False),
    "ru": dict(path="ru/privacy-policy.html", label="Политика конфиденциальности", home="Главная", blog="Блог",
               updated="Последнее обновление", date="8 октября 2026 г.", rtl=False),
    "ar": dict(path="ar/privacy-policy.html", label="سياسة الخصوصية", home="الرئيسية", blog="المدونة",
               updated="آخر تحديث", date="8 أكتوبر 2026", rtl=True),
    "zh": dict(path="zh/privacy-policy.html", label="隐私政策", home="首页", blog="博客",
               updated="最后更新", date="2026年10月8日", rtl=False),
}
for code, d in LANGS.items():
    d.setdefault("com", f"{COM}/{code}/")
    d.setdefault("net", f"{NET}/{code}/")
    d["url"] = f"{NET}/{d['path']}"

# ---------------------------------------------------------------------------
# METİNLER  (her bölüm: (başlık, html))
# ---------------------------------------------------------------------------
M = CONTACT
TEXT = {
"tr": [
 ("Kısaca", "<p>MobilCV, üyelik gerektirmeyen ücretsiz bir CV oluşturma aracıdır (<a href=\"https://www.mobilcv.com\">mobilcv.com</a>) ve bir kariyer blogudur (mobilcv.net). <strong>CV'nize yazdığınız bilgiler sunucularımıza gönderilmez ve tarafımızca saklanmaz.</strong> Reklam göstermiyoruz ve kişisel verileri satmıyoruz.</p>"),
 ("Veri sorumlusu", f"<p>MobilCV, İlhan Taşan tarafından geliştirilen bağımsız bir projedir. Gizlilikle ilgili tüm sorularınız için: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("CV bilgileriniz", "<p>Ad, iletişim bilgileri, fotoğraf, deneyim gibi CV'ye girdiğiniz tüm bilgiler <strong>yalnızca kendi cihazınızda, tarayıcınızın yerel depolama alanında</strong> tutulur. Böylece sayfayı kapatıp açtığınızda kaldığınız yerden devam edebilirsiniz. PDF dosyası da tamamen tarayıcınızda oluşturulur. Bu bilgilere biz erişemeyiz.</p><ul><li>Bilgilerinizi silmek için araçtaki <strong>Tümünü Temizle</strong> düğmesini kullanabilir veya tarayıcınızın site verilerini silebilirsiniz.</li><li>Ortak kullanılan bir bilgisayardaysanız işiniz bitince bilgilerinizi silmenizi öneririz.</li><li><strong>Yedekle</strong> düğmesi bilgilerinizi bir dosya olarak sizin cihazınıza indirir; bu dosya bize gönderilmez.</li><li><strong>Paylaş</strong> düğmesi PDF'inizi cihazınızın kendi paylaşım menüsüne iletir; paylaşımı siz yaparsınız.</li></ul>"),
 ("Kullandığımız üçüncü taraf hizmetler", "<ul><li><strong>Google Analytics</strong> (yalnızca mobilcv.com): Ziyaretçi sayısını ve hangi sayfaların kullanıldığını anlamak için anonim kullanım istatistikleri toplar (ör. cihaz türü, yaklaşık konum, ziyaret edilen sayfa). Bunun için çerez kullanır. CV içeriğiniz Google Analytics'e gönderilmez.</li><li><strong>Tawk.to</strong> (yalnızca mobilcv.com): Canlı destek penceresini sağlar. Pencerenin çalışması için çerez kullanır ve teknik bilgiler (ör. tarayıcı, yaklaşık konum) işleyebilir. Sohbet başlatırsanız yazdığınız mesajlar bu hizmet üzerinden bize ulaşır.</li><li><strong>Formspree</strong>: Geri bildirim ve iletişim formlarında yazdığınız mesaj ile isteğe bağlı olarak verdiğiniz ad ve e-posta adresi bu hizmet aracılığıyla e-posta kutumuza iletilir.</li><li><strong>GitHub Pages</strong>: Sitelerimiz bu hizmette barındırılır. Barındırma sağlayıcısı, güvenlik amacıyla erişim kayıtları (ör. IP adresi) tutabilir.</li><li><strong>İçerik dağıtım ağları</strong> (cdnjs, flagcdn): Sayfanın çalışması için gereken kod dosyaları ve bayrak görselleri bu sunuculardan yüklenir; bu sırada IP adresiniz teknik olarak bu sağlayıcılara iletilir.</li></ul><p>Bu hizmet sağlayıcıları verileri Türkiye dışındaki sunucularda işleyebilir.</p>"),
 ("Çerezler", "<p>Çerezleri yalnızca yukarıda belirtilen Google Analytics ve Tawk.to hizmetleri kullanır; CV aracının kendisi çalışmak için çerez gerektirmez. Çerezleri tarayıcı ayarlarınızdan engelleyebilir veya silebilirsiniz. Google Analytics ölçümünü engellemek için Google'ın resmi <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">devre dışı bırakma eklentisini</a> kullanabilirsiniz.</p>"),
 ("Saklama süresi", "<p>CV bilgileriniz siz silene kadar yalnızca cihazınızda kalır. Bize e-posta veya form yoluyla gönderdiğiniz mesajları yalnızca yanıt vermek için gerektiği süre boyunca saklarız. Kullanım istatistikleri Google Analytics'in saklama ayarlarına göre sınırlı süre tutulur.</p>"),
 ("Haklarınız", f"<p>6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) ve bulunduğunuz ülkenin mevzuatı (ör. AB'de GDPR) kapsamında; hakkınızda veri işlenip işlenmediğini öğrenme, bu verilere erişme, düzeltilmesini veya silinmesini isteme ve işlemeye itiraz etme haklarına sahipsiniz. Taleplerinizi <a href=\"mailto:{M}\">{M}</a> adresine iletebilirsiniz. Ayrıca yetkili veri koruma kurumuna (Türkiye'de Kişisel Verileri Koruma Kurumu) şikâyette bulunma hakkınız saklıdır.</p>"),
 ("Değişiklikler", "<p>Bu politikayı zaman zaman güncelleyebiliriz. Güncel sürüm her zaman bu sayfada yayımlanır.</p>"),
],
"en": [
 ("In short", "<p>MobilCV is a free CV builder that requires no sign-up (<a href=\"https://www.mobilcv.com/en/\">mobilcv.com</a>) and a career blog (mobilcv.net). <strong>The information you enter in your CV is not sent to our servers and is not stored by us.</strong> We do not show ads and we do not sell personal data.</p>"),
 ("Who is responsible", f"<p>MobilCV is an independent project developed by İlhan Taşan. For any privacy questions, contact: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("Your CV information", "<p>Everything you enter in your CV (name, contact details, photo, experience, etc.) is kept <strong>only on your own device, in your browser's local storage</strong>, so you can continue where you left off. The PDF is also created entirely in your browser. We cannot access this information.</p><ul><li>To delete your information, use the <strong>Clear All</strong> button in the tool or clear your browser's site data.</li><li>If you are using a shared computer, we recommend deleting your information when you are done.</li><li>The <strong>Download Backup</strong> button saves your data as a file on your own device; this file is not sent to us.</li><li>The <strong>Share</strong> button passes your PDF to your device's own share menu; you decide where it goes.</li></ul>"),
 ("Third-party services we use", "<ul><li><strong>Google Analytics</strong> (mobilcv.com only): collects anonymous usage statistics (e.g. device type, approximate location, pages visited) to help us understand how the site is used. It uses cookies. Your CV content is never sent to Google Analytics.</li><li><strong>Tawk.to</strong> (mobilcv.com only): provides the live chat window. It uses cookies and may process technical information (e.g. browser, approximate location). If you start a chat, your messages reach us through this service.</li><li><strong>Formspree</strong>: messages you send through our feedback and contact forms, together with the name and email address you optionally provide, are delivered to our inbox through this service.</li><li><strong>GitHub Pages</strong>: our websites are hosted here. The hosting provider may keep access logs (e.g. IP addresses) for security purposes.</li><li><strong>Content delivery networks</strong> (cdnjs, flagcdn): code files and flag images needed by the page are loaded from these servers, which technically receive your IP address.</li></ul><p>These providers may process data on servers outside your country.</p>"),
 ("Cookies", "<p>Cookies are used only by Google Analytics and Tawk.to as described above; the CV tool itself does not need cookies to work. You can block or delete cookies in your browser settings. To opt out of Google Analytics, you can use Google's official <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">opt-out browser add-on</a>.</p>"),
 ("How long data is kept", "<p>Your CV information stays only on your device until you delete it. Messages you send us by email or form are kept only as long as needed to reply. Usage statistics are kept for a limited period according to Google Analytics retention settings.</p>"),
 ("Your rights", f"<p>Depending on where you live (for example under the EU GDPR or Turkey's KVKK), you have the right to know whether we process data about you, to access it, to request its correction or deletion, and to object to its processing. Send your request to <a href=\"mailto:{M}\">{M}</a>. You also have the right to lodge a complaint with your local data protection authority.</p>"),
 ("Changes", "<p>We may update this policy from time to time. The current version is always published on this page.</p>"),
],
"de": [
 ("Kurz gesagt", "<p>MobilCV ist ein kostenloser Lebenslauf-Generator ohne Anmeldung (<a href=\"https://www.mobilcv.com/de/\">mobilcv.com</a>) und ein Karriere-Blog (mobilcv.net). <strong>Die Angaben in Ihrem Lebenslauf werden nicht an unsere Server übertragen und nicht von uns gespeichert.</strong> Wir zeigen keine Werbung und verkaufen keine personenbezogenen Daten.</p>"),
 ("Verantwortlicher", f"<p>MobilCV ist ein unabhängiges Projekt von İlhan Taşan. Bei Fragen zum Datenschutz: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("Ihre Lebenslaufdaten", "<p>Alle Angaben in Ihrem Lebenslauf (Name, Kontaktdaten, Foto, Berufserfahrung usw.) werden <strong>ausschließlich auf Ihrem eigenen Gerät im lokalen Speicher Ihres Browsers</strong> gespeichert, damit Sie später weitermachen können. Auch das PDF wird vollständig in Ihrem Browser erstellt. Wir haben keinen Zugriff auf diese Daten.</p><ul><li>Zum Löschen nutzen Sie die Schaltfläche <strong>Alles löschen</strong> oder löschen Sie die Websitedaten in Ihrem Browser.</li><li>Auf gemeinsam genutzten Computern empfehlen wir, Ihre Daten nach der Nutzung zu löschen.</li><li>Die Funktion <strong>Backup herunterladen</strong> speichert Ihre Daten als Datei auf Ihrem Gerät; diese Datei wird nicht an uns gesendet.</li><li>Die Funktion <strong>Teilen</strong> übergibt Ihr PDF an das Teilen-Menü Ihres Geräts; Sie entscheiden, wohin es geht.</li></ul>"),
 ("Eingesetzte Drittanbieter", "<ul><li><strong>Google Analytics</strong> (nur mobilcv.com): erfasst anonyme Nutzungsstatistiken (z. B. Gerätetyp, ungefährer Standort, besuchte Seiten) und verwendet dafür Cookies. Ihre Lebenslaufinhalte werden nie an Google Analytics übertragen.</li><li><strong>Tawk.to</strong> (nur mobilcv.com): stellt das Live-Chat-Fenster bereit, verwendet Cookies und kann technische Informationen (z. B. Browser, ungefährer Standort) verarbeiten. Wenn Sie einen Chat starten, erreichen uns Ihre Nachrichten über diesen Dienst.</li><li><strong>Formspree</strong>: Nachrichten aus unseren Feedback- und Kontaktformularen sowie optional angegebener Name und E-Mail-Adresse werden über diesen Dienst an unser Postfach weitergeleitet.</li><li><strong>GitHub Pages</strong>: Hosting unserer Websites. Der Anbieter kann aus Sicherheitsgründen Zugriffsprotokolle (z. B. IP-Adressen) speichern.</li><li><strong>Content-Delivery-Netzwerke</strong> (cdnjs, flagcdn): Von dort werden benötigte Code-Dateien und Flaggenbilder geladen; dabei wird Ihre IP-Adresse technisch übermittelt.</li></ul><p>Diese Anbieter können Daten auf Servern außerhalb Ihres Landes verarbeiten.</p>"),
 ("Cookies", "<p>Cookies werden nur von Google Analytics und Tawk.to verwendet; das Lebenslauf-Tool selbst benötigt keine Cookies. Sie können Cookies in Ihren Browsereinstellungen blockieren oder löschen. Google Analytics können Sie mit dem offiziellen <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">Browser-Add-on zur Deaktivierung</a> abschalten.</p>"),
 ("Speicherdauer", "<p>Ihre Lebenslaufdaten bleiben nur auf Ihrem Gerät, bis Sie sie löschen. Nachrichten an uns bewahren wir nur so lange auf, wie es für eine Antwort nötig ist. Nutzungsstatistiken werden gemäß den Aufbewahrungseinstellungen von Google Analytics für einen begrenzten Zeitraum gespeichert.</p>"),
 ("Ihre Rechte", f"<p>Nach der DSGVO haben Sie das Recht auf Auskunft, Berichtigung, Löschung und Widerspruch gegen die Verarbeitung Ihrer Daten. Senden Sie Ihre Anfrage an <a href=\"mailto:{M}\">{M}</a>. Zudem können Sie sich bei der zuständigen Datenschutzaufsichtsbehörde beschweren.</p>"),
 ("Änderungen", "<p>Wir können diese Erklärung gelegentlich aktualisieren. Die aktuelle Fassung finden Sie immer auf dieser Seite.</p>"),
],
"fr": [
 ("En bref", "<p>MobilCV est un outil gratuit de création de CV sans inscription (<a href=\"https://www.mobilcv.com/fr/\">mobilcv.com</a>) et un blog carrière (mobilcv.net). <strong>Les informations saisies dans votre CV ne sont pas envoyées à nos serveurs et ne sont pas conservées par nous.</strong> Nous n'affichons pas de publicité et ne vendons pas de données personnelles.</p>"),
 ("Responsable du traitement", f"<p>MobilCV est un projet indépendant développé par İlhan Taşan. Pour toute question relative à la confidentialité : <a href=\"mailto:{M}\">{M}</a></p>"),
 ("Les informations de votre CV", "<p>Tout ce que vous saisissez (nom, coordonnées, photo, expérience, etc.) est conservé <strong>uniquement sur votre appareil, dans le stockage local de votre navigateur</strong>, afin que vous puissiez reprendre plus tard. Le PDF est lui aussi créé entièrement dans votre navigateur. Nous n'avons pas accès à ces informations.</p><ul><li>Pour les supprimer, utilisez le bouton <strong>Tout effacer</strong> ou effacez les données du site dans votre navigateur.</li><li>Sur un ordinateur partagé, nous vous conseillons de supprimer vos informations après utilisation.</li><li>Le bouton <strong>Sauvegarder</strong> enregistre vos données dans un fichier sur votre appareil ; ce fichier ne nous est pas envoyé.</li><li>Le bouton <strong>Partager</strong> transmet votre PDF au menu de partage de votre appareil ; c'est vous qui choisissez le destinataire.</li></ul>"),
 ("Services tiers utilisés", "<ul><li><strong>Google Analytics</strong> (mobilcv.com uniquement) : collecte des statistiques d'utilisation anonymes (type d'appareil, localisation approximative, pages consultées) à l'aide de cookies. Le contenu de votre CV n'est jamais transmis à Google Analytics.</li><li><strong>Tawk.to</strong> (mobilcv.com uniquement) : fournit la fenêtre de discussion en direct, utilise des cookies et peut traiter des informations techniques (navigateur, localisation approximative). Si vous lancez une discussion, vos messages nous parviennent via ce service.</li><li><strong>Formspree</strong> : les messages envoyés via nos formulaires de contact et de retour, ainsi que le nom et l'adresse e-mail fournis facultativement, sont transmis à notre boîte de réception par ce service.</li><li><strong>GitHub Pages</strong> : hébergement de nos sites. L'hébergeur peut conserver des journaux d'accès (adresses IP, par ex.) à des fins de sécurité.</li><li><strong>Réseaux de diffusion de contenu</strong> (cdnjs, flagcdn) : les fichiers de code et images de drapeaux nécessaires y sont chargés ; votre adresse IP leur est techniquement transmise.</li></ul><p>Ces prestataires peuvent traiter des données sur des serveurs situés hors de votre pays.</p>"),
 ("Cookies", "<p>Seuls Google Analytics et Tawk.to utilisent des cookies ; l'outil de CV lui-même n'en a pas besoin. Vous pouvez bloquer ou supprimer les cookies dans les paramètres de votre navigateur et désactiver Google Analytics avec le <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">module officiel de désactivation</a>.</p>"),
 ("Durée de conservation", "<p>Les informations de votre CV restent sur votre appareil jusqu'à ce que vous les supprimiez. Les messages que vous nous envoyez ne sont conservés que le temps nécessaire pour y répondre. Les statistiques d'utilisation sont conservées pour une durée limitée selon les paramètres de Google Analytics.</p>"),
 ("Vos droits", f"<p>Conformément au RGPD, vous disposez d'un droit d'accès, de rectification, d'effacement et d'opposition. Adressez votre demande à <a href=\"mailto:{M}\">{M}</a>. Vous pouvez également introduire une réclamation auprès de l'autorité de protection des données compétente (en France, la CNIL).</p>"),
 ("Modifications", "<p>Nous pouvons mettre à jour cette politique de temps à autre. La version en vigueur est toujours publiée sur cette page.</p>"),
],
"es": [
 ("En resumen", "<p>MobilCV es una herramienta gratuita para crear currículums sin registro (<a href=\"https://www.mobilcv.com/es/\">mobilcv.com</a>) y un blog de carrera (mobilcv.net). <strong>La información que escribes en tu currículum no se envía a nuestros servidores ni la guardamos nosotros.</strong> No mostramos anuncios ni vendemos datos personales.</p>"),
 ("Responsable", f"<p>MobilCV es un proyecto independiente desarrollado por İlhan Taşan. Para cualquier consulta sobre privacidad: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("La información de tu currículum", "<p>Todo lo que introduces (nombre, datos de contacto, foto, experiencia, etc.) se guarda <strong>solo en tu propio dispositivo, en el almacenamiento local de tu navegador</strong>, para que puedas continuar más tarde. El PDF también se crea por completo en tu navegador. No tenemos acceso a esta información.</p><ul><li>Para borrarla, usa el botón <strong>Limpiar todo</strong> o elimina los datos del sitio en tu navegador.</li><li>Si usas un ordenador compartido, te recomendamos borrar tu información al terminar.</li><li>El botón <strong>Descargar copia</strong> guarda tus datos en un archivo en tu dispositivo; ese archivo no se nos envía.</li><li>El botón <strong>Compartir</strong> envía tu PDF al menú para compartir de tu dispositivo; tú decides a dónde va.</li></ul>"),
 ("Servicios de terceros", "<ul><li><strong>Google Analytics</strong> (solo mobilcv.com): recopila estadísticas de uso anónimas (tipo de dispositivo, ubicación aproximada, páginas visitadas) mediante cookies. El contenido de tu currículum nunca se envía a Google Analytics.</li><li><strong>Tawk.to</strong> (solo mobilcv.com): ofrece la ventana de chat en vivo, usa cookies y puede tratar información técnica (navegador, ubicación aproximada). Si inicias un chat, tus mensajes nos llegan a través de este servicio.</li><li><strong>Formspree</strong>: los mensajes de nuestros formularios de contacto y opinión, junto con el nombre y el correo que indiques opcionalmente, llegan a nuestro buzón a través de este servicio.</li><li><strong>GitHub Pages</strong>: alojamiento de nuestros sitios. El proveedor puede guardar registros de acceso (p. ej., direcciones IP) por motivos de seguridad.</li><li><strong>Redes de distribución de contenido</strong> (cdnjs, flagcdn): desde ellas se cargan archivos de código e imágenes de banderas; técnicamente reciben tu dirección IP.</li></ul><p>Estos proveedores pueden tratar datos en servidores fuera de tu país.</p>"),
 ("Cookies", "<p>Solo Google Analytics y Tawk.to usan cookies; la herramienta de currículum no las necesita para funcionar. Puedes bloquear o eliminar las cookies en la configuración de tu navegador y desactivar Google Analytics con el <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">complemento oficial de inhabilitación</a>.</p>"),
 ("Conservación", "<p>La información de tu currículum permanece en tu dispositivo hasta que la borres. Los mensajes que nos envías se conservan solo el tiempo necesario para responder. Las estadísticas de uso se conservan durante un periodo limitado según la configuración de Google Analytics.</p>"),
 ("Tus derechos", f"<p>Según el RGPD y la legislación aplicable, puedes solicitar acceso, rectificación, supresión u oponerte al tratamiento de tus datos escribiendo a <a href=\"mailto:{M}\">{M}</a>. También puedes presentar una reclamación ante la autoridad de protección de datos competente.</p>"),
 ("Cambios", "<p>Podemos actualizar esta política ocasionalmente. La versión vigente siempre se publica en esta página.</p>"),
],
"it": [
 ("In breve", "<p>MobilCV è uno strumento gratuito per creare CV senza registrazione (<a href=\"https://www.mobilcv.com/it/\">mobilcv.com</a>) e un blog sulla carriera (mobilcv.net). <strong>Le informazioni inserite nel tuo CV non vengono inviate ai nostri server e non vengono conservate da noi.</strong> Non mostriamo pubblicità e non vendiamo dati personali.</p>"),
 ("Titolare", f"<p>MobilCV è un progetto indipendente sviluppato da İlhan Taşan. Per domande sulla privacy: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("Le informazioni del tuo CV", "<p>Tutto ciò che inserisci (nome, contatti, foto, esperienze, ecc.) viene conservato <strong>solo sul tuo dispositivo, nella memoria locale del browser</strong>, così puoi riprendere in seguito. Anche il PDF viene creato interamente nel tuo browser. Non abbiamo accesso a queste informazioni.</p><ul><li>Per cancellarle usa il pulsante <strong>Pulisci tutto</strong> o elimina i dati del sito nel browser.</li><li>Su un computer condiviso ti consigliamo di cancellare i dati al termine.</li><li>Il pulsante <strong>Scarica backup</strong> salva i dati in un file sul tuo dispositivo; il file non ci viene inviato.</li><li>Il pulsante <strong>Condividi</strong> passa il PDF al menu di condivisione del dispositivo; sei tu a decidere dove inviarlo.</li></ul>"),
 ("Servizi di terze parti", "<ul><li><strong>Google Analytics</strong> (solo mobilcv.com): raccoglie statistiche d'uso anonime (tipo di dispositivo, posizione approssimativa, pagine visitate) tramite cookie. Il contenuto del CV non viene mai inviato a Google Analytics.</li><li><strong>Tawk.to</strong> (solo mobilcv.com): fornisce la chat dal vivo, usa cookie e può trattare informazioni tecniche (browser, posizione approssimativa). Se avvii una chat, i tuoi messaggi ci arrivano tramite questo servizio.</li><li><strong>Formspree</strong>: i messaggi dei moduli di contatto e feedback, con nome ed e-mail facoltativi, vengono inoltrati alla nostra casella tramite questo servizio.</li><li><strong>GitHub Pages</strong>: hosting dei nostri siti. Il fornitore può conservare log di accesso (es. indirizzi IP) per motivi di sicurezza.</li><li><strong>Reti di distribuzione dei contenuti</strong> (cdnjs, flagcdn): da qui vengono caricati file di codice e immagini delle bandiere; tecnicamente ricevono il tuo indirizzo IP.</li></ul><p>Questi fornitori possono trattare dati su server situati fuori dal tuo Paese.</p>"),
 ("Cookie", "<p>Solo Google Analytics e Tawk.to usano cookie; lo strumento CV non ne ha bisogno. Puoi bloccare o eliminare i cookie dalle impostazioni del browser e disattivare Google Analytics con il <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">componente aggiuntivo ufficiale</a>.</p>"),
 ("Conservazione", "<p>Le informazioni del CV restano sul tuo dispositivo finché non le cancelli. I messaggi che ci invii sono conservati solo per il tempo necessario a rispondere. Le statistiche d'uso sono conservate per un periodo limitato secondo le impostazioni di Google Analytics.</p>"),
 ("I tuoi diritti", f"<p>Ai sensi del GDPR puoi chiedere accesso, rettifica, cancellazione o opporti al trattamento dei tuoi dati scrivendo a <a href=\"mailto:{M}\">{M}</a>. Puoi inoltre presentare reclamo all'autorità di controllo competente (in Italia, il Garante per la protezione dei dati personali).</p>"),
 ("Modifiche", "<p>Possiamo aggiornare questa informativa di tanto in tanto. La versione aggiornata è sempre pubblicata in questa pagina.</p>"),
],
"pt": [
 ("Em resumo", "<p>O MobilCV é uma ferramenta gratuita para criar currículos sem cadastro (<a href=\"https://www.mobilcv.com/pt/\">mobilcv.com</a>) e um blog de carreira (mobilcv.net). <strong>As informações que você escreve no currículo não são enviadas aos nossos servidores nem armazenadas por nós.</strong> Não exibimos anúncios e não vendemos dados pessoais.</p>"),
 ("Responsável", f"<p>O MobilCV é um projeto independente desenvolvido por İlhan Taşan. Para dúvidas sobre privacidade: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("As informações do seu currículo", "<p>Tudo o que você preenche (nome, contatos, foto, experiência etc.) fica <strong>somente no seu próprio dispositivo, no armazenamento local do navegador</strong>, para que você possa continuar depois. O PDF também é criado inteiramente no seu navegador. Não temos acesso a essas informações.</p><ul><li>Para apagá-las, use o botão <strong>Limpar tudo</strong> ou apague os dados do site no navegador.</li><li>Em computadores compartilhados, recomendamos apagar suas informações ao terminar.</li><li>O botão <strong>Baixar backup</strong> salva seus dados em um arquivo no seu dispositivo; esse arquivo não é enviado para nós.</li><li>O botão <strong>Compartilhar</strong> envia o PDF para o menu de compartilhamento do seu dispositivo; você decide o destino.</li></ul>"),
 ("Serviços de terceiros", "<ul><li><strong>Google Analytics</strong> (somente mobilcv.com): coleta estatísticas de uso anônimas (tipo de dispositivo, localização aproximada, páginas visitadas) por meio de cookies. O conteúdo do seu currículo nunca é enviado ao Google Analytics.</li><li><strong>Tawk.to</strong> (somente mobilcv.com): fornece o chat ao vivo, usa cookies e pode tratar informações técnicas (navegador, localização aproximada). Se você iniciar uma conversa, suas mensagens chegam até nós por esse serviço.</li><li><strong>Formspree</strong>: mensagens enviadas pelos formulários de contato e feedback, com nome e e-mail informados opcionalmente, são encaminhadas à nossa caixa de entrada por esse serviço.</li><li><strong>GitHub Pages</strong>: hospedagem dos nossos sites. O provedor pode manter registros de acesso (ex.: endereços IP) por segurança.</li><li><strong>Redes de distribuição de conteúdo</strong> (cdnjs, flagcdn): arquivos de código e imagens de bandeiras são carregados delas; tecnicamente recebem seu endereço IP.</li></ul><p>Esses provedores podem tratar dados em servidores fora do seu país.</p>"),
 ("Cookies", "<p>Somente o Google Analytics e o Tawk.to usam cookies; a ferramenta de currículo não precisa deles. Você pode bloquear ou apagar cookies nas configurações do navegador e desativar o Google Analytics com o <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">complemento oficial de desativação</a>.</p>"),
 ("Prazo de guarda", "<p>As informações do currículo ficam no seu dispositivo até você apagá-las. As mensagens que você nos envia são guardadas apenas pelo tempo necessário para responder. As estatísticas de uso são mantidas por tempo limitado conforme as configurações do Google Analytics.</p>"),
 ("Seus direitos", f"<p>De acordo com a LGPD, o GDPR e demais leis aplicáveis, você pode solicitar acesso, correção, exclusão ou se opor ao tratamento dos seus dados escrevendo para <a href=\"mailto:{M}\">{M}</a>. Você também pode apresentar reclamação à autoridade de proteção de dados competente (no Brasil, a ANPD).</p>"),
 ("Alterações", "<p>Podemos atualizar esta política periodicamente. A versão vigente está sempre publicada nesta página.</p>"),
],
"ru": [
 ("Коротко", "<p>MobilCV — бесплатный конструктор резюме без регистрации (<a href=\"https://www.mobilcv.com/ru/\">mobilcv.com</a>) и карьерный блог (mobilcv.net). <strong>Данные, которые вы вводите в резюме, не передаются на наши серверы и не хранятся у нас.</strong> Мы не показываем рекламу и не продаём персональные данные.</p>"),
 ("Ответственное лицо", f"<p>MobilCV — независимый проект, разработанный İlhan Taşan. По вопросам конфиденциальности: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("Данные вашего резюме", "<p>Всё, что вы вводите (имя, контакты, фото, опыт и т. д.), хранится <strong>только на вашем устройстве, в локальном хранилище браузера</strong>, чтобы вы могли продолжить позже. PDF также создаётся полностью в вашем браузере. У нас нет доступа к этим данным.</p><ul><li>Чтобы удалить данные, нажмите <strong>Очистить все</strong> или удалите данные сайта в браузере.</li><li>На общем компьютере рекомендуем удалять данные после работы.</li><li>Кнопка <strong>Скачать копию</strong> сохраняет данные в файл на вашем устройстве; этот файл нам не отправляется.</li><li>Кнопка <strong>Поделиться</strong> передаёт PDF в меню «Поделиться» вашего устройства; получателя выбираете вы.</li></ul>"),
 ("Сторонние сервисы", "<ul><li><strong>Google Analytics</strong> (только mobilcv.com): собирает анонимную статистику использования (тип устройства, примерное местоположение, посещённые страницы) с помощью файлов cookie. Содержимое резюме в Google Analytics не передаётся.</li><li><strong>Tawk.to</strong> (только mobilcv.com): окно онлайн-чата; использует cookie и может обрабатывать технические данные (браузер, примерное местоположение). Если вы начнёте чат, ваши сообщения поступят к нам через этот сервис.</li><li><strong>Formspree</strong>: сообщения из форм обратной связи и контактов, а также указанные по желанию имя и e-mail пересылаются в наш почтовый ящик через этот сервис.</li><li><strong>GitHub Pages</strong>: хостинг наших сайтов. Провайдер может вести журналы доступа (например, IP-адреса) в целях безопасности.</li><li><strong>Сети доставки контента</strong> (cdnjs, flagcdn): отсюда загружаются файлы кода и изображения флагов; технически они получают ваш IP-адрес.</li></ul><p>Эти провайдеры могут обрабатывать данные на серверах за пределами вашей страны.</p>"),
 ("Файлы cookie", "<p>Cookie используют только Google Analytics и Tawk.to; сам конструктор резюме в них не нуждается. Вы можете блокировать или удалять cookie в настройках браузера и отключить Google Analytics с помощью <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">официального дополнения</a>.</p>"),
 ("Срок хранения", "<p>Данные резюме остаются на вашем устройстве, пока вы их не удалите. Ваши сообщения хранятся только столько, сколько нужно для ответа. Статистика использования хранится ограниченное время согласно настройкам Google Analytics.</p>"),
 ("Ваши права", f"<p>В соответствии с применимым законодательством вы вправе узнать, обрабатываются ли ваши данные, получить к ним доступ, потребовать их исправления или удаления и возразить против обработки. Направьте запрос на <a href=\"mailto:{M}\">{M}</a>. Вы также можете обратиться с жалобой в уполномоченный орган по защите данных.</p>"),
 ("Изменения", "<p>Мы можем время от времени обновлять эту политику. Актуальная версия всегда публикуется на этой странице.</p>"),
],
"ar": [
 ("باختصار", "<p>MobilCV أداة مجانية لإنشاء السيرة الذاتية دون تسجيل (<a href=\"https://www.mobilcv.com/ar/\">mobilcv.com</a>) ومدونة مهنية (mobilcv.net). <strong>المعلومات التي تكتبها في سيرتك الذاتية لا تُرسل إلى خوادمنا ولا نحتفظ بها.</strong> لا نعرض إعلانات ولا نبيع البيانات الشخصية.</p>"),
 ("الجهة المسؤولة", f"<p>MobilCV مشروع مستقل طوّره İlhan Taşan. لأي استفسار يتعلق بالخصوصية: <a href=\"mailto:{M}\">{M}</a></p>"),
 ("معلومات سيرتك الذاتية", "<p>كل ما تُدخله (الاسم، بيانات الاتصال، الصورة، الخبرات وغيرها) يُحفظ <strong>على جهازك فقط، في التخزين المحلي لمتصفحك</strong>، لتتمكن من المتابعة لاحقًا. ويُنشأ ملف PDF بالكامل داخل متصفحك. لا يمكننا الوصول إلى هذه المعلومات.</p><ul><li>لحذفها استخدم زر <strong>مسح الكل</strong> أو احذف بيانات الموقع من متصفحك.</li><li>إذا كنت تستخدم جهازًا مشتركًا فننصحك بحذف معلوماتك بعد الانتهاء.</li><li>زر <strong>تنزيل نسخة</strong> يحفظ بياناتك في ملف على جهازك، ولا يُرسل هذا الملف إلينا.</li><li>زر <strong>مشاركة</strong> ينقل ملف PDF إلى قائمة المشاركة في جهازك، وأنت من يختار الجهة.</li></ul>"),
 ("خدمات الأطراف الثالثة", "<ul><li><strong>Google Analytics</strong> (في mobilcv.com فقط): يجمع إحصاءات استخدام مجهولة الهوية (نوع الجهاز، الموقع التقريبي، الصفحات التي تمت زيارتها) باستخدام ملفات تعريف الارتباط. لا يُرسل محتوى سيرتك الذاتية إلى Google Analytics أبدًا.</li><li><strong>Tawk.to</strong> (في mobilcv.com فقط): يوفر نافذة الدردشة المباشرة، ويستخدم ملفات تعريف الارتباط وقد يعالج معلومات تقنية (المتصفح، الموقع التقريبي). إذا بدأت محادثة تصلنا رسائلك عبر هذه الخدمة.</li><li><strong>Formspree</strong>: تُرسل الرسائل الواردة من نماذج التواصل والملاحظات، مع الاسم والبريد الإلكتروني الاختياريين، إلى بريدنا عبر هذه الخدمة.</li><li><strong>GitHub Pages</strong>: استضافة مواقعنا. قد يحتفظ مزود الاستضافة بسجلات الوصول (مثل عناوين IP) لأغراض أمنية.</li><li><strong>شبكات توزيع المحتوى</strong> (cdnjs وflagcdn): تُحمّل منها ملفات البرمجة وصور الأعلام، وتتلقى تقنيًا عنوان IP الخاص بك.</li></ul><p>قد يعالج هؤلاء المزودون البيانات على خوادم خارج بلدك.</p>"),
 ("ملفات تعريف الارتباط", "<p>تستخدم ملفات تعريف الارتباط فقط من قبل Google Analytics وTawk.to، ولا تحتاجها أداة السيرة الذاتية نفسها. يمكنك حظرها أو حذفها من إعدادات متصفحك، وإيقاف Google Analytics عبر <a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">الإضافة الرسمية لإلغاء الاشتراك</a>.</p>"),
 ("مدة الاحتفاظ", "<p>تبقى معلومات سيرتك الذاتية على جهازك حتى تحذفها. نحتفظ بالرسائل التي ترسلها إلينا فقط للمدة اللازمة للرد عليها. وتُحفظ إحصاءات الاستخدام لفترة محدودة وفق إعدادات Google Analytics.</p>"),
 ("حقوقك", f"<p>وفقًا للقوانين المعمول بها يحق لك معرفة ما إذا كانت بياناتك تُعالج، والوصول إليها، وطلب تصحيحها أو حذفها، والاعتراض على معالجتها. أرسل طلبك إلى <a href=\"mailto:{M}\">{M}</a>. كما يحق لك تقديم شكوى إلى الجهة المختصة بحماية البيانات في بلدك.</p>"),
 ("التغييرات", "<p>قد نُحدّث هذه السياسة من وقت لآخر، وتُنشر النسخة الحالية دائمًا في هذه الصفحة.</p>"),
],
"zh": [
 ("简要说明", "<p>MobilCV 是一款无需注册的免费简历制作工具（<a href=\"https://www.mobilcv.com/zh/\">mobilcv.com</a>），同时也是一个职业博客（mobilcv.net）。<strong>您在简历中填写的信息不会发送到我们的服务器，我们也不会保存这些信息。</strong>我们不展示广告，也不出售个人数据。</p>"),
 ("负责人", f"<p>MobilCV 是由 İlhan Taşan 开发的独立项目。如有隐私相关问题，请联系：<a href=\"mailto:{M}\">{M}</a></p>"),
 ("您的简历信息", "<p>您填写的所有内容（姓名、联系方式、照片、工作经历等）<strong>仅保存在您自己的设备上，即浏览器的本地存储中</strong>，方便您下次继续编辑。PDF 也完全在您的浏览器中生成。我们无法访问这些信息。</p><ul><li>如需删除，请使用工具中的<strong>全部清除</strong>按钮，或在浏览器中清除网站数据。</li><li>如果使用公共电脑，建议使用完毕后删除您的信息。</li><li><strong>下载备份</strong>按钮会将数据保存为您设备上的文件，该文件不会发送给我们。</li><li><strong>分享</strong>按钮会把 PDF 交给您设备自带的分享菜单，由您决定发送给谁。</li></ul>"),
 ("我们使用的第三方服务", "<ul><li><strong>Google Analytics</strong>（仅 mobilcv.com）：通过 Cookie 收集匿名使用统计（如设备类型、大致位置、访问的页面）。您的简历内容绝不会发送给 Google Analytics。</li><li><strong>Tawk.to</strong>（仅 mobilcv.com）：提供在线客服窗口，使用 Cookie，并可能处理技术信息（如浏览器、大致位置）。如果您发起聊天，您的消息将通过该服务发送给我们。</li><li><strong>Formspree</strong>：您通过反馈表和联系表发送的消息，以及您选择填写的姓名和电子邮箱，会经由该服务转发到我们的邮箱。</li><li><strong>GitHub Pages</strong>：我们的网站托管服务。托管方可能出于安全目的保存访问日志（如 IP 地址）。</li><li><strong>内容分发网络</strong>（cdnjs、flagcdn）：页面所需的代码文件和国旗图片从这些服务器加载，它们在技术上会收到您的 IP 地址。</li></ul><p>这些服务商可能会在您所在国家以外的服务器上处理数据。</p>"),
 ("Cookie", "<p>只有 Google Analytics 和 Tawk.to 使用 Cookie，简历工具本身无需 Cookie 即可运行。您可以在浏览器设置中阻止或删除 Cookie，也可以使用 Google 官方的<a href=\"https://tools.google.com/dlpage/gaoptout\" rel=\"noopener\">停用插件</a>停用 Google Analytics。</p>"),
 ("保存期限", "<p>简历信息会一直保存在您的设备上，直到您删除为止。您发给我们的消息仅在回复所需期间保存。使用统计数据按照 Google Analytics 的保留设置在有限期限内保存。</p>"),
 ("您的权利", f"<p>根据适用的法律，您有权了解我们是否处理您的数据、访问这些数据、要求更正或删除，以及反对处理。请将您的请求发送至 <a href=\"mailto:{M}\">{M}</a>。您也有权向当地的数据保护主管机关投诉。</p>"),
 ("变更", "<p>我们可能会不时更新本政策，最新版本始终发布在本页面。</p>"),
],
}

CSS = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f8fafc; color: #0f172a; line-height: 1.8; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: #fff; border-radius: 24px; box-shadow: 0 8px 40px rgba(0,0,0,0.06); overflow: hidden; }
        .site-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 28px; border-bottom: 1px solid #e2e8f0; flex-wrap: wrap; gap: 10px; }
        .logo { font-size: 1.6em; font-weight: 900; color: #0f172a; text-decoration: none; }
        .logo span { color: #2563eb; }
        .nav-links { display: flex; list-style: none; gap: 6px; flex-wrap: wrap; }
        .nav-links a { padding: 8px 18px; color: #64748b; text-decoration: none; font-weight: 600; border-radius: 40px; }
        .nav-links a:hover { color: #2563eb; background: #dbeafe; }
        .page-content { padding: 40px; }
        h1 { font-size: 2.1em; margin-bottom: 6px; }
        .updated { color: #94a3b8; font-size: 0.9em; margin-bottom: 28px; }
        h2 { font-size: 1.3em; margin: 28px 0 10px; }
        p { color: #334155; margin-bottom: 12px; }
        ul { color: #334155; margin: 0 0 12px 22px; }
        [dir="rtl"] ul { margin: 0 22px 12px 0; }
        li { margin-bottom: 8px; }
        a { color: #2563eb; }
        .footer { background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 24px; text-align: center; color: #94a3b8; }
        .footer a { text-decoration: none; font-weight: 600; }
        @media (max-width: 640px) { .page-content { padding: 24px 18px; } h1 { font-size: 1.6em; } }"""


def build_page(code):
    d = LANGS[code]
    dir_attr = ' dir="rtl"' if d["rtl"] else ""
    sections = "\n".join(f"        <h2>{h}</h2>\n        {body}" for h, body in TEXT[code])
    alternates = "\n".join(f'    <link rel="alternate" hreflang="{c}" href="{v["url"]}">' for c, v in LANGS.items())
    desc = re.sub(r"<[^>]+>", "", TEXT[code][0][1])[:155].strip()
    return f"""<!DOCTYPE html>
<html lang="{code}"{dir_attr}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{d['label']} | MobilCV</title>
    <meta name="description" content="{desc.replace('"', '&quot;')}">
    <link rel="canonical" href="{d['url']}">
{alternates}
    <link rel="alternate" hreflang="x-default" href="{LANGS['en']['url']}">
    <style>{CSS}
    </style>
</head>
<body>
<div class="container">
    <header class="site-header">
        <a href="{d['net']}" class="logo">Mobil<span>CV</span></a>
        <ul class="nav-links">
            <li><a href="{d['com']}">{d['home']}</a></li>
            <li><a href="{d['net']}">{d['blog']}</a></li>
        </ul>
    </header>
    <div class="page-content">
        <h1>{d['label']}</h1>
        <p class="updated">{d['updated']}: {d['date']}</p>
{sections}
    </div>
    <footer class="footer">
        <p>&copy; {UPDATED.year} MobilCV &mdash; <a href="{d['com']}">mobilcv.com</a></p>
    </footer>
</div>
</body>
</html>
"""


def lang_of(rel):
    first = rel.split("/")[0]
    return first if first in LANGS and "/" in rel else "tr"


def main():
    root = Path(".")
    if not (root / "MobilCV.AIEngine").exists():
        raise SystemExit("HATA: Scripti mobilcv-net deposunun kök klasöründe çalıştırın.")

    # 1) Gizlilik sayfaları
    written = 0
    for code, d in LANGS.items():
        p = root / d["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        html = build_page(code)
        if not p.exists() or p.read_text(encoding="utf-8") != html:
            p.write_text(html, encoding="utf-8")
            written += 1
    privacy_files = {LANGS[c]["path"] for c in LANGS}

    links = forms = news = 0
    for f in sorted(root.rglob("*.html")):
        rel = f.as_posix()
        if rel.startswith("MobilCV.AIEngine/") or f.name.startswith("google") or rel in privacy_files:
            continue
        s = f.read_text(encoding="utf-8")
        orig = s
        d = LANGS[lang_of(rel)]

        # 2) Footer'a gizlilik linki
        if "data-privacy-link" not in s and "</footer>" in s:
            link = (f'        <p data-privacy-link style="margin-top:6px;font-size:0.85em;">'
                    f'<a href="{d["url"]}">{d["label"]}</a></p>\n    ')
            idx = s.rfind("</footer>")
            s = s[:idx] + link + s[idx:]
            links += 1

        # 3) İletişim formları
        if f.name in ("iletisim.html", "contact.html"):
            s2 = re.sub(r'<!-- İLETİŞİM FORMU -->\s*<div[\s\S]*?sadece görseldir[\s\S]*?</p>\s*</div>', "", s)
            s2 = s2.replace('<form action="#" method="POST">',
                            f'<form action="{FORMSPREE}" method="POST">\n'
                            f'            <input type="hidden" name="_subject" value="MobilCV.net iletişim formu">')
            if s2 != s:
                s = s2
                forms += 1

        # 4) Çalışmayan bülten (Abone Ol) kutusu
        s2 = re.sub(r'\s*<div class="newsletter-box">[\s\S]*?</form>[\s\S]*?</div>', "", s)
        if s2 != s:
            s = s2
            news += 1

        if s != orig:
            f.write_text(s, encoding="utf-8")

    # 5) Sitemap
    added = 0
    sm = root / "sitemap.xml"
    if sm.exists():
        content = sm.read_text(encoding="utf-8")
        for d in LANGS.values():
            if f"<loc>{d['url']}</loc>" not in content and "</urlset>" in content:
                entry = f"  <url>\n    <loc>{d['url']}</loc>\n    <lastmod>{UPDATED.isoformat()}</lastmod>\n  </url>\n</urlset>"
                content = content.replace("</urlset>", entry, 1)
                added += 1
        sm.write_text(content, encoding="utf-8")

    print(f"Gizlilik sayfası yazıldı/güncellendi : {written}")
    print(f"Footer'a gizlilik linki eklenen sayfa: {links}")
    print(f"Düzeltilen iletişim formu            : {forms}")
    print(f"Kaldırılan bülten kutusu             : {news}")
    print(f"Sitemap'e eklenen adres              : {added}")


if __name__ == "__main__":
    main()
