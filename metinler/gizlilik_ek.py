# -*- coding: utf-8 -*-
"""Gizlilik politikasi ekleri (13 Ekim 2026): hukuki sebep, toplama yontemi, yurt disina aktarim,
cocuklar/otomatik karar, tam haklar listesi, CDN yerine kendi sunucu, hata bildirimi.
gizlilik_ve_bakim.py tarafindan iceri aktarilir. Her dil: ga_add, cdn, sections[(baslik, govde)], rights."""

B = "<ul>{}</ul>"
li = lambda *xs: B.format("".join(f"<li>{x}</li>" for x in xs))
REF_GA = " (KVKK m.5/1; GDPR m.6/1-a)"
REF_LI = " (KVKK m.5/2-f; GDPR m.6/1-f)"

EK = {
"tr": dict(
 ga_add=" Ayrıca sayfada oluşan teknik hataları (hata türü ve kısa hata mesajı) bildirir; mesajdaki e-posta adresleri ve uzun sayılar silinir, CV içeriği eklenmez.",
 cdn="<b>Kod kütüphaneleri ve bayrak görselleri:</b> mobilcv.com'un kendi sunucusundan yüklenir; bunlar için üçüncü taraf sunuculara bağlanılmaz.",
 sections=[
  ("Hukuki sebepler ve toplama yöntemi", li(
   "<b>Google Analytics:</b> Yalnızca açık rızanız ile işlenir. Veriler, çerez bandında “Kabul et”i seçmenizin ardından çerezler aracılığıyla otomatik olarak toplanır. Onayınızı istediğiniz zaman sayfanın altındaki “Çerez ayarları” bağlantısından geri alabilirsiniz; geri alma, o ana kadarki işlemeyi etkilemez." + REF_GA,
   "<b>İletişim ve geri bildirim formları:</b> Formu doldurup gönderdiğinizde, mesajınızı yanıtlayabilmek amacıyla, talebinize yanıt vermeye yönelik meşru menfaatimize dayanılarak işlenir." + REF_LI,
   "<b>Barındırma erişim kayıtları:</b> Sitelerin güvenli çalışması amacıyla barındırma sağlayıcısı tarafından otomatik olarak tutulur; meşru menfaate dayanır." + REF_LI,
   "<b>Çerez tercihiniz:</b> Seçiminizi hatırlamak için yalnızca tarayıcınızda saklanır (anahtar: <code>mobilcv_consent</code>). Sitenin sizin tercihinize göre çalışması için gereklidir ve bize gönderilmez.")),
  ("Yurt dışına aktarım",
   "<p>Google (Analytics), Formspree (iletişim formları) ve GitHub (barındırma) verileri başta ABD olmak üzere Türkiye ve Avrupa Birliği dışındaki ülkelerde işleyebilir. Bu ülkelerde kişisel verilerin korunma düzeyi bulunduğunuz ülkedekiyle aynı olmayabilir.</p>" + li(
   "Google Analytics yalnızca onay verirseniz çalışır. Onay vermeden önce bu bilgiyi dikkate almanızı rica ederiz; onay vermezseniz bu kapsamda Google'a veri aktarılmaz.",
   "İletişim formunu kullanırsanız mesajınız yalnızca o mesaj için ve sizin isteğiniz üzerine Formspree aracılığıyla iletilir.",
   "Barındırma sağlayıcısına aktarım, sitelerin size gösterilebilmesi için teknik olarak gereklidir.")),
  ("Çocuklar ve otomatik kararlar",
   "<p>CV aracına girdiğiniz bilgiler bize ulaşmaz. 16 yaşından küçükseniz Google Analytics için onay vermeden önce ebeveyninize danışın ya da “Reddet”i seçin. Hakkınızda yalnızca otomatik işlemeye dayalı bir karar alınmaz; ziyaret istatistiklerini reklam amacıyla kullanmayız.</p>")],
 rights="<p>KVKK m.11 kapsamında; kişisel verilerinizin işlenip işlenmediğini öğrenme, işlenmişse buna ilişkin bilgi talep etme, işlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme, yurt içinde veya yurt dışında aktarıldığı üçüncü kişileri bilme, eksik veya yanlış işlenmişse düzeltilmesini isteme, silinmesini veya yok edilmesini isteme, bu işlemlerin verilerin aktarıldığı üçüncü kişilere bildirilmesini isteme, münhasıran otomatik sistemlerle analiz edilmesi sonucu aleyhinize bir sonucun ortaya çıkmasına itiraz etme ve kanuna aykırı işleme nedeniyle zarara uğramanız hâlinde zararın giderilmesini talep etme haklarına sahipsiniz.</p>"
        "<p>AB'de GDPR, Birleşik Krallık'ta UK GDPR ve benzer mevzuatı olan ülkelerde (ör. Brezilya LGPD, Japonya APPI, Çin PIPL, Kaliforniya CCPA/CPRA) ayrıca işlemenin kısıtlanmasını isteme, verilerinizi yaygın kullanılan bir biçimde alma ve verdiğiniz onayı her zaman geri alma haklarınız vardır.</p>"
        "<p>Taleplerinizi <a href=\"mailto:info@mobilcv.com\">info@mobilcv.com</a> adresine iletebilirsiniz; en geç 30 gün içinde ücretsiz olarak yanıt veririz. Talebin size ait olduğunu doğrulamak için ek bilgi isteyebiliriz. CV bilgilerinize erişimimiz olmadığından, bunları cihazınızdan kendiniz silebilirsiniz. Kişisel Verileri Koruma Kurulu'na veya bulunduğunuz ülkenin veri koruma otoritesine şikâyette bulunma hakkınız saklıdır.</p>"
        "<p>Kişisel verileri satmıyor ve reklam amacıyla paylaşmıyoruz (Kaliforniya CCPA/CPRA anlamında “satış” ya da “paylaşım” yapılmaz).</p>"),

"en": dict(
 ga_add=" It also reports technical errors on the page (error type and a short error message); email addresses and long numbers are removed from the message and no CV content is included.",
 cdn="<b>Code libraries and flag images:</b> loaded from mobilcv.com's own server; no third-party servers are contacted for them.",
 sections=[
  ("Legal bases and how data is collected", li(
   "<b>Google Analytics:</b> processed only with your consent. Data is collected automatically through cookies after you choose “Accept” in the cookie banner. You can withdraw consent at any time via the “Cookie settings” link at the bottom of the page; withdrawal does not affect processing carried out before it." + REF_GA,
   "<b>Contact and feedback forms:</b> when you fill in and send a form, your message is processed so that we can reply, based on our legitimate interest in responding to your request." + REF_LI,
   "<b>Hosting access logs:</b> kept automatically by the hosting provider so that the websites run securely; based on legitimate interest." + REF_LI,
   "<b>Your cookie choice:</b> stored only in your browser (key: <code>mobilcv_consent</code>) to remember your decision. It is needed for the site to follow your choice and is not sent to us.")),
  ("Transfers abroad",
   "<p>Google (Analytics), Formspree (contact forms) and GitHub (hosting) may process data in countries outside Türkiye and the European Union, in particular the United States. The level of personal data protection in those countries may differ from the level in your country.</p>" + li(
   "Google Analytics runs only if you consent. Please take this information into account before consenting; if you do not consent, no data is transferred to Google for this purpose.",
   "If you use the contact form, your message is transferred through Formspree only for that message and at your request.",
   "Transfer to the hosting provider is technically necessary to show you the websites.")),
  ("Children and automated decisions",
   "<p>Information you enter in the CV tool never reaches us. If you are under 16, talk to a parent before consenting to Google Analytics, or choose “Reject”. No decision about you is made solely by automated processing, and we do not use visit statistics for advertising.</p>")],
 rights="<p>Depending on where you live, you have the right to know whether personal data about you is processed and to access it; to know the purposes of processing and the recipients in your country or abroad; to have inaccurate data corrected; to have data deleted; to have recipients informed of such corrections or deletions; to restrict or object to processing; to receive your data in a commonly used format; to object to decisions based solely on automated processing; to withdraw your consent at any time; and, where applicable, to claim compensation for damage caused by unlawful processing. These rights arise in particular from Türkiye's KVKK (Art. 11), the EU GDPR, the UK GDPR and similar laws such as Brazil's LGPD, Japan's APPI, China's PIPL and California's CCPA/CPRA.</p>"
        "<p>Send requests to <a href=\"mailto:info@mobilcv.com\">info@mobilcv.com</a>. We reply free of charge within 30 days at the latest and may ask for information to confirm that the request is yours. As we have no access to your CV information, you can delete it yourself on your device. You also have the right to lodge a complaint with your country's data protection authority (in Türkiye, the Personal Data Protection Board).</p>"
        "<p>We do not sell personal information or share it for advertising (no “sale” or “sharing” within the meaning of California's CCPA/CPRA).</p>"),
}

