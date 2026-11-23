# -*- coding: utf-8 -*-
"""Generates the three Komodo & Ko Terms & Conditions signing pages
(full-day-trip.html, open-trip.html, private-trip.html) plus index.html
from the shared template below. Run: python generate.py

English is shown as the primary language throughout, with the Indonesian
translation given as its own separate paragraph directly underneath
(never joined on one line with a slash).
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body data-file-label="{file_label}">

<div id="contract">
<div class="hero">
  <img src="assets/logo.jpg" alt="Komodo & Ko logo" class="logo">
  <div class="brand">Komodo &amp; Ko</div>
  <h1>Terms &amp; Conditions</h1>
  <h2>{trip_name}</h2>
  <div class="sub">Please read the full agreement below, then complete and sign at the bottom of this page.</div>
</div>

<div class="wrap">
  <div class="card">
    <p style="margin:0;color:var(--muted);font-size:.9rem;">
      This document is provided in two (2) languages: <strong>English</strong>, the universal language,
      and <strong>Bahasa Indonesia</strong>, the national language of the Republic of Indonesia.
      In the event of any discrepancy in interpretation, the Indonesian language shall prevail.
    </p>
  </div>

{content}

  <div class="section" id="reservation-form">
    <h2>Reservation Form<span class="title-id">Formulir Reservasi</span></h2>
    <p style="margin:0 0 4px;color:var(--muted);font-size:.85rem;">All fields below are required before this
    agreement can be signed and downloaded.</p>
    <div class="formgrid">
      <div class="field">
        <label for="resName">Name<span class="req">*</span><span class="label-id">Nama</span></label>
        <input type="text" id="resName" placeholder="Full name as per ID / passport" required>
      </div>
      <div class="field">
        <label for="resEmail">Email<span class="req">*</span></label>
        <input type="email" id="resEmail" placeholder="you@example.com" required>
      </div>
      <div class="field">
        <label for="resId">NIK / Passport Number<span class="req">*</span><span class="label-id">NIK / No. Paspor</span></label>
        <input type="text" id="resId" placeholder="National ID or passport number" required>
      </div>
      <div class="field">
        <label for="resBoat">Name of Boat<span class="req">*</span><span class="label-id">Nama Kapal</span></label>
        <input type="text" id="resBoat" placeholder="Boat name (if known)" required>
      </div>
      <div class="field">
        <label for="resDate">Date of Travel<span class="req">*</span><span class="label-id">Tanggal Keberangkatan</span></label>
        <input type="date" id="resDate" required>
      </div>
      <div class="field">
        <label for="resRoom">Room Type<span class="req">*</span><span class="label-id">Tipe Kamar</span></label>
        <select id="resRoom" required>
          <option value="">— select —</option>
          <option value="Leisure (Wisata)">Leisure (Wisata)</option>
          <option value="Diving (Menyelam)">Diving (Menyelam)</option>
          <option value="Combined (Gabungan)">Combined (Gabungan)</option>
        </select>
      </div>
      <div class="field full">
        <label for="resDestination">Destination<span class="label-id">Destinasi</span></label>
        <input type="text" id="resDestination" value="Labuan Bajo" readonly>
      </div>
    </div>
  </div>

  <div class="section" id="acknowledgement">
    <h2>Acknowledgement &amp; Signature<span class="title-id">Persetujuan &amp; Tanda Tangan</span></h2>
    <div class="closing">
      <p>{closing_en}</p>
      <p class="id">{closing_id}</p>
    </div>

    <div class="agree-box">
      <input type="checkbox" id="agreeCheckbox">
      <label for="agreeCheckbox">
        <p>I confirm that I have read, understood and voluntarily agree to be bound by all the terms and
        conditions of this {trip_name} agreement with Komodo &amp; Ko.</p>
        <p class="id">Saya menyatakan telah membaca, memahami, dan dengan sukarela menyetujui seluruh syarat dan
        ketentuan perjalanan {trip_name} ini dengan Komodo &amp; Ko.</p>
      </label>
    </div>

    <div class="sig-grid">
      <div class="sig-block">
        <h4>Guest Signature<span class="id">Tanda Tangan Tamu</span></h4>
        <div class="sig-canvas-wrap">
          <canvas id="guestSignatureCanvas" class="sig-canvas"></canvas>
          <div class="sig-placeholder">Sign here with mouse or finger</div>
        </div>
        <button type="button" id="clearSignature" class="sig-clear no-print">Clear signature</button>
        <div class="sig-line">
          <input type="text" id="guestSignName" class="sig-name-input" placeholder="Guest full name" required>
        </div>
        <div class="sig-date">Date: <span id="guestSignDate">—</span></div>
      </div>

      <div class="sig-block">
        <h4>Komodo &amp; Ko Signature<span class="id">Tanda Tangan Komodo &amp; Ko</span></h4>
        <div class="sig-static">
          <img src="assets/logo.jpg" alt="Komodo & Ko logo" class="company-logo">
          <img src="assets/company-signature.png" alt="Komodo & Ko authorized signature" class="company-sig">
        </div>
        <div class="sig-line">
          <span style="width:100%;text-align:center;">Komodo &amp; Ko, Authorized Signatory</span>
        </div>
        <div class="sig-date">Date: <span id="companySignDate">—</span></div>
      </div>
    </div>
  </div>

  <div class="actions no-print">
    <button type="button" id="downloadPdfBtn" class="btn btn-primary" disabled>Sign &amp; Download PDF</button>
    <div class="status-msg" id="statusMsg"></div>
  </div>

  <footer class="site-footer no-print">
    Komodo &amp; Ko &middot; This page is a private link for completing and signing your trip's Terms &amp; Conditions.
  </footer>
</div>
</div>

<script src="assets/signature_pad.umd.min.js"></script>
<script src="assets/html2canvas.min.js"></script>
<script src="assets/jspdf.umd.min.js"></script>
<script src="assets/app.js"></script>
</body>
</html>
"""

FLIGHT_INFO = """
  <div class="section">
    <h2>Labuan Bajo Flight Information<span class="title-id">Informasi Penerbangan Labuan Bajo</span></h2>
    <table class="flight">
      <tr><th>Route</th><th>Direct Flights</th><th>1 Transit</th><th>2 Transits</th></tr>
      <tr>
        <td><strong>Jakarta (CGK) &ndash; Labuan Bajo (LBJ)</strong></td>
        <td>Garuda Indonesia, AirAsia, Citilink, Batik Air</td>
        <td>Garuda Indonesia, AirAsia, Batik Air, Super Air Jet, Nam Air, Pelita Air</td>
        <td>Lion Air, Wings Air</td>
      </tr>
      <tr>
        <td><strong>Surabaya (SUB) &ndash; Labuan Bajo (LBJ)</strong></td>
        <td>Batik Air, Super Air Jet</td>
        <td>Batik Air, Lion Air, Super Air Jet</td>
        <td>&mdash;</td>
      </tr>
      <tr>
        <td><strong>Bali (DPS) &ndash; Labuan Bajo (LBJ)</strong></td>
        <td>Garuda Indonesia, AirAsia, Batik Air</td>
        <td>&mdash;</td>
        <td>&mdash;</td>
      </tr>
    </table>
  </div>

  <div class="section">
    <h2>Hotel Information<span class="title-id">Informasi Hotel</span></h2>
    <div class="twocol">
      <div>
        <ul class="pill-list">
          <li>Ayana Komodo</li>
          <li>Plataran Komodo Resort</li>
          <li>Loccal Collection Labuan Bajo</li>
          <li>Sudamala Resort</li>
          <li>La Prima Hotel</li>
          <li>Ta'Aktana Resort</li>
        </ul>
      </div>
      <div>
        <ul class="pill-list">
          <li>Bintang Flores</li>
          <li>Sylvia Resort</li>
          <li>Seaesta Hotel</li>
          <li>The Jayakarta</li>
          <li>Mohini Komodo Resort</li>
          <li>La Cecile</li>
          <li>Bajo Escape</li>
        </ul>
      </div>
    </div>
  </div>
"""


def note(title_id, text_id, title_en, text_en):
    """English block first, Indonesian block second — two separate
    paragraphs, never joined with a slash."""
    return """    <div class="note">
      <h3>{title_en}</h3>
      {text_en}
      <h4 class="sub-id">{title_id}</h4>
      {text_id}
    </div>
""".format(title_id=title_id, text_id=text_id, title_en=title_en, text_en=text_en)


def section(title_en, title_id, body):
    return """  <div class="section">
    <h2>{title_en}<span class="title-id">{title_id}</span></h2>
{body}  </div>
""".format(title_en=title_en, title_id=title_id, body=body)


def lang_group(title_en, title_id, en_items, id_items, note_en=None, note_id=None):
    def ul(items):
        lis = "\n".join("          <li>{0}</li>".format(x) for x in items)
        return "        <ul>\n{0}\n        </ul>".format(lis)

    extra = ""
    if note_en:
        extra += '\n        <p style="font-size:.85rem;color:var(--muted);">{0}</p>'.format(note_en)
    if note_id:
        extra += '\n        <p style="font-size:.85rem;color:var(--muted);font-style:italic;">{0}</p>'.format(note_id)

    return """      <div class="lang-group">
        <h4>{title_en}</h4>
{en_list}
        <h4 class="id">{title_id}</h4>
{id_list}{extra}
      </div>
""".format(title_en=title_en, title_id=title_id, en_list=ul(en_items), id_list=ul(id_items), extra=extra)


# ---------------------------------------------------------------------------
# Shared "Must Bring Items" list (identical across all three trip types)
# ---------------------------------------------------------------------------

