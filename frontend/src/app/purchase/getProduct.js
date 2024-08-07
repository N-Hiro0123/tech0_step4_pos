export default async function fetchProduct(product_id, jwt) {
  const res = await fetch(
    process.env.NEXT_PUBLIC_API_ENDPOINT + `/product?product_code=${product_id}`,
    {
      cache: "no-cache",
      headers: { Authorization: `Bearer ${jwt}` },
    }
  );
  if (!res.ok) {
    throw new Error("Failed to fetch roadmap");
  }
  return res.json();
}