# Diger diller: ayni yapi, ceviri
def mk(ga_add, cdn, h1, ga, form, logs, choice, h2, tr_p, t1, t2, t3, h3, kids, rights1, rights2, rights3):
    return dict(ga_add=ga_add, cdn=cdn, sections=[
        (h1, li(ga + REF_GA, form + REF_LI, logs + REF_LI, choice)),
        (h2, f"<p>{tr_p}</p>" + li(t1, t2, t3)),
        (h3, f"<p>{kids}</p>")],
        rights=f"<p>{rights1}</p><p>{rights2}</p><p>{rights3}</p>")

MAIL = '<a href="mailto:info@mobilcv.com">info@mobilcv.com</a>'
LAWS = "KVKK (Art. 11), GDPR, UK GDPR, LGPD, APPI, PIPL, CCPA/CPRA"

EK["de"] = mk(
 " Außerdem meldet es technische Fehler auf der Seite (Fehlerart und kurze Fehlermeldung); E-Mail-Adressen und lange Zahlen werden aus der Meldung entfernt, Lebenslaufinhalte werden nicht übermittelt.",
 "<b>Code-Bibliotheken und Flaggenbilder:</b> werden vom eigenen Server von mobilcv.com geladen; dafür werden keine Server von Drittanbietern kontaktiert.",
 "Rechtsgrundlagen und Art der Erhebung",
 "<b>Google Analytics:</b> nur mit Ihrer Einwilligung. Die Daten werden automatisch über Cookies erhoben, nachdem Sie im Cookie-Banner „Akzeptieren“ gewählt haben. Sie können Ihre Einwilligung jederzeit über den Link „Cookie-Einstellungen“ unten auf der Seite widerrufen; der Widerruf berührt die bis dahin erfolgte Verarbeitung nicht.",
 "<b>Kontakt- und Feedbackformulare:</b> Wenn Sie ein Formular absenden, wird Ihre Nachricht verarbeitet, damit wir antworten können; Grundlage ist unser berechtigtes Interesse, Ihre Anfrage zu beantworten.",
 "<b>Zugriffsprotokolle des Hosters:</b> werden vom Hosting-Anbieter automatisch für den sicheren Betrieb der Websites geführt; Grundlage ist das berechtigte Interesse.",
 "<b>Ihre Cookie-Auswahl:</b> wird nur in Ihrem Browser gespeichert (Schlüssel: <code>mobilcv_consent</code>), damit Ihre Entscheidung beachtet wird. Sie wird nicht an uns gesendet.",
 "Übermittlung in Drittländer",
 "Google (Analytics), Formspree (Kontaktformulare) und GitHub (Hosting) können Daten außerhalb der Türkei und der Europäischen Union verarbeiten, insbesondere in den USA. Das Datenschutzniveau dort kann von dem in Ihrem Land abweichen.",
 "Google Analytics läuft nur mit Ihrer Einwilligung. Bitte berücksichtigen Sie diese Information vor Ihrer Einwilligung; ohne Einwilligung werden zu diesem Zweck keine Daten an Google übermittelt.",
 "Wenn Sie das Kontaktformular nutzen, wird Ihre Nachricht nur für diese Nachricht und auf Ihren Wunsch über Formspree übermittelt.",
 "Die Übermittlung an den Hosting-Anbieter ist technisch notwendig, um Ihnen die Websites anzuzeigen.",
 "Kinder und automatisierte Entscheidungen",
 "Angaben, die Sie im Lebenslauf-Tool eingeben, erreichen uns nie. Wenn Sie jünger als 16 Jahre sind, sprechen Sie vor einer Einwilligung in Google Analytics mit einem Elternteil oder wählen Sie „Ablehnen“. Es werden keine Entscheidungen über Sie ausschließlich automatisiert getroffen, und wir nutzen Besuchsstatistiken nicht für Werbung.",
 f"Je nach Wohnort haben Sie das Recht auf Auskunft darüber, ob und welche personenbezogenen Daten über Sie verarbeitet werden, über Zwecke und Empfänger im In- und Ausland, auf Berichtigung, Löschung, Einschränkung der Verarbeitung, Widerspruch, Datenübertragbarkeit, Unterrichtung der Empfänger über Berichtigungen oder Löschungen, Widerspruch gegen ausschließlich automatisierte Entscheidungen, jederzeitigen Widerruf Ihrer Einwilligung sowie gegebenenfalls auf Schadensersatz bei rechtswidriger Verarbeitung ({LAWS}).",
 f"Anfragen richten Sie an {MAIL}. Wir antworten kostenlos innerhalb von höchstens 30 Tagen und können Angaben zur Bestätigung Ihrer Identität erbitten. Da wir keinen Zugriff auf Ihre Lebenslaufdaten haben, können Sie diese selbst auf Ihrem Gerät löschen. Sie haben das Recht, sich bei der Datenschutzaufsichtsbehörde Ihres Landes zu beschweren.",
 "Wir verkaufen keine personenbezogenen Daten und geben sie nicht zu Werbezwecken weiter (kein „Verkauf“ oder „Teilen“ im Sinne des kalifornischen CCPA/CPRA).")