MUST_BRING_EN_FULLDAY = [
    "Sunblock", "Sunglasses", "Beach hat", "Personal snacks", "Personal supplements",
    "Spare clothes", "Toiletries", "Swimsuit", "Wet wipes", "Drybag", "Personal medicine",
    "Telkomsel SIM card", "Hiking sandals", "Additional Cash",
    "Power bank (just in case the passenger runs out of battery on the island)",
]
MUST_BRING_ID_FULLDAY = [
    "Tabir surya", "Kacamata hitam", "Topi pantai", "Camilan pribadi", "Suplemen pribadi",
    "Pakaian ganti", "Perlengkapan mandi", "Pakaian renang", "Tisu basah", "Kantong Kering",
    "Obat-obatan pribadi", "Kartu SIM Telkomsel", "Sandal mendaki", "Uang Tunai Tambahan",
    "Power bank (hanya digunakan apabila penumpang kehabisan baterai di pulau)",
]
MUST_BRING_EN_OVERNIGHT = [
    "Sunblock", "Sunglasses", "Beach hat", "Personal snacks", "Personal supplements",
    "Spare clothes", "Toiletries", "Swimsuit", "Wet wipes", "Drybag", "Personal medicine",
    "Telkomsel SIM card", "Hiking sandals", "Additional Cash",
    "Power bank (just in case the passenger runs out of battery on the island)",
]
MUST_BRING_ID_OVERNIGHT = [
    "Tabir surya", "Kacamata hitam", "Topi pantai", "Camilan pribadi", "Suplemen pribadi",
    "Pakaian cadangan", "Perlengkapan mandi", "Pakaian renang", "Tisu basah", "Tas Kedap Air",
    "Obat-obatan pribadi", "Kartu SIM Telkomsel", "Sandal mendaki", "Uang Tunai Tambahan",
    "Power bank (hanya digunakan apabila penumpang kehabisan baterai di pulau)",
]


# ---------------------------------------------------------------------------
# FULL DAY TRIP CONTENT
# ---------------------------------------------------------------------------

FULL_DAY_TRIP_DETAILS = section(
    "Trip Details", "Detail Perjalanan",
    '    <div class="twocol">\n      <div>\n'
    + lang_group(
        "Include", "Termasuk",
        [
            "Boat Crew", "Lunch box", "Snack &amp; Soft Drink", "Mineral Water", "Dry Towel",
            "Guide", "Snorkeling Gear",
            "Transportation includes one-time pick-up and drop-off service",
        ],
        [
            "Awak kapal", "Makan siang", "Makanan dan Minuman Ringan", "Air Mineral", "Handuk Kering",
            "Pemandu", "Peralatan snorkeling",
            "Transportasi penjemputan dan pengantaran dalam satu kali perjalanan",
        ],
    )
    + "      </div>\n      <div>\n"
    + lang_group(
        "Exclude", "Yang Tidak Termasuk",
        [
            "Komodo National Park Entrance Fees",
            "Documentation &ndash; please consult the admin if you wish to use professional photographer services",
            "Personal Expenses", "Crew Gratuity (optional)", "Health Insurance",
            "Liability for the loss of personal items due to personal negligence",
        ],
        [
            "Biaya masuk Taman Nasional Komodo",
            "Dokumentasi (silakan hubungi admin jika ingin menggunakan jasa fotografer profesional)",
            "Pengeluaran pribadi", "Tip untuk kru (opsional)", "Asuransi kesehatan",
            "Pertanggungjawaban atas kehilangan barang pribadi karena kelalaian pribadi",
        ],
    )
    + "      </div>\n    </div>\n"
    + lang_group("Must Bring Items", "Barang yang Wajib Dibawa", MUST_BRING_EN_FULLDAY, MUST_BRING_ID_FULLDAY)
)

FULL_DAY_IMPORTANT_NOTES = section(
    "Important Notes", "Catatan Penting",
    note(
        "1. Pengaturan Penerbangan",
        "<p>Beberapa maskapai mungkin tidak secara konsisten menyediakan penerbangan langsung ke Labuan Bajo. Penumpang disarankan untuk memastikan ketersediaan penerbangan langsung melalui aplikasi resmi atau pusat informasi maskapai terkait.</p>",
        "1. Flight Arrangements",
        "<p>Some airlines may not consistently offer direct flights to Labuan Bajo. Passengers are advised to confirm the availability of direct flights through the respective airline's official application or information center.</p>",
    )
    + note(
        "2. Saran Terkait Kedatangan",
        "<p>Sehari Sebelum Perjalanan: Penumpang sangat disarankan untuk tiba di Labuan Bajo setidaknya satu hari sebelum perjalanan dimulai guna memastikan kelancaran rencana perjalanan serta menghindari gangguan akibat kemungkinan penundaan atau pembatalan penerbangan.</p>",
        "2. Arrival Recommendations",
        "<p>Day Before the Trip: It is strongly recommended that passengers arrive in Labuan Bajo at least one day before the trip to ensure a smooth itinerary and avoid disruptions caused by potential flight delays or cancellations.</p>",
    )
    + note(
        "3. Masalah yang Terjadi Saat Perjalanan",
        """<ul>
          <li>Peserta wajib segera melaporkan setiap masalah atau kendala selama perjalanan kepada awak kapal yang bertugas atau pemimpin perjalanan. Pelaporan yang cepat memungkinkan masalah tersebut ditangani selagi perjalanan masih berlangsung.</li>
          <li>Keluhan yang disampaikan dengan terlambat atau setelah perjalanan berakhir tidak dapat ditindaklanjuti.</li>
          <li>Masalah yang dimaksud adalah masalah yang berhubungan dengan kapal, fasilitas kapal, pelayanan kapal.</li>
          <li>Setiap keluhan akan ditindaklanjuti dengan pengecekan keluhan terlebih dahulu.</li>
          <li>Keluhan yang terlambat tidak dapat dikeluhkan kembali.</li>
          <li>Penumpang tidak diperkenankan mengupload keluhan yang tidak sesuai dengan angka ini di media sosial.</li>
          <li>Keluhan yang tidak sesuai dengan angka ini dan dikeluhkan di dunia sosial akan dianggap sebagai suatu perbuatan pelanggaran terhadap privasi penyedia layanan perjalanan dan pelanggaran terhadap UU ITE.</li>
        </ul>""",
        "3. On-Trip Issues",
        """<ul>
          <li>Guests must immediately report any issues or concerns during the trip to the on-duty crew members or the trip leader. Prompt reporting ensures the opportunity to resolve the matter during the journey.</li>
          <li>Delayed or post-trip complaints cannot be addressed after the trip concludes.</li>
          <li>The issues in question are those related to the vessel, vessel facilities, and vessel services.</li>
          <li>Every complaint will be addressed by first verifying the details of the complaint.</li>
          <li>Late complaints cannot be resubmitted.</li>
          <li>Passengers are not permitted to post complaints on social media that do not align with the terms outlined herein.</li>
          <li>Complaints that do not align with these terms and are posted on social media will be considered a violation of the travel service provider's privacy and a violation of the ITE Law (Electronic Information and Transactions Law).</li>
        </ul>""",
    )
    + note(
        "4. Musim Ramai",
        "<p>Selama musim ramai, destinasi populer seperti Manta Point, Pulau Padar, Pink Beach, dan Pulau Komodo dapat mengalami kepadatan pengunjung yang tinggi. <strong>Komodo &amp; Ko</strong> tidak bertanggung jawab atas keluhan apa pun terkait kondisi ramai di lokasi-lokasi tersebut.</p>",
        "4. High Season Crowds",
        "<p>During the high season, popular destinations such as Manta Point, Padar Island, Pink Beach, and Komodo Island may experience high visitor traffic. <strong>Komodo &amp; Ko</strong> is not responsible for any complaints related to crowded conditions at these locations.</p>",
    )
    + note(
        "5. Kebijakan Penanganan Keluhan",
        """<ul>
          <li>Segala keluhan terkait kekurangan layanan selama perjalanan harus segera dilaporkan kepada Pemimpin Tur (Tour Leader) atau Direktur Kapal (Cruise Director) yang bertugas di kapal. Direktur Kapal akan berupaya memberikan solusi yang tepat.</li>
          <li>Harap diperhatikan bahwa keluhan yang disampaikan setelah perjalanan berakhir tidak akan diterima oleh <strong>Komodo &amp; Ko</strong>.</li>
          <li>Pertanggungjawaban keluhan berdasarkan kepastian hukum, verifikasi berbasis bukti, serta batasan tanggung jawab yang adil tidak hanya bagi konsumen namun adil bagi penyedia usaha.</li>
        </ul>""",
        "5. Complaint Policy",
        """<ul>
          <li>Any concerns regarding service shortfalls during the trip must be reported to the Tour Leader or Cruise Director onboard immediately. The Cruise Director will work to provide an appropriate solution.</li>
          <li>Please note that complaints lodged after the trip will not be accepted by <strong>Komodo &amp; Ko</strong>.</li>
          <li>Addressing complaints based on legal certainty and evidence-based verification, alongside liability limits that are fair to both consumers and business providers.</li>
        </ul>""",
    )
)

