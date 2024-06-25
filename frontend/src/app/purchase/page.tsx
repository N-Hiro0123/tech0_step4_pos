"use client";
import { useEffect, useState } from "react";
import fetchProduct from "./getProduct";
import addProduct from "./addProduct";
import fetchPurchase from "./postPurchase";

export default function Purchase() {
  const [inputValue, setInputValue] = useState("");
  const [productInfo, setProductInfo] = useState({});
  const [displayName, setDisplayName] = useState("");
  const [displayPrice, setDisplayPrice] = useState("");
  const [purchaseList, setPurchaseList] = useState([]);
  const [totalValue, setTotalValue] = useState("");
  const [showAlert, setShowAlert] = useState(false);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (inputValue.trim() === "") {
      alert(`商品コードを入力してください`);
    } else if (inputValue.trim().length !== 13) {
      alert(`商品コードは13文字である必要があります`);
    } else {
      const datas = await fetchProduct(inputValue);
      if (datas === null) {
        setProductInfo({});
        setDisplayName("商品がマスタ未登録です");
        setDisplayPrice("");
      } else {
        setProductInfo(datas);
        setDisplayName(datas.product_name);
        setDisplayPrice(datas.product_price);
      }
    }
  };

  const handleAddProduct = (event) => {
    event.preventDefault();
    if (Object.keys(productInfo).length !== 0) {
      setPurchaseList((prevList) => {
        const newList = [...prevList];
        addProduct(newList, productInfo);
        return newList;
      });
      setInputValue("");
      setDisplayName("");
      setDisplayPrice("");
      setProductInfo({});
    }
  };

  const handlePurchase = async (event) => {
    event.preventDefault();
    if (purchaseList.length !== 0) {
      const res = await fetchPurchase(purchaseList, "0123456789");
      setTotalValue(res.total_amount);
    }
  };

  const handleRemoveProduct = (product_code) => {
    setPurchaseList((prevList) => prevList.filter((item) => item.product_code !== product_code));
  };

  const handleIncrement = (product_code) => {
    setPurchaseList((prevList) =>
      prevList.map((item) =>
        item.product_code === product_code
          ? { ...item, product_count: item.product_count + 1 }
          : item
      )
    );
  };

  const handleDecrement = (product_code) => {
    setPurchaseList((prevList) =>
      prevList.map((item) =>
        item.product_code === product_code && item.product_count > 1
          ? { ...item, product_count: item.product_count - 1 }
          : item
      )
    );
  };

  useEffect(() => {
    if (totalValue === "") return;
    alert("合計金額は" + totalValue + "円です");
    setShowAlert(true);
  }, [totalValue]);

  useEffect(() => {
    if (showAlert) {
      window.location.reload();
    }
  }, [showAlert]);

  return (
    <div className="bg-lightblue-100 min-h-screen flex flex-col items-center">
      <div className="container mx-auto p-4 bg-white shadow-md rounded-lg flex-grow">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="form-control">
            <label className="label">
              <span className="label-text">商品コード</span>
            </label>
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              className="input input-bordered"
            />
          </div>
          <button type="submit" className="btn btn-primary w-full">
            商品コード読み込み
          </button>
        </form>
        <div className="my-4">
          <h2 className="text-lg font-bold">商品情報</h2>
          <p>商品名: {displayName}</p>
          {displayPrice ? <p>価格: {displayPrice}円</p> : <p>価格: </p>}
        </div>
        <button onClick={handleAddProduct} className="btn btn-primary mb-4 w-full">
          商品を追加
        </button>
        <div>
          <h2 className="text-lg font-bold">購入リスト</h2>
          {purchaseList.map((product) => (
            <div
              key={product.product_code}
              className="border-b border-gray-200 py-2 flex justify-between items-center"
            >
              <div>
                <p>商品名: {product.product_name}</p>
                <p>価格: {product.product_price}円</p>
                <p>合計: {product.product_count * product.product_price}円</p>
              </div>
              <div className="flex items-center">
                <input
                  type="text"
                  value={product.product_count}
                  readOnly
                  className="input input-bordered input-sm text-center w-12 mx-2"
                />
                <p> 個　</p>
                <div className="flex flex-col items-center">
                  <button
                    onClick={() => handleIncrement(product.product_code)}
                    className="btn btn-outline btn-sm"
                  >
                    ▲
                  </button>
                  <button
                    onClick={() => handleDecrement(product.product_code)}
                    className="btn btn-outline btn-sm"
                  >
                    ▼
                  </button>
                </div>
                <button
                  onClick={() => handleRemoveProduct(product.product_code)}
                  className="btn btn-error ml-4"
                >
                  削除
                </button>
              </div>
            </div>
          ))}
        </div>
        <button onClick={handlePurchase} className="btn btn-primary w-full mb-4 btm-nav-xs">
          購入
        </button>
      </div>
    </div>
  );
}