EK["fr"] = mk(
 " Il signale également les erreurs techniques de la page (type d'erreur et court message) ; les adresses e-mail et les longs nombres sont supprimés du message et aucun contenu de CV n'est inclus.",
 "<b>Bibliothèques de code et images de drapeaux :</b> chargées depuis le propre serveur de mobilcv.com ; aucun serveur tiers n'est contacté pour cela.",
 "Bases juridiques et mode de collecte",
 "<b>Google Analytics :</b> uniquement avec votre consentement. Les données sont collectées automatiquement par des cookies après que vous avez choisi « Accepter » dans le bandeau. Vous pouvez retirer votre consentement à tout moment via le lien « Paramètres des cookies » en bas de page ; le retrait n'affecte pas le traitement effectué auparavant.",
 "<b>Formulaires de contact et de retour :</b> lorsque vous envoyez un formulaire, votre message est traité pour que nous puissions répondre, sur la base de notre intérêt légitime à répondre à votre demande.",
 "<b>Journaux d'accès de l'hébergeur :</b> conservés automatiquement par l'hébergeur pour le fonctionnement sécurisé des sites ; sur la base de l'intérêt légitime.",
 "<b>Votre choix concernant les cookies :</b> enregistré uniquement dans votre navigateur (clé : <code>mobilcv_consent</code>) pour respecter votre décision ; il ne nous est pas envoyé.",
 "Transferts hors de votre pays",
 "Google (Analytics), Formspree (formulaires de contact) et GitHub (hébergement) peuvent traiter des données en dehors de la Turquie et de l'Union européenne, notamment aux États-Unis. Le niveau de protection des données personnelles dans ces pays peut différer de celui de votre pays.",
 "Google Analytics ne fonctionne qu'avec votre consentement. Veuillez tenir compte de cette information avant de consentir ; sans consentement, aucune donnée n'est transférée à Google à cette fin.",
 "Si vous utilisez le formulaire de contact, votre message est transmis via Formspree uniquement pour ce message et à votre demande.",
 "Le transfert vers l'hébergeur est techniquement nécessaire pour afficher les sites.",
 "Enfants et décisions automatisées",
 "Les informations saisies dans l'outil CV ne nous parviennent jamais. Si vous avez moins de 16 ans, parlez-en à un parent avant de consentir à Google Analytics, ou choisissez « Refuser ». Aucune décision vous concernant n'est prise sur le seul fondement d'un traitement automatisé, et nous n'utilisons pas les statistiques de visite à des fins publicitaires.",
 f"Selon votre lieu de résidence, vous disposez du droit de savoir si des données vous concernant sont traitées et d'y accéder, de connaître les finalités et les destinataires dans votre pays ou à l’étranger, de rectification, d'effacement, de limitation, d'opposition, de portabilité, d'information des destinataires en cas de rectification ou d'effacement, de vous opposer à une décision fondée exclusivement sur un traitement automatisé, de retirer votre consentement à tout moment et, le cas échéant, d'obtenir réparation d'un préjudice causé par un traitement illicite ({LAWS}).",
 f"Adressez vos demandes à {MAIL}. Nous répondons gratuitement dans un délai maximal de 30 jours et pouvons demander des informations pour vérifier que la demande émane de vous. Comme nous n'avons pas accès aux informations de votre CV, vous pouvez les supprimer vous-même sur votre appareil. Vous avez le droit d'introduire une réclamation auprès de l'autorité de protection des données de votre pays.",
 "Nous ne vendons pas de données personnelles et ne les partageons pas à des fins publicitaires (aucune « vente » ni aucun « partage » au sens du CCPA/CPRA californien).")