FULL_DAY_RESERVATION = section(
    "Reservation Terms", "Ketentuan Reservasi",
    note(
        "1. Konfirmasi Ketersediaan",
        "<p>Mohon konfirmasi ketersediaan terlebih dahulu. Pemesanan dilakukan paling lambat 20 hari sebelum tanggal keberangkatan.</p>",
        "1. Availability Confirmation",
        "<p>Please confirm availability before booking. Reservations must be made at least 20 days before the departure date.</p>",
    )
    + note(
        "2. Persyaratan Uang Muka",
        "<p>Pemesanan hanya dapat dilakukan dengan pembayaran uang muka.</p>",
        "2. Down Payment Requirement",
        "<p>Booking can only be made with a down payment.</p>",
    )
    + note(
        "3. Proses Pembayaran",
        """<ul>
          <li>Deposit sebesar 50% diperlukan untuk mengamankan pemesanan perjalanan.</li>
          <li>Deposit tidak dapat dikembalikan jika peserta membatalkan keikutsertaan kapan pun.</li>
          <li>Sisa pembayaran harus dilunasi paling lambat 20 hari sebelum perjalanan dimulai.</li>
          <li>Pelunasan penuh wajib dilakukan jika perjalanan akan berlangsung dalam waktu kurang dari 20 hari.</li>
        </ul>""",
        "3. Payment Process",
        """<ul>
          <li>A 50% deposit is required to secure the trip.</li>
          <li>The deposit is non-refundable in the event of participant cancellation at any time.</li>
          <li>The remaining payment must be made no later than 20 days before the trip.</li>
          <li>The full payment must be made if the trip is less than 20 days away.</li>
        </ul>""",
    )
    + note(
        "4. Rincian &amp; Konfirmasi Pembayaran",
        "<p>Rincian dan proses pembayaran akan dibantu oleh tim Layanan Pelanggan kami. Konfirmasikan pembayaran melalui agent terkait dengan mengirimkan bukti pembayaran.</p>",
        "4. Payment Details &amp; Confirmation",
        "<p>The payment details and process will be assisted by our Customer Service team. Please send proof of payment to your booking agent for confirmation.</p>",
    )
    + note(
        "5. Persetujuan Dokumentasi",
        "<p>Agent menyediakan dokumentasi selama perjalanan berlangsung. Setiap peserta menyetujui untuk direkam dan difoto, serta Agent berhak menggunakan hasil dokumentasi tersebut untuk tujuan promosi.</p>",
        "5. Documentation Consent",
        "<p>Agent provides documentation during the trip. Each participant agrees to be recorded and photographed, and Agent reserves the right to use the footage for promotional purposes.</p>",
    )
)

FULL_DAY_BILLING = section(
    "Payment &amp; Billing Policy", "Kebijakan Penagihan dan Pembayaran",
    note(
        "1. Ketentuan Harga",
        """<ul>
          <li>Tarif berlaku untuk tahun penerbitannya dan dapat berubah setiap tahun.</li>
          <li>Penyesuaian harga dapat terjadi akibat faktor-faktor seperti biaya bahan bakar, rute atau aktivitas tambahan, peraturan pemerintah, atau kondisi lain di luar kendali Agent.</li>
        </ul>""",
        "1. Pricing Terms",
        """<ul>
          <li>Rates apply to the year in which they are issued and are subject to change annually.</li>
          <li>Price adjustments may occur due to factors such as fuel costs, additional routes or activities, government regulations, or other conditions beyond the control of Agent.</li>
        </ul>""",
    )
    + note(
        "2. Jadwal Pemesanan dan Pembayaran",
        "<p>Uang muka sebesar 50% diperlukan untuk mengamankan pemesanan. Pelunasan pembayaran wajib dilakukan paling lambat 20 hari sebelum tanggal keberangkatan. Harap diperhatikan bahwa syarat dan ketentuan dari masing-masing kapal akan berlaku untuk kapal-kapal tertentu.</p>",
        "2. Booking and Payment Schedule",
        "<p>A 50% down payment is required to secure a booking. Full payment must be made no later than 20 days prior to the departure date. Kindly note that the terms and conditions of the respective vessel will apply to certain vessels.</p>",
    )
    + note(
        "3. Kebijakan Anak",
        "<p>Anak-anak berusia 3 tahun ke atas akan dikenakan tarif penuh.</p>",
        "3. Child Policy",
        "<p>Children aged 3 years and above will be charged the full rate.</p>",
    )
    + note(
        "4. Biaya Bank",
        """<ul>
          <li>Seluruh biaya bank yang terkait dengan pembayaran wajib ditanggung oleh pihak pengirim.</li>
          <li>Total jumlah pembayaran yang kami terima harus sama persis dengan jumlah yang tercantum pada faktur. Segala selisih jumlah akibat biaya bank atau biaya transfer menjadi tanggung jawab klien.</li>
          <li>Baik Agent maupun operator tur tidak bertanggung jawab atas biaya bank tambahan yang timbul selama proses transfer, pembayaran deposit, atau pelunasan sisa pembayaran.</li>
        </ul>""",
        "4. Bank Charges",
        """<ul>
          <li>All bank charges related to payments must be borne by the sender.</li>
          <li>The total payment amount received by us must exactly match the amount specified on the invoice. Any discrepancies due to bank charges or transfer fees will be the responsibility of the client.</li>
          <li>Neither Agent nor the tour operator will be held accountable for additional bank charges incurred during transfers, deposits, or balance payments.</li>
        </ul>""",
    )
)

FULL_DAY_CANCELLATION = section(
    "Cancellation Policy", "Kebijakan Pembatalan",
    note(
        "1. Ketentuan Umum Pembatalan",
        "<p>Peserta setuju untuk pembatalan yang dilakukan 20 hari atau kurang sebelum tanggal keberangkatan, 100% dari total pembayaran akan hangus dan tidak dapat dikembalikan.</p>",
        "1. General Cancellation Terms",
        "<p>Participants agree that for cancellations made 20 days or less prior to the departure date, 100% of the total payment will be forfeited and is non-refundable.</p>",
    )
    + note(
        "2. Ketentuan Biaya Pembatalan",
        """<ul>
          <li>Setelah pendaftaran, uang muka (deposit) dianggap hangus dan tidak dapat dikembalikan.</li>
          <li>Jika peserta membatalkan keikutsertaan, pembayaran tidak dapat dikembalikan, dijadwalkan ulang, ataupun dialihkan ke perjalanan lain. Namun, peserta dapat menunjuk orang lain sebagai pengganti untuk mengikuti perjalanan tersebut.</li>
        </ul>""",
        "2. Cancellation Fee Conditions",
        """<ul>
          <li>Upon registration, the down payment (deposit) is considered forfeited and non-refundable.</li>
          <li>Participants agree that if they cancel their participation, the payment is non-refundable, non-reschedulable, and non-transferable to another trip. However, participants may designate a substitute to take their place on the trip.</li>
        </ul>""",
    )
    + note(
        "3. Keadaan Kahar",
        """<ul>
          <li>Dalam situasi keadaan kahar &ndash; seperti bencana alam, kondisi cuaca buruk, kerusuhan sipil, wabah penyakit, peraturan pemerintah, pembatalan penerbangan, atau peristiwa lain di luar kendali &ndash; perjalanan dapat diubah atau dibatalkan tanpa pengembalian dana.</li>
          <li>Agent tidak bertanggung jawab atas kerugian atau ketidaknyamanan apa pun yang diakibatkan oleh peristiwa-peristiwa tersebut.</li>
          <li>Keadaan kahar mengacu pada situasi tak terduga di luar kendali manusia yang menghalangi pelaksanaan perjalanan sesuai rencana.</li>
        </ul>""",
        "3. Force Majeure",
        """<ul>
          <li>In cases of force majeure &ndash; such as natural disasters, adverse weather conditions, civil unrest, disease outbreaks, government regulations, flight cancellation, or other uncontrollable events &ndash; the trip may be changed or canceled without a refund.</li>
          <li>Agent is not responsible for any losses or inconveniences caused by such events.</li>
          <li>Force majeure refers to unforeseen circumstances beyond human control that prevent the trip from proceeding as planned.</li>
        </ul>""",
    )
    + note(
        "4. Keterlambatan Kedatangan",
        "<p>Peserta perjalanan pribadi diinformasikan bahwa setiap keterlambatan yang memengaruhi rencana perjalanan atau jadwal akan mengakibatkan penyesuaian rencana perjalanan berdasarkan waktu yang tersedia. Pihak kapal tidak dapat bertanggung jawab dalam bentuk apa pun atas, ataupun mengakomodasi, perpanjangan durasi perjalanan yang telah ditetapkan.</p>",
        "4. Late Arrival",
        "<p>Private tour participants are advised that any delays affecting the itinerary or schedule will result in adjustments to the itinerary based on the time available. The vessel operator cannot be held liable for, nor accommodate, any extension to the established duration of the trip.</p>",
    )
)

