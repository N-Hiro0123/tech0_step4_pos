export default async function addProduct(jsonList, newProduct) {
  // product_count を追加
  newProduct.product_count = 1;

  // 既存リストに同じ product_id があるか確認
  let existingProduct = jsonList.find((product) => product.product_id === newProduct.product_id);

  if (existingProduct) {
    // 同じ product_id が存在する場合、個数を増やす
    existingProduct.product_count += 1;
  } else {
    // 存在しない場合、新しい商品をリストに追加
    jsonList.push(newProduct);
  }
  return;
}