EK["es"] = mk(
 " También informa de errores técnicos de la página (tipo de error y un mensaje breve); se eliminan del mensaje las direcciones de correo y los números largos, y no se incluye contenido del currículum.",
 "<b>Bibliotecas de código e imágenes de banderas:</b> se cargan desde el propio servidor de mobilcv.com; no se contacta con servidores de terceros para ello.",
 "Bases jurídicas y forma de obtención",
 "<b>Google Analytics:</b> solo con tu consentimiento. Los datos se recogen automáticamente mediante cookies después de que elijas «Aceptar» en el aviso. Puedes retirar el consentimiento en cualquier momento desde el enlace «Configuración de cookies» al pie de la página; la retirada no afecta al tratamiento realizado antes.",
 "<b>Formularios de contacto y comentarios:</b> cuando envías un formulario, tratamos tu mensaje para poder responderte, sobre la base de nuestro interés legítimo en atender tu solicitud.",
 "<b>Registros de acceso del alojamiento:</b> el proveedor de alojamiento los guarda automáticamente para el funcionamiento seguro de los sitios; sobre la base del interés legítimo.",
 "<b>Tu elección sobre cookies:</b> se guarda solo en tu navegador (clave: <code>mobilcv_consent</code>) para respetar tu decisión; no se nos envía.",
 "Transferencias internacionales",
 "Google (Analytics), Formspree (formularios de contacto) y GitHub (alojamiento) pueden tratar datos fuera de Turquía y de la Unión Europea, en particular en Estados Unidos. El nivel de protección de datos personales en esos países puede ser distinto al de tu país.",
 "Google Analytics solo funciona con tu consentimiento. Ten en cuenta esta información antes de consentir; si no consientes, no se transfieren datos a Google con este fin.",
 "Si usas el formulario de contacto, tu mensaje se transfiere a través de Formspree solo para ese mensaje y a petición tuya.",
 "La transferencia al proveedor de alojamiento es técnicamente necesaria para mostrarte los sitios.",
 "Menores y decisiones automatizadas",
 "La información que introduces en la herramienta de currículum nunca nos llega. Si tienes menos de 16 años, habla con tu madre, padre o tutor antes de aceptar Google Analytics, o elige «Rechazar». No se toman decisiones sobre ti basadas únicamente en tratamientos automatizados y no usamos las estadísticas de visitas con fines publicitarios.",
 f"Según dónde vivas, tienes derecho a saber si se tratan datos personales sobre ti y a acceder a ellos, a conocer los fines y los destinatarios en tu país o en el extranjero, a la rectificación, la supresión, la limitación, la oposición y la portabilidad, a que se informe a los destinatarios de las rectificaciones o supresiones, a oponerte a decisiones basadas únicamente en tratamientos automatizados, a retirar tu consentimiento en cualquier momento y, en su caso, a ser indemnizado por daños causados por un tratamiento ilícito ({LAWS}).",
 f"Envía tus solicitudes a {MAIL}. Respondemos gratis en un plazo máximo de 30 días y podemos pedirte información para comprobar que la solicitud es tuya. Como no tenemos acceso a la información de tu currículum, puedes borrarla tú mismo en tu dispositivo. Tienes derecho a presentar una reclamación ante la autoridad de protección de datos de tu país.",
 "No vendemos datos personales ni los compartimos con fines publicitarios (no hay «venta» ni «compartición» en el sentido de la CCPA/CPRA de California).")