FULL_DAY_RESPONSIBILITY = section(
    "Responsibility", "Tanggung Jawab",
    note(
        "1. Tanggung Jawab",
        """<p><strong>A.</strong> Agent tidak bertanggung jawab dan tidak dapat dimintai pertanggungjawaban atas perubahan atau pembatalan yang disebabkan oleh:</p>
        <ul>
          <li>Jadwal perjalanan yang sangat ketat.</li>
          <li>Kerusakan, kehilangan, atau keterlambatan bagasi oleh maskapai penerbangan, hotel, atau penyedia transportasi lainnya.</li>
        </ul>
        <p><strong>B.</strong> Agent juga tidak bertanggung jawab atas:</p>
        <ul>
          <li>Kerusakan atau kehilangan barang pribadi peserta selama perjalanan.</li>
          <li>Perubahan atau pengurangan rencana perjalanan akibat keadaan kahar/force majeure.</li>
        </ul>""",
        "1. Liability",
        """<p><strong>A.</strong> Agent is not responsible for and cannot be held liable for changes or cancellations caused by:</p>
        <ul>
          <li>Tight travel schedules.</li>
          <li>Damage, loss, or delays of baggage by airlines, hotels, or other transportation providers.</li>
        </ul>
        <p><strong>B.</strong> Agent is also not liable for:</p>
        <ul>
          <li>Damage or loss of participants' personal belongings during the trip.</li>
          <li>Changes or reductions in the itinerary due to force majeure.</li>
        </ul>""",
    )
    + note(
        "2. Tanggung Jawab Peserta",
        """<p><strong>A.</strong> Peserta bertanggung jawab atas segala kehilangan atau kerusakan pada fasilitas perjalanan, seperti jaket pelampung, snorkel, dan masker. Biaya penggantian penuh akan dibebankan kepada peserta untuk barang yang rusak atau hilang.</p>
        <p><strong>B.</strong> Seluruh peserta wajib mematuhi instruksi pemimpin tur selama perjalanan berlangsung. Keputusan atau tindakan sepihak yang menyimpang dari rencana perjalanan (itinerary) atau instruksi yang telah disepakati tidak diperbolehkan tanpa persetujuan sebelumnya dari pihak pengelola kapal.</p>""",
        "2. Participant Responsibility",
        """<p><strong>A.</strong> Participants are responsible for any loss or damage to trip facilities, such as life jackets, snorkels, and masks. Damaged or lost items will be charged at their full replacement value.</p>
        <p><strong>B.</strong> All participants are required to follow the tour leader's instructions throughout the trip. Unilateral decisions or actions that deviate from the agreed itinerary or instructions are not permitted without prior approval from boat management.</p>""",
    )
    + note(
        "3. Perilaku yang Dilarang",
        """<p><strong>A.</strong> Penggunaan narkoba atau tindakan apa pun yang menimbulkan gangguan maupun ketidaknyamanan bagi peserta lain selama perjalanan akan mengakibatkan dikeluarkannya individu tersebut dari rombongan secara langsung.</p>
        <p><strong>B.</strong> Melakukan perbuatan yang merugikan pelaku usaha perjalanan.</p>
        <p><strong>C.</strong> Melakukan perbuatan yang bertentangan dengan hukum Republik Indonesia.</p>
        <p><strong>D.</strong> Dalam situasi demikian, tidak ada pengembalian dana (refund) atas pembayaran yang telah dilakukan.</p>""",
        "3. Prohibited Behavior",
        """<p><strong>A.</strong> The use of illegal drugs or any actions causing disturbances or inconvenience to other participants during the trip will result in the immediate removal of the individual from the group.</p>
        <p><strong>B.</strong> Engaging in acts that cause harm to travel business operators.</p>
        <p><strong>C.</strong> Committing acts contrary to the laws of the Republic of Indonesia.</p>
        <p><strong>D.</strong> In such cases, no refunds will be provided for any payments made.</p>""",
    )
)

FULL_DAY_CLOSING_ID = ("Tamu mengakui telah membaca keseluruhan isi dokumen, memahami keseluruhan isi dokumen dan "
    "menyetujui seluruh syarat dan ketentuan yang tercantum dalam dokumen ini. Semua syarat dan ketentuan ini "
    "dilindungi oleh hukum yang berlaku di wilayah hukum Republik Indonesia.")
FULL_DAY_CLOSING_EN = ("The Guest acknowledges having read and understood the entire contents of this document and "
    "agrees to all terms and conditions set forth therein. All terms and conditions established herein are "
    "governed by the laws and regulations applicable within the jurisdiction of the Republic of Indonesia.")

FULL_DAY_CONTENT = (
    FULL_DAY_TRIP_DETAILS + FULL_DAY_IMPORTANT_NOTES + FLIGHT_INFO + FULL_DAY_RESERVATION
    + FULL_DAY_BILLING + FULL_DAY_CANCELLATION + FULL_DAY_RESPONSIBILITY
)


# ---------------------------------------------------------------------------
# OPEN TRIP CONTENT
# ---------------------------------------------------------------------------

OPEN_TRIP_DETAILS = section(
    "Trip Details", "Detail Perjalanan",
    '    <div class="twocol">\n      <div>\n'
    + lang_group(
        "Include", "Termasuk",
        [
            "Overnight stay on board during the trip",
            "Premium photo and video documentation using Drone, GoPro, and Mirrorless cameras (raw footage only)",
            "Meals during the trip", "Mineral water, coffee, and tea during the trip", "Guide",
            "Snorkeling gear", "Life vest",
            "Pick-up and drop-off services from the hotel or airport to the meeting point, provided exclusively within the Labuan Bajo mainland area near the harbor",
        ],
        [
            "Menginap di kapal selama perjalanan",
            "Dokumentasi foto dan video premium menggunakan kamera Drone, GoPro, dan mirrorless (hanya rekaman mentah)",
            "Makanan selama perjalanan", "Air mineral, kopi, dan teh selama perjalanan", "Pemandu",
            "Perlengkapan snorkeling", "Rompi pelampung",
            "Layanan penjemputan dan pengantaran dari hotel atau bandara ke titik pertemuan disediakan secara eksklusif di area daratan Labuan Bajo dekat pelabuhan",
        ],
        note_en="Accommodation on other islands or in the Manjaga area will not be covered for pick-up services.",
        note_id="Akomodasi di pulau lain atau di area Manjaga tidak akan ditanggung untuk layanan penjemputan.",
    )
    + "      </div>\n      <div>\n"
    + lang_group(
        "Exclude", "Yang Tidak Termasuk",
        [
            "Hotel accommodation before or after the trip (Day -1 / Day +1)",
            "Crew gratuities", "Flight ticket", "Alcohol and non-alcoholic drinks", "Personal snacks",
            "Komodo National Park fee &ndash; ticket prices subject to change based on government regulations",
        ],
        [
            "Akomodasi hotel sebelum atau sesudah perjalanan (H-1/H+1)",
            "Tip kru", "Tiket pesawat", "Alkohol dan minuman non-alkohol", "Camilan pribadi",
            "Biaya Taman Nasional Komodo (harga tiket dapat berubah sesuai dengan peraturan pemerintah yang berlaku pada saat perjalanan)",
        ],
    )
    + "      </div>\n    </div>\n"
    + lang_group("Must Bring Items", "Barang yang Wajib Dibawa", MUST_BRING_EN_OVERNIGHT, MUST_BRING_ID_OVERNIGHT)
)

OPEN_TRIP_IMPORTANT_NOTES = section(
    "Important Notes", "Catatan Penting",
    note(
        "1. Pengaturan Penerbangan",
        "<p>Beberapa maskapai mungkin tidak secara konsisten menawarkan penerbangan langsung ke Labuan Bajo. Penumpang disarankan untuk mengonfirmasi ketersediaan penerbangan langsung melalui aplikasi resmi maskapai tersebut atau pusat informasi.</p>",
        "1. Flight Arrangements",
        "<p>Some airlines may not consistently offer direct flights to Labuan Bajo. Passengers are advised to confirm the availability of direct flights through the respective airline's official application or information center.</p>",
    )
    + note(
        "2. Rekomendasi Kedatangan",
        """<ul>
          <li>Hari Sebelum Perjalanan: Sangat disarankan agar penumpang tiba di Labuan Bajo setidaknya satu hari sebelum perjalanan untuk memastikan jadwal perjalanan berjalan lancar dan menghindari gangguan akibat kemungkinan keterlambatan atau pembatalan penerbangan.</li>
          <li>Hari Perjalanan: Peserta juga dapat tiba pada hari perjalanan, asalkan mereka berada di Labuan Bajo dan siap sebelum pukul 9:00 pagi waktu setempat (WITA/GMT+8). Harap diketahui bahwa kami tidak bertanggung jawab atas pembatalan atau keterlambatan penerbangan apa pun.</li>
        </ul>""",
        "2. Arrival Recommendations",
        """<ul>
          <li>Day Before the Trip: It is strongly recommended that passengers arrive in Labuan Bajo at least one day before the trip to ensure a smooth itinerary and avoid disruptions caused by potential flight delays or cancellations.</li>
          <li>Day of the Trip: Participants may also arrive on the day of the trip, provided they are in Labuan Bajo and ready by 9:00 a.m. local time (WITA/GMT+8). Please be aware that we are not responsible for any flight cancellations or delays.</li>
        </ul>""",
    )
    + note(
        "3. Masalah Selama Perjalanan",
        """<ul>
          <li>Tamu harus segera melaporkan masalah atau kekhawatiran selama perjalanan kepada kru yang bertugas atau Pemandu Wisata. Pelaporan cepat memastikan kesempatan untuk menyelesaikan masalah selama perjalanan.</li>
          <li>Keluhan yang tertunda atau setelah perjalanan tidak dapat ditangani setelah perjalanan selesai.</li>
        </ul>""",
        "3. On-Trip Issues",
        """<ul>
          <li>Guests must immediately report any issues or concerns during the trip to the on-duty crew members or the Tour Guide. Prompt reporting ensures the opportunity to resolve the matter during the journey.</li>
          <li>Delayed or post-trip complaints cannot be addressed after the trip concludes.</li>
        </ul>""",
    )
    + note(
        "4. Keramaian Musim Ramai",
        "<p>Selama musim puncak, destinasi populer seperti Manta Point, Pulau Padar, Pink Beach, dan Pulau Komodo mungkin mengalami lalu lintas pengunjung yang tinggi. Agent tidak bertanggung jawab atas keluhan terkait kondisi padat di lokasi-lokasi tersebut.</p>",
        "4. High Season Crowds",
        "<p>During the high season, popular destinations such as Manta Point, Padar Island, Pink Beach, and Komodo Island may experience high visitor traffic. Agent is not responsible for any complaints related to crowded conditions at these locations.</p>",
    )
    + note(
        "5. Kebijakan Keluhan",
        """<ul>
          <li>Setiap kekhawatiran terkait kekurangan layanan selama perjalanan harus segera dilaporkan kepada Pemimpin Tur atau Direktur Phinisi di kapal. Direktur Phinisi akan bekerja untuk memberikan solusi yang tepat.</li>
          <li>Harap dicatat bahwa keluhan yang diajukan setelah perjalanan tidak akan diterima oleh Agent.</li>
        </ul>""",
        "5. Complaint Policy",
        """<ul>
          <li>Any concerns regarding service shortfalls during the trip must be reported to the Tour Leader or Cruise Director onboard immediately. The Cruise Director will work to provide an appropriate solution.</li>
          <li>Please note that complaints lodged after the trip will not be accepted by Agent.</li>
        </ul>""",
    )
    + note(
        "6. Persyaratan Peserta Minimum",
        "<p>Perjalanan kami membutuhkan minimal 10 peserta untuk melanjutkan. Ambang batas ini memastikan semua tamu menikmati pengalaman yang penuh dan menarik.</p>",
        "6. Minimum Participant Requirement",
        "<p>Our trips require a minimum of 10 participants to proceed. This threshold ensures that all guests enjoy a full and engaging experience.</p>",
    )
    + note(
        "7. Pengaturan Alternatif",
        "<p>Jika jumlah peserta minimum tidak terpenuhi, kami berhak menawarkan kapal alternatif untuk tanggal perjalanan yang dijadwalkan. Langkah ini menjamin tidak ada perjalanan terjadwal yang dibatalkan dan rencana perjalanan tamu kami dihormati.</p>",
        "7. Alternative Arrangements",
        "<p>In the event that the minimum number of participants is not met, we reserve the right to offer an alternative vessel for the scheduled trip date. This measure guarantees that no scheduled trip is canceled and that our guests' travel plans are respected.</p>",
    )
)

