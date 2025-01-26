const items = {
  1: { name: "Coke", price: 1.0, image: "https://picsum.photos/400/300" },
  2: { name: "Pepsi", price: 2.0, image: "https://picsum.photos/400/300" },
  3: { name: "Sprite", price: 3.0, image: "https://picsum.photos/400/300" },
  4: { name: "Fanta", price: 4.0, image: "https://picsum.photos/400/300" },
  5: { name: "Water", price: 5.0, image: "https://picsum.photos/400/300" },
  6: { name: "Gatorade", price: 6.0, image: "https://picsum.photos/400/300" },
  7: {
    name: "Mountain Dew",
    price: 7.0,
    image: "https://picsum.photos/400/300",
  },
  8: { name: "Root Beer", price: 8.0, image: "https://picsum.photos/400/300" },
  9: { name: "Lemonade", price: 9.0, image: "https://picsum.photos/400/300" },
  10: { name: "Coffee", price: 10.0, image: "https://picsum.photos/400/300" },
  11: { name: "Tea", price: 11.0, image: "https://picsum.photos/400/300" },
  12: { name: "Juice", price: 12.0, image: "https://picsum.photos/400/300" },
  13: { name: "Milk", price: 13.0, image: "https://picsum.photos/400/300" },
  14: { name: "Soda", price: 14.0, image: "https://picsum.photos/400/300" },
  15: { name: "Beer", price: 15.0, image: "https://picsum.photos/400/300" },
  16: { name: "Wine", price: 16.0, image: "https://picsum.photos/400/300" },
  17: { name: "Whiskey", price: 17.0, image: "https://picsum.photos/400/300" },
  18: { name: "Vodka", price: 18.0, image: "https://picsum.photos/400/300" },
  19: { name: "Rum", price: 19.0, image: "https://picsum.photos/400/300" },
  20: { name: "Tequila", price: 20.0, image: "https://picsum.photos/400/300" },
};
// // 初期化
const display = document.getElementById("display");
const description = document.getElementById("description");
const name_value = document.getElementById("name-value");
const price_value = document.getElementById("price-value");

let slideShow = document.createElement("div");
let main = document.createElement("div");
let extra = document.createElement("div");

slideShow.classList.add("col-12", "d-flex", "flex-nowrap", "overflow-hidden");
main.classList.add("main", "full-width");
extra.classList.add("extra", "full-width");

slideShow.appendChild(main);
slideShow.appendChild(extra);

// displayにslideShowを追加
display.appendChild(slideShow);

// 初期画像とデータの表示
const initialElement = document.createElement("img");
initialElement.src = items[1].image;
initialElement.classList.add("main-image");
main.appendChild(initialElement);

// 初期の商品情報を表示
name_value.textContent = items[1].name;
price_value.textContent = `$${items[1].price.toFixed(2)}`;

// // ボタンの追加
const button_field = document.getElementById("button-field");
for (let i = 0; i < Object.keys(items).length; i++) {
  let button = document.createElement("button");
  button.innerHTML = i + 1;
  button.classList.add("btn", "btn-outline-dark", "m-1");
  button.style.width = "60px"; // ボタンの幅を設定
  button_field.appendChild(button);
}

function slideJump(nextIndex) {
  const currentIndex = parseInt(display.getAttribute("data-index"));
  const currentElement = document.createElement("img");
  const nextElement = document.createElement("img");

  currentElement.classList.add("extra-image");
  nextElement.classList.add("main-image");

  currentElement.src = items[currentIndex].image;
  nextElement.src = items[nextIndex].image;

  display.setAttribute("data-index", nextIndex.toString());
  const direction = nextIndex > currentIndex ? "right" : "left";
  animateMain(currentElement, nextElement, direction);
}

function animateMain(currentElement, nextElement, animationType) {
  main.innerHTML = "";
  extra.innerHTML = "";
  main.appendChild(nextElement);
  extra.appendChild(currentElement);

  main.classList.add("expand-animation");
  extra.classList.add("deplete-animation");

  if (animationType === "right") {
    slideShow.innerHTML = "";
    slideShow.append(extra);
    slideShow.append(main);
  } else if (animationType === "left") {
    slideShow.innerHTML = "";
    slideShow.append(main);
    slideShow.append(extra);
  }
}

buttons = document.querySelectorAll(".btn");
buttons.forEach((button) => {
  button.addEventListener("click", (event) => {
    const index = parseInt(event.target.innerHTML);
    slideJump(index);
    // 商品情報を更新
    name_value.textContent = items[index].name;
    price_value.textContent = `$${items[index].price.toFixed(2)}`;
  });
});
