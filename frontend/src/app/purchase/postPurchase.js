export default async function fetchPurchase(purchaseList, employeeCode = "", storeCode = 30, posNumber = 90) {
  const transaction = {
    employee_code: employeeCode,
    store_code: storeCode,
    pos_number: posNumber,
  };

  const values = {
    transaction: transaction,
    transactiondetails: purchaseList,
  };

  const body_msg = JSON.stringify(values);
  console.log(body_msg);

  const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + `/transaction`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body_msg,
  });

  // レスポンスのステータスを確認
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to fetch purchase: ${errorDetail}`);
  }

  return res.json();
}