OPEN_TRIP_RESERVATION = section(
    "Reservation Terms", "Ketentuan Reservasi",
    note(
        "1. Konfirmasi Ketersediaan",
        "<p>Mohon konfirmasi ketersediaan terlebih dahulu. Pemesanan dilakukan paling lambat 20 hari sebelum tanggal keberangkatan.</p>",
        "1. Availability Confirmation",
        "<p>Please confirm availability before booking. Reservations must be made at least 20 days before the departure date.</p>",
    )
    + note(
        "2. Persyaratan Uang Muka",
        "<p>Pemesanan hanya dapat dilakukan dengan pembayaran uang muka.</p>",
        "2. Down Payment Requirement",
        "<p>Booking can only be made with a down payment.</p>",
    )
    + note(
        "3. Proses Pembayaran",
        """<ul>
          <li>Deposit sebesar 50% diperlukan untuk mengamankan pemesanan perjalanan.</li>
          <li>Deposit tidak dapat dikembalikan jika peserta membatalkan kapan saja.</li>
          <li>Sisa pembayaran harus dilakukan paling lambat 20 hari sebelum perjalanan.</li>
          <li>Pembayaran penuh harus dilakukan jika perjalanan kurang dari 20 hari lagi.</li>
        </ul>""",
        "3. Payment Process",
        """<ul>
          <li>A 50% deposit is required to secure the trip.</li>
          <li>The deposit is non-refundable in the event of participant cancellation at any time.</li>
          <li>The remaining payment must be made no later than 20 days before the trip.</li>
          <li>The full payment must be made if the trip is less than 20 days away.</li>
        </ul>""",
    )
    + note(
        "4. Konfirmasi Pembayaran &amp; Dokumentasi",
        "<p>Konfirmasikan pembayaran melalui Agent terkait dengan mengirimkan bukti pembayaran. Agent menyediakan dokumentasi selama perjalanan. Setiap peserta setuju untuk direkam dan difoto, dan Agent berhak menggunakan rekaman tersebut untuk tujuan promosi.</p>",
        "4. Payment Confirmation &amp; Documentation",
        "<p>Please send proof of payment to your booking agent for confirmation. Agent provides documentation during the trip. Each participant agrees to be recorded and photographed, and Agent reserves the right to use the footage for promotional purposes.</p>",
    )
)

OPEN_TRIP_BILLING = section(
    "Payment &amp; Billing Policy", "Kebijakan Pembayaran &amp; Penagihan",
    note(
        "1. Syarat Harga",
        """<ul>
          <li>Tarif berlaku untuk tahun penerbitan dan dapat berubah setiap tahun.</li>
          <li>Penyesuaian harga dapat terjadi akibat faktor-faktor seperti biaya bahan bakar, rute atau aktivitas tambahan, peraturan pemerintah, atau kondisi lain di luar kendali Agent.</li>
        </ul>""",
        "1. Pricing Terms",
        """<ul>
          <li>Rates apply to the year in which they are issued and are subject to change annually.</li>
          <li>Price adjustments may occur due to factors such as fuel costs, additional routes or activities, government regulations, or other conditions beyond the control of Agent.</li>
        </ul>""",
    )
    + note(
        "2. Jadwal Pemesanan dan Pembayaran",
        "<p>Uang muka sebesar 50% diperlukan untuk mengamankan pemesanan. Pembayaran penuh harus dilakukan paling lambat 20 hari sebelum tanggal keberangkatan. Harap dicatat bahwa syarat dan ketentuan kapal terkait akan berlaku untuk kapal tertentu.</p>",
        "2. Booking and Payment Schedule",
        "<p>A 50% down payment is required to secure a booking. Full payment must be made no later than 20 days prior to the departure date. Kindly note that the terms and conditions of the respective vessel will apply to certain vessels.</p>",
    )
    + note(
        "3. Kebijakan Anak",
        "<p>Anak-anak berusia 3 tahun ke atas akan dikenakan tarif penuh.</p>",
        "3. Child Policy",
        "<p>Children aged 3 years and above will be charged the full rate.</p>",
    )
    + note(
        "4. Biaya Bank",
        """<ul>
          <li>Semua biaya bank terkait pembayaran harus ditanggung oleh pengirim.</li>
          <li>Total jumlah pembayaran yang kami terima harus persis sesuai dengan jumlah yang tercantum pada faktur. Setiap ketidaksesuaian akibat biaya bank atau biaya transfer akan menjadi tanggung jawab klien.</li>
          <li>Baik Agent maupun operator tur tidak akan bertanggung jawab atas biaya bank tambahan yang timbul selama transfer, deposit, atau pembayaran saldo.</li>
        </ul>""",
        "4. Bank Charges",
        """<ul>
          <li>All bank charges related to payments must be borne by the sender.</li>
          <li>The total payment amount received by us must exactly match the amount specified on the invoice. Any discrepancies due to bank charges or transfer fees will be the responsibility of the client.</li>
          <li>Neither Agent nor the tour operator will be held accountable for additional bank charges incurred during transfers, deposits, or balance payments.</li>
        </ul>""",
    )
)

OPEN_TRIP_CANCELLATION = section(
    "Cancellation Policy", "Kebijakan Pembatalan",
    note(
        "1. Ketentuan Umum Pembatalan",
        "<p>Untuk pembatalan yang dilakukan 20 hari, kurang atau lebih sebelum tanggal keberangkatan, 100% dari total pembayaran akan hangus dan tidak dapat dikembalikan.</p>",
        "1. General Cancellation Terms",
        "<p>For cancellations made 20 days, less or more before the departure date, 100% of the total payment will be forfeited and is non-refundable.</p>",
    )
    + note(
        "2. Syarat Biaya Pembatalan",
        """<ul>
          <li>Setelah pendaftaran, deposit habis dan tidak dapat dikembalikan.</li>
          <li>Jika peserta membatalkan, pembayaran tidak dapat dikembalikan, dijadwalkan ulang, atau dipindahkan ke perjalanan lain. Namun, peserta dapat menominasikan pengganti untuk menggantikan mereka.</li>
        </ul>""",
        "2. Cancellation Fee Conditions",
        """<ul>
          <li>After registration, the deposit is forfeited and non-refundable.</li>
          <li>If a participant cancels, payments cannot be refunded, rescheduled, or transferred to another trip. However, participants may nominate a replacement person to take their place.</li>
        </ul>""",
    )
    + note(
        "3. Keadaan Kahar",
        """<ul>
          <li>Dalam kasus Keadaan Kahar &ndash; seperti bencana alam, kondisi cuaca buruk, kerusuhan sipil, wabah penyakit, peraturan pemerintah, pembatalan penerbangan, atau kejadian lain yang tidak dapat dikendalikan &ndash; perjalanan dapat diubah atau dibatalkan tanpa pengembalian dana.</li>
          <li>Agent tidak bertanggung jawab atas kerugian atau ketidaknyamanan yang disebabkan oleh kejadian tersebut.</li>
          <li>Keadaan Kahar mengacu pada keadaan tak terduga di luar kendali manusia yang menghalangi perjalanan berjalan sesuai rencana.</li>
        </ul>""",
        "3. Force Majeure",
        """<ul>
          <li>In cases of force majeure &ndash; such as natural disasters, adverse weather conditions, civil unrest, disease outbreaks, government regulations, flight cancellation, or other uncontrollable events &ndash; the trip may be changed or canceled without a refund.</li>
          <li>Agent is not responsible for any losses or inconveniences caused by such events.</li>
          <li>Force majeure refers to unforeseen circumstances beyond human control that prevent the trip from proceeding as planned.</li>
        </ul>""",
    )
    + note(
        "4. Keterlambatan Kedatangan",
        "<p>Peserta perjalanan pribadi diberitahu bahwa setiap keterlambatan yang memengaruhi itinerary atau jadwal akan mengakibatkan penyesuaian itinerary berdasarkan waktu yang tersedia. Kapal tidak dapat dimintai pertanggungjawaban atau mengakomodasi perpanjangan durasi perjalanan yang dialokasikan.</p>",
        "4. Late Arrival",
        "<p>Participants of private trips are advised that any delays impacting the itinerary or schedule will result in adjustments to the itinerary based on the available time. The vessel cannot be held responsible for or accommodate extensions to the allocated trip duration.</p>",
    )
)

