export default async function fetchPurchase(purchaseList, employeeCode = "", storeCode = 30, posNumber = 90) {
  const transaction = {
    employee_code: employeeCode,
    store_code: storeCode,
    pos_number: posNumber,
  };

  // // purchaseListをtransactiondetailsに変換　内容は同じだと思うが念のため
  // const transactiondetails = purchaseList.map((product) => ({
  //   product_id: product.product_id,
  //   product_code: product.product_code,
  //   product_name: product.product_name,
  //   product_price: product.product_price,
  //   product_quantity: product.product_quantity,
  // }));

  const body_msg = {
    transaction: transaction,
    transactiondetails: purchaseList,
  };

  //   const body_msg = JSON.stringify(values);
  console.log(body_msg);

  const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + `/transaction`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body_msg,
  });

  // レスポンスのステータスを確認
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to fetch roadmap: ${errorDetail}`);
  }

  return res.json();
}
