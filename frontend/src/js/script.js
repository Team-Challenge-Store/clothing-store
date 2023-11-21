// Для зміни вигляду товарів при відкриванні/закриванні фільтрації

const filterDetails = document.getElementById("filter-details");
const goodsList = document.getElementById("goods-list");

filterDetails.addEventListener("toggle", function () {
   if (filterDetails.open) {
      goodsList.classList.remove("filter-closed");
   } else {
      goodsList.classList.add("filter-closed");
   }
});


// Реалізація інпута з ціною
const range = document.getElementById("input-left");
const range2 = document.getElementById("input-right");

range.addEventListener("input", function () {
   const value = this.value;
   const min = this.min;
   const max = this.max;
   const percent = ((value - min) / (max - min)) * 100;
   const percent2 =
      ((range2.value - range2.min) / (range2.max - range2.min)) * 100;
   document.querySelector(".range").style.left = percent + "%";
   document.querySelector(".thumb.left").style.left = percent + "%";
   document.querySelector(".price__value-min").innerText = this.value;
});

range2.addEventListener("input", function () {
   const value = this.value;
   const min = this.min;
   const max = this.max;
   const percent = ((value - min) / (max - min)) * 100;
   const percent2 = ((range.value - range.min) / (range.max - range.min)) * 100;
   document.querySelector(".range").style.right = 100 - percent + "%";
   document.querySelector(".thumb.right").style.right = 100 - percent + "%";
   document.querySelector(".price__value-max").innerText = this.value;
});
