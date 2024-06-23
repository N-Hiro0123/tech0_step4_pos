"use client";
import { useParams, useRouter } from "next/navigation";
import fetchProduct from "./getProduct";
import addProduct from "./addProduct";
import fetchPurchase from "./postPurchase";

import { use, useEffect, useState } from "react";

export default function Purchase() {
  const [inputValue, setInputValue] = useState("");
  const [productInfo, setProductInfo] = useState([]);
  const [displayName, setDisyplayName] = useState("");
  const [displayPrice, setDisyplayPrice] = useState("");
  const [purchaseList, setPurchaseList] = useState([]);
  const [totalValue, setTortalValue] = useState("");

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
      if (datas === null) {
        setProductInfo([]); // 初期化
        setDisyplayName("商品がマスタ未登録です");
      } else {
        setProductInfo(datas);
        setDisyplayName(datas.product_name);
        setDisyplayPrice(datas.product_price);
      }
    }
  };

  //  ボタンを押した時に製品をリストへ追加するともに、各ボックスを初期化
  const handleAddProduct = async (event) => {
    if (productInfo.length !== 0) {
      event.preventDefault();
      console.log(purchaseList);
      addProduct(purchaseList, productInfo);
      console.log(purchaseList);

      setInputValue("");
      setDisyplayName("");
      setDisyplayPrice("");
      setProductInfo([]);
    }
    console.log(purchaseList);
  };

  //  ボタンを押した時にリストの内容を購入する
  const handlePurchase = async (event) => {
    if (purchaseList.length !== 0) {
      event.preventDefault();
      const res = await fetchPurchase(purchaseList, "0123456789");
      setTortalValue(res.total_amount);
    }
  };

  useEffect(() => {
    if (totalValue === "") return;
    alert("合計金額は" + totalValue);
  }, [totalValue]);

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Input:
          <input type="text" value={inputValue} onChange={handleInputChange} />
        </label>
        <button type="submit">★★★商品コード読み込み★★★</button>
      </form>
      <h1>ProductInfo</h1>

      <p>Product Code: {productInfo?.product_code}</p>
      <p>Product ID: {productInfo?.product_id}</p>
      <p>Product Name: {productInfo?.product_name}</p>
      <p>Product Price: {productInfo?.product_price}</p>
      <h1>■■仕様１■■</h1>

      <p>表示する商品名:{displayName}</p>
      <p>商品の値段 {displayPrice}</p>

      <h1>■■仕様２■■</h1>
      <button type="button" onClick={handleAddProduct}>
        ★★★商品の追加★★★
      </button>
      <div>
        {purchaseList?.map((product) => (
          <div key={product?.product_id}>
            <p>Product Code: {product?.product_code}</p>
            <p>Product ID: {product?.product_id}</p>
            <p>Product Name: {product?.product_name}</p>
            <p>Product Price: {product?.product_price}</p>
            <p>Product Count: {product?.product_count}</p>
          </div>
        ))}
      </div>
      <h1>■■仕様３■■</h1>
      <button type="button" onClick={handlePurchase}>
        ★★★商品の購入★★★
      </button>
    </div>
  );
}