EK["it"] = mk(
 " Segnala inoltre gli errori tecnici della pagina (tipo di errore e un breve messaggio); indirizzi e-mail e numeri lunghi vengono rimossi dal messaggio e non è incluso alcun contenuto del CV.",
 "<b>Librerie di codice e immagini delle bandiere:</b> caricate dal server di mobilcv.com; per questo non vengono contattati server di terze parti.",
 "Basi giuridiche e modalità di raccolta",
 "<b>Google Analytics:</b> solo con il tuo consenso. I dati sono raccolti automaticamente tramite cookie dopo che hai scelto «Accetta» nel banner. Puoi revocare il consenso in qualsiasi momento dal link «Impostazioni cookie» in fondo alla pagina; la revoca non pregiudica il trattamento effettuato prima.",
 "<b>Moduli di contatto e feedback:</b> quando invii un modulo, il tuo messaggio è trattato per poterti rispondere, sulla base del nostro legittimo interesse a dare seguito alla tua richiesta.",
 "<b>Log di accesso dell'hosting:</b> conservati automaticamente dal fornitore di hosting per il funzionamento sicuro dei siti; sulla base del legittimo interesse.",
 "<b>La tua scelta sui cookie:</b> salvata solo nel tuo browser (chiave: <code>mobilcv_consent</code>) per rispettare la tua decisione; non ci viene inviata.",
 "Trasferimenti all'estero",
 "Google (Analytics), Formspree (moduli di contatto) e GitHub (hosting) possono trattare dati fuori dalla Turchia e dall'Unione europea, in particolare negli Stati Uniti. Il livello di protezione dei dati personali in quei paesi può essere diverso da quello del tuo paese.",
 "Google Analytics funziona solo con il tuo consenso. Tieni conto di questa informazione prima di acconsentire; senza consenso nessun dato viene trasferito a Google per questo scopo.",
 "Se usi il modulo di contatto, il tuo messaggio è trasferito tramite Formspree solo per quel messaggio e su tua richiesta.",
 "Il trasferimento al fornitore di hosting è tecnicamente necessario per mostrarti i siti.",
 "Minori e decisioni automatizzate",
 "Le informazioni inserite nello strumento CV non ci arrivano mai. Se hai meno di 16 anni, parlane con un genitore prima di acconsentire a Google Analytics, oppure scegli «Rifiuta». Nessuna decisione che ti riguarda è basata unicamente su un trattamento automatizzato e non usiamo le statistiche di visita a fini pubblicitari.",
 f"A seconda di dove vivi, hai il diritto di sapere se sono trattati dati personali che ti riguardano e di accedervi, di conoscere le finalità e i destinatari nel tuo paese o all’estero, di rettifica, cancellazione, limitazione, opposizione e portabilità, di far informare i destinatari di rettifiche o cancellazioni, di opporti a decisioni basate unicamente su trattamenti automatizzati, di revocare il consenso in qualsiasi momento e, se del caso, di ottenere il risarcimento del danno causato da un trattamento illecito ({LAWS}).",
 f"Invia le richieste a {MAIL}. Rispondiamo gratuitamente entro 30 giorni al massimo e possiamo chiedere informazioni per verificare che la richiesta provenga da te. Poiché non abbiamo accesso alle informazioni del tuo CV, puoi cancellarle tu stesso dal tuo dispositivo. Hai il diritto di proporre reclamo all'autorità per la protezione dei dati del tuo paese.",
 "Non vendiamo dati personali e non li condividiamo a fini pubblicitari (nessuna «vendita» o «condivisione» ai sensi del CCPA/CPRA della California).")