OPEN_TRIP_RESPONSIBILITY = section(
    "Responsibility", "Tanggung Jawab",
    note(
        "1. Tanggung Jawab",
        """<p><strong>A.</strong> Agent tidak bertanggung jawab atas dan tidak dapat dimintai pertanggungjawaban atas perubahan atau pembatalan yang disebabkan oleh:</p>
        <ul>
          <li>Jadwal perjalanan yang ketat.</li>
          <li>Kerusakan, kehilangan, atau keterlambatan bagasi oleh maskapai penerbangan, hotel, atau penyedia transportasi lainnya.</li>
        </ul>
        <p><strong>B.</strong> Agent juga tidak bertanggung jawab atas:</p>
        <ul>
          <li>Kerusakan atau kehilangan barang pribadi peserta selama perjalanan.</li>
          <li>Perubahan atau pengurangan jadwal perjalanan akibat force majeure.</li>
        </ul>""",
        "1. Liability",
        """<p><strong>A.</strong> Agent is not responsible for and cannot be held liable for changes or cancellations caused by:</p>
        <ul>
          <li>Tight travel schedules.</li>
          <li>Damage, loss, or delays of baggage by airlines, hotels, or other transportation providers.</li>
        </ul>
        <p><strong>B.</strong> Agent is also not liable for:</p>
        <ul>
          <li>Damage or loss of participants' personal belongings during the trip.</li>
          <li>Changes or reductions in the itinerary due to force majeure.</li>
        </ul>""",
    )
    + note(
        "2. Tanggung Jawab Peserta",
        """<p><strong>A.</strong> Peserta bertanggung jawab atas kerugian atau kerusakan fasilitas perjalanan, seperti jaket pelampung, snorkel, dan masker. Barang yang rusak atau hilang akan dikenakan biaya penggantian penuh.</p>
        <p><strong>B.</strong> Semua peserta diwajibkan mengikuti instruksi pemimpin tur sepanjang perjalanan. Keputusan atau tindakan sepihak yang menyimpang dari itinerary atau instruksi yang disepakati tidak diperbolehkan tanpa persetujuan sebelumnya dari manajemen kapal.</p>
        <p><strong>C.</strong> Peserta bertanggung jawab sendiri dengan kesehatan dan pengobatan masing-masing peserta.</p>""",
        "2. Participant Responsibility",
        """<p><strong>A.</strong> Participants are responsible for any loss or damage to trip facilities, such as life jackets, snorkels, and masks. Damaged or lost items will be charged at their full replacement value.</p>
        <p><strong>B.</strong> All participants are required to follow the tour leader's instructions throughout the trip. Unilateral decisions or actions that deviate from the agreed itinerary or instructions are not permitted without prior approval from boat management.</p>
        <p><strong>C.</strong> Participants are responsible for their own health and treatment.</p>""",
    )
    + note(
        "3. Perilaku yang Dilarang",
        """<p><strong>A.</strong> Penggunaan narkoba ilegal atau tindakan yang menimbulkan gangguan atau ketidaknyamanan bagi peserta lain selama perjalanan akan mengakibatkan individu tersebut segera dikeluarkan dari kelompok.</p>
        <p><strong>B.</strong> Dalam kasus seperti itu, tidak akan diberikan pengembalian dana untuk pembayaran yang dilakukan.</p>""",
        "3. Prohibited Behavior",
        """<p><strong>A.</strong> The use of illegal drugs or any actions causing disturbances or inconvenience to other participants during the trip will result in the immediate removal of the individual from the group.</p>
        <p><strong>B.</strong> In such cases, no refunds will be provided for any payments made.</p>""",
    )
)

OPEN_TRIP_CLOSING_ID = ("Tamu mengakui telah terlebih dahulu membaca keseluruhan syarat dan ketentuan yang ada dan "
    "menyetujui semua syarat dan ketentuan yang diuraikan dalam dokumen ini. Semua syarat dan ketentuan ini "
    "dilindungi oleh hukum yang berlaku di wilayah hukum Republik Indonesia.")
OPEN_TRIP_CLOSING_EN = ("The Guest acknowledges that he has first read all of the terms and conditions and agrees to "
    "all the terms and conditions outlined in this document. All terms and conditions made are protected by the "
    "rule of law applicable in the jurisdiction of the Republic of Indonesia.")

OPEN_TRIP_CONTENT = (
    OPEN_TRIP_DETAILS + OPEN_TRIP_IMPORTANT_NOTES + FLIGHT_INFO + OPEN_TRIP_RESERVATION
    + OPEN_TRIP_BILLING + OPEN_TRIP_CANCELLATION + OPEN_TRIP_RESPONSIBILITY
)


# ---------------------------------------------------------------------------
# PRIVATE TRIP CONTENT (shares most structure with Open Trip; 30-day terms,
# drone ticket note, and extra clauses on complaints / health / social media)
# ---------------------------------------------------------------------------

PRIVATE_TRIP_DETAILS = section(
    "Trip Details", "Detail Perjalanan",
    '    <div class="twocol">\n      <div>\n'
    + lang_group(
        "Include", "Termasuk",
        [
            "Overnight stay on board during the trip",
            "Premium photo and video documentation using Drone, GoPro, and Mirrorless cameras (raw footage only)",
            "Meals during the trip", "Mineral water, coffee, and tea during the trip", "Guide",
            "Snorkeling gear", "Life vest",
            "Pick-up and drop-off services from the hotel or airport to the meeting point, provided exclusively within the Labuan Bajo mainland area near the harbor",
        ],
        [
            "Menginap di kapal selama perjalanan",
            "Dokumentasi foto dan video premium menggunakan kamera Drone, GoPro, dan mirrorless (hanya rekaman mentah)",
            "Makanan selama perjalanan", "Air mineral, kopi, dan teh selama perjalanan", "Pemandu",
            "Perlengkapan snorkeling", "Rompi pelampung",
            "Layanan penjemputan dan pengantaran dari hotel atau bandara ke titik pertemuan disediakan secara eksklusif di area daratan Labuan Bajo dekat pelabuhan",
        ],
        note_en="Accommodation on other islands or in the Manjaga area will not be covered for pick-up services.",
        note_id="Akomodasi di pulau lain atau di area Manjaga tidak akan ditanggung untuk layanan penjemputan.",
    )
    + "      </div>\n      <div>\n"
    + lang_group(
        "Exclude", "Yang Tidak Termasuk",
        [
            "Hotel accommodation before or after the trip (Day -1 / Day +1)",
            "Crew gratuities", "Flight ticket", "Alcohol and non-alcoholic drinks", "Personal snacks",
            "Komodo National Park fee &ndash; ticket prices subject to change based on government regulations",
            "Drone ticket for Komodo National Park &ndash; estimated cost IDR 2,100,000; not mandatory, permit should be requested 7 days before the trip",
        ],
        [
            "Akomodasi hotel sebelum atau sesudah perjalanan (H-1/H+1)",
            "Tip kru", "Tiket pesawat", "Alkohol dan minuman non-alkohol", "Camilan pribadi",
            "Biaya Taman Nasional Komodo (harga tiket dapat berubah sesuai dengan peraturan pemerintah yang berlaku pada saat perjalanan)",
            "Tiket drone ke Taman Nasional Komodo (perkiraan biaya IDR 2.100.000; tidak wajib &amp; izin harus diminta 7 hari sebelum perjalanan)",
        ],
    )
    + "      </div>\n    </div>\n"
    + lang_group("Must Bring Items", "Barang yang Wajib Dibawa", MUST_BRING_EN_OVERNIGHT, MUST_BRING_ID_OVERNIGHT)
)

