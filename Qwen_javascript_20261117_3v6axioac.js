/* ==========================================================
   app.js — мост между страницей и Python.
   Логику считает Python (slovarik.py), JS только рисует.
   ========================================================== */

let pyodide = null;            // среда Python в браузере
let gotovo = false;            // готов ли Python к работе
let tekushieStroki = [];       // строки таблицы, которые сейчас на экране
const KLJUCH = "slovarik";     // ключ в памяти браузера

let test = { voprosy: [], nomer: 0, pravilno: 0, oshibki: [], rezhim: "de-ru", otvechen: false };

/* ---------- 1. ЗАПУСК PYTHON ---------- */
async function zapustitPython() {
  try {
    document.getElementById("zagruzka-text").textContent = "Скачиваю интерпретатор Python…";
    // await — дождаться загрузки; loadPyodide даёт функция из pyodide.js
    pyodide = await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v314.0.8/full/" });

    document.getElementById("zagruzka-text").textContent = "Загружаю slovarik.py…";
    const otvet = await fetch("slovarik.py");   // скачиваем Python-файл
    const kod = await otvet.text();
    pyodide.FS.writeFile("slovarik.py", kod);   // кладём файл в память браузера
    pyodide.runPython("import slovarik");       // Python импортирует его как модуль

    const versiya = pyodide.runPython("import sys\nsys.version.split()[0]");
    document.getElementById("python-versiya").textContent =
      "Работает настоящий Python " + versiya + " в браузере (Pyodide)";

    const dannye = localStorage.getItem(KLJUCH) || "";
    pyVyzov("api_start", [dannye]);             // заполняем словарь
    gotovo = true;
    document.getElementById("zagruzka").classList.add("skryto");
    obnovitVse();
  } catch (oshibka) {
    document.getElementById("zagruzka-text").textContent =
      "Не удалось загрузить Python. Проверь интернет и обнови страницу. " + oshibka;
  }
}

/* ---------- 2. ВЫЗОВ ФУНКЦИИ PYTHON ---------- */
function pyVyzov(imya, parametry) {
  let argumenty = "";
  for (let i = 0; i < parametry.length; i++) {
    pyodide.globals.set("p" + i, parametry[i]);  // передаём значение в переменную Python
    if (i > 0) argumenty = argumenty + ", ";
    argumenty = argumenty + "p" + i;
  }
  // выполняем одну строчку Python, например: slovarik.api_slova(p0, p1)
  const tekst = pyodide.runPython("slovarik." + imya + "(" + argumenty + ")");
  return JSON.parse(tekst);   // Python вернул текст JSON → превращаем в массив
}

function sohranitVBrauzer() {
  const dannye = pyVyzov("api_sohranit", []);
  localStorage.setItem(KLJUCH, JSON.stringify(dannye));
  document.getElementById("dannye-info").textContent =
    "Сейчас в словаре " + dannye.length + " записей. Данные сохраняются автоматически.";
}