EK["pt"] = mk(
 " Também comunica erros técnicos da página (tipo de erro e uma mensagem curta); os endereços de e-mail e os números longos são removidos da mensagem e não é incluído qualquer conteúdo do currículo.",
 "<b>Bibliotecas de código e imagens de bandeiras:</b> carregadas a partir do próprio servidor do mobilcv.com; não é contactado qualquer servidor de terceiros para esse efeito.",
 "Fundamentos jurídicos e forma de recolha",
 "<b>Google Analytics:</b> apenas com o seu consentimento. Os dados são recolhidos automaticamente através de cookies depois de escolher «Aceitar» no aviso. Pode retirar o consentimento a qualquer momento através da ligação «Definições de cookies» no rodapé; a retirada não afeta o tratamento efetuado anteriormente.",
 "<b>Formulários de contacto e de comentários:</b> quando envia um formulário, a sua mensagem é tratada para que possamos responder, com base no nosso interesse legítimo em dar resposta ao seu pedido.",
 "<b>Registos de acesso do alojamento:</b> mantidos automaticamente pelo fornecedor de alojamento para o funcionamento seguro dos sites; com base no interesse legítimo.",
 "<b>A sua escolha sobre cookies:</b> guardada apenas no seu navegador (chave: <code>mobilcv_consent</code>) para respeitar a sua decisão; não nos é enviada.",
 "Transferência internacional",
 "A Google (Analytics), a Formspree (formulários de contacto) e o GitHub (alojamento) podem tratar dados fora da Turquia e da União Europeia, em especial nos Estados Unidos. O nível de proteção de dados pessoais nesses países pode ser diferente do nível do seu país.",
 "O Google Analytics só funciona com o seu consentimento. Tenha esta informação em conta antes de consentir; sem consentimento, não são transferidos dados para a Google para essa finalidade.",
 "Se utilizar o formulário de contacto, a sua mensagem é transferida através da Formspree apenas para essa mensagem e a seu pedido.",
 "A transferência para o fornecedor de alojamento é tecnicamente necessária para lhe mostrar os sites.",
 "Crianças e decisões automatizadas",
 "As informações que escreve na ferramenta de currículo nunca chegam até nós. Se tiver menos de 16 anos, fale com o seu encarregado de educação antes de consentir o Google Analytics, ou escolha «Recusar». Não é tomada qualquer decisão sobre si exclusivamente com base em tratamento automatizado, e não utilizamos as estatísticas de visitas para publicidade.",
 f"Consoante o local onde reside, tem o direito de saber se os seus dados pessoais são tratados e de lhes aceder, de conhecer as finalidades e os destinatários no seu país ou no estrangeiro, à retificação, ao apagamento, à limitação, à oposição e à portabilidade, a que os destinatários sejam informados das retificações ou apagamentos, de se opor a decisões tomadas exclusivamente com base em tratamento automatizado, de retirar o consentimento a qualquer momento e, quando aplicável, de ser indemnizado por danos causados por tratamento ilícito ({LAWS}).",
 f"Envie os seus pedidos para {MAIL}. Respondemos gratuitamente no prazo máximo de 30 dias e podemos pedir informações para confirmar que o pedido é seu. Como não temos acesso às informações do seu currículo, pode apagá-las diretamente no seu dispositivo. Tem o direito de apresentar reclamação à autoridade de proteção de dados do seu país (em Portugal, a CNPD; no Brasil, a ANPD).",
 "Não vendemos dados pessoais nem os partilhamos para publicidade (não há «venda» nem «partilha» na aceção da CCPA/CPRA da Califórnia).")

EK["ru"] = mk(
 " Кроме того, он сообщает о технических ошибках на странице (тип ошибки и короткое сообщение); адреса электронной почты и длинные числа удаляются из сообщения, содержимое резюме не передаётся.",
 "<b>Программные библиотеки и изображения флагов:</b> загружаются с собственного сервера mobilcv.com; сторонние серверы для этого не используются.",
 "Правовые основания и способ сбора",
 "<b>Google Analytics:</b> только с вашего согласия. Данные собираются автоматически с помощью файлов cookie после того, как вы выбрали «Принять» в баннере. Вы можете в любой момент отозвать согласие по ссылке «Настройки cookie» внизу страницы; отзыв не влияет на обработку, выполненную до этого.",
 "<b>Формы обратной связи и контактов:</b> когда вы отправляете форму, ваше сообщение обрабатывается, чтобы мы могли ответить, на основании нашего законного интереса в ответе на ваш запрос.",
 "<b>Журналы доступа хостинга:</b> автоматически ведутся хостинг-провайдером для безопасной работы сайтов; на основании законного интереса.",
 "<b>Ваш выбор в отношении cookie:</b> хранится только в вашем браузере (ключ: <code>mobilcv_consent</code>), чтобы учитывать ваше решение; нам он не передаётся.",
 "Трансграничная передача",
 "Google (Analytics), Formspree (контактные формы) и GitHub (хостинг) могут обрабатывать данные за пределами Турции и Европейского союза, в частности в США. Уровень защиты персональных данных в этих странах может отличаться от уровня в вашей стране.",
 "Google Analytics работает только с вашего согласия. Пожалуйста, учтите эту информацию до того, как дать согласие; без согласия данные для этой цели Google не передаются.",
 "Если вы используете контактную форму, ваше сообщение передаётся через Formspree только для этого сообщения и по вашему запросу.",
 "Передача хостинг-провайдеру технически необходима, чтобы показать вам сайты.",
 "Дети и автоматизированные решения",
 "Данные, которые вы вводите в инструмент для резюме, к нам не попадают. Если вам меньше 16 лет, прежде чем согласиться на Google Analytics, посоветуйтесь с родителями или выберите «Отклонить». Решения о вас не принимаются исключительно на основе автоматизированной обработки, и мы не используем статистику посещений в рекламных целях.",
 f"В зависимости от места проживания вы вправе узнать, обрабатываются ли ваши персональные данные, и получить к ним доступ; узнать цели обработки и получателей в вашей стране и за рубежом; потребовать исправления, удаления, ограничения обработки; возразить против обработки; получить данные в распространённом формате; потребовать уведомления получателей об исправлении или удалении; возразить против решений, основанных исключительно на автоматизированной обработке; в любой момент отозвать согласие и, где применимо, потребовать возмещения вреда от незаконной обработки ({LAWS}).",
 f"Направляйте запросы на {MAIL}. Мы бесплатно отвечаем в течение не более 30 дней и можем запросить сведения, чтобы убедиться, что запрос исходит от вас. Поскольку у нас нет доступа к данным вашего резюме, вы можете удалить их сами на своём устройстве. Вы вправе подать жалобу в орган по защите персональных данных вашей страны.",
 "Мы не продаём персональные данные и не передаём их в рекламных целях (никакой «продажи» или «передачи» в смысле CCPA/CPRA штата Калифорния).")

