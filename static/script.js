async function loadDevices() {
  // Get the CSV file
  const csvFile = await fetch("static/devices.csv");
  //const csvFile = await fetch("static/new_dev.csv");
  const csvData = await csvFile.text();

  // Split the CSV data into rows
  const rows = csvData.split("\n");

  // Process each row
  for (const row of rows) {
    // Split the row into columns
    const columns = row.split(";");

    // Create a tab
    const tab = document.createElement("li");
    tab.className = "main_info-device";
    tab.innerHTML = `<a onclick="db_device('${columns[2]}')" href="#${columns[2]}">${columns[0]}</a>`;

    // Create the tab content
    const content = document.createElement("div");
    content.id = columns[2];
    content.className = "info-device";
    let parametersList = ''
    if (columns[3]) {
      const parameters = columns[3].split(", "); // Розділити параметри по комах та пробіла
      parametersList = parameters.map(param => `<p>${param}</p>`).join("");
    }
    
    content.innerHTML = `
      <h2>Тип пристрою: ${columns[0]}</h2>
      <p>Назва пристрою: ${columns[1]}</p>
      <p>Локація: ${columns[2]}</p>
      ${parametersList}
    `;

    // Add the tab and tab content to the DOM
    document.getElementById("tabs").appendChild(tab);
    document.body.appendChild(content);
  }
  for (const row of rows) {
    const columns = row.split(";");
    const tab = document.createElement("li");
    tab.className = "remote_device-row";
    tab.innerHTML = `<input type="radio" name="renote_device" id="remote_${columns[2]}" value="${columns[2]}"><label for="${columns[0]} ${columns[2]}">${columns[0]} ${columns[2]}</label>`;
    document.getElementById("remote_device-ul").appendChild(tab);
  }
}

function sendDeviceToServer(func, textToSend) {
    // Відправлення GET-запиту на сервер
    fetch(`http://localhost:8080/${func}?text=${encodeURIComponent(textToSend)}`)
        .then(response => response.text())
        .then(data => console.log(data))
        .catch(error => console.error('Помилка:', error));
}



function db_device(id_device) {
  const infoBlocks = document.getElementsByClassName('info-device');
  for (let i = 0; i < infoBlocks.length; i++) {
  infoBlocks[i].style.display = 'none';
  }
  document.getElementById(id_device).style.display = 'block';
}

function addDevice() {
  // Отримати значення поля вибору пристрою
  var device = document.querySelector('input[name="device"]:checked').value;

  // Отримати значення поля вводу тексту
  var ip = document.querySelector('input[name="input"]').value;

  // Перевірити, чи вибрано пристрій
  if (!device) {
    alert('Необхідно вибрати пристрій');
    return;
  }

  // Перевірити, чи введено IP-адресу
  if (!ip) {
    alert('Необхідно ввести IP-адресу');
    return;
  }

  // Вивести повідомлення
  alert(`Додано пристрій ${device} з IP-адресою ${ip}`);

  sendDeviceToServer('add',`${device};${device};${ip};`)

  // Запобігти переходу на іншу сторінку
  event.preventDefault();
  reload_url();
}

function remoteDevice() {
  // Отримати значення вибраної радіокнопки
  var device = document.querySelector('input[name="renote_device"]:checked').value;

  // Якщо радіокнопка не обрана
  if (!device) {
    // Вивести сповіщення
    alert('Не обраний пристрій для видалення');
  }
  // Вивести сповіщення із value даної радіокнопки
  alert('Видалено обраний девайс');
  sendDeviceToServer('remote', device)
  
  event.preventDefault();
  reload_url();
}


function reload_url() {
    setTimeout(function() {
        location.reload();
    }, 3000); // 3000 мілісекунд = 3 секунди
}

document.querySelector(".dropdown-toggle").addEventListener("click", () => {
  document.querySelector(".dropdown-menu").classList.toggle("show");
});

function showQRCode() {
    document.getElementById('qr-modal').style.display = 'block';
  }

function hideQRCode() {
  document.getElementById('qr-modal').style.display = 'none';
}


document.addEventListener("DOMContentLoaded", () => {
  loadDevices();
  sendDeviceToServer('load','load');
});