/* ---------- 3. МЕЛКИЕ ПОМОЩНИКИ ---------- */
function esc(tekst) {
  // чтобы символы < > & не ломали таблицу
  return tekst.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

let taymerToast = null;
function toast(tekst) {
  const el = document.getElementById("toast");
  el.textContent = tekst;
  el.className = "show";
  clearTimeout(taymerToast);
  taymerToast = setTimeout(function () { el.className = ""; }, 2500);
}

function obnovitVse() {
  zapolnitTemy();
  pokazatSlovar();
  const s = pyVyzov("api_slovo_dnya", []);
  document.getElementById("slovo-dnya").innerHTML = "Слово дня: <b>" + esc(s[0]) + "</b> — " + esc(s[1]);
  sohranitVBrauzer();
}

function zapolnitTemy() {
  const temy = pyVyzov("api_temy", []);        // список тем считает Python
  const polya = ["filtr-temy", "test-temy", "nov-temy"];
  for (let p = 0; p < polya.length; p++) {
    const pole = document.getElementById(polya[p]);
    const bylo = pole.value;
    let html = "";
    if (polya[p] !== "nov-temy") html += "<option value=''>Все темы</option>";
    for (let i = 0; i < temy.length; i++) html += "<option value='" + temy[i] + "'>" + temy[i] + "</option>";
    if (polya[p] === "nov-temy") html += "<option value='Мои слова'>Мои слова</option>";
    pole.innerHTML = html;
    pole.value = bylo;                         // возвращаем прежний выбор
  }
}

function otkrytVkladku(id) {
  const stranicy = document.querySelectorAll(".page");
  for (let i = 0; i < stranicy.length; i++) stranicy[i].classList.remove("active");
  const knopki = document.querySelectorAll(".tab");
  for (let i = 0; i < knopki.length; i++) {
    knopki[i].classList.remove("active");
    if (knopki[i].dataset.tab === id) knopki[i].classList.add("active");
  }
  document.getElementById(id).classList.add("active");
  if (id === "slovar") pokazatSlovar();
  if (id === "stat") pokazatStat();
}

/* ---------- 4. СЛОВАРЬ И РЕДАКТОР ---------- */
function pokazatSlovar() {
  if (!gotovo) return;
  const tema = document.getElementById("filtr-temy").value;
  const poisk = document.getElementById("poisk").value;
  const dannye = pyVyzov("api_slova", [tema, poisk]);  // [найдено, всего, строки]
  tekushieStroki = dannye[2];
  let html = "";
  for (let i = 0; i < tekushieStroki.length; i++) {
    const s = tekushieStroki[i];               // [номер, слово, перевод, тема]
    html += "<tr><td>" + (i + 1) + "</td><td class='de'>" + esc(s[1]) + "</td><td>" + esc(s[2]) + "</td>" +
            "<td><span class='badge'>" + esc(s[3]) + "</span></td>" +
            "<td><button class='mini' onclick='izmenit(" + s[0] + ")'>✏️</button> " +
            "<button class='mini' onclick='udalit(" + s[0] + ")'>🗑️</button></td></tr>";
  }
  document.getElementById("telo-tablicy").innerHTML = html;
  document.getElementById("schetchik").textContent = "Найдено записей: " + dannye[0] + " из " + dannye[1];
}

function najtiVTekushih(nomer) {
  for (let i = 0; i < tekushieStroki.length; i++) {
    if (tekushieStroki[i][0] === nomer) return tekushieStroki[i];
  }
  return [nomer, "", "", ""];
}

function izmenit(nomer) {
  const s = najtiVTekushih(nomer);
  const slovo = prompt("Немецкое слово:", s[1]);   // prompt — окно ввода в браузере
  if (slovo === null) return;                      // null = нажали «Отмена»
  const perevod = prompt("Перевод:", s[2]);
  if (perevod === null) return;
  const rez = pyVyzov("api_izmenit", [nomer, slovo, perevod]);
  toast(rez[1]);
  if (rez[0] === 1) obnovitVse();
}

function udalit(nomer) {
  const s = najtiVTekushih(nomer);
  if (confirm("Удалить «" + s[1] + " — " + s[2] + "»?")) {
    const rez = pyVyzov("api_udalit", [nomer]);
    toast(rez[1]);
    obnovitVse();
  }
}

function dobavitSlovo() {
  const slovo = document.getElementById("nov-slovo").value;
  const perevod = document.getElementById("nov-perevod").value;
  let tema = document.getElementById("nov-temy").value;
  const svoya = document.getElementById("nov-svoya").value.trim();
  if (svoya !== "") tema = svoya;
  const rez = pyVyzov("api_dobavit", [slovo, perevod, tema]);   // проверяет Python
  toast(rez[1]);
  if (rez[0] === 1) {
    document.getElementById("nov-slovo").value = "";
    document.getElementById("nov-perevod").value = "";
    document.getElementById("nov-svoya").value = "";
    obnovitVse();
  }
}

/* ---------- 5. ТЕСТЫ ---------- */
function nachatTest() {
  const rezhim = document.getElementById("test-rezhim").value;
  const tema = document.getElementById("test-temy").value;
  let kol = parseInt(document.getElementById("test-kol").value, 10);
  if (isNaN(kol) || kol < 1) kol = 10;
  const dannye = pyVyzov("api_voprosy", [rezhim, tema, kol]);   // вопросы готовит Python
  if (dannye[0] === 0) { toast("Нет слов для теста"); return; }
  test.voprosy = dannye[1];
  test.nomer = 0; test.pravilno = 0; test.oshibki = []; test.rezhim = rezhim;
  document.getElementById("test-nastrojki").classList.add("skryto");
  document.getElementById("test-itog").classList.add("skryto");
  document.getElementById("test-ekran").classList.remove("skryto");
  pokazatVopros();
}

function pokazatVopros() {
  const s = test.voprosy[test.nomer];      // [вопрос, эталон, подсказка]
  test.otvechen = false;
  document.getElementById("test-progress").textContent =
    "Вопрос " + (test.nomer + 1) + " из " + test.voprosy.length + " · верных ответов: " + test.pravilno;
  document.getElementById("test-polosa").style.width = (test.nomer / test.voprosy.length * 100) + "%";
  const status = document.getElementById("test-otvet-status");
  status.textContent = ""; status.className = "status";
  document.getElementById("knopka-dalshe").classList.add("skryto");

  let zagolovok = "Переведи на русский: ";
  if (test.rezhim === "ru-de") zagolovok = "Переведи на немецкий: ";
  if (test.rezhim === "artikli") zagolovok = "Подставь артикль: ___ ";
  document.getElementById("test-vopros").innerHTML =
    zagolovok + "<b>" + esc(s[0]) + "</b> <span class='podskazka'>(" + esc(s[2]) + ")</span>";

  if (test.rezhim === "artikli") {
    document.getElementById("blok-vvod").classList.add("skryto");
    document.getElementById("blok-artikli").classList.remove("skryto");
  } else {
    document.getElementById("blok-vvod").classList.remove("skryto");
    document.getElementById("blok-artikli").classList.add("skryto");
    const pole = document.getElementById("test-otvet");
    pole.value = ""; pole.disabled = false; pole.focus();
  }
}

function otvetit(otvet) {
  if (test.otvechen) return;               // повторно на тот же вопрос ответить нельзя
  test.otvechen = true;
  const s = test.voprosy[test.nomer];
  const rez = pyVyzov("api_proverit", [otvet, s[1]]);   // ответ проверяет Python
  const status = document.getElementById("test-otvet-status");
  if (rez[0] === 1) {
    test.pravilno = test.pravilno + 1;
    status.textContent = "✅ Верно!";
    status.className = "status ok";
  } else {
    status.textContent = "❌ Ошибка. Правильный ответ: " + rez[1];
    status.className = "status err";
    test.oshibki.push([s[0], rez[1], otvet]);
  }
  document.getElementById("test-otvet").disabled = true;
  document.getElementById("knopka-dalshe").classList.remove("skryto");
}

function dalshe() {
  test.nomer = test.nomer + 1;
  if (test.nomer >= test.voprosy.length) konecTesta();
  else pokazatVopros();
}

function konecTesta() {
  document.getElementById("test-ekran").classList.add("skryto");
  const rez = pyVyzov("api_itog", [test.pravilno, test.voprosy.length]);  // [процент, оценка]
  let html = "<h3>Результат: " + test.pravilno + " из " + test.voprosy.length + " (" + rez[0] + "%)</h3>";
  html += "<p>Оценка: <b>" + rez[1] + "</b></p>";
  html += "<div class='polosa'><div style='width:" + rez[0] + "%'></div></div>";
  if (test.oshibki.length > 0) {
    html += "<h4>Работа над ошибками — повтори эти слова:</h4><ul>";
    for (let i = 0; i < test.oshibki.length; i++) {
      const o = test.oshibki[i];
      html += "<li>" + esc(o[0]) + " → <b>" + esc(o[1]) + "</b> <span class='podskazka'>(твой ответ: " + esc(o[2]) + ")</span></li>";
    }
    html += "</ul>";
  } else {
    html += "<p>🎉 Ни одной ошибки! Sehr gut!</p>";
  }
  html += "<button class='btn' onclick='snovaTest()'>Пройти ещё раз</button>";
  const itog = document.getElementById("test-itog");
  itog.innerHTML = html;
  itog.classList.remove("skryto");
}

function snovaTest() {
  document.getElementById("test-itog").classList.add("skryto");
  document.getElementById("test-nastrojki").classList.remove("skryto");
}

/* ---------- 6. СТАТИСТИКА ---------- */
function pokazatStat() {
  if (!gotovo) return;
  const d = pyVyzov("api_statistika", []);   // все числа посчитал Python
  const k = d[0];
  const podpisi = ["Всего записей", "Уникальных слов", "Тем", "Слов в двух темах",
                   "С артиклем", "Без артикля", "Средняя длина", "Самое длинное"];
  let html = "";
  for (let i = 0; i < podpisi.length; i++) {
    html += "<div class='stat-card'><div class='znachenie'>" + k[i] + "</div><div class='podpis'>" + podpisi[i] + "</div></div>";
  }
  document.getElementById("stat-bloki").innerHTML = html;

  let maksimum = 0;
  for (let i = 0; i < d[1].length; i++) if (d[1][i][1] > maksimum) maksimum = d[1][i][1];
  let html2 = "";
  for (let i = 0; i < d[1].length; i++) {
    const proc = Math.round(d[1][i][1] / maksimum * 100);
    html2 += "<div class='bar-row'><span class='bar-name'>" + d[1][i][0] + "</span>" +
             "<div class='bar'><div style='width:" + proc + "%'></div></div><b>" + d[1][i][1] + "</b></div>";
  }
  document.getElementById("stat-temy").innerHTML = html2;
  document.getElementById("stat-dubli").textContent = d[2] !== "" ? "Слова, которые есть в двух темах: " + d[2] : "";
}

/* ---------- 7. ФАЙЛЫ ---------- */
function skachat(imya, tekst, tip) {
  const blob = new Blob([tekst], { type: tip });   // файл в памяти браузера
  const ssylka = document.createElement("a");
  ssylka.href = URL.createObjectURL(blob);
  ssylka.download = imya;
  ssylka.click();
  URL.revokeObjectURL(ssylka.href);
}

function exportCSV() {
  const tekst = pyVyzov("api_csv", [])[0];         // таблицу собрал Python
  skachat("slovarik.csv", "\uFEFF" + tekst, "text/csv;charset=utf-8");  // BOM для Excel
  toast("CSV сохранён — открой его в Excel");
}

function exportTXT() {
  const tekst = pyVyzov("api_txt", [])[0];
  skachat("slovarik.txt", tekst, "text/plain;charset=utf-8");
  toast("TXT сохранён — его читает консольная версия");
}

function importTXT(sobytie) {
  const fayl = sobytie.target.files[0];
  if (!fayl) return;
  const chitatel = new FileReader();               // читает файл с компьютера
  chitatel.onload = function (e) {
    const rez = pyVyzov("api_import", [e.target.result]);   // разбирает Python
    toast(rez[2]);
    if (rez[0] === 1) obnovitVse();
  };
  chitatel.readAsText(fayl, "UTF-8");
}

function sbros() {
  if (confirm("Вернуть базовый словарь? Твои добавленные слова удалятся.")) {
    pyVyzov("api_sbros", []);
    obnovitVse();
    toast("Словарь сброшен к базовому");
  }
}

/* ---------- 8. ПРИВЯЗКА КНОПОК И СТАРТ ---------- */
document.getElementById("filtr-temy").addEventListener("change", pokazatSlovar);
document.getElementById("poisk").addEventListener("input", pokazatSlovar);
document.getElementById("knopka-start").addEventListener("click", nachatTest);
document.getElementById("knopka-otvet").addEventListener("click", function () { otvetit(document.getElementById("test-otvet").value); });
document.getElementById("knopka-dalshe").addEventListener("click", dalshe);
document.getElementById("knopka-dobavit").addEventListener("click", dobavitSlovo);
document.getElementById("knopka-csv").addEventListener("click", exportCSV);
document.getElementById("knopka-txt").addEventListener("click", exportTXT);
document.getElementById("fayl-txt").addEventListener("change", importTXT);
document.getElementById("knopka-sbros").addEventListener("click", sbros);

const vkladki = document.querySelectorAll(".tab");
for (let i = 0; i < vkladki.length; i++) {
  vkladki[i].addEventListener("click", function () { otkrytVkladku(this.dataset.tab); });
}

// Enter в поле ответа: сначала ответить, потом перейти дальше
document.getElementById("test-otvet").addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    if (test.otvechen) dalshe();
    else otvetit(this.value);
  }
});

zapustitPython();   // включаем Python