EK["ar"] = mk(
 " كما يبلّغ عن الأخطاء التقنية في الصفحة (نوع الخطأ ورسالة قصيرة)؛ وتُحذف عناوين البريد الإلكتروني والأرقام الطويلة من الرسالة، ولا يُرسل أي محتوى من سيرتك الذاتية.",
 "<b>مكتبات البرمجة وصور الأعلام:</b> تُحمَّل من خادم mobilcv.com نفسه، ولا يُتصل بخوادم أطراف ثالثة لهذا الغرض.",
 "الأسس القانونية وطريقة الجمع",
 "<b>Google Analytics:</b> بموافقتك فقط. تُجمع البيانات تلقائيًا عبر ملفات تعريف الارتباط بعد اختيارك «قبول» في الشريط. يمكنك سحب موافقتك في أي وقت من رابط «إعدادات ملفات تعريف الارتباط» أسفل الصفحة، ولا يؤثر السحب في المعالجة التي تمت قبله.",
 "<b>نماذج التواصل والملاحظات:</b> عند إرسالك نموذجًا تُعالج رسالتك كي نتمكن من الرد عليك، استنادًا إلى مصلحتنا المشروعة في الرد على طلبك.",
 "<b>سجلات الوصول لدى الاستضافة:</b> يحتفظ بها مزود الاستضافة تلقائيًا لتشغيل المواقع بأمان، استنادًا إلى المصلحة المشروعة.",
 "<b>اختيارك بشأن ملفات تعريف الارتباط:</b> يُحفظ في متصفحك فقط (المفتاح: <code>mobilcv_consent</code>) لاحترام قرارك، ولا يُرسل إلينا.",
 "النقل إلى خارج بلدك",
 "قد تعالج Google ‏(Analytics) وFormspree (نماذج التواصل) وGitHub (الاستضافة) البيانات خارج تركيا والاتحاد الأوروبي، ولا سيما في الولايات المتحدة. وقد يختلف مستوى حماية البيانات الشخصية في تلك الدول عن مستواه في بلدك.",
 "لا يعمل Google Analytics إلا بموافقتك. يُرجى مراعاة هذه المعلومة قبل الموافقة؛ وإن لم توافق فلن تُنقل أي بيانات إلى Google لهذا الغرض.",
 "إذا استخدمت نموذج التواصل فستُنقل رسالتك عبر Formspree لتلك الرسالة فقط وبناءً على طلبك.",
 "النقل إلى مزود الاستضافة ضروري تقنيًا لعرض المواقع عليك.",
 "الأطفال والقرارات الآلية",
 "لا تصل إلينا أبدًا المعلومات التي تُدخلها في أداة السيرة الذاتية. إذا كان عمرك أقل من 16 عامًا فتحدث مع أحد والديك قبل الموافقة على Google Analytics أو اختر «رفض». لا تُتخذ بشأنك قرارات تستند فقط إلى المعالجة الآلية، ولا نستخدم إحصاءات الزيارات لأغراض إعلانية.",
 f"بحسب مكان إقامتك، يحق لك معرفة ما إذا كانت بياناتك الشخصية تُعالج والاطلاع عليها، ومعرفة أغراض المعالجة والجهات المتلقية داخل بلدك وخارجه، وطلب تصحيحها أو حذفها أو تقييد معالجتها، والاعتراض على المعالجة، والحصول على بياناتك بصيغة شائعة الاستخدام، وإبلاغ الجهات المتلقية بالتصحيح أو الحذف، والاعتراض على القرارات المستندة فقط إلى المعالجة الآلية، وسحب موافقتك في أي وقت، والمطالبة عند الاقتضاء بالتعويض عن الضرر الناتج عن معالجة غير مشروعة ({LAWS}).",
 f"أرسل طلباتك إلى {MAIL}. نرد مجانًا خلال 30 يومًا كحد أقصى، وقد نطلب معلومات للتحقق من أن الطلب صادر عنك. ولأننا لا نصل إلى معلومات سيرتك الذاتية، يمكنك حذفها بنفسك من جهازك. ويحق لك تقديم شكوى إلى سلطة حماية البيانات في بلدك.",
 "لا نبيع البيانات الشخصية ولا نشاركها لأغراض إعلانية (لا يوجد «بيع» أو «مشاركة» بالمعنى الوارد في قانون CCPA/CPRA في كاليفورنيا).")

