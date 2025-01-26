const battery = [
  {
    batteryName: "WKL-78",
    capacityAh: 2.3,
    voltage: 14.4,
    maxDraw: 3.2,
    endVoltage: 10,
  },
  {
    batteryName: "WKL-140",
    capacityAh: 4.5,
    voltage: 14.4,
    maxDraw: 9.2,
    endVoltage: 5,
  },
  {
    batteryName: "Wmacro-78",
    capacityAh: 2.5,
    voltage: 14.5,
    maxDraw: 10,
    endVoltage: 5,
  },
  {
    batteryName: "Wmacro-140",
    capacityAh: 3.6,
    voltage: 14.4,
    maxDraw: 14,
    endVoltage: 5,
  },
  {
    batteryName: "IOP-E78",
    capacityAh: 6.6,
    voltage: 14.4,
    maxDraw: 10.5,
    endVoltage: 8,
  },
  {
    batteryName: "IOP-E140",
    capacityAh: 9.9,
    voltage: 14.4,
    maxDraw: 14,
    endVoltage: 10,
  },
  {
    batteryName: "IOP-E188",
    capacityAh: 13.2,
    voltage: 14.4,
    maxDraw: 14,
    endVoltage: 11,
  },
  {
    batteryName: "RYN-C65",
    capacityAh: 4.9,
    voltage: 14.8,
    maxDraw: 4.9,
    endVoltage: 11,
  },
  {
    batteryName: "RYN-C85",
    capacityAh: 6.3,
    voltage: 14.4,
    maxDraw: 6.3,
    endVoltage: 12,
  },
  {
    batteryName: "RYN-C140",
    capacityAh: 9.8,
    voltage: 14.8,
    maxDraw: 10,
    endVoltage: 12,
  },
  {
    batteryName: "RYN-C290",
    capacityAh: 19.8,
    voltage: 14.4,
    maxDraw: 14,
    endVoltage: 12,
  },
];
const camera = [
  {
    brand: "Cakon",
    model: "ABC 3000M",
    powerConsumptionWh: 35.5,
  },
  {
    brand: "Cakon",
    model: "ABC 5000M",
    powerConsumptionWh: 37.2,
  },
  {
    brand: "Cakon",
    model: "ABC 7000M",
    powerConsumptionWh: 39.7,
  },
  {
    brand: "Cakon",
    model: "ABC 9000M",
    powerConsumptionWh: 10.9,
  },
  {
    brand: "Cakon",
    model: "ABC 9900M",
    powerConsumptionWh: 15.7,
  },
  {
    brand: "Go MN",
    model: "UIK 110C",
    powerConsumptionWh: 62.3,
  },
  {
    brand: "Go MN",
    model: "UIK 210C",
    powerConsumptionWh: 64.3,
  },
  {
    brand: "Go MN",
    model: "UIK 230C",
    powerConsumptionWh: 26.3,
  },
  {
    brand: "Go MN",
    model: "UIK 250C",
    powerConsumptionWh: 15.3,
  },
  {
    brand: "Go MN",
    model: "UIK 270C",
    powerConsumptionWh: 20.3,
  },
  {
    brand: "VANY",
    model: "CEV 1100P",
    powerConsumptionWh: 22,
  },
  {
    brand: "VANY",
    model: "CEV 1300P",
    powerConsumptionWh: 23,
  },
  {
    brand: "VANY",
    model: "CEV 1500P",
    powerConsumptionWh: 24,
  },
  {
    brand: "VANY",
    model: "CEV 1700P",
    powerConsumptionWh: 25,
  },
  {
    brand: "VANY",
    model: "CEV 1900P",
    powerConsumptionWh: 26,
  },
];

const brandSelect = document.querySelector("#brand-select");
const modelSelect = document.querySelector("#model-select");
const powerInput = document.querySelector("#power-input");
const batteryList = document.querySelector("#battery-list");
// 初期表示
document.addEventListener("DOMContentLoaded", () => {
  brandSelect.value = brandSelect.getAttribute("data-default-value");
  const cameraBrand = brandSelect.value;
  const cameraModel = getCameraModelList(cameraBrand);
  updateModelSelect(cameraModel);
  powerInput.value = powerInput.getAttribute("data-default-value");
  updateBatteryList();
});

// ブランド選択時
brandSelect.addEventListener("change", () => {
  const cameraBrand = brandSelect.value;
  const cameraModel = getCameraModelList(cameraBrand);

  updateModelSelect(cameraModel);
  updateBatteryList();
});

// モデル選択時
modelSelect.addEventListener("change", () => {
  updateBatteryList();
});

// 電力入力時
powerInput.addEventListener("change", () => {
  if (validatePowerInput()) {
    updateBatteryList();
  }
});

function validatePowerInput() {
  if (powerInput.value < 0 || powerInput.value > 100) {
    alert("電力は0~100Wの範囲で入力してください");
    return false;
  }
  return true;
}

function getCameraModelList(cameraBrand) {
  const cameraModel = camera.filter((item) => item.brand === cameraBrand);
  return cameraModel;
}

function getCompatibleBatteries(selectedCamera, accessoryPower) {
  const batteryList = battery.filter((item) => {
    const endVoltagePower = calcEndVoltagePower(item);
    const totalPower = selectedCamera.powerConsumptionWh + accessoryPower;
    return endVoltagePower >= totalPower;
  });
  return batteryList;
}

function updateModelSelect(cameraModel) {
  //update modelSelect
  modelSelect.innerHTML = "";
  cameraModel.map((model) => {
    const option = document.createElement("option");
    option.value = model.model;
    option.textContent = model.model;
    modelSelect.appendChild(option);
  });
}

function updateBatteryList() {
  const selectedCamera = camera.find(
    (camera) => camera.model === modelSelect.value
  );
  const accessoryPower = Number(powerInput.value);
  const compatibleBatteries = getCompatibleBatteries(
    selectedCamera,
    accessoryPower
  );

  //update batteryList
  batteryList.innerHTML = "";
  const table = document.createElement("div");
  table.className = "battery-table";

  compatibleBatteries.map((battery) => {
    const row = document.createElement("div");
    row.className = "battery-row";
    const totalPower = selectedCamera.powerConsumptionWh + accessoryPower;
    const batteryRunTime = calcBatteryRunTime(battery, totalPower);
    row.innerHTML = `
    <div class="battery-name">${battery.batteryName}</div>
    <div class="battery-runtime"> runtime: ${batteryRunTime.toFixed(
      1
    )} hours</div>
  `;
    table.appendChild(row);
  });
  batteryList.appendChild(table);
}

function calcBatteryRunTime(battery, power) {
  const batteryRunTime = (battery.capacityAh * battery.voltage) / power;

  return batteryRunTime;
}

function calcEndVoltagePower(battery) {
  const endVoltagePower = battery.endVoltage * battery.maxDraw;
  return endVoltagePower;
}