PRIVATE_TRIP_IMPORTANT_NOTES = section(
    "Important Notes", "Catatan Penting",
    note(
        "1. Pengaturan Penerbangan",
        "<p>Beberapa maskapai mungkin tidak secara konsisten menawarkan penerbangan langsung ke Labuan Bajo. Penumpang disarankan untuk mengonfirmasi ketersediaan penerbangan langsung melalui aplikasi resmi maskapai tersebut atau pusat informasi.</p>",
        "1. Flight Arrangements",
        "<p>Some airlines may not consistently offer direct flights to Labuan Bajo. Passengers are advised to confirm the availability of direct flights through the respective airline's official application or information center.</p>",
    )
    + note(
        "2. Rekomendasi Kedatangan",
        """<ul>
          <li>Hari Sebelum Perjalanan: Sangat disarankan agar penumpang tiba di Labuan Bajo setidaknya satu hari sebelum perjalanan untuk memastikan jadwal perjalanan berjalan lancar dan menghindari gangguan akibat kemungkinan keterlambatan atau pembatalan penerbangan.</li>
          <li>Hari Perjalanan: Peserta juga dapat tiba pada hari perjalanan, asalkan mereka berada di Labuan Bajo dan siap sebelum pukul 9:00 pagi waktu setempat (WITA/GMT+8). Harap diketahui bahwa kami tidak bertanggung jawab atas pembatalan atau keterlambatan penerbangan apa pun.</li>
        </ul>""",
        "2. Arrival Recommendations",
        """<ul>
          <li>Day Before the Trip: It is strongly recommended that passengers arrive in Labuan Bajo at least one day before the trip to ensure a smooth itinerary and avoid disruptions caused by potential flight delays or cancellations.</li>
          <li>Day of the Trip: Participants may also arrive on the day of the trip, provided they are in Labuan Bajo and ready by 9:00 a.m. local time (WITA/GMT+8). Please be aware that we are not responsible for any flight cancellations or delays.</li>
        </ul>""",
    )
    + note(
        "3. Masalah Selama Perjalanan",
        """<ul>
          <li>Tamu harus segera melaporkan masalah atau kekhawatiran selama perjalanan kepada kru yang bertugas atau Pemandu Wisata. Pelaporan cepat memastikan kesempatan untuk menyelesaikan masalah selama perjalanan.</li>
          <li>Keluhan yang tertunda atau setelah perjalanan tidak dapat ditangani setelah perjalanan selesai.</li>
        </ul>""",
        "3. On-Trip Issues",
        """<ul>
          <li>Guests must immediately report any issues or concerns during the trip to the on-duty crew members or the Tour Guide. Prompt reporting ensures the opportunity to resolve the matter during the journey.</li>
          <li>Delayed or post-trip complaints cannot be addressed after the trip concludes.</li>
        </ul>""",
    )
    + note(
        "4. Keramaian Musim Ramai",
        "<p>Selama musim puncak, destinasi populer seperti Manta Point, Pulau Padar, Pink Beach, dan Pulau Komodo mungkin mengalami lalu lintas pengunjung yang tinggi. Agent tidak bertanggung jawab atas keluhan terkait kondisi padat di lokasi-lokasi tersebut.</p>",
        "4. High Season Crowds",
        "<p>During the high season, popular destinations such as Manta Point, Padar Island, Pink Beach, and Komodo Island may experience high visitor traffic. Agent is not responsible for any complaints related to crowded conditions at these locations.</p>",
    )
    + note(
        "5. Kebijakan Keluhan",
        """<ul>
          <li>Setiap kekhawatiran terkait kekurangan layanan selama perjalanan harus segera dilaporkan kepada Pemimpin Tur atau Direktur Phinisi di kapal. Direktur Phinisi akan bekerja untuk memberikan solusi yang tepat.</li>
          <li>Harap dicatat bahwa keluhan yang diajukan setelah perjalanan tidak akan diterima oleh Agent.</li>
          <li>Keluhan yang ditanggapi adalah keluhan yang dilaporkan kepada Pemimpin Tur atau Direktur Kapal Phinisi di kapal; keluhan kepada pihak lain tidak akan ditanggapi.</li>
        </ul>""",
        "5. Complaint Policy",
        """<ul>
          <li>Any concerns regarding service shortfalls during the trip must be reported to the Tour Leader or Cruise Director onboard immediately. The Cruise Director will work to provide an appropriate solution.</li>
          <li>Please note that complaints lodged after the trip will not be accepted by Agent.</li>
          <li>Complaints that are responded to are complaints reported to the Tour Leader or Cruise Director on the ship; complaints to other parties will not be responded to.</li>
        </ul>""",
    )
)

PRIVATE_TRIP_RESERVATION = section(
    "Reservation Terms", "Ketentuan Reservasi",
    note(
        "1. Konfirmasi Ketersediaan",
        "<p>Mohon konfirmasi ketersediaan terlebih dahulu. Pemesanan dilakukan paling lambat 30 hari sebelum tanggal keberangkatan.</p>",
        "1. Availability Confirmation",
        "<p>Please confirm availability before booking. Reservations must be made at least 30 days before the departure date.</p>",
    )
    + note(
        "2. Persyaratan Uang Muka",
        "<p>Pemesanan hanya dapat dilakukan dengan pembayaran uang muka.</p>",
        "2. Down Payment Requirement",
        "<p>Booking can only be made with a down payment.</p>",
    )
    + note(
        "3. Proses Pembayaran",
        """<ul>
          <li>Deposit sebesar 50% diperlukan untuk mengamankan pemesanan perjalanan.</li>
          <li>Peserta setuju deposit tidak dapat dikembalikan jika peserta membatalkan secara sepihak kapan saja sejak uang deposit diberikan.</li>
          <li>Sisa pembayaran harus dilakukan paling lambat 30 hari sebelum perjalanan.</li>
          <li>Pembayaran penuh harus dilakukan jika perjalanan kurang dari 30 hari lagi.</li>
        </ul>""",
        "3. Payment Process",
        """<ul>
          <li>A 50% deposit is required to secure the trip.</li>
          <li>The participant agrees that the deposit is non-refundable if the participant unilaterally cancels at any time after the deposit has been paid.</li>
          <li>The remaining payment must be made no later than 30 days before the trip.</li>
          <li>The full payment must be made if the trip is less than 30 days away.</li>
        </ul>""",
    )
    + note(
        "4. Konfirmasi Pembayaran &amp; Dokumentasi",
        "<p>Konfirmasikan pembayaran melalui agent terkait dengan mengirimkan bukti pembayaran. Agent menyediakan dokumentasi selama perjalanan. Setiap peserta setuju untuk direkam dan difoto, dan Agent berhak menggunakan rekaman tersebut untuk tujuan promosi.</p>",
        "4. Payment Confirmation &amp; Documentation",
        "<p>Please send proof of payment to your booking agent for confirmation. Agent provides documentation during the trip. Each participant agrees to be recorded and photographed, and Agent reserves the right to use the footage for promotional purposes.</p>",
    )
)

PRIVATE_TRIP_BILLING = section(
    "Payment &amp; Billing Policy", "Kebijakan Pembayaran &amp; Penagihan",
    note(
        "1. Ketentuan Harga",
        """<ul>
          <li>Tarif berlaku untuk tahun penerbitannya dan dapat berubah setiap tahun.</li>
          <li>Penyesuaian harga dapat terjadi akibat faktor-faktor seperti biaya bahan bakar, rute atau aktivitas tambahan, peraturan pemerintah, atau kondisi lain di luar kendali Agent.</li>
        </ul>""",
        "1. Pricing Terms",
        """<ul>
          <li>Rates apply to the year in which they are issued and are subject to change annually.</li>
          <li>Price adjustments may occur due to factors such as fuel costs, additional routes or activities, government regulations, or other conditions beyond the control of Agent.</li>
        </ul>""",
    )
    + note(
        "2. Jadwal Pemesanan dan Pembayaran",
        """<ul>
          <li>Uang muka sebesar 50% diperlukan untuk mengamankan pemesanan.</li>
          <li>Pembayaran penuh harus dilakukan paling lambat 30 hari sebelum tanggal keberangkatan.</li>
          <li>Untuk pemesanan yang dilakukan satu tahun sebelumnya, deposit 30% diperlukan untuk mengonfirmasi charter. Tambahan 20% dari deposit harus dibayarkan 120 hari sebelum perjalanan, dengan sisa pembayaran (pembayaran penuh) jatuh tempo 30 hari sebelum keberangkatan.</li>
          <li>Harap dicatat bahwa syarat dan ketentuan kapal terkait akan berlaku untuk kapal tertentu.</li>
        </ul>""",
        "2. Booking and Payment Schedule",
        """<ul>
          <li>A 50% down payment is required to secure a booking.</li>
          <li>Full payment must be made no later than 30 days prior to the departure date.</li>
          <li>For bookings made one year in advance, a 30% deposit is required to confirm the charter. An additional 20% of the deposit must be paid 120 days before the trip, with the remaining balance (full payment) due 30 days before departure.</li>
          <li>Kindly note that the terms and conditions of the respective vessel will apply to certain vessels.</li>
        </ul>""",
    )
    + note(
        "3. Kebijakan Anak",
        "<p>Anak-anak berusia 3 tahun ke atas akan dikenakan tarif penuh.</p>",
        "3. Child Policy",
        "<p>Children aged 3 years and above will be charged the full rate.</p>",
    )
    + note(
        "4. Biaya Bank",
        """<ul>
          <li>Semua biaya bank terkait pembayaran harus ditanggung oleh pengirim.</li>
          <li>Total jumlah pembayaran yang kami terima harus persis sesuai dengan jumlah yang tercantum pada faktur. Setiap ketidaksesuaian akibat biaya bank atau biaya transfer akan menjadi tanggung jawab klien.</li>
          <li>Baik Agent maupun operator tur tidak akan bertanggung jawab atas biaya bank tambahan yang timbul selama transfer, deposit, atau pembayaran saldo.</li>
        </ul>""",
        "4. Bank Charges",
        """<ul>
          <li>All bank charges related to payments must be borne by the sender.</li>
          <li>The total payment amount received by us must exactly match the amount specified on the invoice. Any discrepancies due to bank charges or transfer fees will be the responsibility of the client.</li>
          <li>Neither Agent nor the tour operator will be held accountable for additional bank charges incurred during transfers, deposits, or balance payments.</li>
        </ul>""",
    )
)