EK["zh"] = mk(
 " 它还会报告页面上的技术错误（错误类型和简短的错误信息）；信息中的电子邮件地址和长数字会被删除，不包含任何简历内容。",
 "<b>代码库和国旗图片：</b>从 mobilcv.com 自己的服务器加载，不会为此连接第三方服务器。",
 "法律依据与收集方式",
 "<b>Google Analytics：</b>仅在您同意后处理。您在 Cookie 提示中选择“接受”后，数据通过 Cookie 自动收集。您可随时通过页面底部的“Cookie 设置”链接撤回同意；撤回不影响此前已进行的处理。",
 "<b>联系和反馈表单：</b>您提交表单时，我们为回复您而处理您的消息，依据是回应您请求的正当利益。",
 "<b>托管访问日志：</b>由托管服务商为网站安全运行而自动保存，依据是正当利益。",
 "<b>您的 Cookie 选择：</b>仅保存在您的浏览器中（键名：<code>mobilcv_consent</code>），用于遵循您的决定，不会发送给我们。",
 "跨境传输",
 "Google（Analytics）、Formspree（联系表单）和 GitHub（托管）可能在土耳其和欧盟以外的国家（尤其是美国）处理数据。这些国家的个人信息保护水平可能与您所在国家不同。",
 "Google Analytics 仅在您同意后运行。请在同意前考虑这一信息；如您不同意，不会为此目的向 Google 传输数据。",
 "如果您使用联系表单，您的消息仅针对该条消息、应您的要求通过 Formspree 传输。",
 "向托管服务商的传输是向您展示网站所必需的技术环节。",
 "未成年人与自动化决策",
 "您在简历工具中输入的信息不会到达我们。若您未满 16 岁，请在同意 Google Analytics 前与父母沟通，或选择“拒绝”。我们不会仅基于自动化处理对您作出决定，也不会将访问统计用于广告。",
 f"根据您所在地，您有权了解是否处理了您的个人信息并查阅；了解处理目的以及境内外接收方；要求更正、删除、限制处理；反对处理；以常用格式获取您的数据；要求将更正或删除通知接收方；反对仅基于自动化处理的决定；随时撤回同意；并在适用时就违法处理造成的损害要求赔偿（{LAWS}）。",
 f"请将请求发送至 {MAIL}。我们将在最长 30 天内免费回复，并可能要求提供信息以确认请求由您本人提出。由于我们无法访问您的简历信息，您可以在自己的设备上自行删除。您有权向所在国家或地区的个人信息保护机构投诉。",
 "我们不出售个人信息，也不为广告目的共享个人信息（不存在加州 CCPA/CPRA 意义上的“出售”或“共享”）。")

EK["ja"] = mk(
 " また、ページで発生した技術的なエラー（エラーの種類と短いメッセージ）を報告します。メッセージ内のメールアドレスや長い数字は削除され、履歴書の内容は含まれません。",
 "<b>プログラムライブラリと国旗画像：</b>mobilcv.com 自身のサーバーから読み込まれ、そのために第三者のサーバーに接続することはありません。",
 "利用の根拠と取得方法",
 "<b>Google Analytics：</b>お客様の同意がある場合にのみ利用します。Cookieバナーで「同意する」を選択された後、Cookieにより自動的に取得されます。ページ下部の「Cookie設定」からいつでも同意を撤回でき、撤回はそれ以前の取扱いに影響しません。",
 "<b>お問い合わせ・フィードバックフォーム：</b>フォームを送信された場合、返信のためにメッセージを取り扱います。根拠はお問い合わせに対応するという当方の正当な利益です。",
 "<b>ホスティングのアクセスログ：</b>サイトを安全に運営するため、ホスティング事業者が自動的に記録します。根拠は正当な利益です。",
 "<b>Cookieの選択：</b>お客様の選択を守るため、ブラウザ内にのみ保存されます（キー：<code>mobilcv_consent</code>）。当方には送信されません。",
 "外国への移転",
 "Google（Analytics）、Formspree（お問い合わせフォーム）、GitHub（ホスティング）は、トルコおよび欧州連合以外の国、特に米国でデータを取り扱う場合があります。これらの国における個人情報の保護水準は、お客様の国と異なる場合があります。",
 "Google Analytics はお客様が同意した場合にのみ動作します。同意の前にこの情報をご考慮ください。同意しない場合、この目的でGoogleにデータは移転されません。",
 "お問い合わせフォームを利用された場合、メッセージはその1件についてのみ、お客様の求めに応じてFormspree経由で移転されます。",
 "ホスティング事業者への移転は、サイトを表示するために技術的に必要です。",
 "未成年者と自動化された意思決定",
 "履歴書ツールに入力された情報が当方に届くことはありません。16歳未満の方は、Google Analytics に同意する前に保護者に相談するか、「拒否する」を選択してください。自動処理のみに基づいてお客様に関する決定を行うことはなく、訪問統計を広告目的に利用することもありません。",
 f"お住まいの地域に応じて、お客様には、ご自身の個人情報が取り扱われているかを知り開示を求める権利、利用目的と国内外の提供先を知る権利、訂正・削除・利用停止を求める権利、取扱いに異議を述べる権利、一般的な形式でデータを受け取る権利、訂正や削除を提供先に通知するよう求める権利、自動処理のみに基づく決定に異議を述べる権利、いつでも同意を撤回する権利、また該当する場合は違法な取扱いによる損害の賠償を求める権利があります（{LAWS}）。",
 f"ご請求は {MAIL} までお送りください。30日以内に無料でお答えします。ご本人からの請求であることを確認するため、情報の提供をお願いすることがあります。履歴書の情報には当方はアクセスできないため、お使いの端末でご自身で削除できます。お住まいの国の個人情報保護機関に苦情を申し立てる権利もあります。",
 "当方は個人情報を販売せず、広告目的で共有することもありません（カリフォルニア州CCPA/CPRAにいう「販売」や「共有」は行いません）。")
