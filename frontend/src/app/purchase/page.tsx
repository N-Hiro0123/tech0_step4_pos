"use client";
import { useParams, useRouter } from "next/navigation";
import fetchProduct from "./getProduct";

import { useEffect, useState } from "react";

export default function Purchase() {
  // const router = useRouter();
  // const params = useParams();
  // console.log(params.user_id, params.parent_id, params.item_name);
  // const [input_code, setInputCode] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [productInfo, setProductInfo] = useState([]);

  // 入力ボックスの内容を常に取得
  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  //  ボタンを押した時に製品情報を取得
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (inputValue.trim() === "") {
      alert(`商品コードを入力してください`);
    } else if (inputValue.trim().length !== 13) {
      alert(`商品コードは13文字である必要があります`);
    } else {
      const datas = await fetchProduct(inputValue);
      setProductInfo(datas);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Input:
          <input type="text" value={inputValue} onChange={handleInputChange} />
        </label>
        <button type="submit">Submit</button>
      </form>
      <h1>ProductInfo</h1>
      {/* prettier-ignore */}
      <>
        <p><strong>Product Code:</strong> {productInfo.product_code}</p>
        <p><strong>Product ID:</strong> {productInfo.product_id}</p>
        <p><strong>Product Name:</strong> {productInfo.product_name}</p>
        <p><strong>Product Price:</strong> {productInfo.product_price}</p>
      </>
    </div>
  );
}