PRIVATE_TRIP_CANCELLATION = section(
    "Cancellation Policy", "Kebijakan Pembatalan",
    note(
        "1. Ketentuan Umum Pembatalan",
        "<p>Untuk pembatalan sepihak atau atas keinginan dari penumpang yang dilakukan 30 hari, kurang atau lebih sebelum tanggal keberangkatan, 100% dari total pembayaran akan hangus dan tidak dapat dikembalikan.</p>",
        "1. General Cancellation Terms",
        "<p>For unilateral cancellations or those initiated by the passenger &ndash; whether made 30 days, less than 30 days, or more than 30 days prior to the departure date &ndash; 100% of the total payment will be forfeited and is non-refundable.</p>",
    )
    + note(
        "2. Ketentuan Biaya Pembatalan",
        """<ul>
          <li>Peserta setuju: setelah pendaftaran, deposit habis dan tidak dapat dikembalikan.</li>
          <li>Peserta setuju: jika peserta membatalkan perjalanan karena keinginan sendiri, pembayaran yang sudah dilakukan tidak dapat dikembalikan, kecuali ada kebijakan lain dari perusahaan seperti perjalanan dijadwalkan ulang atau dipindahkan ke perjalanan lain. Namun, peserta dapat menominasikan pengganti untuk menggantikan mereka.</li>
        </ul>""",
        "2. Cancellation Fee Conditions",
        """<ul>
          <li>Participant agreement after registration: the deposit is fully utilized and non-refundable.</li>
          <li>Participants agree that if they cancel the trip of their own volition, payments already made are non-refundable, unless the company adopts a different policy &ndash; such as rescheduling the trip or transferring the booking to another trip. However, participants may nominate a substitute to take their place.</li>
        </ul>""",
    )
    + note(
        "3. Keadaan Kahar",
        """<ul>
          <li>Dalam kasus Keadaan Kahar &ndash; seperti bencana alam, kondisi cuaca buruk, kerusuhan sipil, wabah penyakit, peraturan pemerintah, pembatalan penerbangan, atau kejadian lain yang tidak dapat dikendalikan &ndash; perjalanan dapat diubah atau dibatalkan tanpa pengembalian dana.</li>
          <li>Agent tidak bertanggung jawab atas kerugian atau ketidaknyamanan yang disebabkan oleh kejadian tersebut.</li>
          <li>Keadaan Kahar mengacu pada keadaan tak terduga di luar kendali manusia yang menghalangi perjalanan berjalan sesuai rencana.</li>
        </ul>""",
        "3. Force Majeure",
        """<ul>
          <li>In cases of force majeure &ndash; such as natural disasters, adverse weather conditions, civil unrest, disease outbreaks, government regulations, flight cancellation, or other uncontrollable events &ndash; the trip may be changed or canceled without a refund.</li>
          <li>Agent is not responsible for any losses or inconveniences caused by such events.</li>
          <li>Force majeure refers to unforeseen circumstances beyond human control that prevent the trip from proceeding as planned.</li>
        </ul>""",
    )
    + note(
        "4. Keterlambatan Kedatangan",
        "<p>Peserta perjalanan pribadi diberitahu bahwa setiap keterlambatan yang memengaruhi itinerary atau jadwal akan mengakibatkan penyesuaian itinerary berdasarkan waktu yang tersedia. Kapal tidak dapat dimintai pertanggungjawaban atau mengakomodasi perpanjangan durasi perjalanan yang dialokasikan.</p>",
        "4. Late Arrival",
        "<p>Participants of private trips are advised that any delays impacting the itinerary or schedule will result in adjustments to the itinerary based on the available time. The vessel cannot be held responsible for or accommodate extensions to the allocated trip duration.</p>",
    )
)

PRIVATE_TRIP_RESPONSIBILITY = section(
    "Responsibility", "Tanggung Jawab",
    note(
        "1. Tanggung Jawab",
        """<p><strong>A.</strong> Agent tidak bertanggung jawab atas dan tidak dapat dimintai pertanggungjawaban atas perubahan atau pembatalan yang disebabkan oleh:</p>
        <ul>
          <li>Jadwal perjalanan yang ketat.</li>
          <li>Kerusakan, kehilangan, atau keterlambatan bagasi oleh maskapai penerbangan, hotel, atau penyedia transportasi lainnya.</li>
        </ul>
        <p><strong>B.</strong> Agent juga tidak bertanggung jawab atas:</p>
        <ul>
          <li>Kerusakan atau kehilangan barang pribadi peserta selama perjalanan.</li>
          <li>Perubahan atau pengurangan jadwal perjalanan akibat force majeure.</li>
        </ul>""",
        "1. Liability",
        """<p><strong>A.</strong> Agent is not responsible for and cannot be held liable for changes or cancellations caused by:</p>
        <ul>
          <li>Tight travel schedules.</li>
          <li>Damage, loss, or delays of baggage by airlines, hotels, or other transportation providers.</li>
        </ul>
        <p><strong>B.</strong> Agent is also not liable for:</p>
        <ul>
          <li>Damage or loss of participants' personal belongings during the trip.</li>
          <li>Changes or reductions in the itinerary due to force majeure.</li>
        </ul>""",
    )
    + note(
        "2. Tanggung Jawab Peserta",
        """<p><strong>A.</strong> Peserta bertanggung jawab atas kerugian atau kerusakan fasilitas perjalanan, seperti jaket pelampung, snorkel, dan masker. Barang yang rusak atau hilang akan dikenakan biaya penggantian penuh.</p>
        <p><strong>B.</strong> Peserta bertanggung jawab sendiri dengan kesehatan dan pengobatan masing-masing peserta.</p>
        <p><strong>C.</strong> Semua peserta diwajibkan mengikuti instruksi pemimpin tur sepanjang perjalanan. Keputusan atau tindakan sepihak yang menyimpang dari itinerary atau instruksi yang disepakati tidak diperbolehkan tanpa persetujuan sebelumnya dari manajemen kapal.</p>""",
        "2. Participant Responsibility",
        """<p><strong>A.</strong> Participants are responsible for any loss or damage to trip facilities, such as life jackets, snorkels, and masks. Damaged or lost items will be charged at their full replacement value.</p>
        <p><strong>B.</strong> Participants are responsible for their own health and treatment.</p>
        <p><strong>C.</strong> All participants are required to follow the tour leader's instructions throughout the trip. Unilateral decisions or actions that deviate from the agreed itinerary or instructions are not permitted without prior approval from boat management.</p>""",
    )
    + note(
        "3. Perilaku yang Dilarang",
        """<p><strong>A.</strong> Penggunaan narkoba ilegal atau tindakan yang menimbulkan gangguan atau ketidaknyamanan bagi peserta lain selama perjalanan akan mengakibatkan individu tersebut segera dikeluarkan dari kelompok.</p>
        <p><strong>B.</strong> Dalam kasus seperti itu, tidak akan diberikan pengembalian dana untuk pembayaran yang dilakukan.</p>
        <p><strong>C.</strong> Memberikan informasi di media sosial yang merugikan Pihak Perusahaan.</p>""",
        "3. Prohibited Behavior",
        """<p><strong>A.</strong> The use of illegal drugs or any actions causing disturbances or inconvenience to other participants during the trip will result in the immediate removal of the individual from the group.</p>
        <p><strong>B.</strong> In such cases, no refunds will be provided for any payments made.</p>
        <p><strong>C.</strong> Providing information on social media that is detrimental to the Company.</p>""",
    )
)

PRIVATE_TRIP_CLOSING_ID = OPEN_TRIP_CLOSING_ID
PRIVATE_TRIP_CLOSING_EN = OPEN_TRIP_CLOSING_EN

PRIVATE_TRIP_CONTENT = (
    PRIVATE_TRIP_DETAILS + PRIVATE_TRIP_IMPORTANT_NOTES + FLIGHT_INFO + PRIVATE_TRIP_RESERVATION
    + PRIVATE_TRIP_BILLING + PRIVATE_TRIP_CANCELLATION + PRIVATE_TRIP_RESPONSIBILITY
)


# ---------------------------------------------------------------------------
# Build pages
# ---------------------------------------------------------------------------

PAGES = [
    dict(
        filename="full-day-trip.html",
        file_label="Full-Day-Trip",
        page_title="Full Day Trip Komodo Island — Terms & Conditions | Komodo & Ko",
        trip_name="Full Day Trip Komodo Island",
        content=FULL_DAY_CONTENT,
        closing_id=FULL_DAY_CLOSING_ID,
        closing_en=FULL_DAY_CLOSING_EN,
    ),
    dict(
        filename="open-trip.html",
        file_label="Open-Trip",
        page_title="Open Trip Komodo Island — Terms & Conditions | Komodo & Ko",
        trip_name="Open Trip Komodo Island",
        content=OPEN_TRIP_CONTENT,
        closing_id=OPEN_TRIP_CLOSING_ID,
        closing_en=OPEN_TRIP_CLOSING_EN,
    ),
    dict(
        filename="private-trip.html",
        file_label="Private-Trip",
        page_title="Private Trip Komodo Island — Terms & Conditions | Komodo & Ko",
        trip_name="Private Trip Komodo Island",
        content=PRIVATE_TRIP_CONTENT,
        closing_id=PRIVATE_TRIP_CLOSING_ID,
        closing_en=PRIVATE_TRIP_CLOSING_EN,
    ),
]

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Komodo & Ko — Terms & Conditions Signing</title>
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="hero">
  <img src="assets/logo.jpg" alt="Komodo & Ko logo" class="logo">
  <div class="brand">Komodo &amp; Ko</div>
  <h1>Terms &amp; Conditions</h1>
  <h2>Choose your trip type to review and sign</h2>
</div>
<div class="wrap">
  <div class="hub-grid" style="margin-top:4px;">
    <a class="hub-card" href="full-day-trip">
      <h3>Full Day Trip Komodo Island</h3>
      <p>Single-day trip terms, reservation form, and guest signature.</p>
    </a>
    <a class="hub-card" href="open-trip">
      <h3>Open Trip Komodo Island</h3>
      <p>Multi-day shared/open trip terms, reservation form, and guest signature.</p>
    </a>
    <a class="hub-card" href="private-trip">
      <h3>Private Trip Komodo Island</h3>
      <p>Multi-day private charter terms, reservation form, and guest signature.</p>
    </a>
  </div>
  <footer class="site-footer">Komodo &amp; Ko</footer>
</div>
</body>
</html>
"""


def main():
    for page in PAGES:
        html = PAGE_TEMPLATE.format(**page)
        with open(page["filename"], "w", encoding="utf-8") as f:
            f.write(html)
        print("Wrote", page["filename"])

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(INDEX_TEMPLATE)
    print("Wrote index.html")


if __name__ == "__main__":
    main()
