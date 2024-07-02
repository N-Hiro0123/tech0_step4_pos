export default async function fetchUserInfo(jwt) {
  const res = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + `/user-info`, {
    cache: "no-cache",
    method: "GET",
    headers: { Authorization: `Bearer ${jwt}` },
  });
  if (!res.ok) {
    return false;
  }
  return res.json();
}
