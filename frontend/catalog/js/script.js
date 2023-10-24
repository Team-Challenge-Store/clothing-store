const filterDetails = document.getElementById("filter-details");
const goodsList = document.getElementById("goods-list");

filterDetails.addEventListener("toggle", function () {
   if (filterDetails.open) {
      goodsList.classList.add('test');
      goodsList.classList.remove('filter-closed')
   } else {
      goodsList.classList.remove('test')
      goodsList.classList.add('filter-closed')
   }
});
